import os
import json

from src.agent import EmporioAgent

def generate_markdown(filename: str, title: str, user_prompt: str, tool_calls_info: list, agent_response: str):
    os.makedirs("conversas", exist_ok=True)
    filepath = os.path.join("conversas", filename)
    
    md_content = f"# {title}\n\n"
    md_content += f"**Entrada do Cliente:**\n> \"{user_prompt}\"\n\n"
    
    if tool_calls_info:
        md_content += "### Execução de Ferramentas (Function Calling)\n"
        for idx, tc in enumerate(tool_calls_info, 1):
            md_content += f"**Chamada {idx}:** `{tc['name']}`\n"
            md_content += f"**Argumentos:**\n```json\n{json.dumps(tc['args'], ensure_ascii=False, indent=2)}\n```\n"
            if tc.get("result"):
                md_content += f"**Resultado Retornado:**\n```text\n{tc['result']}\n```\n"
            md_content += "\n"
    else:
        md_content += "### Execução de Ferramentas\n*Nenhuma ferramenta externa foi necessária (Resposta baseada na Persona/System Prompt).* \n\n"
        
    md_content += f"### Resposta Final do Agente:\n{agent_response}\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"Arquivo salvo em: {filepath}")

def main():
    print("=== Empório da Música - Gerador de Logs de Diálogos (.md) ===\n")
    
    scenarios = [
        {
            "filename": "exemplo_1_catalogo_violoes.md",
            "title": "Exemplo 1: Consulta ao Catálogo de Violões (Filtro por Preço)",
            "prompt": "Quais violões vocês têm disponíveis abaixo de R$ 1000?"
        },
        {
            "filename": "exemplo_2_preco_takamine.md",
            "title": "Exemplo 2: Consulta Específica de Produto e Estoque (Takamine GD20)",
            "prompt": "Qual o valor e a quantidade em estoque do Takamine GD20?"
        },
        {
            "filename": "exemplo_3_politica_devolucao.md",
            "title": "Exemplo 3: Consulta às Políticas da Loja (Trocas e Devoluções)",
            "prompt": "Qual é a política de devolução e troca da loja?"
        },
        {
            "filename": "exemplo_4_informacoes_loja.md",
            "title": "Exemplo 4: Informações Operacionais (Endereço e Horários)",
            "prompt": "Onde fica a loja, qual o telefone de contato e o horário de funcionamento?"
        },
        {
            "filename": "exemplo_5_escopo_acessorios.md",
            "title": "Exemplo 5: Tratamento de Pedido Fora de Escopo (Acessórios)",
            "prompt": "Vocês vendem encordoamento de nylon avulso ou cabos P10?"
        }
    ]
    
    for s in scenarios:
        print(f"Executando cenário: {s['title']}...")
        agent = EmporioAgent()
        
        start_msg_count = len(agent.messages)
        response = agent.chat(s['prompt'])
        new_messages = agent.messages[start_msg_count:]
        
        tool_calls_info = []
        for i, msg in enumerate(new_messages):
            tool_calls = getattr(msg, 'tool_calls', None)
            if tool_calls:
                for tc in tool_calls:
                    func_name = tc.function.name
                    func_args = tc.function.arguments
                    if isinstance(func_args, str):
                        try:
                            func_args = json.loads(func_args)
                        except Exception:
                            pass
                    
                    result_text = ""
                    if (i + 1 < len(new_messages)) and isinstance(new_messages[i + 1], dict) and new_messages[i + 1].get('role') == 'tool':
                        result_text = new_messages[i + 1].get('content', '')
                    
                    tool_calls_info.append({
                        "name": func_name,
                        "args": func_args,
                        "result": result_text
                    })
        
        generate_markdown(
            filename=s['filename'],
            title=s['title'],
            user_prompt=s['prompt'],
            tool_calls_info=tool_calls_info,
            agent_response=response
        )
        
    print("\nSucesso! Todos os 5 arquivos .md foram gerados na pasta 'conversas/'!")

if __name__ == "__main__":
    main()
