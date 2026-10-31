-- READ simples de produtos
-- Quais produtos temos com ou sem estoque?

select * from produtos;

-------------------------------

-- READ do nome e preço de cada produto
-- QUal produtos temos e seus valores?

select nome, preco from produtos;

--------------------------------

-- READ do nome e quantidade em estoque de cada produto
-- Quais produtos temos e qual seu estoque?

select nome, estoque from produtos;

----------------------------------

-- READ dos produtos ordenados por preço de forma crescente
-- Quais são os produtos mais caros que temos?

select nome, preco from produtos
    order by preco asc;

----------------------------------

-- READ dos produtos ordenados por preço de forma descrescente
-- Quais são os produtos mais baratos?

select nome, preco from produtos
    order by preco desc;

------------------------------------

-- READ de produtos com o valor a cima de 50 e menor que 1000
-- Quais produtos estão na faixa dos R$50-R$1000?

select nome, preco from produtos
    where preco > 50 and preco < 1000;