import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Definir o tamanho da fonte
font_tamanho = ("Arial", 10)  # Nome da fonte e tamanho


# Função para conectar ao banco de dados SQLite
def conectar_bd():
    try:
        with sqlite3.connect("clinica_veterinaria.db") as conn:
            return conn
    except sqlite3.Error as e:
        messagebox.showerror(
            "Erro", f"Não foi possível conectar ao banco de dados: {e}"
        )
        return None


def cadastrar_cliente():
    conn = conectar_bd()
    if conn:
        try:
            cur = conn.cursor()

            # Convertendo todos os campos para maiúsculas
            nome_cliente = entry_nome_cadastro.get().upper()
            telefone = entry_telefone.get().upper()
            email = entry_email.get().upper()
            endereco = entry_endereco.get().upper()
            cpf = entry_cpf.get().upper()
            nome_pet = entry_nome_pet.get().upper()
            nome_racao = entry_nome_racao.get().upper()

            # Verificar se o CPF, Email e Nome do Pet estão preenchidos
            if not email:
                messagebox.showerror("Erro", "O campo Email não pode estar em branco!")
                return

            if not nome_pet:
                messagebox.showerror(
                    "Erro", "O campo Nome do Pet não pode estar em branco!"
                )
                return

            # Verificar se o CPF já está cadastrado
            cur.execute("SELECT id FROM clientes WHERE cpf = ?", (cpf,))
            resultado = cur.fetchone()
            if resultado:
                messagebox.showerror("Erro", "Este CPF já está cadastrado!")
                return

            # Cadastro do cliente
            cur.execute(
                "INSERT INTO clientes (nome, telefone, email, endereco, cpf) VALUES (?, ?, ?, ?, ?)",
                (
                    nome_cliente,
                    telefone,
                    email,
                    endereco,
                    cpf,
                ),
            )
            cliente_id = cur.lastrowid

            # Cadastro do pet
            if nome_pet:
                cur.execute(
                    "INSERT INTO pets (nome_pet, cliente_id) VALUES (?, ?)",
                    (nome_pet, cliente_id),
                )

            # Cadastro da amostra de ração
            if nome_racao:
                cur.execute(
                    "INSERT INTO amostras (nome_racao) VALUES (?)",
                    (nome_racao,),
                )
                racao_id = cur.lastrowid
                # Registrar a distribuição da amostra
                cur.execute(
                    "INSERT INTO distribuicoes (cliente_id, amostra_id) VALUES (?, ?)",
                    (cliente_id, racao_id),
                )

            conn.commit()
            messagebox.showinfo(
                "Sucesso", "Cliente, pet e amostra cadastrados com sucesso!"
            )
            limpar_campos_cadastro()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")
            conn.rollback()
        finally:
            conn.close()


def buscar_cliente_ou_pet():
    try:
        conn = conectar_bd()
        cur = conn.cursor()

        nome_cliente = entry_nome_busca_cliente.get().strip().upper()
        nome_pet = entry_nome_busca_pet.get().strip().upper()
        cpf = entry_cpf_busca.get().strip().upper()

        query = """
            SELECT c.id, c.nome, c.telefone, c.email, c.endereco, c.cpf, p.nome_pet, a.nome_racao
            FROM clientes c
            LEFT JOIN pets p ON c.id = p.cliente_id
            LEFT JOIN distribuicoes d ON c.id = d.cliente_id
            LEFT JOIN amostras a ON d.amostra_id = a.id
            WHERE
        """
        params = []

        if cpf:
            query += "c.cpf = ?"
            params.append(cpf)
        elif nome_cliente:
            query += "c.nome = ?"
            params.append(nome_cliente)
        elif nome_pet:
            query += "p.nome_pet = ?"
            params.append(nome_pet)
        else:
            messagebox.showerror(
                "Erro", "Digite o nome do cliente, do pet ou o CPF para buscar."
            )
            return

        cur.execute(query, params)

        resultados = cur.fetchall()

        if resultados:
            info = ""
            for resultado in resultados:
                info += (
                    f"ID: {resultado[0]}\n"
                    f"Nome do Cliente: {resultado[1]}\n"
                    f"Telefone: {resultado[2]}\n"
                    f"Email: {resultado[3]}\n"
                    f"Endereço: {resultado[4]}\n"
                    f"CPF: {resultado[5]}\n"
                    f"Nome do Pet: {resultado[6] if resultado[6] else 'Nenhum pet cadastrado'}\n"
                    f"Nome da Amostra de Ração: {resultado[7] if resultado[7] else 'Nenhuma amostra cadastrada'}\n"
                    "--------------------\n"
                )
            messagebox.showinfo("Resultado da Busca", info)
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")

        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar: {e}")


