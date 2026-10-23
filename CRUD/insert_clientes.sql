-- Inserindo Clientes no banco:

insert into clientes (nome, cpf)
values ('Marcos', 55566677788);

-- Inserindo o Estado do cliente 'Marcos':

update clientes set estado = 'RS'
where id_cliente = 1;

-- Inserindo todas as informações de uma vez:

insert into clientes (nome,cpf,estado)
values ('Ana', 10010010010, 'PR')

-- Inserindo mais de um cliente:

insert into clientes (nome, cpf, estado)
values
('Jairo', 90010020035, 'RJ'),
('Tom', 50060070080, 'MG'),
('Maria', 10020030030, 'SC');