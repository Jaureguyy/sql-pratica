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

-- Menores preços registrados dos produtos nos últimos 7 dias

select compras.id_produto, nome, min(valor_unidade) as valor_minimo, data
from compras
join produtos on compras.id_produto = produtos.id_produto
join historico_de_compras on compras.id_compra = historico_de_compras.id_compra
where data >= date('2026-10-31', '-7 days')
group by compras.id_produto;