# Função para limpar os campos de cadastro
def limpar_campos_cadastro():
    entry_nome_cadastro.delete(0, END)
    entry_telefone.delete(0, END)
    entry_email.delete(0, END)
    entry_endereco.delete(0, END)
    entry_cpf.delete(0, END)
    entry_nome_pet.delete(0, END)
    entry_nome_racao.delete(0, END)


# Interface Gráfica (Tkinter)
root = Tk()
root.title("Cadastro - Doação")
root.geometry("600x480")
root.resizable(False, False)
root.configure(bg="#E0FED9")
# root.iconbitmap("img/dog.ico")

# Criação do Notebook e abas
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Aba de Login
aba_login = Frame(notebook, bg="#A7DB9B")
notebook.add(aba_login, text="Login")

# Título da Aba de Login
titulo_login = Label(
    aba_login,
    text="LOGIN",
    font=("Helvetica", 15, "bold", "underline"),
    bg="#A7DB9B",
    fg="#093002",
)
titulo_login.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")


# Função de login
def fazer_login():
    username = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    conn = conectar_bd()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM usuarios WHERE username = ? AND senha = ?", (username, senha)
        )
        usuario = cur.fetchone()

        if usuario:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            mostrar_abas()  # Exibe as abas principais após o login
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        conn.close()


