"""
Gestão Avançada de Usuários - Apenas para Administradores
"""
import tkinter as tk
from tkinter import messagebox
import hashlib
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class UsersManagementWindow:
    """Janela de gestão de usuários"""

    def __init__(self, parent, db_manager, current_user=None):
        self.parent = parent
        self.db_manager = db_manager
        self.current_user = current_user
        self.selected_id = None

        # Verificar se é admin
        if current_user and current_user.get('nivel_acesso') != 'Admin':
            messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar esta funcionalidade!")
            return

        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        """Cria interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Gestão de Usuários", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        # Formulário
        form_frame = ttk.LabelFrame(main_container, text="Dados do Usuário", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Nome de Usuário:*").grid(row=row, column=0, sticky=W, pady=5)
        self.username_entry = ttk.Entry(form_frame, width=25)
        self.username_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Nome Completo:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.nome_entry = ttk.Entry(form_frame, width=35)
        self.nome_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Email:").grid(row=row, column=0, sticky=W, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=35)
        self.email_entry.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Nível de Acesso:*").grid(row=row, column=0, sticky=W, pady=5)
        self.nivel_combo = ttk.Combobox(form_frame, width=20, state="readonly", values=["Admin", "Gerente", "Operador"])
        self.nivel_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.nivel_combo.set("Operador")

        ttk.Label(form_frame, text="Status:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.ativo_var = tk.IntVar(value=1)
        ttk.Checkbutton(form_frame, text="Ativo", variable=self.ativo_var).grid(row=row, column=3, sticky=W, pady=5)

        row += 1
        ttk.Label(form_frame, text="Nova Senha:").grid(row=row, column=0, sticky=W, pady=5)
        self.senha_entry = ttk.Entry(form_frame, width=25, show="*")
        self.senha_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Confirmar Senha:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.senha_conf_entry = ttk.Entry(form_frame, width=25, show="*")
        self.senha_conf_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        form_frame.columnconfigure(3, weight=1)

        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_user, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_user, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Resetar Senha", command=self.reset_password, width=15).pack(side=LEFT, padx=5)

        # Lista
        list_frame = ttk.LabelFrame(main_container, text="Usuários Cadastrados", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para TreeView e scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Usuário", "Nome", "Email", "Nível", "Status", "Último Login")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10,
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col in ["Nível", "Status"]:
                self.tree.column(col, width=100, anchor=CENTER)
            else:
                self.tree.column(col, width=150)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_users(self):
        """Carrega usuários"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.db_manager.select('usuarios', order_by='username')

        for user in users:
            status = "Ativo" if user['ativo'] else "Inativo"
            ultimo_login = user['ultimo_login'][:16] if user['ultimo_login'] else "Nunca"
            values = (
                user['id'],
                user['username'],
                user['nome_completo'] or '',
                user['email'] or '',
                user['nivel_acesso'] or 'Operador',
                status,
                ultimo_login
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        """Carrega usuário selecionado"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        user_id = item['values'][0]

        users = self.db_manager.select('usuarios', where_clause='id = ?', where_params=[user_id])
        if not users:
            return

        user = users[0]
        self.selected_id = user['id']

        self.username_entry.delete(0, END)
        self.username_entry.insert(0, user['username'])
        self.username_entry.config(state='disabled')  # Não permitir alterar username

        self.nome_entry.delete(0, END)
        if user['nome_completo']:
            self.nome_entry.insert(0, user['nome_completo'])

        self.email_entry.delete(0, END)
        if user['email']:
            self.email_entry.insert(0, user['email'])

        self.nivel_combo.set(user['nivel_acesso'] or 'Operador')
        self.ativo_var.set(user['ativo'])

        self.senha_entry.delete(0, END)
        self.senha_conf_entry.delete(0, END)

    def clear_form(self):
        """Limpa formulário"""
        self.selected_id = None
        self.username_entry.config(state='normal')
        self.username_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.nivel_combo.set("Operador")
        self.ativo_var.set(1)
        self.senha_entry.delete(0, END)
        self.senha_conf_entry.delete(0, END)

    def save_user(self):
        """Salva usuário"""
        if not self.username_entry.get().strip():
            messagebox.showerror("Erro", "Informe o nome de usuário!")
            return

        # Se novo usuário, senha é obrigatória
        if not self.selected_id:
            if not self.senha_entry.get():
                messagebox.showerror("Erro", "Informe a senha!")
                return
            if self.senha_entry.get() != self.senha_conf_entry.get():
                messagebox.showerror("Erro", "As senhas não conferem!")
                return

        data = {
            'username': self.username_entry.get().strip(),
            'nome_completo': self.nome_entry.get().strip() or None,
            'email': self.email_entry.get().strip() or None,
            'nivel_acesso': self.nivel_combo.get(),
            'ativo': self.ativo_var.get()
        }

        # Se senha foi informada, atualizar
        if self.senha_entry.get():
            if self.senha_entry.get() != self.senha_conf_entry.get():
                messagebox.showerror("Erro", "As senhas não conferem!")
                return
            password_hash = hashlib.sha256(self.senha_entry.get().encode()).hexdigest()
            data['password'] = password_hash
            data['primeiro_acesso'] = 0

        try:
            if self.selected_id:
                self.db_manager.update('usuarios', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            else:
                data['primeiro_acesso'] = 1  # Forçar troca de senha no primeiro login
                self.db_manager.insert('usuarios', data)
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            self.clear_form()
            self.load_users()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar usuário: {str(e)}")

    def delete_user(self):
        """Exclui usuário"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return

        # Não permitir excluir o próprio usuário
        if self.current_user and self.current_user.get('id') == self.selected_id:
            messagebox.showerror("Erro", "Você não pode excluir seu próprio usuário!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este usuário?"):
            try:
                self.db_manager.delete('usuarios', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.clear_form()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")

    def reset_password(self):
        """Reseta senha para padrão e força troca"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return

        if messagebox.askyesno("Confirmar", "Resetar senha para 'senha123' e forçar troca no próximo login?"):
            try:
                password_hash = hashlib.sha256('senha123'.encode()).hexdigest()
                data = {
                    'password': password_hash,
                    'primeiro_acesso': 1
                }
                self.db_manager.update('usuarios', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Senha resetada! Nova senha: senha123")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao resetar senha: {str(e)}")
