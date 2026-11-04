import json
import os
from dotenv import load_dotenv
from ollama import Client
from src.database_tools import DatabaseTools
from src.rag_tools import PolicyRAG
from src.tools_schema import TOOLS_SCHEMA

load_dotenv()

class EmporioAgent:

    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("OLLAMA_MODEL") or "gemma4:31b-cloud"

        host = os.getenv("OLLAMA_API_URL", "https://ollama.com")
        api_key = os.getenv("OLLAMA_API_KEY", "")

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self.client = Client(host=host,headers=headers)

        data_dir = os.getenv("DATA_DIR", "data")
        self.db = DatabaseTools(data_dir=data_dir)
        self.rag = PolicyRAG(pdf_path=os.path.join(data_dir, "políticas_da_loja.pdf"))

        self.messages = [{"role": "system", "content": self._build_system_prompt()}]

    def _build_system_prompt(self) -> str:
        schemas_sql = self.db.get_table_schemas()

        return f"""Você é o atendente virtual inteligente da loja "Empório da Música", localizada em Campo Grande/MS.
        Sua persona é acolhedora, amigável, educada e apaixonada por instrumentos musicais.
        
        ### ESQUEMA DO BANCO DE DADOS DA LOJA (SQLite em memória):
        {schemas_sql}
        
        ### VALORES E MAPEAMENTOS DO BANCO DE DADOS:
        - **Tabela `products`**:
          - `status`: usa valores em inglês: `'active'` (ativo/disponível), `'discontinued'` (descontinuado), `'coming_soon'` (em breve).
          - `category_id`: 1=Guitarras, 2=Baixos, 3=Baterias e Percussão, 4=Teclados e Pianos, 5=Violões, 6=Sopro (Madeiras), 7=Sopro (Metais), 8=Cordas Orquestrais, 9=Ukuleles.
          - **Instruções para SQL de Violões**: Para filtrar violões, prefira `p.category_id = 5` OU `p.description LIKE '%viol%'` OU `c.name LIKE '%Viol%'`.
          - **Filtro de Ativo e Estoque**: Sempre utilize `p.status = 'active'` e `p.stock_quantity > 0` ao buscar produtos disponíveis.
        
        - **Tabela `orders`**:
          - `status`: `'delivered'`, `'shipped'`, `'confirmed'`, `'pending'`, `'cancelled'`.
          - `payment_method`: `'pix'`, `'credit_6x'`, `'credit_12x'`, `'boleto'`, `'credit_3x'`, `'debit'`.
        
        ### REGRAS E DIRETRIZES DE ATENDIMENTO:
        1. **Escolha das Ferramentas**:
           - Para preços, estoque, especificações ou catálogo de produtos: execute `consultar_banco_sql`.
           - Para status de pedido, clientes ou histórico: execute `consultar_banco_sql`.
           - Para regras de devolução, garantia, formas de pagamento, frete, endereço ou horários: execute `consultar_politicas_loja`.
        2. **Escopo Restrito a Instrumentos**:
           - A loja vende **EXCLUSIVAMENTE instrumentos musicais**.
           - **NÃO vende acessórios** (cordas, palhetas, cabos, cases, pedais, amplificadores, etc.).
           - Se o cliente solicitar acessórios ou perguntar sobre outros assuntos (futebol, receitas, etc.), informe educadamente que a loja comercializa apenas instrumentos e redirecione o atendimento.
        3. **Desconto no PIX**:
           - O pagamento via PIX oferece **5% de desconto** sobre o preço de tabela (aplicável a produtos que não estejam já em preço promocional).
        """

    def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name == "consultar_banco_sql":
            query = arguments.get("query", "")
            return self.db.execute_sql(query)
        elif tool_name == "consultar_politicas_loja":
            duvida = arguments.get("duvida", "")
            return self.rag.search_policy(duvida)
        else:
            return f"Erro: Ferramenta '{tool_name}' não reconhecida."

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat(model=self.model_name, messages=self.messages, tools=TOOLS_SCHEMA)

        response_message = response.message

        while getattr(response_message, "tool_calls", None):
            self.messages.append(response_message)

            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                if isinstance(tool_args, str):
                    tool_args = json.loads(tool_args)

                print(f"\n[Agente acionou a ferramenta '{tool_name}' com argumentos: {tool_args}]")

                tool_result = self._execute_tool(tool_name, tool_args)

                self.messages.append({"role": "tool", "content": tool_result})

            response = self.client.chat(model=self.model_name, messages=self.messages, tools=TOOLS_SCHEMA)
            response_message = response.message

        final_content = response_message.content or ""
        self.messages.append({"role": "assistant", "content": final_content})
        return final_content