# Função para abrir a janela de registro de novo usuário
def abrir_janela_registro():
    janela_registro = Toplevel(root)
    janela_registro.title("Registrar Novo Usuário")

    janela_registro.geometry("600x500")  # Aumente a altura para acomodar o novo campo
    janela_registro.configure(bg="#E0FED9")
    janela_registro.resizable(False, False)

    # Configure a grade para centralizar os elementos
    for i in range(6):
        janela_registro.grid_rowconfigure(i, weight=1)
    for i in range(2):
        janela_registro.grid_columnconfigure(i, weight=1)

    Label(
        janela_registro, text="Novo Usuário:", font=("Arial", 10, "bold"), bg="#E0FED9"
    ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_novo_usuario = Entry(
        janela_registro, font=("Arial", 10, "bold"), bg="#A7DB9B"
    )
    entry_novo_usuario.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    Label(
        janela_registro, text="Senha:", font=("Arial", 10, "bold"), bg="#E0FED9"
    ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_nova_senha = Entry(
        janela_registro, font=("Arial", 10, "bold"), bg="#A7DB9B", show="*"
    )
    entry_nova_senha.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    Label(
        janela_registro,
        text="Confirme a Senha:",
        font=("Arial", 10, "bold"),
        bg="#E0FED9",
    ).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_confirmacao_senha = Entry(  # Corrigido: use entry_confirmacao_senha
        janela_registro, font=("Arial", 10, "bold"), bg="#A7DB9B", show="*"
    )
    entry_confirmacao_senha.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Novo campo para o e-mail
    Label(
        janela_registro, text="Email:", font=("Arial", 10, "bold"), bg="#E0FED9"
    ).grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_email_usuario = Entry(
        janela_registro, font=("Arial", 10, "bold"), bg="#A7DB9B"
    )
    entry_email_usuario.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    Button(
        janela_registro,
        text="Registrar",
        command=lambda: registrar_usuario(
            entry_novo_usuario.get(),
            entry_nova_senha.get(),
            entry_email_usuario.get(),
            entry_confirmacao_senha.get(),  # Passa a confirmação de senha
        ),
        bg="#093002",
        fg="#ffffff",
        bd=5,
        padx=20,
        pady=5,
        cursor="hand2",
        font=("Arial", 10, "bold"),
    ).grid(row=4, columnspan=2, pady=20)


# Função para registrar um novo usuário
def registrar_usuario(username, senha, email, confirmacao_senha):
    if not username or not senha or not email or not confirmacao_senha:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if senha != confirmacao_senha:
        messagebox.showerror("Erro", "As senhas não coincidem.")
        return

    conn = conectar_bd()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (username, senha, email) VALUES (?, ?, ?)",
                (username, senha, email),
            )
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar usuário: {e}")
        finally:
            conn.close()


# Função para ocultar as abas principais
def ocultar_abas():
    notebook.hide(aba_cadastro)
    notebook.hide(aba_busca)


# Função para mostrar as abas principais
def mostrar_abas():
    notebook.add(aba_cadastro, text="Cadastrar")
    notebook.add(aba_busca, text="Buscar")
    notebook.hide(aba_login)  # Oculta a aba de login após o login ser bem-sucedido


# Definindo as linhas e colunas para expandir
aba_login.grid_rowconfigure(0, weight=1)
aba_login.grid_rowconfigure(1, weight=1)
aba_login.grid_rowconfigure(2, weight=1)
aba_login.grid_rowconfigure(3, weight=1)
aba_login.grid_columnconfigure(0, weight=1)
aba_login.grid_columnconfigure(1, weight=1)

# Campos de login
Label(
    aba_login,
    text="Usuário:",
    font=("Arial", 12, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(row=1, column=0, padx=0, pady=(60, 0), sticky="e")
entry_usuario = Entry(aba_login, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_usuario.grid(row=1, column=1, padx=0, pady=(60, 0), sticky="w")
Label(
    aba_login,
    text="Senha:",
    font=("Arial", 12, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(row=2, column=0, padx=10, pady=(0, 120), sticky="e")
entry_senha = Entry(aba_login, font=("Arial", 10, "bold"), bg="#E0FED9", show="*")
entry_senha.grid(row=2, column=1, padx=0, pady=(0, 120), sticky="w")

Button(
    aba_login,
    text="Login",
    command=fazer_login,
    bg="#093002",
    fg="#ffffff",
    bd=5,
    padx=20,
    pady=10,
    cursor="hand2",
    font=("Arial", 10, "bold"),
    width=20,
).grid(row=2, columnspan=2, pady=(80, 0), sticky="s")

# Frase adicional
frase = Label(
    aba_login,
    text="Não tem uma conta? Registre-se abaixo:",
    font=("Arial", 9),
    bg="#A7DB9B",
    fg="#093002",
)
frase.grid(
    row=4, column=0, columnspan=2, pady=(2, 0), sticky="n"
)  # Ajuste o row conforme necessário

# Atualizando o botão de registrar na aba de login
Button(
    aba_login,
    text="Registrar",
    command=abrir_janela_registro,  # Abre a nova janela
    bg="#093002",
    fg="#ffffff",
    bd=5,
    padx=20,
    pady=10,
    cursor="hand2",
    font=("Arial", 10, "bold"),
    width=20,
).grid(row=5, columnspan=2, pady=(5, 50), sticky="s")

# Aba de Cadastro
aba_cadastro = Frame(notebook, bg="#A7DB9B")
notebook.add(aba_cadastro, text="Cadastrar")

# Título da Aba
titulo = Label(
    aba_cadastro,
    text="CADASTRAR",
    font=("Helvetica", 15, "bold", "underline"),
    bg="#A7DB9B",
    fg="#093002",
)
titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")


# Carregar e redimensionar a imagem de fundo
imagem_fundo = Image.open("img/dogreal.png")  # Coloque o caminho da sua imagem
imagem_fundo = imagem_fundo.resize((300, 250))

imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)

# Criar um Label com a imagem de fundo
label_fundo = Label(aba_cadastro, image=imagem_fundo_tk, bg="#A7DB9B")
label_fundo.place(x=160, y=110, relwidth=1, relheight=1)  # Ajustar para preencher a aba


# Cadastro de Cliente
Label(
    aba_cadastro, text="Nome:", font=("Arial", 10, "bold"), bg="#A7DB9B", fg="#093002"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=(70, 10),
    sticky="w",
)

entry_nome_cadastro = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_nome_cadastro.grid(
    row=0,
    column=1,
    padx=10,
    pady=(70, 10),
    sticky="w",
)


Label(
    aba_cadastro,
    text="Telefone:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)
entry_telefone = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_telefone.grid(
    row=1,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

Label(
    aba_cadastro, text="Email:", font=("Arial", 10, "bold"), bg="#A7DB9B", fg="#093002"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)

entry_email = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_email.grid(
    row=2,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

Label(
    aba_cadastro,
    text="Endereço:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=3,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)
entry_endereco = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_endereco.grid(
    row=3,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

Label(
    aba_cadastro, text="CPF:", font=("Arial", 10, "bold"), bg="#A7DB9B", fg="#093002"
).grid(
    row=4,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)

entry_cpf = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_cpf.grid(
    row=4,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

# Cadastro de Pet
Label(
    aba_cadastro,
    text="Nome do Pet:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=5,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)
entry_nome_pet = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_nome_pet.grid(
    row=5,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

# Cadastro de Amostra de Ração
Label(
    aba_cadastro,
    text="Amostra de Ração:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=6,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)
entry_nome_racao = Entry(aba_cadastro, font=("Arial", 10, "bold"), bg="#E0FED9")
entry_nome_racao.grid(
    row=6,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

Button(
    aba_cadastro,
    text="Finalizar Cadastro",
    command=cadastrar_cliente,
    bg="#093002",
    fg="#ffffff",
    bd=5,
    padx=50,
    pady=5,
    cursor="hand2",
    font=("Arial", 10, "bold"),
).grid(row=7, columnspan=2, pady=20)

# Aba de Busca
aba_busca = Frame(notebook, bg="#A7DB9B")
notebook.add(aba_busca, text="Buscar")

# Carregar e redimensionar a imagem de fundo para a aba de busca
imagem_fundo_busca = Image.open("img/pata.png")  # Coloque o caminho da sua imagem
imagem_fundo_busca = imagem_fundo_busca.resize((300, 250))

imagem_fundo_busca_tk = ImageTk.PhotoImage(imagem_fundo_busca)

# Criar um Label com a imagem de fundo na aba de busca
label_fundo_busca = Label(aba_busca, image=imagem_fundo_busca_tk, bg="#A7DB9B")
label_fundo_busca.place(
    x=160, y=110, relwidth=1, relheight=1
)  # Ajustar para preencher a aba


# Título da Aba
titulo = Label(
    aba_busca,
    text="BUSCAR",
    font=("Helvetica", 15, "bold", "underline"),
    bg="#A7DB9B",
    fg="#093002",
)
titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")


# Campo de busca por nome do cliente
Label(
    aba_busca,
    text="Cliente para Busca:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=0,
    column=0,
    padx=10,
    pady=(100, 10),
    sticky="w",
)
entry_nome_busca_cliente = Entry(aba_busca, font=font_tamanho, bg="#E0FED9")
entry_nome_busca_cliente.grid(
    row=0,
    column=1,
    padx=10,
    pady=(100, 10),
    sticky="w",
)

# Campo de busca por nome do pet
Label(
    aba_busca,
    text="Pet para Busca:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)
entry_nome_busca_pet = Entry(aba_busca, font=font_tamanho, bg="#E0FED9")
entry_nome_busca_pet.grid(
    row=1,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

# Campo de busca por CPF
Label(
    aba_busca,
    text="CPF para Busca:",
    font=("Arial", 10, "bold"),
    bg="#A7DB9B",
    fg="#093002",
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w",
)
entry_cpf_busca = Entry(aba_busca, font=font_tamanho, bg="#E0FED9")
entry_cpf_busca.grid(
    row=2,
    column=1,
    padx=10,
    pady=10,
    sticky="w",
)

Button(
    aba_busca,
    text="Buscar",
    command=buscar_cliente_ou_pet,
    bg="#093002",
    fg="#ffffff",
    bd=5,
    padx=50,
    pady=5,
    cursor="hand2",
    font=("Arial", 10, "bold"),
).grid(row=7, columnspan=2, pady=20)

ocultar_abas()

root.mainloop()
