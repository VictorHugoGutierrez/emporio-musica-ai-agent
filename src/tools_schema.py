TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "consultar_banco_sql",
            "description": (
                "Executa uma consulta SQL no banco de dados da loja (SQLite em memória). "
                "Utilize para buscar produtos, preços, estoque, clientes, pedidos, itens de pedidos e promoções. "
                "Apenas consultas SELECT de leitura são permitidas."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta SQL de leitura (SELECT...) a ser executada no banco de dados.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_politicas_loja",
            "description": (
                "Consulta o manual interno de políticas e regras da Empório da Música (PDF). "
                "Utilize para dúvidas sobre regras de troca, devolução, garantia, formas de pagamento, horários e entregas."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "duvida": {
                        "type": "string",
                        "description": "Termos ou pergunta sobre a política da loja a ser pesquisada no PDF.",
                    }
                },
                "required": ["duvida"],
            },
        },
    },
]
