import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import pytz
import sys
import json
import os
import pandas as pd
from datetime import datetime
from button_styles import style_button_confirm, style_button_cancel, style_button_default, style_button_default2


# Caminho do arquivo de configuração
CONFIG_FILE = 'config.json'

# Função para carregar configuração
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            numero_familias = config.get('numero_familias', '0')
            return numero_familias
    return '0'

# Função para salvar configuração
def save_config(numero_familias):
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'numero_familias': numero_familias}, file)

# Conectar ao banco de dados PostgreSQL
def connect_db():
    if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
    else:
                base_path = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(base_path, 'estoque_ftm.db')
    print(f"Acessando banco de dados em: {db_path}")
    return sqlite3.connect(db_path)

def check_table_exists():
    conn = connect_db()  # Função connect_db para garantir o caminho correto
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ESTOQUE'")
    result = cursor.fetchone()
    conn.close()

    if result:
        print("Tabela 'ESTOQUE' existe.")
    else:
        print("Tabela 'ESTOQUE' não existe.")

# Carregar dados na tabela do Tkinter
def load_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item, peso, quantidade FROM estoque ORDER BY item ASC")
        rows = cursor.fetchall()
        conn.close()

        # Atualizar a tabela
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert('', 'end', values=row)

        # Atualizar a data da última atualização
        update_last_update_date()
        # Forçar a atualização da interface
        root.update_idletasks()

def update_last_update_date():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT data_atualizacao FROM estoque ORDER BY data_atualizacao DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()

    if result:
        last_update_str = result[0]
        try:
            # Converta a string para um objeto datetime em UTC
            utc_time = datetime.strptime(last_update_str, "%Y-%m-%d %H:%M:%S")
            utc_time = utc_time.replace(tzinfo=pytz.utc)
            # Converta para o fuso horário local
            local_time = utc_time.astimezone()
            # Formate a data para a string desejada
            formatted_date = local_time.strftime("%d/%m/%Y %H:%M:%S")
            # Atualize o texto da label
            label_last_update.config(text=f"Última atualização feita em {formatted_date}")
        except ValueError as e:
            print(f"Erro ao analisar a data: {e}")
            label_last_update.config(text="Erro ao formatar a data")
    else:
        label_last_update.config(text="Última atualização não disponível")

# Carregar dados da tabela cestabase na aba Cesta Básica
def load_cesta_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item, peso, quantidade FROM cestabase ORDER BY item ASC")
        rows = cursor.fetchall()
        conn.close()

        for item in tree_cesta.get_children():
            tree_cesta.delete(item)

        for row in rows:
            tree_cesta.insert('', 'end', values=row)

