import tkinter as tk
from tkinter import ttk, messagebox

# ------------------------------------------------------------
# Configurações
# ------------------------------------------------------------
ARQUIVO = "alunos.txt"

PLANOS = {
    "Basico": 80.00,
    "Intermediario": 120.00,
    "Premium": 180.00,
}


# ------------------------------------------------------------
# Persistência
# ------------------------------------------------------------
def carregar_alunos() -> list:
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
        pass
    return alunos


def salvar_alunos(alunos: list) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        for a in alunos:
            pago = "sim" if a["pago"] else "nao"
            arquivo.write(f"{a['nome']};{a['idade']};{a['plano']};{pago}\n")


# ------------------------------------------------------------
# Interface
# ------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Academia")
        self.geometry("760x520")
        self.minsize(700, 480)

        self.alunos = carregar_alunos()

        self.var_nome = tk.StringVar()
        self.var_idade = tk.StringVar()
        self.var_plano = tk.StringVar(value=list(PLANOS)[0])
        self.var_busca = tk.StringVar()
        self.var_pendentes = tk.BooleanVar(value=False)

        self.criar_widgets()
        self.atualizar_lista()

    def criar_widgets(self):
        # --- Formulário de cadastro ---
        form = ttk.LabelFrame(self, text="Aluno", padding=10)
        form.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_nome, width=30).grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Idade:").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_idade, width=6).grid(row=0, column=3, padx=5)

        ttk.Label(form, text="Plano:").grid(row=0, column=4, sticky="w")
        ttk.Combobox(form, textvariable=self.var_plano, values=list(PLANOS),
                     state="readonly", width=14).grid(row=0, column=5, padx=5)

        ttk.Button(form, text="Cadastrar", command=self.cadastrar).grid(row=0, column=6, padx=(10, 0))

        # --- Busca e filtro ---
        filtro = ttk.Frame(self)
        filtro.pack(fill="x", padx=10, pady=5)

        ttk.Label(filtro, text="Pesquisar:").pack(side="left")
        entrada_busca = ttk.Entry(filtro, textvariable=self.var_busca, width=30)
        entrada_busca.pack(side="left", padx=5)
        self.var_busca.trace_add("write", lambda *_: self.atualizar_lista())

        ttk.Checkbutton(filtro, text="Somente pendentes", variable=self.var_pendentes,
                        command=self.atualizar_lista).pack(side="left", padx=10)

        # --- Tabela ---
        quadro = ttk.Frame(self)
        quadro.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("nome", "idade", "plano", "valor", "situacao")
        self.tabela = ttk.Treeview(quadro, columns=colunas, show="headings", selectmode="browse")
        titulos = {"nome": "Nome", "idade": "Idade", "plano": "Plano",
                   "valor": "Valor (R$)", "situacao": "Mensalidade"}
        larguras = {"nome": 220, "idade": 60, "plano": 120, "valor": 90, "situacao": 110}
        for c in colunas:
            self.tabela.heading(c, text=titulos[c])
            self.tabela.column(c, width=larguras[c], anchor="w" if c == "nome" else "center")

        barra = ttk.Scrollbar(quadro, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.tabela.tag_configure("pendente", foreground="#b00020")
        self.tabela.tag_configure("pago", foreground="#1b7a2f")
        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar)

        # --- Botões de ação ---
        botoes = ttk.Frame(self)
        botoes.pack(fill="x", padx=10, pady=(5, 5))

        ttk.Button(botoes, text="Alterar plano (usa o plano do formulário)",
                   command=self.alterar_plano).pack(side="left")
        ttk.Button(botoes, text="Registrar pagamento",
                   command=self.registrar_pagamento).pack(side="left", padx=5)
        ttk.Button(botoes, text="Remover aluno",
                   command=self.remover).pack(side="left")
        ttk.Button(botoes, text="Relatório",
                   command=self.relatorio).pack(side="right")

        # --- Barra de status ---
        self.var_status = tk.StringVar()
        ttk.Label(self, textvariable=self.var_status, relief="sunken",
                  anchor="w", padding=3).pack(fill="x", side="bottom")

    # --------------------------------------------------------
    # Utilidades
    # --------------------------------------------------------
    def buscar_por_nome(self, nome):
        for a in self.alunos:
            if a["nome"].lower() == nome.lower():
                return a
        return None

    def aluno_selecionado(self):
        sel = self.tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela.")
            return None
        return self.alunos[int(sel[0])]

    def atualizar_lista(self):
        self.tabela.delete(*self.tabela.get_children())
        texto = self.var_busca.get().strip().lower()
        for i, a in enumerate(self.alunos):
            if self.var_pendentes.get() and a["pago"]:
                continue
            if texto and texto not in a["nome"].lower():
                continue
            situacao = "Pago" if a["pago"] else "Pendente"
            self.tabela.insert(
                "", "end", iid=str(i),
                values=(a["nome"], a["idade"], a["plano"],
                        f"{PLANOS[a['plano']]:.2f}", situacao),
                tags=("pago" if a["pago"] else "pendente",),
            )
        self.var_status.set(f"{len(self.tabela.get_children())} aluno(s) exibido(s) "
                            f"de {len(self.alunos)}")

    def ao_selecionar(self, _evento):
        sel = self.tabela.selection()
        if sel:
            self.var_plano.set(self.alunos[int(sel[0])]["plano"])

    # --------------------------------------------------------
    # Ações
    # --------------------------------------------------------
    def cadastrar(self):
        nome = self.var_nome.get().strip().replace(";", "")
        if nome == "":
            messagebox.showerror("Erro", "Nome inválido.")
            return
        if self.buscar_por_nome(nome):
            messagebox.showerror("Erro", "Já existe um aluno com esse nome.")
            return
        try:
            idade = int(self.var_idade.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite uma idade válida (número inteiro).")
            return
        if idade < 12:
            messagebox.showerror("Erro", "Idade mínima para matrícula: 12 anos.")
            return

        self.alunos.append({"nome": nome, "idade": idade,
                            "plano": self.var_plano.get(), "pago": False})
        salvar_alunos(self.alunos)
        self.var_nome.set("")
        self.var_idade.set("")
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")

    def alterar_plano(self):
        aluno = self.aluno_selecionado()
        if not aluno:
            return
        novo = self.var_plano.get()
        if novo == aluno["plano"]:
            messagebox.showinfo("Aviso", "O aluno já está nesse plano.")
            return
        aluno["plano"] = novo
        salvar_alunos(self.alunos)
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Plano alterado com sucesso!")

    def registrar_pagamento(self):
        aluno = self.aluno_selecionado()
        if not aluno:
            return
        if aluno["pago"]:
            messagebox.showinfo("Aviso", "A mensalidade deste aluno já está paga.")
            return
        aluno["pago"] = True
        salvar_alunos(self.alunos)
        self.atualizar_lista()
        messagebox.showinfo("Sucesso",
                            f"Pagamento de R$ {PLANOS[aluno['plano']]:.2f} registrado!")

    def remover(self):
        aluno = self.aluno_selecionado()
        if not aluno:
            return
        if messagebox.askyesno("Confirmar", f"Remover {aluno['nome']}?"):
            self.alunos.remove(aluno)
            salvar_alunos(self.alunos)
            self.atualizar_lista()

    def relatorio(self):
        recebido = pendente = 0.0
        contagem = {p: 0 for p in PLANOS}
        for a in self.alunos:
            valor = PLANOS[a["plano"]]
            if a["pago"]:
                recebido += valor
            else:
                pendente += valor
            contagem[a["plano"]] += 1

        linhas = [f"Total de alunos: {len(self.alunos)}", ""]
        linhas += [f"  {p}: {q}" for p, q in contagem.items()]
        linhas += ["",
                   f"Valor recebido:  R$ {recebido:.2f}",
                   f"Valor pendente:  R$ {pendente:.2f}",
                   f"Total previsto:  R$ {recebido + pendente:.2f}"]
        messagebox.showinfo("Relatório", "\n".join(linhas))


if __name__ == "__main__":
    App().mainloop()