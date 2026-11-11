-- Aumento de preço fixo em determinado produto

update produtos
    set preco = 10
where id_produto = 11;

-- Queda de preço (valor antigo - mudança)

update produtos
    set preco = (select preco from produtos
        where id_produto = 1) - 50
    where id_produto = 1;