# Adicionar um item
def add_item():
    def save_item():
        selected_item = item_combobox.get()
        quantidade = entry_quantidade.get()

        if not selected_item or not quantidade:
            messagebox.showerror("Erro", "Item e Quantidade devem ser preenchidos")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            
            # Buscar o código do item selecionado
            cursor.execute("SELECT codigo FROM estoque WHERE item = ?", [selected_item])
            item_code = cursor.fetchone()
            
            if item_code:
                item_code = item_code[0]  # Pegar o código retornado

                # Atualizar o item no banco de dados
                cursor.execute(
            "UPDATE estoque SET quantidade = quantidade + ?, data_atualizacao = CURRENT_TIMESTAMP WHERE codigo = ?",
            (quantidade, item_code)
        )
                conn.commit()
                conn.close()
                load_data()
                add_window.destroy()
            else:
                messagebox.showerror("Erro", "Item não encontrado.")
                conn.close()

    def add_new_item():
        def confirm_new_item():
            item = entry_new_item.get()
            peso = entry_peso.get()
            quantidade = entry_quantidade.get()

            if not item or not peso or not quantidade:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Buscar o último código da tabela
                cursor.execute("SELECT MAX(codigo) FROM estoque")
                last_code = cursor.fetchone()[0]

                # Definir o novo código
                new_code = 1 if last_code is None else last_code + 1

                cursor.execute(
            "INSERT INTO estoque (codigo, item, peso, quantidade, data_atualizacao) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (new_code, item, peso, quantidade)
        )
                conn.commit()
                conn.close()
                load_data()
                add_window.destroy()

        def cancel():
            add_window.destroy()

        add_window = tk.Toplevel(root)
        add_window.title("Adicionar Novo Item")

        tk.Label(add_window, text="Item").grid(row=0, column=0, padx=10, pady=5)
        entry_new_item = tk.Entry(add_window)
        entry_new_item.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Peso").grid(row=1, column=0, padx=10, pady=5)
        entry_peso = tk.Entry(add_window)
        entry_peso.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Quantidade").grid(row=2, column=0, padx=10, pady=5)
        entry_quantidade = tk.Entry(add_window)
        entry_quantidade.grid(row=2, column=1, padx=10, pady=5)

        confirm_button = tk.Button(add_window, text="Confirmar", command=confirm_new_item)
        style_button_confirm(confirm_button)  # Aplicar o estilo ao botão Confirmar
        confirm_button.grid(row=3, column=0, padx=10, pady=10)

        cancel_button = tk.Button(add_window, text="Cancelar", command=cancel)
        style_button_cancel(cancel_button)  # Aplicar o estilo ao botão Cancelar
        cancel_button.grid(row=3, column=1, padx=10, pady=10)

    def cancel():
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Adicionar Item")

    tk.Label(add_window, text="Selecionar Item").grid(row=0, column=0, padx=10, pady=5)
    item_combobox = ttk.Combobox(add_window)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item FROM estoque ORDER BY item ASC")
        items = cursor.fetchall()
        item_combobox['values'] = [i[0] for i in items]
        conn.close()
    item_combobox.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Quantidade").grid(row=2, column=0, padx=10, pady=5)
    entry_quantidade = tk.Entry(add_window)
    entry_quantidade.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

    default_button = tk.Button(add_window, text="Adicionar Item Novo", command=add_new_item)
    style_button_default(default_button)  # Aplicar o estilo aos demais botões
    default_button.grid(row=4, column=0, padx=5, pady=10)

    confirm_button = tk.Button(add_window, text="Confirmar", command=save_item, width=10)
    style_button_confirm(confirm_button)  # Aplicar o estilo ao botão Confirmar
    confirm_button.grid(row=4, column=1, padx=5, pady=10)

    cancel_button = tk.Button(add_window, text="Cancelar", command=cancel, width=10)
    style_button_cancel(cancel_button)  # Aplicar o estilo ao botão Cancelar
    cancel_button.grid(row=4, column=2, padx=5, pady=10)

# Remover um item
def remove_item():
    def confirm_deletion():
        selected_item = item_combobox.get()

        if not selected_item:
            messagebox.showerror("Erro", "Nenhum item selecionado")
            return

        # Mensagem de confirmação
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Isso apagará o item '{selected_item}', assim como toda a quantidade do estoque. Deseja Continuar?")
        if confirm:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()

                # Remover o item da tabela estoque
                cursor.execute("DELETE FROM estoque WHERE item = ?", [selected_item])
                conn.commit()
                conn.close()

                load_data()  # Recarregar dados da tabela após exclusão
                remove_window.destroy()

    def cancel():
        remove_window.destroy()

    remove_window = tk.Toplevel(root)
    remove_window.title("Remover Item")

    tk.Label(remove_window, text="Selecionar Item").grid(row=0, column=0, padx=10, pady=5)
    item_combobox = ttk.Combobox(remove_window)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item FROM estoque ORDER BY item ASC")
        items = cursor.fetchall()
        item_combobox['values'] = [i[0] for i in items]
        conn.close()
    item_combobox.grid(row=0, column=1, padx=10, pady=5)

    confirm_button=tk.Button(remove_window, text="Confirmar", command=confirm_deletion, width=15)
    style_button_confirm(confirm_button)
    confirm_button.grid(row=1, column=0, padx=10, pady=10)

    cancel_button = tk.Button(remove_window, text="Cancelar", command=cancel, width=15)
    style_button_cancel(cancel_button)
    cancel_button.grid(row=1, column=1, padx=10, pady=10) 

