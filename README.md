# Empório da Música — AI Customer Support Agent

An intelligent, production-ready virtual customer service assistant developed for **Empório da Música**, a regional musical instrument store based in Campo Grande/MS, Brazil.

This project was built as part of the **Artefact AI Engineer Technical Challenge**. It combines a **hybrid reasoning system** leveraging **Text-to-SQL (Function Calling)** over SQLite database records and **Retrieval-Augmented Generation (RAG)** over official store policy documents, powered by **Ollama** (`gemma4:31b-cloud` / `gemma2`).

--- 

## Key Features

* **Autonomous Tool Routing (Function Calling)**: Dynamically selects between SQL queries (products, categories, pricing, stock, orders, promotions) and policy text retrieval based on customer intent.
* **Text-to-SQL Engine**: Translates natural language inquiries into structured SQLite queries against an in-memory relational database hydrated from store CSVs.
* **Store Policy RAG**: Extracts and grounds responses in official store guidelines (`políticas_da_loja.pdf`), covering returns, warranties, shipping, and store hours.
* **Warm & Professional Persona**: Adheres to store identity—welcoming, passionate about musical instruments, helpful, and strictly scoped to instrument sales.
* **Out-of-Scope Safeguards**: Politely declines queries regarding unrelated topics (cooking, politics) as well as non-catalog items (small accessories like single guitar strings or plectrums).

--- 

## Scientific Rationale & Academic Literature Grounding

The design and system prompt architecture of this agent are strictly grounded in key principles from three landmark AI research papers:

### 1. Orca: Progressive Learning from Complex Explanation Traces (*Mukherjee et al., 2023*)
* **Core Insight**: Smaller language models achieve superior reasoning capabilities when guided by rich system instructions that incorporate step-by-step reasoning traces (*Explanation Tuning*).
* **Implementation**: The agent's system prompt utilizes explicit Chain-of-Thought (CoT) guidelines. Before producing a user-facing response or calling a tool, the model performs intermediate logical reasoning regarding data requirements, schema constraints, and intent boundaries.

### 2. Distilling Step-by-Step Outperforms Large Language Models (*Hsieh et al., 2023*)
* **Core Insight**: Task performance and efficiency improve when intermediate reasoning rationale is decoupled from final output generation.
* **Implementation**: The system separates the **tool invocation rationale** (e.g., constructing valid SQL queries with flexible unaccented matching or querying PDF sections) from the **final answer synthesis**, ensuring clean, human-like customer communications without exposing backend mechanics.

### 3. QLoRA: Efficient Finetuning of Quantized LLMs (*Dettmers et al., 2023*)
* **Core Insight**: Quantized 4-bit models (e.g., NF4/GGUF architectures) preserve full 16-bit reasoning capabilities and instruction-following fidelity while dramatically reducing memory consumption and inference latency.
* **Implementation**: The project leverages Ollama's quantized models (`gemma4:31b-cloud` / `gemma2`), enabling fast, low-latency function calling and low memory footprint suitable for edge or cloud microservice deployment.

--- 

## Architecture & System Design

```text
                     ┌──────────────────────────────┐
                     │   User Query (CLI / Main)    │
                     └──────────────┬───────────────┘
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │   EmporioAgent (src/agent.py) │
                     │   - System Prompt (Persona)  │
                     │   - Ollama Client SDK        │
                     └──────────────┬───────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           │ Tool Selection (Function Calling / Schema)      │
           ▼                                                 ▼
┌─────────────────────────────┐           ┌────────────────────────────────┐
│    consultar_banco_sql      │           │    consultar_politicas_loja    │
│  (src/database_tools.py)    │           │      (src/rag_tools.py)        │
└──────────┬──────────────────┘           └──────────────┬─────────────────┘
           │                                             │
           ▼                                             ▼
┌─────────────────────────────┐           ┌────────────────────────────────┐
│  In-Memory SQLite Database  │           │   PyPDF Text Extractor &       │
│  (products, categories,     │           │   Keyword Search Engine        │
│  orders, promotions, etc.)  │           │   (políticas_da_loja.pdf)      │
└──────────┬──────────────────┘           └──────────────┬─────────────────┘
           │                                             │
           └────────────────────────┬────────────────────┘
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │   Final Response Synthesis    │
                     │  (Natural Language Output)   │
                     └──────────────┬───────────────┘
```

