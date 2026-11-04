import os
import pypdf

class PolicyRAG:

  def __init__(self, pdf_path: str = 'data/políticas_da_loja.pdf'):
    self.pdf_path = pdf_path
    self.chunks = []
    if os.path.exists(pdf_path):
      self._process_pdf()
    else:
      print(f"[Aviso] PDF de políticas não encontrado em '{pdf_path}'")

  def _process_pdf(self):
    reader = pypdf.PdfReader(self.pdf_path)

    for idx, page in enumerate(reader.pages):
      text = page.extract_text()

      if not text:
        continue

      clean_text = ' '.join(text.split())

      self.chunks.append({"page": idx + 1, "text": clean_text})

      print(f"PDF de políticas processado com sucesso! ({len(self.chunks)} páginas carregadas)")

  def search_policy(self, query: str, max_results: int = 3) -> str:
    if not self.chunks:
      return 'Base de políticas indisponível no momento.'

    query_terms = [
      term.lower() 
      for term in query.split() 
      if len(term) > 2
    ]

    scored_chunks = []
    for chunk in self.chunks:
      text_lower = chunk['text'].lower()
      score = sum(text_lower.count(term) for term in query_terms)
      if score > 0:
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    if not scored_chunks:
      return 'Nenhuma política específica encontrada no manual para este termo.'

    formatted_results = []
    for _, chunk in scored_chunks[:max_results]:
      formatted_results.append(f"--- Trecho (Página {chunk['page']}) ---\\n{chunk['text']}")

    return "\n\n".join(formatted_results)