from src.agent import EmporioAgent

def main():
    print("=== Empório da Música - Teste do Agente de Atendimento ===")
    agent = EmporioAgent()

    perguntas_teste = [
        "Quais violões vocês têm disponíveis abaixo de R$ 1000?",
        "Qual é a política de devolução e troca da loja?",
        "Quem venceu o campeonato brasileiro de futebol ontem?",
    ]

    for p in perguntas_teste:
        print(f"\n--------------------------------------------------")
        print(f"Cliente: {p}")
        resposta = agent.chat(p)
        print(f"Agente:\n{resposta}")

if __name__ == "__main__":
    main()
