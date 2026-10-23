# DataBase E-commerce

## Tabelas:

### -Clientes:
| id_cliente | nome |CPF  | estado |
| --- | --- | --- | --- |

PK: **id_cliente**

Detalha as informações dos clientes.

### -Produtos:
|id_produto|nome|preço|estoque|
|---|---|---|---|

PK: **id_produto**

Detalha as informações dos produtos, bem como a sua quantidade em estoque e preço atual.

### -Histórico de Compras:
|id_compra|id_cliente|valor_compra|data|
|---|---|---|---|

PK: **id_compra**                         
FK: **id_cliente** -> Clientes

Descreve as informações da compra.

### -Compras (ligação):
|id_compra|id_produto|quantidade|valor_unidade|
|---|---|---|---|

PK/FK: **id_compra e id_produto** ->Histórico de Compras | Produtos                                        

Esta tabela "divide" as informações da compra. Deste modo, diferentes compras podem ter diferentes produtos (N:N). A *quantidade* determina quantos produtos daquele tipo foram atendidos. Já *valor_unidade* se refere ao custo unitário na época da compra.