--- 

## Repository Structure

```text
emporio-musica-ai-agent/
├── data/                             # Raw CSV datasets and PDF policy manual
│   ├── categories.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── promotions.csv
│   └── políticas_da_loja.pdf
├── src/                              # Core application source code
│   ├── agent.py                      # Main EmporioAgent class & function calling loop
│   ├── database_tools.py             # SQLite database loader and execution engine
│   ├── rag_tools.py                  # PyPDF parser and policy search engine
│   └── tools_schema.py               # JSON Schema definition for Ollama tool calling
├── scripts/                          # Automated testing and generation scripts
│   ├── test_ingestion.py             # Database and PDF loading verification
│   ├── test_agent.py                 # Multi-scenario agent test suite
│   └── generate_dialogs.py           # Automated markdown dialogue log exporter
├── conversas/                        # Real execution dialogue logs (Markdown)
│   ├── exemplo_1_catalogo_violoes.md
│   ├── exemplo_2_preco_takamine.md
│   ├── exemplo_3_politica_devolucao.md
│   ├── exemplo_4_informacoes_loja.md
│   └── exemplo_5_escopo_acessorios.md
├── main.py                           # Interactive CLI interface
├── .env.example                      # Environment variables template
├── .gitignore                        # Git exclusion rules
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

--- 

## Quickstart & Installation

### Prerequisites
* **Python**: 3.10 or higher
* **Ollama**: Local Ollama instance or an active Ollama Cloud API Key

### Step 1: Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows: venv\Scripts\activate
# On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env` and fill in your settings:
```env
OLLAMA_API_URL=https://ollama.com
OLLAMA_API_KEY=your_key_here
OLLAMA_MODEL=gemma4:31b-cloud
DATA_DIR=data
```

### Step 3: Run Interactive CLI Assistant
```bash
python main.py
```

--- 

## Running Tests & Dialogue Exporter

To verify database ingestion and PDF text extraction:
```bash
python -m scripts.test_ingestion
```

To execute the automated test scenarios:
```bash
python -m scripts.test_agent
```

To regenerate the 5 Markdown dialogue logs with real tool calls:
```bash
python -m scripts.generate_dialogs
```

--- 

## Sample Dialogue Summaries

The `conversas/` folder contains 5 validated real interaction logs:

1. **`exemplo_1_catalogo_violoes.md`**: Catalog search for acoustic guitars under R$ 1,000.00. The agent executes an SQL query, returning 12 available models grouped by Nylon/Steel strings, including a 5% PIX discount note.
2. **`exemplo_2_preco_takamine.md`**: Product inquiry for the *Takamine GD20*. SQL query fetches exact price (R$ 2,199.00) and stock level (5 units).
3. **`exemplo_3_politica_devolucao.md`**: Inquiry about return policies. RAG retrieves Section 4 from `políticas_da_loja.pdf`, detailing 7-day right of withdrawal, 30-day store warranty, and non-returnable items.
4. **`exemplo_4_informacoes_loja.md`**: Store location, business hours, and contact details retrieved from policy manual.
5. **`exemplo_5_escopo_acessorios.md`**: Request for guitar strings and cables. The agent politely declines based on store guidelines restricting inventory strictly to instruments.

--- 

## Known Limitations & Future Improvements

1. **Text-to-SQL Robustness**: Complex nested queries are currently constrained by Ollama's schema interpretation. Future iterations could incorporate AST-based SQL sanitization or a dedicated Text-to-SQL fine-tuned adapter.
2. **Dense Vector Search (RAG)**: The current implementation uses keyword/text retrieval. Upgrading to dense embeddings (e.g., ChromaDB or FAISS with `nomic-embed-text`) will enhance semantic retrieval for subtle policy queries.
3. **Frontend Integration**: Transitioning the current CLI interface (`main.py`) to a Streamlit or FastAPI web dashboard.

--- 

## AI Assistant Disclosure

In accordance with transparency guidelines, **Gemini Notebook** was utilized as an agentic workbench during development to assist with data exploration, schema validation, paper synthesis, and rapid prototyping of script structures. All architectural decisions, code integrations, and prompt engineering strategies were reviewed and verified against the challenge specifications.
