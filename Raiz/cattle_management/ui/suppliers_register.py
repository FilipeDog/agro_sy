"""
Cadastro de Fornecedores
"""
import tkinter as tk
from tkinter import messagebox
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class SuppliersRegisterWindow:
    """Janela de cadastro de fornecedores"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_suppliers()

    def create_widgets(self):
        """Cria os widgets da interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(title_frame, text="Cadastro de Fornecedores", font=("Helvetica", 16, "bold")).pack(side=LEFT)

        # Frame dividido
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Coluna esquerda - Formulário com Scrollbar
        left_outer_frame = ttk.LabelFrame(content_frame, text="Dados do Fornecedor", padding=10)
        left_outer_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Canvas e Scrollbar para o formulário
        canvas = tk.Canvas(left_outer_frame, highlightthickness=0)
        scrollbar_form = ttk.Scrollbar(left_outer_frame, orient=VERTICAL, command=canvas.yview)
        left_frame = ttk.Frame(canvas)

        left_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=left_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_form.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar_form.pack(side=RIGHT, fill=Y)

        # Habilitar scroll com mouse - Bind apenas no canvas para evitar erros
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass

        # Bind nos widgets relevantes, não globalmente
        canvas.bind("<MouseWheel>", _on_mousewheel)
        left_outer_frame.bind("<MouseWheel>", _on_mousewheel)

        # Frame interno com padding
        form_inner = ttk.Frame(left_frame, padding=10)
        form_inner.pack(fill=BOTH, expand=YES)

        row = 0
        # Nome
        ttk.Label(form_inner, text="Nome:*").grid(row=row, column=0, sticky=W, pady=5)
        self.nome_entry = ttk.Entry(form_inner, width=40)
        self.nome_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        row += 1
        # CPF/CNPJ
        ttk.Label(form_inner, text="CPF/CNPJ:").grid(row=row, column=0, sticky=W, pady=5)
        self.cpf_cnpj_entry = ttk.Entry(form_inner, width=40)
        self.cpf_cnpj_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        row += 1
        # Email
        ttk.Label(form_inner, text="Email:").grid(row=row, column=0, sticky=W, pady=5)
        self.email_entry = ttk.Entry(form_inner, width=40)
        self.email_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        row += 1
        # Telefone
        ttk.Label(form_inner, text="Telefone:").grid(row=row, column=0, sticky=W, pady=5)
        self.telefone_entry = ttk.Entry(form_inner, width=40)
        self.telefone_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        row += 1
        # UF
        ttk.Label(form_inner, text="UF:").grid(row=row, column=0, sticky=W, pady=5)
        self.uf_entry = ttk.Entry(form_inner, width=5)
        self.uf_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        row += 1
        # Cidade
        ttk.Label(form_inner, text="Cidade:").grid(row=row, column=0, sticky=W, pady=5)
        self.cidade_entry = ttk.Entry(form_inner, width=40)
        self.cidade_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        row += 1
        # Endereço
        ttk.Label(form_inner, text="Endereço:").grid(row=row, column=0, sticky=W, pady=5)
        self.endereco_entry = ttk.Entry(form_inner, width=40)
        self.endereco_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        row += 1
        # CEP
        ttk.Label(form_inner, text="CEP:").grid(row=row, column=0, sticky=W, pady=5)
        self.cep_entry = ttk.Entry(form_inner, width=15)
        self.cep_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        row += 1
        # Observações
        ttk.Label(form_inner, text="Observações:").grid(row=row, column=0, sticky=W+N, pady=5)
        self.obs_text = tk.Text(form_inner, height=5, width=40)
        self.obs_text.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        form_inner.columnconfigure(1, weight=1)

        # Botões
        buttons_frame = ttk.Frame(form_inner)
        buttons_frame.grid(row=row+1, column=0, columnspan=2, pady=20)

        ttk.Button(buttons_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Salvar", command=self.save_supplier, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Excluir", command=self.delete_supplier, width=12).pack(side=LEFT, padx=5)

        # Coluna direita - Lista
        right_frame = ttk.LabelFrame(content_frame, text="Fornecedores Cadastrados", padding=20)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Busca
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(search_frame, text="Buscar:").pack(side=LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=LEFT)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_suppliers())

        # Tabela
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Nome", "CPF/CNPJ", "Email", "Telefone", "Endereco", "Cidade", "UF", "CEP", "Observacoes")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_h.set)
        scrollbar.config(command=self.tree.yview)

        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "UF":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "CEP":
                self.tree.column(col, width=90, anchor=CENTER)
            elif col in ["Telefone"]:
                self.tree.column(col, width=110, anchor=CENTER)
            elif col in ["Email", "CPF/CNPJ"]:
                self.tree.column(col, width=140)
            elif col in ["Endereco", "Observacoes"]:
                self.tree.column(col, width=200)
            else:
                self.tree.column(col, width=150)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_selected())

    def load_suppliers(self):
        """Carrega a lista de fornecedores"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        suppliers = self.db_manager.select('fornecedores', where_clause='ativo = 1', order_by='nome')

        for supplier in suppliers:
            # Truncar observações se muito longa
            obs = supplier['observacoes'] or ''
            if len(obs) > 50:
                obs = obs[:47] + '...'

            values = (
                supplier['id'],
                supplier['nome'],
                supplier['cpf_cnpj'] or '',
                supplier['email'] or '',
                supplier['telefone'] or '',
                supplier['endereco'] or '',
                supplier['cidade'] or '',
                supplier['uf'] or '',
                supplier['cep'] or '',
                obs
            )
            self.tree.insert('', END, values=values)

    def filter_suppliers(self):
        """Filtra fornecedores por QUALQUER campo"""
        search_term = self.search_entry.get().strip().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        suppliers = self.db_manager.select('fornecedores', where_clause='ativo = 1', order_by='nome')

        for supplier in suppliers:
            # Buscar em TODOS os campos
            match = False
            if search_term in supplier['nome'].lower():
                match = True
            elif supplier['cpf_cnpj'] and search_term in supplier['cpf_cnpj'].lower():
                match = True
            elif supplier['email'] and search_term in supplier['email'].lower():
                match = True
            elif supplier['telefone'] and search_term in supplier['telefone'].lower():
                match = True
            elif supplier['endereco'] and search_term in supplier['endereco'].lower():
                match = True
            elif supplier['cidade'] and search_term in supplier['cidade'].lower():
                match = True
            elif supplier['uf'] and search_term in supplier['uf'].lower():
                match = True
            elif supplier['cep'] and search_term in supplier['cep'].lower():
                match = True
            elif supplier['observacoes'] and search_term in supplier['observacoes'].lower():
                match = True

            if match:
                # Truncar observações se muito longa
                obs = supplier['observacoes'] or ''
                if len(obs) > 50:
                    obs = obs[:47] + '...'

                values = (
                    supplier['id'],
                    supplier['nome'],
                    supplier['cpf_cnpj'] or '',
                    supplier['email'] or '',
                    supplier['telefone'] or '',
                    supplier['endereco'] or '',
                    supplier['cidade'] or '',
                    supplier['uf'] or '',
                    supplier['cep'] or '',
                    obs
                )
                self.tree.insert('', END, values=values)

    def edit_selected(self):
        """Método unificado para edição por duplo clique ou Ctrl+E"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um fornecedor na lista!")
            return

        item = self.tree.item(selection[0])
        supplier_id = item['values'][0]

        suppliers = self.db_manager.select('fornecedores', where_clause='id = ?', where_params=[supplier_id])
        if not suppliers:
            return

        supplier = suppliers[0]
        self.selected_id = supplier['id']

        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, supplier['nome'])

        self.cpf_cnpj_entry.delete(0, END)
        if supplier['cpf_cnpj']:
            self.cpf_cnpj_entry.insert(0, supplier['cpf_cnpj'])

        self.email_entry.delete(0, END)
        if supplier['email']:
            self.email_entry.insert(0, supplier['email'])

        self.telefone_entry.delete(0, END)
        if supplier['telefone']:
            self.telefone_entry.insert(0, supplier['telefone'])

        self.uf_entry.delete(0, END)
        if supplier['uf']:
            self.uf_entry.insert(0, supplier['uf'])

        self.cidade_entry.delete(0, END)
        if supplier['cidade']:
            self.cidade_entry.insert(0, supplier['cidade'])

        self.endereco_entry.delete(0, END)
        if supplier['endereco']:
            self.endereco_entry.insert(0, supplier['endereco'])

        self.cep_entry.delete(0, END)
        if supplier['cep']:
            self.cep_entry.insert(0, supplier['cep'])

        self.obs_text.delete('1.0', END)
        if supplier['observacoes']:
            self.obs_text.insert('1.0', supplier['observacoes'])

        messagebox.showinfo("Editar", "Registro carregado para edicao! Modifique os dados e clique em Salvar.")

    def clear_form(self):
        """Limpa o formulário"""
        self.selected_id = None
        self.nome_entry.delete(0, END)
        self.cpf_cnpj_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.uf_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.cep_entry.delete(0, END)
        self.obs_text.delete('1.0', END)
        self.nome_entry.focus()

    def save_supplier(self):
        """Salva o fornecedor"""
        if not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return

        data = {
            'nome': self.nome_entry.get().strip(),
            'cpf_cnpj': self.cpf_cnpj_entry.get().strip() or None,
            'email': self.email_entry.get().strip() or None,
            'telefone': self.telefone_entry.get().strip() or None,
            'uf': self.uf_entry.get().strip() or None,
            'cidade': self.cidade_entry.get().strip() or None,
            'endereco': self.endereco_entry.get().strip() or None,
            'cep': self.cep_entry.get().strip() or None,
            'observacoes': self.obs_text.get('1.0', END).strip() or None
        }

        try:
            if self.selected_id:
                self.db_manager.update('fornecedores', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            else:
                self.db_manager.insert('fornecedores', data)
                messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")

            self.clear_form()
            self.load_suppliers()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_supplier(self):
        """Exclui o fornecedor"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um fornecedor para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este fornecedor?"):
            try:
                # Soft delete
                self.db_manager.update('fornecedores', {'ativo': 0}, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
                self.clear_form()
                self.load_suppliers()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")
