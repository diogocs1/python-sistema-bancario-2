LIMITE = 500
extrato = ""
LIMITE_SAQUES = 3

clientes = []
contas = []
cliente_atual = None
conta_atual = None

menu = """
Você pode sacar até R$ {LIMITE:.2f} por transação.
Você pode realizar até {LIMITE_SAQUES} saques por dia.

Escolha uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[nc] Novo Cliente
[nco] Nova Conta
[lc] Listar Clientes
[sc] Selecionar Cliente
[q] Sair

=> """

print('\n' + ' Bem-vindo ao STNDR Bank '.center(40, "="))

def selecionar_cliente(clientes):
    cpf = input("Digite o CPF do cliente para selecionar: ").strip()
    cliente = buscar_cliente(clientes, cpf)
    if cliente:
        print(f"Cliente {cliente['nome']} selecionado.")
        return cliente
    else:
        print("Cliente não encontrado.")
        return None

def selecionar_conta(contas, cliente):
    contas_cliente = [conta for conta in contas if conta["cpf"] == cliente["cpf"]]
    if not contas_cliente:
        print("Este cliente não possui contas. Cadastre uma conta primeiro.")
        return None
    print("Contas disponíveis para o cliente:")
    for conta in contas_cliente:
        print(f"Agência: {conta['agencia']} | Número: {conta['numero']}")
    numero = input("Digite o número da conta que deseja selecionar: ").strip()
    for conta in contas_cliente:
        if str(conta["numero"]) == numero:
            print(f"Conta {numero} selecionada.")
            return conta
    print("Conta não encontrada.")
    return None

def depositar(valor, *, saldo, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(*, saldo, valor, extrato, numero_saques, limite, limite_saque):
    valor = float(input("Informe o valor do saque: ").strip())

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saque

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        if numero_saques == limite_saque - 1:
            print("Você atingiu o limite de saques diários.")
            menu = menu.replace('[s] Sacar', '[s] Sacar (Indisponível)')
        else:
            return saldo, extrato

    else:
        print("Operação falhou! O valor informado é inválido.")

def exibir_extrato():
    print("\n ")
    print(' EXTRATO '.center(40, "="))
    if cliente_atual:
        print("Não foram realizadas movimentações." if not cliente_atual.get("extrato", "") else cliente_atual["extrato"])
        print(f"\nSaldo: R$ {cliente_atual.get('saldo', 0):.2f}")
    else:
        print("Nenhum cliente selecionado.")
    print("==========================================")

def sair():
    print("\nObrigado por utilizar o STNDR Bank!")
    exit()

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ").strip()
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        print("CPF inválido! O CPF deve conter 11 dígitos.")
        return

    for cliente in clientes:
        if cliente["cpf"] == cpf:
            print("Cliente já cadastrado com este CPF.")
            return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    logradouro = input("Informe o logradouro (ex: Rua X): ").strip()
    numero = input("Informe o número: ").strip()
    bairro = input("Informe o bairro: ").strip()
    cidade = input("Informe a cidade: ").strip()
    estado = input("Informe o estado (UF): ").strip().upper()
    endereco = f"Logradouro: {logradouro}, Nro: {numero}, {bairro}, {cidade}/{estado}"

    novo_cliente = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "numero_saques": 0
    }

    clientes.append(novo_cliente)
    print("Cliente cadastrado com sucesso!")

def buscar_cliente(clientes, cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            return cliente
    return None

def exibir_clientes(clientes):
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    print("\nLista de Clientes:")
    for cliente in clientes:
        print(f"CPF: {cliente['cpf']}, Nome: {cliente['nome']}, Data de Nascimento: {cliente['data_nascimento']}, Endereço: {cliente['endereco']}")

def cadastrar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = buscar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado. Por favor, cadastre o cliente primeiro.")
        return

    numero_conta = len(contas) + 1
    conta = {
        "agencia": "0001",
        "numero": numero_conta,
        "cpf": cliente["cpf"],
        "saldo": 0.0,
        "extrato": ""
    }
    contas.append(conta)
    print(f"Conta cadastrada com sucesso! Número da conta: {numero_conta}")

# Inicialização: selecionar cliente e conta antes do menu
conta_atual = None
while not cliente_atual:
    print("\nNenhum cliente selecionado.")
    cliente_atual = selecionar_cliente(clientes)
    if not cliente_atual:
        print("Cadastre um cliente primeiro.")
        cadastrar_cliente(clientes)
while not conta_atual:
    conta_atual = selecionar_conta(contas, cliente_atual)
    if not conta_atual:
        print("Cadastre uma conta para este cliente.")
        cadastrar_conta(clientes, contas)

while True:
    try:
        menu_atual = menu.format(
            saldo=conta_atual.get("saldo", 0) if conta_atual else 0,
            LIMITE=LIMITE,
            numero_saques=cliente_atual.get("numero_saques", 0) if cliente_atual else 0,
            LIMITE_SAQUES=LIMITE_SAQUES
        )
        opcao = input(menu_atual).strip().lower()
    
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo = conta_atual.get("saldo", 0)
            extrato = conta_atual.get("extrato", "")
            resultado = depositar(valor, saldo=saldo, extrato=extrato)
            if resultado:
                conta_atual["saldo"], conta_atual["extrato"] = resultado
        elif opcao == "s":
            saldo = conta_atual.get("saldo", 0)
            extrato = conta_atual.get("extrato", "")
            numero_saques = cliente_atual.get("numero_saques", 0)
            resultado = sacar(
                saldo=saldo,
                valor=None,
                extrato=extrato,
                numero_saques=numero_saques,
                limite=LIMITE,
                limite_saque=LIMITE_SAQUES
            )
            if resultado:
                conta_atual["saldo"], conta_atual["extrato"] = resultado
                cliente_atual["numero_saques"] += 1
        elif opcao == "e":
            print("\n ")
            print(' EXTRATO '.center(40, "="))
            print("Não foram realizadas movimentações." if not conta_atual.get("extrato", "") else conta_atual["extrato"])
            print(f"\nSaldo: R$ {conta_atual.get('saldo', 0):.2f}")
            print("==========================================")
        elif opcao == "nc":
            cadastrar_cliente(clientes)
        elif opcao == "nco":
            cadastrar_conta(clientes, contas)
        elif opcao == "lc":
            exibir_clientes(clientes)
        elif opcao == "sc":
            novo_cliente = selecionar_cliente(clientes)
            if novo_cliente:
                cliente_atual = novo_cliente
                conta_atual = selecionar_conta(contas, cliente_atual)
        elif opcao == "q":
            sair()
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        print("\nObrigado por utilizar o STNDR Bank!")
        break