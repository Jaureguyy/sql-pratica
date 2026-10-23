pragma foreign_keys = on;

create table if not exists clientes (
    id_cliente integer primary key,
    nome text not null,
    CPF integer not null,
    Estado text
);

create table if not exists produtos (
    id_produto integer primary key,
    nome text,
    preço numeric not null,
    estoque integer not null
);

create table if not exists Histórico_de_Compras ( 
    id_compra integer primary key,
    id_cliente integer not null,
    valor_compra numeric,
    data text,
    foreign key (id_cliente) references clientes (id_cliente)
);

drop table if exists compras;

create table if not exists compras (
    id_compra integer,
    id_produto integer
    quantidade integer,
    valor_compra integer,
    foreign key (id_compra) references Histórico_de_Compras (id_compra),
    foreign key (id_produto) references produtos (id_produto),
    primary key (id_compra, id_produto)
);


