-- Acrescentar no estoque do produto X

update produtos 
    set estoque = (select estoque from produtos
        where id_produto = 2) + 5
    where id_produto = 2;

-- Retirar do estoque (sem ter sido por compra)

update produtos
    set estoque = (select estoque from prdoutos
        where id_produto = 2) - 5
    where id_produto = 2;