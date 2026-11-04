# Exemplo 1: Consulta ao Catálogo de Violões (Filtro por Preço)

**Entrada do Cliente:**
> "Quais violões vocês têm disponíveis abaixo de R$ 1000?"

### Execução de Ferramentas (Function Calling)
**Chamada 1:** `consultar_banco_sql`
**Argumentos:**
```json
{
  "query": "SELECT p.name, p.price_brl, p.description FROM products p JOIN categories c ON p.category_id = c.category_id WHERE (p.category_id = 5 OR p.name LIKE '%Violão%' OR p.description LIKE '%violão%') AND p.status = 'active' AND p.stock_quantity > 0 AND p.price_brl < 1000;"
}
```
**Resultado Retornado:**
```text
| name                                  |   price_brl | description                                                                                                                          |
|:--------------------------------------|------------:|:-------------------------------------------------------------------------------------------------------------------------------------|
| Yamaha C40 Nylon Natural              |       599.9 | Violão clássico com tampo em Spruce e fundo/laterais em Meranti. Ideal para estudantes e iniciantes, com excelente projeção sonora.  |
| Yamaha C70 Nylon Natural              |       849   | Violão clássico de nível intermediário com tampo em Spruce sólido. Acabamento de alta qualidade e timbre equilibrado.                |
| Tagima Memphis AC-39 Nylon Natural    |       429.9 | Violão clássico com cordas de nylon, perfeito para quem está começando. Corpo leve e confortável para longas sessões de estudo.      |
| Giannini GN-15 Nylon Cedr Natural     |       689   | Violão clássico Giannini com tampo em cedro. Sonoridade quente e encorpada, excelente custo-benefício para estudantes avançados.     |
| Rozini RC-104 Nylon Estudante         |       459.9 | Violão clássico de estudo da Rozini, feito com madeiras nacionais. Acabamento caprichado e preço acessível para iniciantes.          |
| Tagima Dallas Tuner Aço Natural       |       749   | Violão folk com cordas de aço e afinador integrado. Corpo confortável e som brilhante, ideal para acompanhamento vocal.              |
| Yamaha F310 Aço Natural               |       699.9 | Violão folk aço Yamaha com corpo robusto e timbre encorpado. Um dos modelos mais vendidos do mundo para iniciantes e intermediários. |
| Giannini GF-1R Aço Folk Sunburst      |       579.9 | Violão folk com tampo em Spruce e acabamento Sunburst clássico. Som equilibrado e visual elegante para palco e estúdio.              |
| Shelby SN-100 Folk Aço Preto          |       549   | Violão folk aço com visual moderno em preto. Indicado para quem busca um instrumento versátil com boa relação custo-benefício.       |
| Tagima Woodstock Dreadnought Natural  |       899   | Violão dreadnought com corpo amplo e som potente. Excelente para fingerpicking e strumming com projeção impressionante.              |
| Shelby SGD-195E Elétrico Aço Sunburst |       799   | Violão eletroacústico dreadnought com captação e afinador integrado. Boa opção de custo-benefício para quem precisa de amplificação. |
| Tagima TW-7 7 Cordas Aço Natural      |       999   | Violão 7 cordas com cordas de aço para estilos que exigem projeção extra. Braço confortável com tensor regulável.                    |
| Kala KA-B Barítono Mogno              |       599   | Ukulele barítono Kala em mogno com afinação em DGBE. Corpo amplo com graves profundos, uma ponte entre o ukulele e o violão.         |
```

### Resposta Final do Agente:
Olá! É um prazer ajudar você a encontrar o instrumento ideal para suas músicas! 🎸

Temos ótimas opções de violões disponíveis por menos de R$ 1.000,00, tanto para quem prefere a suavidade do nylon quanto o brilho do aço. Confira nossa seleção:

**🎻 Violões de Nylon (Ideais para iniciantes e música clássica):**
*   **Tagima Memphis AC-39**: R$ 429,90
*   **Rozini RC-104 Estudante**: R$ 459,90
*   **Yamaha C40**: R$ 599,90
*   **Giannini GN-15 (Tampo em cedro)**: R$ 689,00
*   **Yamaha C70 (Nível intermediário)**: R$ 849,00

**🎸 Violões de Aço (Som mais brilhante e potente):**
*   **Shelby SN-100 (Preto)**: R$ 549,00
*   **Giannini GF-1R (Sunburst)**: R$ 579,90
*   **Yamaha F310**: R$ 699,90
*   **Tagima Dallas Tuner (Com afinador)**: R$ 749,00
*   **Shelby SGD-195E (Elétrico/Eletroacústico)**: R$ 799,00
*   **Tagima Woodstock Dreadnought**: R$ 899,00
*   **Tagima TW-7 (7 Cordas)**: R$ 999,00

**✨ Dica Especial:** Se você optar pelo pagamento via **PIX**, oferecemos um **desconto de 5%** sobre o valor de tabela!

Algum desses modelos chamou mais a sua atenção? Se quiser saber mais detalhes sobre as especificações de algum deles, é só me falar! 😊
