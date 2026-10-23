pragma foreign_keys = on;

-- Drop de tables para recriar se necessário:

Drop table if exists clientes;
Drop table if exists produtos;
Drop table if exists Histórico_de_Compras;
Drop table if exists compras;

create table if not exists clientes (
    id_cliente integer primary key,
    nome text not null,
    cpf integer integer not null,
    estado text
);

create table if not exists produtos (
    id_produto integer primary key,
    nome text,
    preco numeric not null,
    estoque integer not null
);

create table if not exists historico_de_compras ( 
    id_compra integer primary key,
    id_cliente integer not null,
    valor_compra numeric,
    data text,
    foreign key (id_cliente) references clientes (id_cliente)
);

create table if not exists compras (
    id_compra integer,
    id_produto integer,
    quantidade integer,
    valor_unidade,
    foreign key (id_compra) references historico_de_compras (id_compra),
    foreign key (id_produto) references produtos (id_produto),
    primary key (id_compra, id_produto)
);