# Entregar cestas
def deliver_baskets():
    # Obter o número de famílias do JSON
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            numero_familias = int(config.get('numero_familias', 0))  # Converter para inteiro
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o número de famílias: {e}")
        return

    if numero_familias <= 0:
        messagebox.showerror("Erro", "Número de famílias inválido.")
        return

    # Conectar ao banco de dados
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        # Obter a lista de itens e suas quantidades na cestabase
        cursor.execute("SELECT item, quantidade FROM cestabase")
        cestas = cursor.fetchall()

        # Dicionário para armazenar a quantidade total que falta
        faltando = {}
        estoque_suficiente = True  # Flag para verificar se todos os itens têm estoque suficiente

        for item, quantidade_na_cesta in cestas:
            quantidade_necessaria = quantidade_na_cesta * numero_familias

            # Verificar o estoque atual
            cursor.execute("SELECT quantidade FROM estoque WHERE item = ?", (item,))
            estoque = cursor.fetchone()

            if estoque:
                quantidade_em_estoque = estoque[0]
                quantidade_final = quantidade_em_estoque - quantidade_necessaria

                if quantidade_final < 0:
                    faltando[item] = -quantidade_final
                    estoque_suficiente = False  # Marcar como falso se faltar algum item
            else:
                faltando[item] = quantidade_necessaria  # Caso o item não esteja no estoque
                estoque_suficiente = False  # Marcar como falso se o item não estiver no estoque

        # Se não houver itens faltando, realizar a subtração no estoque
        if estoque_suficiente:
            for item, quantidade_na_cesta in cestas:
                quantidade_necessaria = quantidade_na_cesta * numero_familias

                # Verificar o estoque atual novamente para atualizar o estoque
                cursor.execute("SELECT quantidade FROM estoque WHERE item = ?", (item,))
                estoque = cursor.fetchone()

                if estoque:
                    quantidade_em_estoque = estoque[0]
                    quantidade_final = quantidade_em_estoque - quantidade_necessaria

                    # Atualizar o estoque
                    cursor.execute("UPDATE estoque SET quantidade = ?, data_atualizacao = datetime('now') WHERE item = ?", (quantidade_final, item))

            conn.commit()

            # Atualizar a tabela de Itens em Estoque após a entrega
            load_data()  # Recarregar a tabela de estoque na interface do Tkinter

            messagebox.showinfo("Sucesso", "Cestas entregues com sucesso! Estoque atualizado.")
        else:
            # Caso contrário, mostrar a mensagem de itens em falta
            mensagem = "Não foi possível continuar com a entrega pois faltam os seguintes itens:\n"

            # Ordenar os itens em ordem alfabética
            for item in sorted(faltando.keys()):
                quantidade_faltando = faltando[item]
                mensagem += f"Item: {item}, Quantidade Faltando: {quantidade_faltando}\n"

            messagebox.showwarning("Itens em Falta", mensagem)

        conn.close()
    else:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")

# Atualizar o número de famílias
def atualizar_familias():
    def salvar_familias():
        numero_familias_atual = entry_num_familias_input.get()
        save_config(numero_familias_atual)
        entry_num_familias.config(state='normal')
        entry_num_familias.delete(0, 'end')
        entry_num_familias.insert(0, numero_familias_atual)
        entry_num_familias.config(state='readonly')
        atualizar_window.destroy()

    def sair():
        atualizar_window.destroy()

    atualizar_window = tk.Toplevel(root)
    atualizar_window.title("Atualizar Número de Famílias")

    tk.Label(atualizar_window, text="Quantas famílias quer atender?").pack(padx=10, pady=10)

    entry_num_familias_input = tk.Entry(atualizar_window)
    entry_num_familias_input.pack(padx=10, pady=10)

    confirm_button = tk.Button(atualizar_window, text="Confirmar", command=salvar_familias, width=10)
    style_button_confirm(confirm_button)
    confirm_button.pack(side='left', padx=10, pady=10)
    
    cancel_button = tk.Button(atualizar_window, text="Cancelar", command=sair, width=10)
    style_button_cancel(cancel_button)
    cancel_button.pack(side='right', padx=10, pady=10)

# Exportar os dados da tabela para um arquivo XLS
def export_to_xls(data, file_path):
    df = pd.DataFrame(data, columns=["Item", "Peso", "Quantidades que Faltam"])
    df.to_excel(file_path, index=False)
    messagebox.showinfo("Exportar", f"Dados exportados com sucesso para {file_path}")

