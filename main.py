import sqlite3


"""
Estão disponíveis as seguintes funções para interagir com o database dentro da main:

    -Cadastrar cliente
    -Cadastrar produto
    -Fazer compra (junto da baixa no estoque)(atualmente um item por vez)
    -Update no preço
    -Update no estoque

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
   
def comprar(id_cliente):
    """
    Para realizar uma compra, as seguintes etapas são necessárias:
    -Mostrar os itens     OK
    -Escolher o item      OK
    -Escolher a quantidade OK
    -Mostrar valor final   OK
    -Confirmar compra ------|-- Conectadas
    -Dar baixa no estoque --|   OK
    -Adicionar compra no histórico  OK
    -Adicionar infos na tabela compras OK
    """    
    
    conn = sqlite3.connect('e-commerce.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_key = ON')
    cur = conn.cursor()


    #Processa a compra (Escolhe item+Quantidade ; confirma+baixa no estoque+ add no historico_compras/compras)
    with conn:
        produto = escolher_produto(com_estoque=True)
        quantidade = int(input(f"Escolha a quantidade: "))

        while quantidade>produto['estoque']:
            print(f"\nQuantidade de itens muito alta")
            quantidade = int(input(f"Escolha novamente:"))
        
        valor_total = quantidade * produto['preco']
        print(f"Valor total: R${valor_total}")

        #Chama confirmar_escolha() para finalizar ou não a compra
        if confirmar_escolha("Confirmar Compra? ('s'/'n')"):
            if atualizar_estoque(conn, produto['id'], -quantidade):    #Importante reparar no '-' responsável pela baixa

                #Inserindo as informações em historico_de_compras e compras
                cur.execute("""INSERT INTO historico_de_compras
                                (id_cliente, valor_compra, data)
                                VALUES (?, ?, date('now', 'localtime'))""",
                                (id_cliente, valor_total)
                )

                id_compra = cur.lastrowid   #Armazena o >>>ÚLTIMO id DA CONEXÃO<<<

                cur.execute("""INSERT INTO compras
                                (id_compra, id_produto, quantidade, valor_unidade)
                                VALUES (?,?,?,?)""",
                                (id_compra, produto['id'], quantidade, produto['preco'])
                )

                ##Finalizando, caso seja confirmado: finaliza as atualizações. Ao contrário tudo será perdido.
                #Por isso o processamento se encontra dentro do "with conn"
                print(f"\nCOMPRA REALIZADA!!!")
            else:
                print(f"\nCOMPRA ENCERRADA!!!")
        else:
            print(f"\nCOMPRA CANCELADA!!!")
            conn.rollback()

def atualizar_estoque(conn, id_produto, quantidade):
    cur = conn.execute(
            """UPDATE produtos
               SET estoque = estoque + ?
                WHERE id_produto = ?
                AND estoque >= ?""",
                (quantidade, id_produto, quantidade)
        )
    return cur.rowcount == 1

def confirmar_escolha(pergunta):
    while True:
        resposta = input(f"{pergunta}: ").strip().lower()
        if resposta in ('s', 'sim'):
                return True
        if resposta in ('n', 'nao'):
            return False
        print(f"Resposta Inválida. Digite novamente.")

def escolher_cliente():
    conn = sqlite3.connect('e-commerce.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    clientes = {}

    print(f"{'':<4}{'CLIENTE':<12}")
    for indice, infos in enumerate(cur.execute("""
        SELECT id_cliente, nome, cpf, estado FROM clientes"""), start=1):

        id_cliente, nome, cpf, estado = int(infos['id_cliente']), infos['nome'], infos['cpf'], infos['estado']
        clientes[indice] = {'id': id_cliente, 'nome': nome, 'cpf': cpf, 'estado': estado}
        print(f"[{indice}] {nome:<12}")

    escolha = int(input(f"Escolha o cliente: "))
    # print(clientes[escolha])    #Confere se escolheu certo
    cliente = clientes[escolha]
    return cliente

def escolher_produto(com_estoque=False):
    conn = sqlite3.connect('e-commerce.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    #Nesta função acontece o aproveitamento da query ser tratada como uma string. Desta forma os parâmetros
    #Serão sempre adicionados como argumentos True/False -> Resultando na "adição" 
    sql = 'SELECT * FROM produtos'

    if com_estoque:
        sql += ' WHERE estoque > 0'

    produtos = {}                             #Cria a agenda para armazenar os produtos

    print(f"ESCOLHA O PRODUTO:\n")
    print(f"{'':<6} {'PRODUTO':<20} {'PREÇO':>12} {'DISPONÍVEL':>15}")
    with conn:
        for indice, info in enumerate(conn.execute(sql), start=1):
            #Desempacota "info"
            id, nome, preco, estoque = int(info['id_produto']), info['nome'], int(info['preco']), int(info['estoque'])
            #Aplica as informações do produto no dicionário
            produtos[indice] = {'id': id, 'nome': nome, 'preco': preco, 'estoque': estoque} 
            rotulo = (f"[{indice}]")
            print(f"{rotulo:<6} {nome:<20} {preco:>12.2f} {estoque:>15}")

        escolha = int(input(f"\nEscolha o produto: "))
        produto = produtos[escolha]
        return produto

def atualizar_preco():
    conn = sqlite3.connect('e-commerce.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    produto = escolher_produto()
    novo_preco = int(input(f"Digite o novo preço do produto: "))

    cur.execute("""UPDATE produtos
                   SET preco = ?
                   WHERE id_produto = ?""",
                   (novo_preco, produto['id'])
                )
    conn.commit()

cliente = escolher_cliente()
comprar(cliente['id'])