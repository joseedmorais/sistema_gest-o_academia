# ------------------------------------------------------------
# Funções auxiliares (entrada de dados)
# ------------------------------------------------------------
def ler_inteiro(mensagem: str) -> int:
    """Lê um número inteiro, repetindo até o usuário digitar um valor válido."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def escolher_plano() -> str:
    """Mostra os planos disponíveis e devolve o nome do plano escolhido."""
    print("\nPlanos disponíveis:")
    for nome, valor in PLANOS.items():
        print(f"  {nome} - R$ {valor:.2f}")

    while True:
        plano = input("Plano: ").strip().capitalize()
        if plano in PLANOS:
            return plano
        print("Plano inexistente. Escolha um da lista.")


# ------------------------------------------------------------
# Funções de arquivo (persistência)
# ------------------------------------------------------------
def carregar_alunos() -> list:
    """Lê o arquivo e devolve uma lista de dicionários (um por aluno)."""
    alunos = []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha == "":
                    continue
                nome, idade, plano, pago = linha.split(";")
                alunos.append({
                    "nome": nome,
                    "idade": int(idade),
                    "plano": plano,
                    "pago": pago == "sim",
                })
    except FileNotFoundError:
        pass   # primeira execução: o arquivo ainda não existe
    return alunos


def salvar_alunos(alunos: list) -> None:
    """Grava todos os alunos no arquivo, substituindo o conteúdo anterior."""
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        for aluno in alunos:
            pago = "sim" if aluno["pago"] else "nao"
            arquivo.write(f"{aluno['nome']};{aluno['idade']};{aluno['plano']};{pago}\n")


# ------------------------------------------------------------
# Funções do sistema
# ------------------------------------------------------------
def buscar_por_nome(alunos: list, nome: str):
    """Devolve o dicionário do aluno ou None se não encontrar."""
    for aluno in alunos:
        if aluno["nome"].lower() == nome.lower():
            return aluno
    return None


def exibir_aluno(aluno: dict) -> None:
    situacao = "Pago" if aluno["pago"] else "Pendente"
    valor = PLANOS[aluno["plano"]]
    print(f"{aluno['nome']} | {aluno['idade']} anos | "
          f"{aluno['plano']} (R$ {valor:.2f}) | Mensalidade: {situacao}")


def cadastrar_aluno(alunos: list) -> None:
    nome = input("Nome do aluno: ").strip().replace(";", "")
    if nome == "":
        print("Nome inválido.")
        return
    if buscar_por_nome(alunos, nome):
        print("Já existe um aluno com esse nome.")
        return

    idade = ler_inteiro("Idade: ")
    if idade < 12:
        print("Idade mínima para matrícula: 12 anos.")
        return

    plano = escolher_plano()
    aluno = {"nome": nome, "idade": idade, "plano": plano, "pago": False}
    alunos.append(aluno)
    salvar_alunos(alunos)
    print("Aluno cadastrado com sucesso!")


def listar_alunos(alunos: list, apenas_pendentes: bool = False) -> None:
    """Lista os alunos. Com apenas_pendentes=True, mostra só quem não pagou."""
    contador = 0
    print("\n--- Alunos ---")
    for aluno in alunos:
        if apenas_pendentes and aluno["pago"]:
            continue
        contador += 1
        print(f"{contador}. ", end="")
        exibir_aluno(aluno)

    if contador == 0:
        print("Nenhum aluno para exibir.")


def pesquisar_aluno(alunos: list) -> None:
    nome = input("Nome do aluno: ").strip()
    aluno = buscar_por_nome(alunos, nome)
    if aluno:
        exibir_aluno(aluno)
    else:
        print("Aluno não encontrado.")


def alterar_plano(alunos: list) -> None:
    nome = input("Nome do aluno: ").strip()
    aluno = buscar_por_nome(alunos, nome)
    if not aluno:
        print("Aluno não encontrado.")
        return

    print(f"Plano atual: {aluno['plano']}")
    aluno["plano"] = escolher_plano()
    salvar_alunos(alunos)
    print("Plano alterado com sucesso!")


def registrar_pagamento(alunos: list) -> None:
    nome = input("Nome do aluno: ").strip()
    aluno = buscar_por_nome(alunos, nome)
    if not aluno:
        print("Aluno não encontrado.")
        return
    if aluno["pago"]:
        print("A mensalidade deste aluno já está paga.")
        return

    aluno["pago"] = True
    salvar_alunos(alunos)
    print(f"Pagamento de R$ {PLANOS[aluno['plano']]:.2f} registrado!")


def remover_aluno(alunos: list) -> None:
    nome = input("Nome do aluno: ").strip()
    aluno = buscar_por_nome(alunos, nome)
    if not aluno:
        print("Aluno não encontrado.")
        return

    confirmacao = input(f"Remover {aluno['nome']}? (s/n): ").strip().lower()
    if confirmacao == "s":
        alunos.remove(aluno)
        salvar_alunos(alunos)
        print("Aluno removido.")
    else:
        print("Operação cancelada.")


def calcular_faturamento(alunos: list) -> tuple:
    """Devolve (valor_recebido, valor_pendente) somando as mensalidades."""
    recebido = 0.0
    pendente = 0.0
    for aluno in alunos:
        valor = PLANOS[aluno["plano"]]
        if aluno["pago"]:
            recebido += valor
        else:
            pendente += valor
    return recebido, pendente


def contar_por_plano(alunos: list) -> dict:
    """Devolve um dicionário {plano: quantidade de alunos}."""
    contagem = {plano: 0 for plano in PLANOS}
    for aluno in alunos:
        contagem[aluno["plano"]] += 1
    return contagem


def exibir_relatorio(alunos: list) -> None:
    recebido, pendente = calcular_faturamento(alunos)
    contagem = contar_por_plano(alunos)

    print("\n========== RELATÓRIO ==========")
    print("Total de alunos:", len(alunos))
    for plano, quantidade in contagem.items():
        print(f"  {plano}: {quantidade}")
    print(f"Valor recebido:  R$ {recebido:.2f}")
    print(f"Valor pendente:  R$ {pendente:.2f}")
    print(f"Total previsto:  R$ {recebido + pendente:.2f}")


# ------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------
def exibir_menu() -> None:
    print("\n================================")
    print("      GESTÃO DE ACADEMIA")
    print("================================")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Listar mensalidades pendentes")
    print("4 - Pesquisar aluno")
    print("5 - Alterar plano")
    print("6 - Registrar pagamento")
    print("7 - Remover aluno")
    print("8 - Relatório")
    print("9 - Sair")


def menu() -> None:
    alunos = carregar_alunos()   # carrega os dados salvos ao iniciar

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_aluno(alunos)
        elif opcao == "2":
            listar_alunos(alunos)
        elif opcao == "3":
            listar_alunos(alunos, apenas_pendentes=True)
        elif opcao == "4":
            pesquisar_aluno(alunos)
        elif opcao == "5":
            alterar_plano(alunos)
        elif opcao == "6":
            registrar_pagamento(alunos)
        elif opcao == "7":
            remover_aluno(alunos)
        elif opcao == "8":
            exibir_relatorio(alunos)
        elif opcao == "9":
            print("Sistema encerrado. Bons treinos!")
            break
        else:
            print("Opção inválida!")


if _name_ == "_main_":
    menu()