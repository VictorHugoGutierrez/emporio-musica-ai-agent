import sys
import os
from dotenv import load_dotenv

from src.agent import EmporioAgent

def main():
    load_dotenv()
    
    print("=" * 65)
    print("EMPÓRIO DA MÚSICA - ATENDIMENTO VIRTUAL (CAMPO GRANDE/MS)")
    print("=" * 65)
    print("Digite sua mensagem para iniciar o atendimento.")
    print("Para encerrar a conversa, digite 'sair', 'exit' ou 'quit'.\n")

    try:
        agent = EmporioAgent()
        print("Agente inicializado com sucesso e conectado às bases de dados.\n")
    except Exception as e:
        print(f"Erro ao inicializar o agente: {e}")
        print("Por favor, verifique a chave OLLAMA_API_KEY e a URL no arquivo .env.")
        sys.exit(1)

    while True:
        try:
            user_input = input("Cliente: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["sair", "exit", "quit", "tchau"]:
                print("\nAgente: Muito obrigado por falar com a Empório da Música! Se precisar de algo para o seu som, estamos sempre por aqui. Até logo! 🎶✨")
                break
            
            resposta = agent.chat(user_input)
            print(f"\nAgente:\n{resposta}\n")
            print("-" * 65)
            
        except KeyboardInterrupt:
            print("\n\n[Atendimento encerrado pelo usuário]")
            break
        except Exception as e:
            print(f"\nErro durante o processamento da mensagem: {e}\n")

if __name__ == "__main__":
    main()
