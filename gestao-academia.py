nomes = []
idades = []
planos = []   
pagos = []    
nomes_planos = ["Basico", "Intermediario", "Premium"]
valores_planos = [80, 110, 150]
idade_minima = 12

while True:
    print("")
    print("===== GESTÃO DE ACADEMIA =====")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Pesquisar aluno")
    print("4 - Listar pendentes")
    print("5 - Alterar plano")
    print("6 - Registrar pagamento")
    print("7 - Remover aluno")
    print("8 - Relatório")
    print("0 - Sair")
    opcao = input("Escolha: ")


    if opcao == "1":
        nome = input("Nome: ")
        idade = int(input("Idade: "))

        if nome == "":
            print("Nome inválido.")
        elif nome in nomes:
            print("Já existe um aluno com esse nome.")
        elif idade < idade_minima:
            print("Idade mínima para matrícula:", idade_minima, "anos.")
        else:
            print("Planos: 1-Basico  2-Intermediario  3-Premium")
            plano = int(input("Plano (1/2/3): "))
            if plano >= 1 and plano <= 3:
                nomes.append(nome)
                idades.append(idade)
                planos.append(plano)
                pagos.append(False)
                print("Aluno cadastrado com sucesso!")
            else:
                print("Plano inválido.")


    elif opcao == "2":
        if len(nomes) == 0:
            print("Nenhum aluno cadastrado.")
        for i in range(len(nomes)):
            if pagos[i] == True:
                situacao = "Pago"
            else:
                situacao = "Pendente"
            print(nomes[i], "|", idades[i], "anos |", nomes_planos[planos[i] - 1],
                  "| R$", valores_planos[planos[i] - 1], "|", situacao)

    elif opcao == "3":
        texto = input("Pesquisar nome: ")
        encontrados = 0
        for i in range(len(nomes)):
            if texto in nomes[i]:
                if pagos[i] == True:
                    situacao = "Pago"
                else:
                    situacao = "Pendente"
                print(nomes[i], "|", idades[i], "anos |", nomes_planos[planos[i] - 1],
                      "| R$", valores_planos[planos[i] - 1], "|", situacao)
                encontrados = encontrados + 1
        print(encontrados, "aluno(s) encontrado(s).")


    elif opcao == "4":
        encontrados = 0
        for i in range(len(nomes)):
            if pagos[i] == False:
                print(nomes[i], "|", idades[i], "anos |", nomes_planos[planos[i] - 1],
                      "| R$", valores_planos[planos[i] - 1], "| Pendente")
                encontrados = encontrados + 1
        print(encontrados, "aluno(s) com mensalidade pendente.")


    elif opcao == "5":
        nome = input("Nome do aluno: ")
        posicao = -1
        for i in range(len(nomes)):
            if nomes[i] == nome:
                posicao = i

        if posicao == -1:
            print("Aluno não encontrado.")
        else:
            print("Planos: 1-Basico  2-Intermediario  3-Premium")
            novo_plano = int(input("Novo plano (1/2/3): "))
            if novo_plano < 1 or novo_plano > 3:
                print("Plano inválido.")
            elif novo_plano == planos[posicao]:
                print("O aluno já está nesse plano.")
            else:
                planos[posicao] = novo_plano
                print("Plano alterado com sucesso!")


    elif opcao == "6":
        nome = input("Nome do aluno: ")
        posicao = -1
        for i in range(len(nomes)):
            if nomes[i] == nome:
                posicao = i

        if posicao == -1:
            print("Aluno não encontrado.")
        elif pagos[posicao] == True:
            print("A mensalidade deste aluno já está paga.")
        else:
            pagos[posicao] = True
            print("Pagamento de R$", valores_planos[planos[posicao] - 1], "registrado!")


    elif opcao == "7":
        nome = input("Nome do aluno: ")
        posicao = -1
        for i in range(len(nomes)):
            if nomes[i] == nome:
                posicao = i

        if posicao == -1:
            print("Aluno não encontrado.")
        else:
            confirmar = input("Remover " + nomes[posicao] + "? (s/n): ")
            if confirmar == "s":
                nomes.pop(posicao)
                idades.pop(posicao)
                planos.pop(posicao)
                pagos.pop(posicao)
                print("Aluno removido.")
            else:
                print("Remoção cancelada.")


    elif opcao == "8":
        recebido = 0
        pendente = 0
        contagem = [0, 0, 0]
        for i in range(len(nomes)):
            valor = valores_planos[planos[i] - 1]
            if pagos[i] == True:
                recebido = recebido + valor
            else:
                pendente = pendente + valor
            contagem[planos[i] - 1] = contagem[planos[i] - 1] + 1

        print("Total de alunos:", len(nomes))
        print("  Basico:", contagem[0])
        print("  Intermediario:", contagem[1])
        print("  Premium:", contagem[2])
        print("Valor recebido: R$", recebido)
        print("Valor pendente: R$", pendente)
        print("Total previsto: R$", recebido + pendente)

    elif opcao == "0":
        print("Até logo!")
        break

    else:
        print("Opção inválida.")