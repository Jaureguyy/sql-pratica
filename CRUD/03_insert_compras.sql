-- As tabelas histórico e compras são rodadas no mesmo arquivo para melhor visuzalização e entendimento entre as PKs e FKs.

delete from compras;
delete from historico_de_compras;

-- Insert no histórico

/*
O insert no histórico é apenas com o cliente e a data. O id_compra é preenchido automaticamente, já valor_compra necessita de dados pertencentes a tabela 'compras' (quantidade * valor_unidade). Para resolver, o próximo insert será feito em compras, assim teremos as informações para um update no valor_compra.
 */

insert into historico_de_compras (id_cliente, data)
values
(2, '24/10/2026'),
(2, '17/10/2026'),
(8, '24/10/2026'),
(7, '23/10/2026'),
(5, '23/10/2026'),
(10, '23/10/2026');

insert into compras (id_compra, id_produto, quantidade, valor_unidade)
values
(1, 2, 1, 500),
(1, 5, 1, 30),
(2, 1, 1, 50000),
(3, 8, 5, 110),
(3, 7, 15, 64),
(3, 10, 20, 2000),
(4, 11, 2, 12),
(5, 9, 9, 225),
(5, 6, 4, 10),
(6, 4, 30, 18000);

/*
Feito os primeiros inserts com as informações "primitivas". Agora utilizamos as mesmas para fazer o valor_compra no historico_de_compras
*/

update historico_de_compras
set valor_compra = (
    select sum(quantidade*valor_unidade) from compras 
    where compras.id_compra = historico_de_compras.id_compra);
    
/*
Para entender o update acima, montei a seguinte frase:
Para cada linha do histórico, atualiza com a soma quantidade*valor_unidade dos itens de compra com o mesmo id_compra, guardando o resultado em valor_compra
*/

-----------------------------------------------


--Agora será necessário dar "baixa" no estoque. Isto será feito pegando a quantidade na tabela COMPRAS e substrair em estoque tabela PRODUTOS

/*
O update acontece na tabela PRODUTOS, coluna ESTOQUE. 
Começando a subconsulta, primeiro temos a quantidade em estoque, depois a soma da quantidade vendida em COMPRAS. Importante diferencias qual tabela está "fora" (produtos) e qual está "dentro" (from COMPRAS). O where da subquery é utilizado da mesma maneira que o update anterior para valor_compra, o primeiro valor é aqule que está sendo "analizado" e o id da tabela de "fora" qual "linha" será atualizada.
O where fora da consulta serve para verificar se o id do produto está dentro de compras, assim evita o erro de NOT NULL
*/

update produtos
set estoque = (                      
    select produtos.estoque - sum(compras.quantidade)
    from compras
    where compras.id_produto = produtos.id_produto
)
where produtos.id_produto in (
    select id_produto from compras
    group by id_produto
);

