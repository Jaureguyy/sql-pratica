# DataBase E-commerce
 
 Este repositório teve fins de estudo e primeiro contato com banco de dados. O banco escolhido foi sqlite3 utilizando tema de ecommerce.

 ## Inicialmente temos o arquivo "*create.sql*" o qual cria as seguintes tabelas e colunas:

 ### **clientes** (1:N)
Com as colunas: **id_cliente**, **nome**, **cpf** e **estado** 

PK: **id_cliente**

### **produtos** (1:N)
Colunas: **id_produto**, **nome**, **preco** e **estoque**

PK: **id_produto**

### **historico_de_compras** (1:N)
Colunas: **id_compra**, **id_cliente**, **valor_compra** e **data**

PK: **id_compra** / FK: **id_cliente**

A coluna valor_compra corresponde ao custo total, independente da quantidade e tipos de produtos (caso tenha mais de um)

### **compras** (N:N)
Colunas: **id_compra**, **id_produto**, **quantidade** e **valor_unidade**

PKs e FKs: **id_compra**, **id_produto**

Cada linha desta tabela faz referência a um pedaço da compra. Sendo uma linha por produto da compra. O *valor_unidade* corresponde ao valor do item no momento da compra, então se no dia 25/11 uma mangueira foi comprada pelo valor de R$15 e no dia seguinte ser atualizada para R$25, o valor da compra será mostrado.

## **CRUD**
Dentro do CRUD existe uma ordem lógica e correta para os inserts. Esta ordem está destacada pela numeração dos primeiros scripts (01,02 e 03).

Dentro do CRUD é possível:
- Inserir clientes
- Inserir produtos
- Inserir compras (simulando uma compra)
- Deletar clientes
- Deletar produtos
- Ler clientes
- Ler compras realizadas
- Ler produtos
- Atualizar estoque
- Atualizar preços

Cada query/script foi criado pensando em responder e trazer um 'problema' real envolvendo o DB do ecommerce.

## Sqlite <> Sqlite3

Dentro do repositório existem os arquivos **functions.py** e **main.py**, estes fazem a integração do sqlite3 no banco já criado.

### **functions.py**:

Tem as funções criadas que interagem diretamente no banco de dados. Algumas trabalham com um conceito novo que aprendi de funções de regra e funções de operação. Aquelas de regra estão em uma camada em que suas funcionalidades são apenas efetuar ações que podem ser "invisíveis" aos olhos de quem está do outro lado da tela. Já as funções de operações são aquelas que estão no **dispatcher**, estas são ações que escolhemos e 'queremos' fazer.

As funções que quero dar destaque são:
- **escolher_produto()**: Mostra uma mecânica de parâmetro True/False que impacta diretamente na query

- **confirmar_escolha()**: Uma 'visão' nova e que pretendo utilizar mais nos próximos projetos

- **comprar()**: É a função que mais trabalhei em cima e que foi o motivo de várias outras existirem. Passou por diversas mudanças e lógicas diferentes. Agora invés de fazer várias coisas, chama outras funções como *escolher_produto*, *confirmar_escolha* e *atualizar_estoque*.

### **main.py**

A main está simples e não foi muito trabalhada na parte visual e de outputs. Está funcional, disponibiliza logo no início as operações disponíveis e logo em seguida atribui uma função do dispatcher na variável **funcao**. Sua estrutura é basicamente o loop *While True* que chama indefinidamente o dispatcher, sempre solicitando se o usuário deseja continuar no programa ou não.

## **Conclusão**

Até agora foi meu projeto que mais exigiu tempo. Não teve tantos commits por conta que muitas alterações foram feitas dentro do mesmo (como a função comprar). Mostrou como funciona um Database junto do Sqlite3.

Muito conteúdo pode ser utilizado afim de revisão e até uma possível continuidade no futuro.

### Se algum desconhecido ta lendo eu agradeço muito! :)