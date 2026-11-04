# Exemplo 2: Consulta Específica de Produto e Estoque (Takamine GD20)

**Entrada do Cliente:**
> "Qual o valor e a quantidade em estoque do Takamine GD20?"

### Execução de Ferramentas (Function Calling)
**Chamada 1:** `consultar_banco_sql`
**Argumentos:**
```json
{
  "query": "SELECT price_brl, stock_quantity FROM products WHERE name LIKE '%Takamine GD20%' AND status = 'active' AND stock_quantity > 0;"
}
```
**Resultado Retornado:**
```text
|   price_brl |   stock_quantity |
|------------:|-----------------:|
|        2199 |                5 |
```

### Resposta Final do Agente:
Olá! É um prazer te ajudar. 😊

O **Takamine GD20** é um instrumento maravilhoso! Atualmente, ele está disponível por **R$ 2.199,00** e temos **5 unidades** em nosso estoque aqui no Empório da Música.

Lembrando que, se você optar pelo pagamento via **PIX**, consegue um desconto de **5%** no valor! 🎸

Gostaria de reservar o seu ou tem mais alguma dúvida?
