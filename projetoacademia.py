# ============================================================
# SISTEMA DE ACADEMIA (versão simplificada) — com IMC
#
# Usa: dicionários, arquivos, funções, repetição e decisão.
# Os dados ficam salvos em "academia.txt", uma linha por aluno:
#   nome;idade;peso;altura;plano;pago
#   Ana;25;60.0;1.65;Premium;sim
# ============================================================

ARQUIVO = "academia.txt"

# Planos: nome -> mensalidade
PLANOS = {"Basico": 80, "Intermediario": 110, "Premium": 150}

# Dica para cada classificação de IMC
DICAS = {
    "Abaixo do peso": "Foco em ganho de massa: treino de força e boa alimentação.",
    "Peso normal": "Manter a rotina: treino de força + cardio equilibrados.",
    "Sobrepeso": "Combinar musculação com cardio 3x por semana.",
    "Obesidade": "Começar leve e com acompanhamento profissional.",
}


# ------------------------------------------------------------
# IMC
# ------------------------------------------------------------
def calcular_imc(peso, altura):
    return peso / (altura * altura)


def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidade"


# ------------------------------------------------------------
# Arquivo
# ------------------------------------------------------------
def carregar_alunos():
    alunos = []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip() == "":
                    continue
                nome, idade, peso, altura, plano, pago = linha.strip().split(";")
                alunos.append({
                    "nome": nome,
                    "idade": int(idade),
                    "peso": float(peso),
                    "altura": float(altura),
                    "plano": plano,
                    "pago": pago == "sim",
                })
    except FileNotFoundError:
        pass  # primeira vez: ainda não existe arquivo
    return alunos


def salvar_alunos(alunos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        for a in alunos:
            pago = "sim" if a["pago"] else "nao"
            arquivo.write(f"{a['nome']};{a['idade']};{a['peso']};{a['altura']};{a['plano']};{pago}\n")


# ------------------------------------------------------------
# Funções de apoio
# ------------------------------------------------------------
def ler_numero(mensagem):
    """Lê um número (aceita vírgula ou ponto) e repete até ser válido."""
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um número válido.")


def buscar_aluno(alunos, nome):
    """Devolve o aluno (dicionário) ou None."""
    for aluno in alunos:
        if aluno["nome"].lower() == nome.lower():
            return aluno
    return None


def mostrar_aluno(aluno):
    imc = calcular_imc(aluno["peso"], aluno["altura"])
    classificacao = classificar_imc(imc)
    situacao = "Pago" if aluno["pago"] else "Pendente"

    print("-" * 40)
    print("Nome:", aluno["nome"])
    print("Idade:", aluno["idade"])
    print(f"Peso: {aluno['peso']} kg | Altura: {aluno['altura']} m")
    print(f"IMC: {imc:.1f} ({classificacao})")
    print("Dica:", DICAS[classificacao])
    print(f"Plano: {aluno['plano']} (R$ {PLANOS[aluno['plano']]})")
    print("Mensalidade:", situacao)


# ------------------------------------------------------------
# Opções do menu
# ------------------------------------------------------------
def cadastrar(alunos):
    nome = input("Nome: ").strip().replace(";", "")
    if nome == "":
        print("Nome inválido.")
        return
    if buscar_aluno(alunos, nome):
        print("Esse aluno já está cadastrado.")
        return

    idade = int(ler_numero("Idade: "))
    peso = ler_numero("Peso (kg): ")
    altura = ler_numero("Altura (m): ")
    if altura > 3:            # se digitou em cm (ex.: 175), converte para metros
        altura = altura / 100

    print("Planos:", ", ".join(f"{p} (R$ {v})" for p, v in PLANOS.items()))
    plano = input("Plano: ").strip().capitalize()
    while plano not in PLANOS:
        plano = input("Plano inválido, digite novamente: ").strip().capitalize()

    alunos.append({"nome": nome, "idade": idade, "peso": peso,
                   "altura": altura, "plano": plano, "pago": False})
    salvar_alunos(alunos)
    print("Aluno cadastrado!")


def listar(alunos):
    if len(alunos) == 0:
        print("Nenhum aluno cadastrado.")
    for aluno in alunos:
        mostrar_aluno(aluno)


def pesquisar(alunos):
    aluno = buscar_aluno(alunos, input("Nome: ").strip())
    if aluno:
        mostrar_aluno(aluno)
    else:
        print("Aluno não encontrado.")


def atualizar_peso(alunos):
    aluno = buscar_aluno(alunos, input("Nome: ").strip())
    if not aluno:
        print("Aluno não encontrado.")
        return

    peso_antigo = aluno["peso"]
    aluno["peso"] = ler_numero("Novo peso (kg): ")
    salvar_alunos(alunos)

    diferenca = aluno["peso"] - peso_antigo
    imc = calcular_imc(aluno["peso"], aluno["altura"])
    print(f"Diferença de peso: {diferenca:+.1f} kg")
    print(f"Novo IMC: {imc:.1f} ({classificar_imc(imc)})")


def registrar_pagamento(alunos):
    aluno = buscar_aluno(alunos, input("Nome: ").strip())
    if not aluno:
        print("Aluno não encontrado.")
    elif aluno["pago"]:
        print("Mensalidade já está paga.")
    else:
        aluno["pago"] = True
        salvar_alunos(alunos)
        print("Pagamento registrado!")


def remover(alunos):
    aluno = buscar_aluno(alunos, input("Nome: ").strip())
    if aluno:
        alunos.remove(aluno)
        salvar_alunos(alunos)
        print("Aluno removido.")
    else:
        print("Aluno não encontrado.")


def relatorio(alunos):
    recebido = 0
    pendente = 0
    for aluno in alunos:
        valor = PLANOS[aluno["plano"]]
        if aluno["pago"]:
            recebido += valor
        else:
            pendente += valor

    print("\n===== RELATÓRIO =====")
    print("Total de alunos:", len(alunos))
    print(f"Recebido: R$ {recebido}")
    print(f"Pendente: R$ {pendente}")
    print(f"Total previsto: R$ {recebido + pendente}")

    # Quantos alunos em cada classificação de IMC
    if len(alunos) > 0:
        contagem = {}
        for aluno in alunos:
            imc = calcular_imc(aluno["peso"], aluno["altura"])
            classificacao = classificar_imc(imc)
            contagem[classificacao] = contagem.get(classificacao, 0) + 1

        print("\nAlunos por IMC:")
        for classificacao, quantidade in contagem.items():
            print(f"  {classificacao}: {quantidade}")


# ------------------------------------------------------------
# Menu
# ------------------------------------------------------------
def menu():
    alunos = carregar_alunos()

    while True:
        print("\n===== ACADEMIA =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Pesquisar aluno")
        print("4 - Atualizar peso")
        print("5 - Registrar pagamento")
        print("6 - Remover aluno")
        print("7 - Relatório")
        print("8 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            cadastrar(alunos)
        elif opcao == "2":
            listar(alunos)
        elif opcao == "3":
            pesquisar(alunos)
        elif opcao == "4":
            atualizar_peso(alunos)
        elif opcao == "5":
            registrar_pagamento(alunos)
        elif opcao == "6":
            remover(alunos)
        elif opcao == "7":
            relatorio(alunos)
        elif opcao == "8":
            print("Até logo!")
            break
        else:
            print("Opção inválida!")


menu()