# Mostrar itens em falta
def show_missing_items():
    def calculate_missing_items():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item, quantidade FROM cestabase")
            cesta_items = cursor.fetchall()
            
            cursor.execute("SELECT item, peso, quantidade FROM estoque")
            estoque_items = cursor.fetchall()
            conn.close()

            missing_items = []
            num_familias = int(load_config())

            # Criar um dicionário para acesso rápido às quantidades do estoque
            estoque_dict = {item[0]: (item[1], item[2]) for item in estoque_items}
            
            for item, qtd_cesta in cesta_items:
                qtd_necessaria = qtd_cesta * num_familias
                peso, qtd_disponivel = estoque_dict.get(item, (0, 0))
                falta = qtd_necessaria - qtd_disponivel
                
                if falta > 0:
                    missing_items.append((item, peso, falta))
            
            # Ordenar a lista de itens faltantes em ordem ascendente pelo nome do item
            missing_items.sort(key=lambda x: x[0])

            # Limpar a tabela de itens faltantes
            for item in tree_missing.get_children():
                tree_missing.delete(item)

            # Inserir os itens faltantes na tabela
            for row in missing_items:
                tree_missing.insert('', 'end', values=row)

            # Atualizar o botão de exportar
            def export_data():
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
                if file_path:
                    export_to_xls(missing_items, file_path)

            export_button.config(command=export_data)

    missing_window = tk.Toplevel(root)
    missing_window.title("Itens em Falta")

    # Criar frame para a árvore e o botão
    frame_missing = tk.Frame(missing_window)
    frame_missing.pack(fill='both', expand=True, padx=10, pady=10)

    tree_missing = ttk.Treeview(frame_missing, columns=("Item", "Peso", "Quantidades que Faltam"), show='headings')

    tree_missing.heading("Item", text="Item")
    tree_missing.heading("Peso", text="Peso")
    tree_missing.heading("Quantidades que Faltam", text="Quantidades que Faltam")

    tree_missing.column("Item", width=200, anchor='center')
    tree_missing.column("Peso", width=100, anchor='center')
    tree_missing.column("Quantidades que Faltam", width=150, anchor='center')

    tree_missing.pack(side='left', fill='both', expand=True)

    vsb = tk.Scrollbar(frame_missing, orient="vertical", command=tree_missing.yview)
    tree_missing.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')

    # Botão de exportar
    export_button = tk.Button(missing_window, text="Exportar Tabela")
    style_button_confirm(export_button)
    export_button.pack(pady=10)

    calculate_missing_items()

# Chamar quando a aba Cesta Básica é selecionada
def on_cesta_tab_selected(event):
    if notebook.index(notebook.select()) == 1:  # Aba "Cesta Básica"
        load_cesta_data()

# Configurar a interface Tkinter
root = tk.Tk()
root.title("Controle Cesta Básica FTM")

# Menu com abas
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10)

# Aba Estoque
frame_estoque = tk.Frame(notebook)
notebook.add(frame_estoque, text="Estoque")

# Aba Cesta Básica
frame_cesta_basica = tk.Frame(notebook)
notebook.add(frame_cesta_basica, text="Cesta Básica")

# Associar o evento de seleção da aba "Cesta Básica"
notebook.bind("<<NotebookTabChanged>>", on_cesta_tab_selected)

# Dividindo a aba "Estoque" em duas partes 
frame_left_estoque = tk.Frame(frame_estoque)
frame_left_estoque.pack(side="left", padx=20, pady=20)

frame_right_estoque = tk.Frame(frame_estoque)
frame_right_estoque.pack(side="right", padx=20, pady=20)

# Configuração da aba Estoque (lado esquerdo)
label_header_estoque = tk.Label(frame_left_estoque, text="Itens em Estoque", font=("Arial", 12, 'bold'))
label_header_estoque.pack(pady=10)

columns_estoque = ("Item", "Peso", "Quantidade")
tree = ttk.Treeview(frame_left_estoque, columns=columns_estoque, show='headings')

tree.heading("Item", text="Item")
tree.heading("Peso", text="Peso")
tree.heading("Quantidade", text="Quantidade")

tree.column("Item", width=200, anchor='center')
tree.column("Peso", width=100, anchor='center')
tree.column("Quantidade", width=100, anchor='center')

tree.pack()

