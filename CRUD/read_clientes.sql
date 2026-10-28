-- READ simples de clientes

select * from clientes;

-------------------------------------

-- READ de clientes por estado

select * from clientes
where estado = 'SP';

--------------------------------------

-- READ apenas do id e nome dos clientes

select id_cliente, nome from clientes;

--------------------------------------

-- READ do nome e estado do cliente

select nome, estado from clientes;

--------------------------------------

-- READ do nome e CPF de cada cliente

select nome, cpf from clientes;