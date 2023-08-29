## Problema de Negócio

### Contexto do Problema de Negócio

Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra a identificar pontos-chave da empresa, respondendo às perguntas que ele fizer utilizando dados! A empresa Fome Zero é um marketplace de restaurantes, facilitando o encontro e negociações entre clientes e restaurantes. Os restaurantes cadastram-se na plataforma Fome Zero, disponibilizando informações como endereço, tipo de culinária, disponibilidade de reservas e entregas, além de avaliações dos serviços e produtos do restaurante.

### O Desafio

O CEO Guerra também é recém-contratado e precisa entender melhor o negócio para tomar decisões estratégicas e alavancar a Fome Zero. Para isso, é necessário realizar uma análise nos dados da empresa e gerar dashboards que respondam às seguintes perguntas:

#### Geral

1. Quantidade de restaurantes únicos registrados?
2. Quantidade de países únicos registrados?
3. Quantidade de cidades únicas registradas?
4. Total de avaliações feitas?
5. Total de tipos de culinária registrados?

#### Países

1. País com mais cidades registradas?
2. País com mais restaurantes registrados?
3. País com mais restaurantes de nível de preço igual a 4?
4. País com a maior variedade de tipos de culinária?
5. País com mais avaliações feitas?
6. País com mais restaurantes que fazem entrega?
7. País com mais restaurantes que aceitam reservas?
8. País com maior média de avaliações registradas?
9. País com maior média de nota média registrada?
10. País com menor média de nota média registrada?
11. Média de preço de um prato para dois por país?

#### Cidades

1. Cidade com mais restaurantes registrados?
2. Cidade com mais restaurantes com nota média acima de 4?
3. Cidade com mais restaurantes com nota média abaixo de 2.5?
4. Cidade com maior valor médio de um prato para dois?
5. Cidade com maior variedade de tipos de culinária?
6. Cidade com mais restaurantes que fazem reservas?
7. Cidade com mais restaurantes que fazem entregas?
8. Cidade com mais restaurantes que aceitam pedidos online?

#### Restaurantes

1. Restaurante com mais avaliações?
2. Restaurante com maior nota média?
3. Restaurante com maior valor em um prato para duas pessoas?
4. Restaurante de culinária brasileira com menor média de avaliação?
5. Restaurante de culinária brasileira, no Brasil, com maior média de avaliação?
6. Restaurantes que aceitam pedidos online têm, em média, mais avaliações?
7. Restaurantes que fazem reservas têm, em média, maior valor médio de um prato para duas pessoas?
8. Restaurantes de culinária japonesa nos EUA têm valor médio de prato para duas pessoas maior que churrascarias americanas (BBQ)?

#### Tipos de Culinária

1. Restaurante de culinária italiana com maior média de avaliação?
2. Restaurante de culinária italiana com menor média de avaliação?
3. Restaurante de culinária americana com maior média de avaliação?
4. Restaurante de culinária americana com menor média de avaliação?
5. Restaurante de culinária árabe com maior média de avaliação?
6. Restaurante de culinária árabe com menor média de avaliação?
7. Restaurante de culinária japonesa com maior média de avaliação?
8. Restaurante de culinária japonesa com menor média de avaliação?
9. Restaurante de culinária caseira com maior média de avaliação?
10. Restaurante de culinária caseira com menor média de avaliação?
11. Tipo de culinária com maior valor médio de um prato para duas pessoas?
12. Tipo de culinária com maior nota média?
13. Tipo de culinária com mais restaurantes que aceitam pedidos online e fazem entregas?

### Premissas para a Análise

1. Marketplace como modelo de negócio.
2. 4 visões principais de negócios: País, Restaurante, Cidade e Culinária.
3. Principais dados concentrados na Índia.

### Estratégia da Solução

Desenvolvimento de um painel estratégico com métricas que refletem as 4 visões do modelo de negócio da empresa: Países, Restaurantes, Cidades e Culinárias.

### Top 3 Insights de Dados

1. Restaurantes com entregas têm mais avaliações do que os que não têm.
2. Culinárias com maiores notas médias: Sri Lankan, Taiwanese e Ramen.
3. Restaurantes de culinária japonesa nos EUA têm valor médio de prato para duas pessoas inferior às churrascarias americanas (BBQ).

### Produto Final

Painel online hospedado em nuvem, acessível em qualquer dispositivo conectado à internet. [Clique aqui para acessar o painel](https://brunolopes-fomezerodashboard.streamlit.app/).

### Conclusão

O objetivo do projeto é apresentar métricas de forma clara e eficaz para o CEO.

### Próximos Passos

1. Reduzir métricas.
2. Adicionar novos filtros.
3. Incluir mais visões de negócio.