# Label para última atualização
label_last_update = tk.Label(frame_left_estoque, text="Última atualização feita em --/--/----")
label_last_update.pack(pady=10)

# Carregar dados da tabela Estoque
load_data()

# Configuração da aba Estoque (lado direito - famílias)
numero_familias_atual = load_config()

tk.Label(frame_right_estoque, text="Número de Famílias", font=("Arial", 10, 'bold')).grid(row=0, column=0, pady=5, sticky='w')
entry_num_familias = tk.Entry(frame_right_estoque, state='normal', width=10)
entry_num_familias.insert(0, numero_familias_atual)
entry_num_familias.config(state='readonly')
entry_num_familias.grid(row=1, column=0, padx=2, pady=5, sticky='w')

default_button2 = tk.Button(frame_right_estoque, text="Atualizar", command=atualizar_familias, width=10)
style_button_default2(default_button2)
default_button2.grid(row=1, column=1, pady=10, sticky='ew')

default_button2 = tk.Button(frame_right_estoque, text="Atualizar Estoque", command=add_item)
style_button_default2(default_button2)
default_button2.grid(row=2, column=0, columnspan=3, pady=10, sticky='ew')

cancel_button = tk.Button(frame_right_estoque, text="Remover Item", command=remove_item)
style_button_cancel(cancel_button)
cancel_button.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')

default_button = tk.Button(frame_right_estoque, text="Itens em Falta", command=show_missing_items)
style_button_default(default_button)
default_button.grid(row=4, column=0, columnspan=3, pady=10, sticky='ew')

confirm_button = tk.Button(frame_right_estoque, text="Entregar Cestas", command=deliver_baskets)
style_button_confirm(confirm_button)
confirm_button.grid(row=5, column=0, columnspan=3, pady=10, sticky='ew')

# Configuração da aba Cesta Básica
label_header_cesta = tk.Label(frame_cesta_basica, text="Itens da Cesta Básica", font=("Arial", 12, 'bold'))
label_header_cesta.pack(pady=10)

columns_cesta = ("Item", "Peso", "Quantidade")
tree_cesta = ttk.Treeview(frame_cesta_basica, columns=columns_cesta, show='headings')

tree_cesta.heading("Item", text="Item")
tree_cesta.heading("Peso", text="Peso")
tree_cesta.heading("Quantidade", text="Quantidade")

tree_cesta.column("Item", width=200, anchor='center')
tree_cesta.column("Peso", width=100, anchor='center')
tree_cesta.column("Quantidade", width=100, anchor='center')

tree_cesta.pack()

# Mantendo o pack
frame_botao = tk.Frame(frame_cesta_basica)
frame_botao.pack(pady=10)

# Atualizando tabela Cesta Base
def update_cesta_basica_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item, peso, quantidade FROM cestabase ORDER BY item ASC")
        rows = cursor.fetchall()
        conn.close()

        for item in tree_cesta.get_children():
            tree_cesta.delete(item)

        for row in rows:
            tree_cesta.insert('', 'end', values=row)

