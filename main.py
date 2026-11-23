import sqlite3


"""
Estão disponíveis as seguintes funções para interagir com o database dentro da main:

    -Cadastrar cliente
    -Cadastrar produto
    -Fazer compra (junto da baixa no estoque)(atualmente um item por vez)
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


    produtos = {}  #Criando agenda para guardar as infos e não chamar o db toda hora

    print("Escolha o produto:\n")
    print(f"{'':<4} {'PRODUTO':<20} {'PREÇO':>7} {'QUANTIDADE DISPONÍVEL':>25}")
    for indice, infos in enumerate(conn.execute("""
        SELECT id_produto, nome, preco, estoque                
        FROM produtos"""), start=1):                  #Talvez poderia ser uma outra função para ler os produtos + desempacota

        
        id, nome, preco, estoque = infos['id_produto'],infos['nome'], int(infos['preco']), int(infos['estoque'])
        #Por conta do row_factory, eu posso indicar a coluna para desempacotar

        produtos[indice] = {'id':id, 'nome': nome, 'preco': preco, 'estoque': estoque}   #Adicionando na agenda
        if produtos[indice]['estoque'] > 0:
            print(f"[{indice}] {nome:<20} {preco:>10.2f} {estoque:>12}")                     


    # for indice, informacoes in produtos.items():
    #     id, nome, preco, estoque = informacoes
    #     print(f"\nINDICE: {indice}")
    #     print(f"ID: {produtos[indice][id]}")                        #Feito para verificar os produtos na agenda
    #     print(f"NOME: {produtos[indice][nome]}")
    #     print(f"PREÇO: {produtos[indice][preco]}")
    #     print(f"ESTOQUE: {produtos[indice][estoque]}")


    #Processa a compra (Escolhe item+Quantidade ; confirma+baixa no estoque+ add no historico_compras/compras)
    with conn:
        escolha = int(input(f"\nEscolha o item: "))
        quantidade = int(input(f"Escolha a quantidade: "))

        # print(f"\n\n{produtos[escolha]}\n\n")    #Confere a escolha se necessário

        while quantidade>produtos[escolha]['estoque']:
            print(f"\nQuantidade de itens muito alta")
            quantidade = int(input(f"Escolha novamente:"))


        # print(f"Produto: {produtos[escolha]['nome']}")
        # print(f"Quantidade: {quantidade}")                                  #Mostra as informações do produto escolhido
        # print(f"Valor do produto: {produtos[escolha]['preco']}")
        
        valor_total = quantidade * produtos[escolha]['preco']
        print(f"Valor total: R${valor_total}")

        #Chama confirmar_escolha() para finalizar ou não a compra
        if confirmar_escolha("Confirmar Compra? ('s'/'n')"):
            if baixa_estoque(conn, produtos[escolha]['id'], quantidade):

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
                                (id_compra, produtos[escolha]['id'], quantidade, produtos[escolha]['preco'])
                )

                ##Finalizando, caso seja confirmado: finaliza as atualizações. Ao contrário tudo será perdido.
                #Por isso o processamento se encontra dentro do "with conn"
                print(f"\nCOMPRA REALIZADA!!!")
            else:
                print(f"\nCOMPRA ENCERRADA!!!")
        else:
            print(f"\nCOMPRA CANCELADA!!!")
            conn.rollback()


def baixa_estoque(conn, id_produto, quantidade_baixa):
    cur = conn.execute(
            """UPDATE produtos
               SET estoque = estoque - ?
                WHERE id_produto = ?
                AND estoque >= ?""",
                (quantidade_baixa, id_produto, quantidade_baixa)
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

print(escolher_produto())