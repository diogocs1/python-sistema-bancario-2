saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

menu = """
Seu saldo é R$ {saldo:.2f}

Você pode sacar até R$ {LIMITE:.2f} por transação.
Você pode realizar até {LIMITE_SAQUES} saques por dia.
Você já realizou {numero_saques} saques hoje.

Escolha uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

print('\n' + ' Bem-vindo ao STNDR Bank '.center(40, "="))

while True:
    try:
        menu_atual = menu.format(saldo=saldo, LIMITE=LIMITE, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)
        opcao = input(menu_atual)
    

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"

            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor > saldo

            excedeu_limite = valor > LIMITE

            excedeu_saques = numero_saques >= LIMITE_SAQUES

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
                if numero_saques == LIMITE_SAQUES - 1:
                    print("Você atingiu o limite de saques diários.")
                    menu = menu.replace('[s] Sacar', '[s] Sacar (Indisponível)')

            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            print("\n ")
            print(' EXTRATO '.center(40, "="))
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        elif opcao == "q":
            print("\nObrigado por utilizar o STNDR Bank!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        print("\nObrigado por utilizar o STNDR Bank!")
        break