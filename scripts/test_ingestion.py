from src.database_tools import DatabaseTools
from src.rag_tools import PolicyRAG

def test_data_ingestion():
  print('=== 1. Testando Banco SQLite (CSVs) ===')
  db = DatabaseTools(data_dir='data')
  print('\nEsquema das tabelas:')
  print(db.get_table_schemas())

  print('\nExecutando teste de consulta SQL:')
  sample_query = "SELECT * FROM produtos LIMIT 3;"
  print(db.execute_sql(sample_query))

  print('\n=== 2. Testando Busca no PDF de Políticas ===')
  rag = PolicyRAG(pdf_path='data/políticas_da_loja.pdf')
  query_test = 'troca e devolução'
  print(f"\nResultado da busca por '{query_test}':")
  print(rag.search_policy(query_test))

if __name__ == "__main__":
    test_data_ingestion()