import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATABASE_FILE = "crm_data.json"

def carregar_dados():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(dados):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def buscar_cliente(nome, dados):
    resultados = [cliente for cliente in dados if nome.lower() in cliente.get("nome", "").lower()]
    return resultados

def editar_cliente(indice, novos_dados, dados):
    if 0 <= indice < len(dados):
        dados[indice].update(novos_dados)
        salvar_dados(dados)
        return True
    return False

def excluir_cliente(indice, dados):
    if 0 <= indice < len(dados):
        del dados[indice]
        salvar_dados(dados)
        return True
    return False

def exibir_clientes():
    lista_clientes.delete(*lista_clientes.get_children())
    for cliente in dados:
        lista_clientes.insert("", "end", values=(cliente["nome"], cliente["endereco"], cliente["telefone"], cliente["email"]))

def adicionar_cliente():
    def salvar_novo_cliente():
        try:
            novo_cliente = {"nome": nome_entry.get(), "endereco": endereco_entry.get(), "telefone": telefone_entry.get(), "email": email_entry.get()}
            if not all(novo_cliente.values()):
                raise ValueError("Todos os campos devem ser preenchidos.")
            dados.append(novo_cliente)
            salvar_dados(dados)
            exibir_clientes()
            adicionar_janela.destroy()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    adicionar_janela = tk.Toplevel(root)
    adicionar_janela.title("Adicionar Cliente")
    labels = ["Nome:", "Endereço:", "Telefone:", "E-mail:"]
    entries = []
    for i, label_text in enumerate(labels):
        tk.Label(adicionar_janela, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(adicionar_janela)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        entries.append(entry)
    nome_entry, endereco_entry, telefone_entry, email_entry = entries
    tk.Button(adicionar_janela, text="Salvar", command=salvar_novo_cliente).grid(row=len(labels), column=0, columnspan=2, pady=10)

def editar_cliente_selecionado():
    selecionado = lista_clientes.selection()
    if selecionado:
        indice = lista_clientes.index(selecionado)
        cliente = dados[indice]

        def salvar_edicao():
            try:
                novos_dados = {"nome": nome_entry.get(), "endereco": endereco_entry.get(), "telefone": telefone_entry.get(), "email": email_entry.get()}
                if not all(novos_dados.values()):
                    raise ValueError("Todos os campos devem ser preenchidos.")

                if editar_cliente(indice, novos_dados, dados):
                    exibir_clientes()
                    editar_janela.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

        editar_janela = tk.Toplevel(root)
        editar_janela.title("Editar Cliente")
        labels = ["Nome:", "Endereço:", "Telefone:", "E-mail:"]
        entries = []
        for i, label_text in enumerate(labels):
            tk.Label(editar_janela, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(editar_janela)
            entry.insert(0, cliente[list(cliente.keys())[i]])
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries.append(entry)

        nome_entry, endereco_entry, telefone_entry, email_entry = entries
        tk.Button(editar_janela, text="Salvar Edição", command=salvar_edicao).grid(row=len(labels), column=0, columnspan=2, pady=10)
    else:
        messagebox.showinfo("Atenção", "Selecione um cliente para editar.")

def excluir_cliente_selecionado():
    selecionado = lista_clientes.selection()
    if selecionado:
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este cliente?"):
            indice = lista_clientes.index(selecionado)
            if excluir_cliente(indice, dados):
                exibir_clientes()
    else:
        messagebox.showinfo("Atenção", "Selecione um cliente para excluir.")

def buscar_cliente_interface():
    nome_busca = busca_entry.get()
    resultados = buscar_cliente(nome_busca, dados)
    lista_clientes.delete(*lista_clientes.get_children())
    for cliente in resultados:
        lista_clientes.insert("", "end", values=(cliente["nome"], cliente["endereco"], cliente["telefone"], cliente["email"]))

# --- Interface Gráfica ---
root = tk.Tk()
root.title("Sistema de CRM")
root.configure(bg="#e0f2f7")

dados = carregar_dados()

# Estilo
style = ttk.Style()
style.configure("Treeview", background="#ffffff", foreground="black", rowheight=25, fieldbackground="#ffffff")
style.configure("Treeview.Heading", background="#d0e0e3", font=('Arial Bold', 10))
style.map('Treeview', background=[('selected', '#a7c5eb')])

main_frame = tk.Frame(root, bg="#e0f2f7", padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

frame_lista = tk.Frame(main_frame, bg="#e0f2f7")
frame_lista.pack(pady=(0,10), fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(frame_lista)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_x = tk.Scrollbar(frame_lista, orient='horizontal')
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

lista_clientes = ttk.Treeview(frame_lista, columns=("Nome", "Endereço", "Telefone", "Email"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
lista_clientes.heading("Nome", text="Nome")
lista_clientes.heading("Endereço", text="Endereço")
lista_clientes.heading("Telefone", text="Telefone")
lista_clientes.heading("Email", text="Email")
lista_clientes.pack(fill=tk.BOTH, expand=True)

scrollbar_y.config(command=lista_clientes.yview)
scrollbar_x.config(command=lista_clientes.xview)

busca_frame = tk.Frame(main_frame, bg="#e0f2f7")
busca_frame.pack(fill=tk.X)

busca_label = tk.Label(busca_frame, text="Buscar Cliente:", bg="#e0f2f7", font=("Arial",15))
busca_label.pack(side=tk.LEFT)
busca_entry = tk.Entry(busca_frame, font=("Arial",15))
busca_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
busca_botao = tk.Button(busca_frame, text="Buscar", command=buscar_cliente_interface, font=("Arial",12,"bold"), bg="#7E03A7", fg="#FFFFFF")
busca_botao.pack(side=tk.LEFT)

frame_botoes = tk.Frame(main_frame, bg="#e0f2f7")
frame_botoes.pack()

botao_adicionar = tk.Button(frame_botoes, text="Adicionar Cliente", command=adicionar_cliente, font=("Arial",12,"bold"), bg="#007F6C", fg="#FFFFFF")
botao_adicionar.pack(side=tk.LEFT, padx=5)

botao_editar = tk.Button(frame_botoes, text="Editar Cliente", command=editar_cliente_selecionado, font=("Arial",12,"bold"), bg="#797A00", fg="#FFFFFF")
botao_editar.pack(side=tk.LEFT, padx=5)

botao_excluir = tk.Button(frame_botoes, text="Excluir Cliente", command=excluir_cliente_selecionado, font=("Arial",12,"bold"), bg="#C88800", fg="#FFFFFF")
botao_excluir.pack(side=tk.LEFT, padx=5)

# Initial Display
exibir_clientes()

# Main loop
root.mainloop()