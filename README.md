# Empório da Música - Agente de Atendimento Virtual com IA

Este repositório contém o protótipo do **Agente de Atendimento Virtual** para a **Empório da Música**, uma loja fictícia de instrumentos musicais localizada em Campo Grande/MS. O projeto foi desenvolvido como parte do **Desafio Técnico para AI Engineer na Artefact**.

---

## 📋 Sumário

- [Visão Geral e Arquitetura](#-visão-geral-e-arquitetura)
- [Fundamentação Teórica e Artigos Acadêmicos](#-fundamentação-teórica-e-artigos-acadêmicos)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Configuração e Instalação](#-configuração-e-instalação)
- [Como Executar](#-como-executar)
- [Exemplos de Interação](#-exemplos-de-interação)
- [Decisões Técnicas e Justificativas](#-decisões-técnicas-e-justificativas)
- [Limitações Conhecidas e Próximos Passos](#-limitações-conhecidas-e-próximos-passos)
- [Uso de Assistentes de IA](#-uso-de-assistentes-de-ia)

---

## 🎯 Visão Geral e Arquitetura

O agente assume a persona de um **atendente virtual acolhedor, apaixonado por música e altamente prestativo**, capaz de tirar dúvidas de clientes em tempo real através de uma abordagem **híbrida (Function Calling + RAG)**:

```text
                                  +-----------------------+
                                  |    Cliente (CLI)      |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |   EmporioAgent (LLM)  |
                                  |  (Gemma via Ollama)   |
                                  +-----------+-----------+
                                              |
                     +------------------------+------------------------+
                     | (Function Calling)                              | (Function Calling)
                     v                                                 v
        +------------+------------+                       +------------+------------+
        |   consultar_banco_sql   |                       |  consultar_politicas_loja  |
        +------------+------------+                       +------------+------------+
                     |                                                 |
                     v                                                 v
        +------------+------------+                       +------------+------------+
        |   SQLite (Em Memória)   |                       |    RAG Manual em PDF      |
        |  (products, orders...)  |                       |  (políticas_da_loja.pdf) |
        +-------------------------+                       +-------------------------+
```

1. **Atendimento a Consultas Operacionais**: Executa queries SQL dinâmicas em um banco **SQLite em memória** carregado a partir dos arquivos CSV fornecidos (`products.csv`, `orders.csv`, `customers.csv`, `promotions.csv`, etc.).
2. **Atendimento a Dúvidas de Políticas**: Realiza busca por relevância (RAG) no manual interno `políticas_da_loja.pdf` para responder sobre trocas, devoluções, garantias e frete.
3. **Filtro Estrito de Escopo**: Reconhece perguntas fora do catálogo comercializado (como pequenos acessórios, palhetas, cabos) ou fora do contexto de instrumentos musicais, recusando educadamente e mantendo o foco do atendimento.

---

## 📚 Fundamentação Teórica e Artigos Acadêmicos

A solução foi projetada incorporando aprendizados dos três artigos fornecidos na documentação do desafio:

### 1. **Orca: Progressive Learning from Complex Explanation Traces of GPT-4** (_Mukherjee et al., 2023_)

- **Conceito Aplicado**: Uso de _System Messages_ ricas e técnicas de _Explanation Tuning_.
- **Aplicação no Projeto**: Em vez de passar apenas regras secas ao modelo, o _System Prompt_ orienta a IA a gerar rastros de raciocínio intermediários (_Chain-of-Thought_) antes de decidir acionar uma ferramenta ou estruturar a resposta ao cliente, garantindo que o agente aprenda a lógica de tomada de decisão.

### 2. **Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data** (_Hsieh et al., 2023_)

- **Conceito Aplicado**: Desacoplamento entre a justificativa da tarefa (_rationales_) e a geração do resultado.
- **Aplicação no Projeto**: A arquitetura do `EmporioAgent` separa claramente o momento de raciocinar sobre qual ferramenta invocar (`consultar_banco_sql` vs `consultar_politicas_loja`) da síntese final da resposta em linguagem natural humana.

### 3. **QLoRA: Efficient Finetuning of Quantized LLMs** (_Dettmers et al., 2023_)

- **Conceito Aplicado**: Eficiência de memória com quantização de 4 bits (NF4/GGUF).
- **Aplicação no Projeto**: Escolha de modelos da família **Gemma / LLaMA 3** servidos via **Ollama**, comprovando cientificamente que modelos quantizados em 4 bits mantêm quase 100% da capacidade de raciocínio de modelos full 16-bit com uma fração do consumo de VRAM e tempo de resposta.

---

## 📁 Estrutura do Repositório

```text
emporio-musica-ai-agent/
├── data/                             # Dados fornecidos pela loja
│   ├── products.csv
│   ├── orders.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── promotions.csv
│   ├── categories.csv
│   └── políticas_da_loja.pdf
├── src/                              # Código fonte do Agente
│   ├── __init__.py
│   ├── agent.py                      # Orquestrador principal do LLM e Function Calling
│   ├── database_tools.py             # Engine de carga e consulta ao banco SQLite
│   ├── rag_tools.py                  # Processador e buscador do PDF de políticas
│   └── tools_schema.py               # Definição dos schemas JSON das ferramentas
├── scripts/                          # Scripts de teste e utilitários
│   ├── test_ingestion.py             # Teste isolado da carga de dados (CSV e PDF)
│   ├── test_agent.py                 # Teste isolado do fluxo do agente
│   └── generate_dialogs.py           # Script que gera os .md de exemplo automaticamente
├── conversas/                        # 5 Diálogos reais de exemplo (.md)
│   ├── exemplo_1_catalogo_violoes.md
│   ├── exemplo_2_preco_takamine.md
│   ├── exemplo_3_politica_devolucao.md
│   ├── exemplo_4_informacoes_loja.md
│   └── exemplo_5_escopo_acessorios.md
├── main.py                           # Interface de linha de comando (CLI interativa)
├── .env.example                      # Modelo de variáveis de ambiente
├── .gitignore                        # Proteção de credenciais e arquivos temporários
├── requirements.txt                  # Dependências do projeto Python
└── README.md                         # Documentação principal
```

---

## ⚙️ Configuração e Instalação

### Pré-requisitos

- **Python 3.10** ou superior instalado.
- **Ollama** instalado localmente ou acesso ao Ollama Cloud.

### 1. Criar e ativar o ambiente virtual

- **Linux/macOS:**
  `python3 -m venv venv`
  `source venv/bin/activate`
- **Windows:**
  `python -m venv venv`
  `venv\Scripts\activate`

### 2. Instalar as dependências

`pip install -r requirements.txt`

### 3. Configurar as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme o seu ambiente:

Conteúdo do `.env`:

```env
OLLAMA_API_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=gemma4:31b-cloud
DATA_DIR=data
```

---

## 🚀 Como Executar

### 1. Atendimento Interativo (CLI)

Para conversar com o agente no terminal em tempo real:
`python main.py`

### 2. Teste Isolado da Ingestão de Dados

Para validar a criação das tabelas SQLite e leitura do PDF:
`python -m scripts.test_ingestion`

### 3. Gerar os Diálogos de Exemplo (`conversas/*.md`)

Para rodar a suíte de testes de diálogo e exportar os logs reais para a pasta `conversas/`:
`python -m scripts.generate_dialogs`

---

## 💬 Exemplos de Interação

O repositório contém 5 exemplos reais de conversa salvos na pasta `conversas/`:

1. **`exemplo_1_catalogo_violoes.md`**: Consulta de violões abaixo de R$ 1.000,00 (`consultar_banco_sql`)
2. **`exemplo_2_preco_takamine.md`**: Consulta pontual do valor e estoque do _Takamine GD20_ (`consultar_banco_sql`)
3. **`exemplo_3_politica_devolucao.md`**: Dúvida sobre política de trocas e devoluções (`consultar_politicas_loja`)
4. **`exemplo_4_informacoes_loja.md`**: Consulta de endereço, telefone e horários da loja (`consultar_politicas_loja`)
5. **`exemplo_5_escopo_acessorios.md`**: Pergunta sobre venda de cabos e palhetas avulsas (Recusa educada via Persona/System Prompt)

---

## 🛠️ Decisões Técnicas e Justificativas

- **Linguagem**: Python 3.12 (Ecossistema padrão de AI/Data Science, facilidade de manipulação de dados e integração com LLMs).
- **Abordagem**: Agente Híbrido (Function Calling + RAG). O Function Calling provê 100% de acurácia determinística para dados tabulares (preços/estoque no SQLite), enquanto o RAG atende textos não estruturados (PDF de políticas).
- **Framework LLM**: API nativa da SDK `ollama`. Optou-se por **não usar frameworks pesados** (como LangChain/LlamaIndex) para manter o código leve, legível, sem abstrações ocultas e com controle total sobre o loop de chamada de ferramentas.
- **Banco Operacional**: SQLite em Memória (`:memory:`). Permite criar dinamicamente a estrutura de tabelas relacionais a partir dos CSVs no startup da aplicação com zero dependências de infraestrutura externa.
- **Interface**: CLI (Linha de Comando Interativa). O foco da avaliação é a inteligência e orquestração do agente. A CLI fornece feedback instantâneo e exibe a transparência do acionamento de ferramentas.
- **Persistência de Histórico**: Sessão em Memória (`self.messages`). Mantém o contexto de conversação durante toda a sessão do cliente no terminal.

---

## 🔮 Limitações Conhecidas e Próximos Passos

Caso houvesse mais tempo de desenvolvimento, as seguintes melhorias seriam priorizadas:

1. **Busca Vetorial Densa (Vector DB)**: Substituir a busca por palavras-chave/relevância no PDF por um banco vetorial local (como **ChromaDB** ou **FAISS**) com embeddings multilíngues.
2. **Text-to-SQL Avançado**: Implementar uma camada de validação e sanitização com _AST Parser_ (ex: `sqlglot`) para validar a sintaxe do SQL gerado pela IA antes da execução no SQLite.
3. **Interface Gráfica Web**: Criar um painel moderno usando **Streamlit** ou **FastAPI + React** para simular uma janela de chat de e-commerce real.
4. **Persistência de Sessão**: Salvar o histórico de conversas dos clientes em um banco de dados relacional ou Redis para permitir a retomada de atendimento em diferentes momentos.

---

## 🤖 Uso de Assistentes de IA

Durante o desenvolvimento deste projeto, utilizou-se o **Gemini Notebook** como workbench e parceiro de engenharia. A ferramenta foi empregada para:

- **Inspeção e Sanitização de Dados**: Análise do esquema das colunas dos CSVs para criar as regras de mapeamento no _System Prompt_.
- **Aceleração do Prototipamento**: Geração inicial dos scripts de boilerplate e formatação dos arquivos `.md`.
- **Revisão de Código e Testes**: Identificação e correção de divergências de tipos no SQLite.

Toda a lógica de orquestração, decisão arquitetural, prompt engineering e validação das respostas foi desenhada e guiada pelo engenheiro responsável.

---

_Empório da Música — Sua música começa aqui. 🎶_
