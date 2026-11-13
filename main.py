import sqlite3


"""
Estão disponíveis as seguintes funções para interagir com o database dentro da main:

    -Cadastrar cliente
    -Cadastrar produto
    -Fazer compra (junto da baixa no estoque)
    -Update no preço
    -Update nas informações dos clientes

"""

def cadastrar_cliente():
    conn = sqlite3.connect('e-commerce.db')   #Conecta ao banco já existente
    cur = conn.cursor()                       #Cria o cursor para a operação

    infos = input(f"Digite o nome, CPF e Estado do cliente:\n")     #Solicita os dados para o insert do novo cliente
    nome, cpf, estado = infos.split()                               #Desempacota as infos

    with conn:
        cur.execute("""INSERT INTO clientes (nome, cpf, estado)
                        VALUES (?, ?, ?)""",
                        (nome, cpf, estado)
                    )
    conn.close()


def cadastrar_produto():
    conn = sqlite3.connect('e-commerce.db')
    cur = conn.cursor()

    print("Vamos cadastrar um produto!\n")
    nome = input("Digite o nome: ")
    preco = input("Digite o preço: ")
    estoque = input("Digite a qunatidade em estoque: ")

    with conn:
        cur.execute("""INSERT INTO produtos (nome, preco, estoque)
                        VALUES (?, ?, ?)""",
                        (nome, preco, estoque)
                    )
    conn.close()

cadastrar_produto()