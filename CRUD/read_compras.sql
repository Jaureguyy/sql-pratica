-- Quais foram as últimas compras que tivemos?

select id_compra, valor_compra, data
    from historico_de_compras
order by data asc;

-- Quem são os clientes das compras?

select id_compra, nome, valor_compra
    from historico_de_compras
join clientes on historico_de_compras.id_cliente = clientes.id_cliente;

-- Quais produtos saíram e suas quantidades?

select compras.id_produto as id, nome, sum(quantidade) from compras
join produtos on compras.id_produto = produtos.id_produto
group by compras.id_produto;
 
