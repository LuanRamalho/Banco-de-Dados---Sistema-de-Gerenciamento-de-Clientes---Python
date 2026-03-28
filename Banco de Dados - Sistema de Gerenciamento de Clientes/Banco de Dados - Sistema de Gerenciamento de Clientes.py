import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATABASE_FILE = "crm_data.json"

# --- Lógica de Dados (Mantida) ---
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

# --- Interface de Cartões ---
def criar_card(parent, cliente, indice):
    """Cria um frame estilizado como cartão para cada cliente."""
    card = tk.Frame(parent, bg="white", highlightbackground="#d1d1d1", highlightthickness=1, bd=0)
    card.pack(fill=tk.X, padx=10, pady=5)

    # Conteúdo do Cartão
    info_frame = tk.Frame(card, bg="white")
    info_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

    tk.Label(info_frame, text=cliente["nome"], font=("Arial", 12, "bold"), bg="white", fg="#333").pack(anchor="w")
    tk.Label(info_frame, text=f"📍 {cliente['endereco']}", font=("Arial", 10), bg="white", fg="#666").pack(anchor="w")
    tk.Label(info_frame, text=f"📞 {cliente['telefone']}  |  ✉️ {cliente['email']}", font=("Arial", 9), bg="white", fg="#888").pack(anchor="w")

    # Botões de Ação no Cartão
    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(side=tk.RIGHT, padx=10)

    tk.Button(btn_frame, text="Editar", bg="#797A00", fg="white", command=lambda: abrir_janela_edicao(indice)).pack(side=tk.LEFT, padx=2)
    tk.Button(btn_frame, text="Excluir", bg="#C88800", fg="white", command=lambda: excluir_card(indice)).pack(side=tk.LEFT, padx=2)

def exibir_clientes(filtro=None):
    """Limpa e redesenha a lista de cartões."""
    # Limpa o frame interno
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    lista_para_exibir = filtro if filtro is not None else dados
    
    for i, cliente in enumerate(lista_para_exibir):
        criar_card(scrollable_frame, cliente, i)

# --- Funções de Ação Atualizadas ---
def adicionar_cliente():
    janela_form(titulo="Adicionar Cliente", callback=salvar_novo)

def abrir_janela_edicao(indice):
    janela_form(titulo="Editar Cliente", cliente=dados[indice], callback=lambda d: salvar_edicao(indice, d))

def excluir_card(indice):
    if messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
        del dados[indice]
        salvar_dados(dados)
        exibir_clientes()

def janela_form(titulo, cliente=None, callback=None):
    """Janela genérica para Adicionar/Editar."""
    win = tk.Toplevel(root)
    win.title(titulo)
    labels = ["Nome", "Endereço", "Telefone", "Email"]
    entries = {}

    for i, text in enumerate(labels):
        tk.Label(win, text=f"{text}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        ent = tk.Entry(win, width=30)
        ent.grid(row=i, column=1, padx=10, pady=5)
        if cliente:
            ent.insert(0, cliente[text.lower()])
        entries[text.lower()] = ent

    def processar():
        new_data = {k: v.get() for k, v in entries.items()}
        if all(new_data.values()):
            callback(new_data)
            win.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    tk.Button(win, text="Salvar", command=processar, bg="#007F6C", fg="white").grid(row=4, column=0, columnspan=2, pady=15)

def salvar_novo(novo_cliente):
    dados.append(novo_cliente)
    salvar_dados(dados)
    exibir_clientes()

def salvar_edicao(indice, novos_dados):
    dados[indice] = novos_dados
    salvar_dados(dados)
    exibir_clientes()

def buscar_cliente_interface():
    termo = busca_entry.get().lower()
    resultados = [c for c in dados if termo in c["nome"].lower()]
    exibir_clientes(resultados)

# --- Configuração da Janela Principal ---
root = tk.Tk()
root.title("Sistema de CRM")
root.geometry("600x500")
root.configure(bg="#f0f4f7")

dados = carregar_dados()

# Barra de Busca
busca_frame = tk.Frame(root, bg="#f0f4f7", pady=10)
busca_frame.pack(fill=tk.X, padx=10)
busca_entry = tk.Entry(busca_frame, font=("Arial", 12))
busca_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
tk.Button(busca_frame, text="🔍 Buscar", command=buscar_cliente_interface).pack(side=tk.LEFT)

# Área de Scroll para os Cartões
container = tk.Frame(root, bg="#f0f4f7")
container.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(container, bg="#f0f4f7", highlightthickness=0)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f4f7")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=580)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Botão Global de Adicionar
btn_add = tk.Button(root, text="+ Adicionar Novo Cliente", font=("Arial", 11, "bold"), 
                   bg="#007F6C", fg="white", pady=10, command=adicionar_cliente)
btn_add.pack(fill=tk.X)

exibir_clientes()
root.mainloop()
