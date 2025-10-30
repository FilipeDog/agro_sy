"""
Cadastro de Funcionários
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class EmployeesRegisterWindow:
    """Janela de cadastro de funcionários"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_employees()

    def create_widgets(self):
        """Cria os widgets da interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(title_frame, text="Cadastro de Funcionários", font=("Helvetica", 16, "bold")).pack(side=LEFT)

        # Frame dividido
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Coluna esquerda - Formulário com Scrollbar
        left_outer_frame = ttk.LabelFrame(content_frame, text="Dados do Funcionário", padding=10)
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
        self.nome_entry.grid(row=row, column=1, columnspan=2, sticky=W+E, pady=5, padx=5)

        row += 1
        # CPF
        ttk.Label(form_inner, text="CPF:*").grid(row=row, column=0, sticky=W, pady=5)
        self.cpf_entry = ttk.Entry(form_inner, width=20)
        self.cpf_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # RG
        ttk.Label(form_inner, text="RG:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.rg_entry = ttk.Entry(form_inner, width=20)
        self.rg_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        # Data de Nascimento
        ttk.Label(form_inner, text="Data Nascimento:").grid(row=row, column=0, sticky=W, pady=5)
        self.data_nasc_entry = ttk.Entry(form_inner, width=15)
        self.data_nasc_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        ttk.Label(form_inner, text="(DD/MM/AAAA)", font=("Arial", 8)).grid(row=row, column=2, sticky=W, pady=5)

        row += 1
        # Telefone
        ttk.Label(form_inner, text="Telefone:").grid(row=row, column=0, sticky=W, pady=5)
        self.telefone_entry = ttk.Entry(form_inner, width=20)
        self.telefone_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Email
        ttk.Label(form_inner, text="Email:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.email_entry = ttk.Entry(form_inner, width=30)
        self.email_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        # Cargo
        ttk.Label(form_inner, text="Cargo:").grid(row=row, column=0, sticky=W, pady=5)
        self.cargo_entry = ttk.Entry(form_inner, width=25)
        self.cargo_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        # Setor
        ttk.Label(form_inner, text="Setor:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.setor_entry = ttk.Entry(form_inner, width=25)
        self.setor_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        # Salário
        ttk.Label(form_inner, text="Salário:").grid(row=row, column=0, sticky=W, pady=5)
        self.salario_entry = ttk.Entry(form_inner, width=15)
        self.salario_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Data de Admissão
        ttk.Label(form_inner, text="Data Admissão:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_admissao_entry = ttk.Entry(form_inner, width=15)
        self.data_admissao_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.data_admissao_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        # Endereço
        ttk.Label(form_inner, text="Endereço:").grid(row=row, column=0, sticky=W, pady=5)
        self.endereco_entry = ttk.Entry(form_inner, width=40)
        self.endereco_entry.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        row += 1
        # Cidade
        ttk.Label(form_inner, text="Cidade:").grid(row=row, column=0, sticky=W, pady=5)
        self.cidade_entry = ttk.Entry(form_inner, width=25)
        self.cidade_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        # UF
        ttk.Label(form_inner, text="UF:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.uf_entry = ttk.Entry(form_inner, width=5)
        self.uf_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        # CEP
        ttk.Label(form_inner, text="CEP:").grid(row=row, column=0, sticky=W, pady=5)
        self.cep_entry = ttk.Entry(form_inner, width=15)
        self.cep_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        row += 1
        # Observações
        ttk.Label(form_inner, text="Observações:").grid(row=row, column=0, sticky=W+N, pady=5)
        self.obs_text = tk.Text(form_inner, height=4, width=40)
        self.obs_text.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        form_inner.columnconfigure(1, weight=1)
        form_inner.columnconfigure(3, weight=1)

        # Botões
        button_frame = ttk.Frame(form_inner)
        button_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(button_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Salvar", command=self.save_employee, width=12).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_employee, width=12).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Demitir", command=self.dismiss_employee, width=12).pack(side=LEFT, padx=5)

        # Coluna direita - Lista
        right_frame = ttk.LabelFrame(content_frame, text="Funcionários Cadastrados", padding=20)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Frame para TreeView e scrollbars
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        # Treeview
        columns = ("ID", "Nome", "CPF", "Email", "Telefone", "Cargo", "Setor", "Salário",
                   "Data Adm.", "Endereço", "Cidade", "UF", "CEP", "Observações", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15,
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "Status":
                self.tree.column(col, width=80, anchor=CENTER)
            elif col == "UF":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "CEP":
                self.tree.column(col, width=90, anchor=CENTER)
            elif col == "Data Adm.":
                self.tree.column(col, width=90, anchor=CENTER)
            elif col == "Salário":
                self.tree.column(col, width=100, anchor=E)
            elif col == "Email":
                self.tree.column(col, width=180)
            elif col == "Observações":
                self.tree.column(col, width=200)
            else:
                self.tree.column(col, width=120)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)

        # Bind duplo clique
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_employees(self):
        """Carrega funcionários no TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        employees = self.db_manager.select('funcionarios', order_by='nome')

        for emp in employees:
            status = "Ativo" if emp['ativo'] else "Inativo"
            salario_fmt = f"R$ {emp['salario']:,.2f}" if emp.get('salario') else ''
            data_adm_fmt = emp.get('data_admissao') or ''
            if data_adm_fmt:
                try:
                    from datetime import datetime
                    dt = datetime.strptime(data_adm_fmt, '%Y-%m-%d')
                    data_adm_fmt = dt.strftime('%d/%m/%Y')
                except:
                    pass

            values = (
                emp['id'],
                emp['nome'],
                emp['cpf'] or '',
                emp['email'] or '',
                emp['telefone'] or '',
                emp['cargo'] or '',
                emp['setor'] or '',
                salario_fmt,
                data_adm_fmt,
                emp['endereco'] or '',
                emp['cidade'] or '',
                emp['uf'] or '',
                emp['cep'] or '',
                emp['observacoes'] or '',
                status
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        """Carrega funcionário selecionado no formulário"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        emp_id = item['values'][0]

        employees = self.db_manager.select('funcionarios', where_clause='id = ?', where_params=[emp_id])
        if not employees:
            return

        emp = employees[0]
        self.selected_id = emp['id']

        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, emp['nome'])

        self.cpf_entry.delete(0, END)
        if emp['cpf']:
            self.cpf_entry.insert(0, emp['cpf'])

        self.rg_entry.delete(0, END)
        if emp['rg']:
            self.rg_entry.insert(0, emp['rg'])

        self.data_nasc_entry.delete(0, END)
        if emp['data_nascimento']:
            self.data_nasc_entry.insert(0, self.format_date_br(emp['data_nascimento']))

        self.telefone_entry.delete(0, END)
        if emp['telefone']:
            self.telefone_entry.insert(0, emp['telefone'])

        self.email_entry.delete(0, END)
        if emp['email']:
            self.email_entry.insert(0, emp['email'])

        self.cargo_entry.delete(0, END)
        if emp['cargo']:
            self.cargo_entry.insert(0, emp['cargo'])

        self.setor_entry.delete(0, END)
        if emp['setor']:
            self.setor_entry.insert(0, emp['setor'])

        self.salario_entry.delete(0, END)
        if emp['salario']:
            self.salario_entry.insert(0, str(emp['salario']))

        self.data_admissao_entry.delete(0, END)
        if emp['data_admissao']:
            self.data_admissao_entry.insert(0, self.format_date_br(emp['data_admissao']))

        self.endereco_entry.delete(0, END)
        if emp['endereco']:
            self.endereco_entry.insert(0, emp['endereco'])

        self.cidade_entry.delete(0, END)
        if emp['cidade']:
            self.cidade_entry.insert(0, emp['cidade'])

        self.uf_entry.delete(0, END)
        if emp['uf']:
            self.uf_entry.insert(0, emp['uf'])

        self.cep_entry.delete(0, END)
        if emp['cep']:
            self.cep_entry.insert(0, emp['cep'])

        self.obs_text.delete('1.0', END)
        if emp['observacoes']:
            self.obs_text.insert('1.0', emp['observacoes'])

    def clear_form(self):
        """Limpa o formulário"""
        self.selected_id = None
        self.nome_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.rg_entry.delete(0, END)
        self.data_nasc_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.cargo_entry.delete(0, END)
        self.setor_entry.delete(0, END)
        self.salario_entry.delete(0, END)
        self.data_admissao_entry.delete(0, END)
        self.data_admissao_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.endereco_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.uf_entry.delete(0, END)
        self.cep_entry.delete(0, END)
        self.obs_text.delete('1.0', END)

    def save_employee(self):
        """Salva funcionário"""
        if not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "Informe o nome do funcionário!")
            return

        if not self.cpf_entry.get().strip():
            messagebox.showerror("Erro", "Informe o CPF do funcionário!")
            return

        # Validar salário se informado
        salario = None
        if self.salario_entry.get().strip():
            try:
                salario = float(self.salario_entry.get().replace(',', '.'))
            except:
                messagebox.showerror("Erro", "Salário inválido!")
                return

        data = {
            'nome': self.nome_entry.get().strip(),
            'cpf': self.cpf_entry.get().strip(),
            'rg': self.rg_entry.get().strip() or None,
            'data_nascimento': self.parse_date_br(self.data_nasc_entry.get()),
            'telefone': self.telefone_entry.get().strip() or None,
            'email': self.email_entry.get().strip() or None,
            'cargo': self.cargo_entry.get().strip() or None,
            'setor': self.setor_entry.get().strip() or None,
            'salario': salario,
            'data_admissao': self.parse_date_br(self.data_admissao_entry.get()),
            'endereco': self.endereco_entry.get().strip() or None,
            'cidade': self.cidade_entry.get().strip() or None,
            'uf': self.uf_entry.get().strip() or None,
            'cep': self.cep_entry.get().strip() or None,
            'observacoes': self.obs_text.get('1.0', END).strip() or None,
            'ativo': 1
        }

        try:
            if self.selected_id:
                self.db_manager.update('funcionarios', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            else:
                self.db_manager.insert('funcionarios', data)
                messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")

            self.clear_form()
            self.load_employees()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar funcionário: {str(e)}")

    def delete_employee(self):
        """Exclui funcionário"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este funcionário?\nEsta ação não pode ser desfeita!"):
            try:
                self.db_manager.delete('funcionarios', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                self.clear_form()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir funcionário: {str(e)}")

    def dismiss_employee(self):
        """Demite funcionário (marca como inativo)"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um funcionário para demitir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja registrar a demissão deste funcionário?"):
            try:
                data = {
                    'ativo': 0,
                    'data_demissao': datetime.now().strftime('%Y-%m-%d')
                }
                self.db_manager.update('funcionarios', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Demissão registrada com sucesso!")
                self.clear_form()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao registrar demissão: {str(e)}")

    def format_date_br(self, date_str):
        """Formata data de YYYY-MM-DD para DD/MM/YYYY"""
        if not date_str:
            return ''
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            return date_str

    def parse_date_br(self, date_str):
        """Converte data de DD/MM/YYYY para YYYY-MM-DD"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        except:
            return None