# Adicionar item Cesta Base
def add_item_cesta_basica():
    # Criar nova janela
    window = tk.Toplevel()
    window.title("Adicionar Item à Cesta Básica")

    tk.Label(window, text="Item").grid(row=0, column=0)
    entry_item = tk.Entry(window)
    entry_item.grid(row=0, column=1)

    tk.Label(window, text="Peso").grid(row=1, column=0)
    entry_peso = tk.Entry(window)
    entry_peso.grid(row=1, column=1)

    tk.Label(window, text="Quantidade").grid(row=2, column=0)
    entry_quantidade = tk.Entry(window)
    entry_quantidade.grid(row=2, column=1)

    # Função para salvar no banco de dados
    def salvar_item_cesta_basica():
        item = entry_item.get()
        peso = entry_peso.get()
        quantidade = entry_quantidade.get()
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO cestabase (chave, item, peso, quantidade)
                    VALUES ((SELECT COALESCE(MAX(chave), 0) + 1 FROM cestabase), ?, ?, ?)
                """, (item, peso, quantidade))
                conn.commit()
                messagebox.showinfo("Sucesso", "Item adicionado à Cesta Básica!")
                               
                update_cesta_basica_table()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar item: {e}")
            finally:
                cursor.close()
                conn.close()
                window.destroy()

    confirm_button = tk.Button(window, text="Confirmar", command=salvar_item_cesta_basica)
    style_button_confirm(confirm_button)
    confirm_button.grid(row=3, column=0, padx=10, pady=10)

    cancel_button = tk.Button(window, text="Cancelar", command=window.destroy)
    style_button_cancel(cancel_button)
    cancel_button.grid(row=3, column=1, padx=10, pady=10)

def remover_item_cesta_basica():
    def confirm_deletion():
        selected_item = item_combobox.get()

        if not selected_item:
            messagebox.showerror("Erro", "Nenhum item selecionado")
            return

        # Mensagem de confirmação
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Isso apagará o item '{selected_item}' da Cesta Básica. Deseja Continuar?")
        if confirm:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM cestabase WHERE item = ?", [selected_item])
                conn.commit()
                conn.close()

                load_data()  # Recarregar dados da tabela após exclusão
                remove_window.destroy()
               
                update_cesta_basica_table()

    def cancel():
        remove_window.destroy()

    remove_window = tk.Toplevel(root)
    remove_window.title("Remover Item Cesta Básica")

    tk.Label(remove_window, text="Selecionar Item").grid(row=0, column=0, padx=10, pady=5)
    item_combobox = ttk.Combobox(remove_window)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item FROM cestabase ORDER BY item ASC")
        items = cursor.fetchall()
        item_combobox['values'] = [i[0] for i in items]
        conn.close()
    item_combobox.grid(row=0, column=1, padx=10, pady=5)

    confirm_button = tk.Button(remove_window, text="Confirmar", command=confirm_deletion)
    style_button_confirm(confirm_button)
    confirm_button.grid(row=1, column=0, padx=10, pady=10)

    cancel_button = tk.Button(remove_window, text="Cancelar", command=cancel)
    style_button_cancel(cancel_button)
    cancel_button.grid(row=1, column=1, padx=10, pady=10)

def alterar_quantidade_cesta_basica():
    def salvar_quantidade():
        selected_item = item_combobox.get()
        nova_quantidade = entry_quantidade.get()

        if not selected_item or not nova_quantidade:
            messagebox.showerror("Erro", "Item e Quantidade devem ser preenchidos")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
                        
            cursor.execute(
                "UPDATE cestabase SET quantidade = ? WHERE item = ?",
                [nova_quantidade, selected_item]
            )
            conn.commit()
            conn.close()
            update_cesta_basica_table()
            alter_window.destroy()

    def cancel():
        alter_window.destroy()

    alter_window = tk.Toplevel(root)
    alter_window.title("Alterar Quantidade na Cesta Básica")

    tk.Label(alter_window, text="Selecionar Item").grid(row=0, column=0, padx=10, pady=5)
    item_combobox = ttk.Combobox(alter_window)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item FROM cestabase ORDER BY item ASC")
        items = cursor.fetchall()
        item_combobox['values'] = [i[0] for i in items]
        conn.close()
    item_combobox.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(alter_window, text="Nova Quantidade").grid(row=1, column=0, padx=10, pady=5)
    entry_quantidade = tk.Entry(alter_window)
    entry_quantidade.grid(row=1, column=1, padx=10, pady=5)

    confirm_button = tk.Button(alter_window, text="Confirmar", command=salvar_quantidade, width=15)
    style_button_confirm(confirm_button)
    confirm_button.grid(row=2, column=0, padx=10, pady=10)
    
    cancel_button = tk.Button(alter_window, text="Cancelar", command=cancel, width=15)
    style_button_cancel(cancel_button)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)


# Adicionando funcionalidade ao botão
default_button = tk.Button(frame_botao, text="Adicionar Item Cesta Básica", command=add_item_cesta_basica)
style_button_default(default_button)
default_button.grid(row=0, column=0, padx=10)

cancel_button = tk.Button(frame_botao, text="Remover Item Cesta Básica", command=remover_item_cesta_basica)
style_button_cancel(cancel_button)
cancel_button.grid(row=0, column=1, padx=10)

default_button2 = tk.Button(frame_botao, text="Alterar Quantidade",command=alterar_quantidade_cesta_basica)
style_button_default2(default_button2)
default_button2.grid(row=0, column=2, padx=10)


root.mainloop()
