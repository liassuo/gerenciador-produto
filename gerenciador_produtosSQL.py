import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox

def cadastrar_produto():
    def salvar_produto():
        serial = entry_serial.get()
        nome = entry_nome.get()
        descricao = entry_descricao.get()
        preco = entry_preco.get()

        try:
            conn = psycopg2.connect(
                host='localhost',
                database='Produtos',
                user='postgres',
                password='aluno'
            )
            cursor = conn.cursor()

            cursor.execute('INSERT INTO Produtos (codigo, nome, descricao, preco) VALUES (%s, %s, %s, %s)', (serial, nome, descricao, preco))
            conn.commit()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            janela_cadastro.destroy()  # Fecha a janela de cadastro após salvar

        except psycopg2.Error as e:
            messagebox.showerror("Erro de Banco de Dados", str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    janela_cadastro = tk.Toplevel(root)
    janela_cadastro.title("Cadastrar Produto")
    janela_cadastro.geometry("400x550")
    janela_cadastro.configure(bg="#ECEFF1")

    label_serial = ttk.Label(janela_cadastro, text="Código Serial:")
    label_serial.pack(pady=5)
    entry_serial = ttk.Entry(janela_cadastro, width=30)
    entry_serial.pack(pady=5)

    label_nome = ttk.Label(janela_cadastro, text="Nome:")
    label_nome.pack(pady=5)
    entry_nome = ttk.Entry(janela_cadastro, width=30)
    entry_nome.pack(pady=5)

    label_descricao = ttk.Label(janela_cadastro, text="Descrição:")
    label_descricao.pack(pady=5)
    entry_descricao = ttk.Entry(janela_cadastro, width=30)
    entry_descricao.pack(pady=5)

    label_preco = ttk.Label(janela_cadastro, text="Preço:")
    label_preco.pack(pady=5)
    entry_preco = ttk.Entry(janela_cadastro, width=30)
    entry_preco.pack(pady=5)

    btn_salvar = ttk.Button(janela_cadastro, text="Salvar Produto", command=salvar_produto)
    btn_salvar.pack(pady=20)

def buscar_produto():
    codigo = entry_serial.get()

    try:
        conn = psycopg2.connect(
            host='localhost',
            database='Produtos',
            user='postgres',
            password='aluno'
        )
        cursor = conn.cursor()

        cursor.execute('SELECT nome, descricao, preco FROM Produtos WHERE codigo = %s', (codigo,))
        resultado = cursor.fetchone()

        if resultado:
            label_nome['text'] = f"Nome: {resultado[0]}"
            label_descricao['text'] = f"Descrição: {resultado[1]}"
            label_preco['text'] = f"Preço: R$ {resultado[2]:.2f}"
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")

    except psycopg2.Error as e:
        messagebox.showerror("Erro de Banco de Dados", str(e))

    finally:
        if conn:
            cursor.close()
            conn.close()

def criar_tabela():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Produtos",
            user="postgres",
            password="aluno",
        )
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produtos(
                codigo SERIAL PRIMARY KEY,
                nome VARCHAR(100),
                descricao TEXT,
                preco NUMERIC(10, 2)
            )
        ''')

        conn.commit()

    except psycopg2.Error as e:
        messagebox.showerror("Erro de Banco de Dados", str(e))

    finally:
        if conn:
            cursor.close()
            conn.close()

def configurar_estilo():
    style = ttk.Style()
    style.configure('TLabel', font=('Helvetica', 12), padding=10)
    style.configure('TButton', font=('Helvetica', 10, 'bold'), background='#4CAF50', foreground='black', padding=5)
    style.configure('TEntry', padding=5)
    style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), foreground='#37474F')
    style.map('TButton', background=[('active', '#66BB6A')])

def centralizar_janela(root, largura, altura):
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

root = tk.Tk()
root.title("Leitor de Código Serial")
centralizar_janela(root, 500, 600)
root.configure(bg="#ECEFF1")

configurar_estilo()

frame = ttk.Frame(root, padding="20 20 20 20")
frame.pack(pady=20)

title_label = ttk.Label(frame, text="Consulta de Produto", style='Title.TLabel')
title_label.grid(row=0, column=0, columnspan=2, pady=10)

label_serial = ttk.Label(frame, text="Código Serial:")
label_serial.grid(row=1, column=0, pady=10, sticky="E")

entry_serial = ttk.Entry(frame, width=30, font=('Helvetica', 12))
entry_serial.grid(row=1, column=1, pady=10, padx=5)

btn_buscar = ttk.Button(frame, text="Buscar", command=buscar_produto)
btn_buscar.grid(row=2, columnspan=2, pady=20)

btn_cadastrar = ttk.Button(frame, text="Cadastrar Produto", command=cadastrar_produto)
btn_cadastrar.grid(row=3, columnspan=2, pady=10)

label_nome = ttk.Label(root, text="Nome: ", font=('Helvetica', 12))
label_nome.pack(pady=5)

label_descricao = ttk.Label(root, text="Descrição: ", font=('Helvetica', 12))
label_descricao.pack(pady=5)

label_preco = ttk.Label(root, text="Preço: ", font=('Helvetica', 12))
label_preco.pack(pady=5)

footer = ttk.Label(root, text="Sistema de Consulta de Produtos", font=('Helvetica', 10), foreground='#78909C')
footer.pack(side='bottom', pady=10)

criar_tabela()

root.mainloop()
