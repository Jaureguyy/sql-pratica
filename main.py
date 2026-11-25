from functions import dispatcher, confirmar_escolha, escolher_cliente

##Inicializa a loja
print(f"BEM VINDO AO ECCOMM!")
print(f"{'-'*15}")

opcao = input(f"""
[1] - Cadastrar Cliente
[2] - Cadastrar Produto
[3] - Comprar
[4] - Atualizar Preço
[5] - Repor Estoque
[6] - Sair

Escolha uma opção: """)

while True:

    if opcao == '6':
        break
    funcao = dispatcher(opcao)
    if funcao:
        funcao()

    if confirmar_escolha("Continuar na loja? ('s'/'n'): "):
        opcao = input(f"""
[1] - Cadastrar Cliente
[2] - Cadastrar Produto
[3] - Comprar
[4] - Atualizar Preço
[5] - Repor Estoque
[6] - Sair

Escolha uma opção: """)
    else:
        break
    