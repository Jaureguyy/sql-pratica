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
   

def comprar():
    """
    Para realizar uma compra, as seguintes etapas são necessárias:
    -Mostrar os itens     OK
    -Escolher o item      OK
    -Escolher a quantidade OK
    -Mostrar valor final   OK
    -Confirmar compra ------|-- Conectadas
    -Dar baixa no estoque --|   OK
    -Adicionar compra no histórico
    -Adicionar infos na tabela compras
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
        print(f"[{indice}] {nome:<20} {preco:>10.2f} {estoque:>12}")                     #Pontos: E se estoque==0?


    # for indice, informacoes in produtos.items():
    #     id, nome, preco, estoque = informacoes
    #     print(f"\nINDICE: {indice}")
    #     print(f"ID: {produtos[indice][id]}")                        #Feito para verificar os produtos na agenda
    #     print(f"NOME: {produtos[indice][nome]}")
    #     print(f"PREÇO: {produtos[indice][preco]}")
    #     print(f"ESTOQUE: {produtos[indice][estoque]}")

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

        if confirmar_escolha("Confirmar Compra? ('s'/'n')"):
            baixa_estoque(produtos[escolha]['id'], quantidade)
            print(f"COMPRA REALIZADA!!!")
        else:
            print(f"COMPRA CANCELADA!!!")
            conn.rollback()

        
     

def baixa_estoque(id_produto, quantidade_baixa):
    conn = sqlite3.connect('e-commerce.db')
    cur = conn.cursor()

    with conn:
        cur.execute("""UPDATE produtos
                        SET estoque = (SELECT estoque
                                    FROM produtos
                                    WHERE id_produto = ?) - ?
                        WHERE id_produto = ?""", (id_produto, quantidade_baixa, id_produto))


def confirmar_escolha(pergunta):
    while True:
        resposta = input(f"{pergunta}: ").strip().lower()
        if resposta in ('s', 'sim'):
                return True
        if resposta in ('n', 'nao'):
            return False
        print(f"Resposta Inválida. Digite novamente.")


comprar()