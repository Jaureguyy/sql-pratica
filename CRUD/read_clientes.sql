-- READ simples de clientes
-- Quais clientes temos cadastrados?

select * from clientes;

-------------------------------------

-- READ de clientes por estado
-- Que clientes são do estado 'X'

select * from clientes
where estado = 'SP';

--------------------------------------

-- READ apenas do id e nome dos clientes
-- Quais são os IDs de nossos clientes?

select id_cliente, nome from clientes;

--------------------------------------

-- READ do nome e estado do cliente
-- Quais são os estados de nosso clientes?

select nome, estado from clientes;

--------------------------------------

-- READ do nome e CPF de cada cliente
-- Qual é o CPF de cada cliente nosso?

select nome, cpf from clientes;