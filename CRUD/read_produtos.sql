-- READ simples de produtos

select * from produtos;

-------------------------------

-- READ do nome e preço de cada produto

select nome, preco from produtos;

--------------------------------

-- READ do nome e quantidade em estoque de cada produto

select nome, estoque from produtos;

----------------------------------

-- READ dos produtos ordenados por preço de forma crescente

select nome, preco from produtos
    order by preco asc;

----------------------------------

-- READ dos produtos ordenados por preço de forma descrescente

select nome, preco from produtos
    order by preco desc;

------------------------------------

-- READ de produtos com o valor a cima de 50 e menor que 1000

select nome, preco from produtos
    where preco > 50 and preco < 1000;