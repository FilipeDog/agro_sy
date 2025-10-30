"""
Formulário Genérico para Cadastros Secundários
"""
import tkinter as tk
from tkinter import messagebox
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class GenericRegisterWindow:
    """Janela genérica para cadastros secundários"""

    def __init__(self, parent, db_manager, table_name, title):
        """
        Inicializa a janela de cadastro genérico

        Args:
            parent: Frame pai
            db_manager: Instância do DatabaseManager
            table_name: Nome da tabela no banco
            title: Título da tela
        """
        self.parent = parent
        self.db_manager = db_manager
        self.table_name = table_name
        self.title = title

        # Variáveis
        self.selected_id = None

        # Criar interface
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=X, padx=20, pady=10)

        title_label = ttk.Label(
            title_frame,
            text=self.title,
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(side=LEFT)

        # Frame dividido em duas colunas
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Coluna esquerda - Formulário
        left_frame = ttk.LabelFrame(content_frame, text="Dados", padding=20)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Campo Nome
        ttk.Label(left_frame, text="Nome:", font=("Helvetica", 10)).grid(row=0, column=0, sticky=W, pady=5)
        self.nome_entry = ttk.Entry(left_frame, font=("Helvetica", 11), width=40)
        self.nome_entry.grid(row=0, column=1, sticky=W+E, pady=5, padx=(10, 0))

        # Campo Descrição
        ttk.Label(left_frame, text="Descrição:", font=("Helvetica", 10)).grid(row=1, column=0, sticky=W+N, pady=5)
        self.descricao_text = tk.Text(left_frame, font=("Helvetica", 10), width=40, height=5)
        self.descricao_text.grid(row=1, column=1, sticky=W+E, pady=5, padx=(10, 0))

        # Configurar grid
        left_frame.columnconfigure(1, weight=1)

        # Botões de ação
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.btn_novo = ttk.Button(buttons_frame, text="Novo", command=self.clear_form, width=12)
        self.btn_novo.pack(side=LEFT, padx=5)

        self.btn_salvar = ttk.Button(buttons_frame, text="Salvar", command=self.save_data, width=12)
        self.btn_salvar.pack(side=LEFT, padx=5)

        self.btn_excluir = ttk.Button(buttons_frame, text="Excluir", command=self.delete_data, width=12)
        self.btn_excluir.pack(side=LEFT, padx=5)

        # Coluna direita - Lista
        right_frame = ttk.LabelFrame(content_frame, text="Registros Cadastrados", padding=20)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Campo de busca
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(search_frame, text="Buscar:").pack(side=LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=LEFT, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_data())

        ttk.Button(search_frame, text="Listar Todos", command=self.load_data).pack(side=LEFT)

        # Tabela
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill=BOTH, expand=YES)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        # Treeview
        columns = ("ID", "Nome", "Descrição")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_h.set
        )
        scrollbar.config(command=self.tree.yview)

        scrollbar_h.config(command=self.tree.xview)

        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Descrição", text="Descrição")

        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("Descrição", width=300)

        self.tree.pack(fill=BOTH, expand=YES)

        # Bind duplo clique
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_data(self):
        """Carrega os dados da tabela"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Buscar dados
        data = self.db_manager.select(self.table_name, order_by="nome")

        # Inserir na tabela
        for row in data:
            values = (
                row['id'],
                row['nome'],
                row['descricao'] if 'descricao' in row.keys() else ''
            )
            self.tree.insert('', END, values=values)

    def filter_data(self):
        """Filtra os dados da tabela"""
        search_term = self.search_entry.get().strip().lower()

        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Buscar dados
        data = self.db_manager.select(self.table_name, order_by="nome")

        # Filtrar e inserir
        for row in data:
            if search_term in row['nome'].lower():
                values = (
                    row['id'],
                    row['nome'],
                    row['descricao'] if 'descricao' in row.keys() else ''
                )
                self.tree.insert('', END, values=values)

    def load_selected(self):
        """Carrega o item selecionado no formulário"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self.selected_id = values[0]
        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, values[1])

        self.descricao_text.delete('1.0', END)
        self.descricao_text.insert('1.0', values[2])

    def clear_form(self):
        """Limpa o formulário"""
        self.selected_id = None
        self.nome_entry.delete(0, END)
        self.descricao_text.delete('1.0', END)
        self.nome_entry.focus()

    def save_data(self):
        """Salva os dados"""
        nome = self.nome_entry.get().strip()
        descricao = self.descricao_text.get('1.0', END).strip()

        # Validar
        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return

        # Preparar dados
        data = {'nome': nome}
        if descricao:
            data['descricao'] = descricao

        try:
            if self.selected_id:
                # Atualizar
                self.db_manager.update(
                    self.table_name,
                    data,
                    "id = ?",
                    [self.selected_id]
                )
                messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
            else:
                # Inserir
                self.db_manager.insert(self.table_name, data)
                messagebox.showinfo("Sucesso", "Registro cadastrado com sucesso!")

            self.clear_form()
            self.load_data()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_data(self):
        """Exclui o registro selecionado"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este registro?"):
            try:
                self.db_manager.delete(self.table_name, "id = ?", [self.selected_id])
                messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
                self.clear_form()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")
