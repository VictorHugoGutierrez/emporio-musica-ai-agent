import glob
import os
import sqlite3
import pandas as pd

class DatabaseTools:
  def __init__(self, data_dir: str = 'data'):
    self.data_dir = data_dir
    self.conn = sqlite3.connect(':memory:', check_same_thread=False)
    self._load_all_csvs()

  def _load_all_csvs(self):
    csv_files = glob.glob(os.path.join(self.data_dir, '*.csv'))
    if not csv_files:
      print(f"[Aviso] Nenhum Arquivo CSV encontrado em '{self.data_dir}'.")
      return

    for file_path in csv_files:
      table_name = os.path.basename(file_path).replace('.csv', '').lower()

      df = pd.read_csv(file_path)
      df.columns = [col.strip().lower() for col in df.columns]

      df.to_sql(table_name, self.conn, index=False, if_exists='replace')
      print(f"Tabela '{table_name}' carregada com {len(df)} registros.")

  def get_table_schemas(self) -> str:
    cursor = self.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    tables = cursor.fetchall()

    schemas = []
    for table_tuple in tables:
      table_name = table_tuple
      cursor.execute(f"PRAGMA table_info('{table_name}');")
      columns_info = cursor.fetchall()
      col_names = [info[3] for info in columns_info]
      schemas.append(f"Tabela '{table_name}': {','.join(col_names)}")

    return '\n'.join(schemas)

  def execute_sql(self, query: str) -> str:
    try:
      if not query.strip().lower().startswith("select"):
        return 'Erro: Apenas consultas SELECT são permitidas.'

      df = pd.read_sql_query(query, self.conn)
      if df.empty:
        return 'Nenhum registro encontrado para essa consulta'

      return df.to_markdown(index=False)
    except Exception as e:
      return f'Erro na execução SQL: {str(e)}'