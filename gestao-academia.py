ARQUIVO = "alunos.txt"
NOMES_PLANOS = ["Basico", "Intermediario", "Premium"]
VALORES_PLANOS = [80.00, 120.00, 180.00]
IDADE_MINIMA = 12


open(ARQUIVO, "a").close()


alunos = []
arquivo = open(ARQUIVO, "r", encoding="utf-8")
for linha in arquivo:
    linha = linha.strip()
    if linha != "":
        alunos.append(linha.split(";"))
arquivo.close()

while True:
    print("\n===== GESTÃO DE ACADEMIA =====")
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
        nome = input("Nome: ").strip().replace(";", "")
        idade = input("Idade: ")

        existe = False
        for a in alunos:
            if a[0].lower() == nome.lower():
                existe = True

        if nome == "":
            print("Nome inválido.")
        elif existe:
            print("Já existe um aluno com esse nome.")
        elif not idade.isdigit():
            print("Digite uma idade válida (número inteiro).")
        elif int(idade) < IDADE_MINIMA:
            print(f"Idade mínima para matrícula: {IDADE_MINIMA} anos.")
        else:
            print("Planos: 1-Basico  2-Intermediario  3-Premium")
            escolha = input("Plano (1/2/3): ")
            if escolha == "1" or escolha == "2" or escolha == "3":
                plano = NOMES_PLANOS[int(escolha) - 1]
                alunos.append([nome, idade, plano, "nao"])
                print("Aluno cadastrado com sucesso!")
            else:
                print("Plano inválido.")


    elif opcao == "2":
        if len(alunos) == 0:
            print("Nenhum aluno cadastrado.")
        for a in alunos:
            valor = VALORES_PLANOS[NOMES_PLANOS.index(a[2])]
            if a[3] == "sim":
                situacao = "Pago"
            else:
                situacao = "Pendente"
            print(f"{a[0]} | {a[1]} anos | {a[2]} | R$ {valor:.2f} | {situacao}")


    elif opcao == "3":
        texto = input("Pesquisar nome: ").strip().lower()
        encontrados = 0
        for a in alunos:
            if texto in a[0].lower():
                valor = VALORES_PLANOS[NOMES_PLANOS.index(a[2])]
                if a[3] == "sim":
                    situacao = "Pago"
                else:
                    situacao = "Pendente"
                print(f"{a[0]} | {a[1]} anos | {a[2]} | R$ {valor:.2f} | {situacao}")
                encontrados += 1
        print(f"{encontrados} aluno(s) encontrado(s).")


    elif opcao == "4":
        encontrados = 0
        for a in alunos:
            if a[3] == "nao":
                valor = VALORES_PLANOS[NOMES_PLANOS.index(a[2])]
                print(f"{a[0]} | {a[1]} anos | {a[2]} | R$ {valor:.2f} | Pendente")
                encontrados += 1
        print(f"{encontrados} aluno(s) com mensalidade pendente.")


    elif opcao == "5":
        nome = input("Nome do aluno: ")
        posicao = -1
        for i in range(len(alunos)):
            if alunos[i][0].lower() == nome.lower():
                posicao = i

        if posicao == -1:
            print("Aluno não encontrado.")
        else:
            print("Planos: 1-Basico  2-Intermediario  3-Premium")
            escolha = input("Novo plano (1/2/3): ")
            if escolha != "1" and escolha != "2" and escolha != "3":
                print("Plano inválido.")
            elif NOMES_PLANOS[int(escolha) - 1] == alunos[posicao][2]:
                print("O aluno já está nesse plano.")
            else:
                alunos[posicao][2] = NOMES_PLANOS[int(escolha) - 1]
                print("Plano alterado com sucesso!")


    elif opcao == "6":
        nome = input("Nome do aluno: ")
        posicao = -1
        for i in range(len(alunos)):
            if alunos[i][0].lower() == nome.lower():
                posicao = i

        if posicao == -1:
            print("Aluno não encontrado.")
        elif alunos[posicao][3] == "sim":
            print("A mensalidade deste aluno já está paga.")
        else:
            alunos[posicao][3] = "sim"
            valor = VALORES_PLANOS[NOMES_PLANOS.index(alunos[posicao][2])]
            print(f"Pagamento de R$ {valor:.2f} registrado!")


    elif opcao == "7":
        nome = input("Nome do aluno: ")
        posicao = -1
        for i in range(len(alunos)):
            if alunos[i][0].lower() == nome.lower():
                posicao = i

        if posicao == -1:
            print("Aluno não encontrado.")
        else:
            confirmar = input(f"Remover {alunos[posicao][0]}? (s/n): ")
            if confirmar.lower() == "s":
                del alunos[posicao]
                print("Aluno removido.")
            else:
                print("Remoção cancelada.")

    # ---------- 8 - RELATÓRIO ----------
    elif opcao == "8":
        recebido = 0.0
        pendente = 0.0
        contagem = [0, 0, 0]
        for a in alunos:
            i = NOMES_PLANOS.index(a[2])
            if a[3] == "sim":
                recebido += VALORES_PLANOS[i]
            else:
                pendente += VALORES_PLANOS[i]
            contagem[i] += 1

        print(f"Total de alunos: {len(alunos)}")
        print(f"  Basico: {contagem[0]}")
        print(f"  Intermediario: {contagem[1]}")
        print(f"  Premium: {contagem[2]}")
        print(f"Valor recebido:  R$ {recebido:.2f}")
        print(f"Valor pendente:  R$ {pendente:.2f}")
        print(f"Total previsto:  R$ {recebido + pendente:.2f}")

    # ---------- 0 - SAIR ----------
    elif opcao == "0":
        print("Até logo!")
        break

    else:
        print("Opção inválida.")

    # Salva tudo no arquivo a cada volta do menu
    arquivo = open(ARQUIVO, "w", encoding="utf-8")
    for a in alunos:
        arquivo.write(f"{a[0]};{a[1]};{a[2]};{a[3]}\n")
    arquivo.close()