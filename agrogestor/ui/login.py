"""
Tela de Login - AgroGestor
"""
import tkinter as tk
from tkinter import messagebox
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    import tkinter.ttk as ttk
    from tkinter.constants import *


class LoginWindow:
    """Janela de login do sistema"""

    def __init__(self, db_manager, on_login_success):
        """
        Inicializa a janela de login

        Args:
            db_manager: Instância do DatabaseManager
            on_login_success: Callback chamado quando login é bem-sucedido
        """
        self.db_manager = db_manager
        self.on_login_success = on_login_success

        # Criar janela principal
        try:
            self.root = ttk.Window(themename="darkly")
        except:
            self.root = tk.Tk()

        self.root.title("AgroGestor - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Centralizar janela
        self.center_window()

        # Criar interface
        self.create_widgets()

        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.do_login())

    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill=BOTH, expand=YES)

        # Logo/Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(0, 30))

        title = ttk.Label(
            title_frame,
            text="🌾 AgroGestor",
            font=("Helvetica", 24, "bold") if hasattr(ttk, 'Window') else None
        )
        title.pack()

        subtitle = ttk.Label(
            title_frame,
            text="Sistema Completo de Gestão Agropecuária",
            font=("Helvetica", 10)
        )
        subtitle.pack(pady=(10, 0))

        # Frame de Login
        login_frame = ttk.LabelFrame(main_frame, text="Acesso ao Sistema", padding=20)
        login_frame.pack(fill=BOTH, expand=YES, pady=20)

        # Usuário
        ttk.Label(login_frame, text="Usuário:", font=("Helvetica", 10)).pack(anchor=W, pady=(10, 5))
        self.username_entry = ttk.Entry(login_frame, font=("Helvetica", 11))
        self.username_entry.pack(fill=X, pady=(0, 15))
        self.username_entry.focus()

        # Senha
        ttk.Label(login_frame, text="Senha:", font=("Helvetica", 10)).pack(anchor=W, pady=(0, 5))
        self.password_entry = ttk.Entry(login_frame, show="*", font=("Helvetica", 11))
        self.password_entry.pack(fill=X, pady=(0, 15))

        # Chave de Licença
        ttk.Label(login_frame, text="Chave de Licença:", font=("Helvetica", 10)).pack(anchor=W, pady=(0, 5))
        self.license_entry = ttk.Entry(login_frame, font=("Helvetica", 11))
        self.license_entry.pack(fill=X, pady=(0, 20))
        self.license_entry.insert(0, "DEMO-2024-GADO-CTRL")  # Licença padrão

        # Botão de Login
        btn_style = "success" if hasattr(ttk, 'Window') else None
        self.login_btn = ttk.Button(
            login_frame,
            text="ENTRAR",
            command=self.do_login,
            bootstyle=btn_style if btn_style else None,
            width=20
        )
        self.login_btn.pack(pady=10)

        # Informações adicionais
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=(20, 0))

        info_text = ttk.Label(
            info_frame,
            text="Usuário padrão: admin | Senha: admin123",
            font=("Helvetica", 9),
            foreground="gray"
        )
        info_text.pack()

        version_text = ttk.Label(
            info_frame,
            text="Versão 1.0.0",
            font=("Helvetica", 8),
            foreground="gray"
        )
        version_text.pack(pady=(5, 0))

    def do_login(self):
        """Executa o processo de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        license_key = self.license_entry.get().strip()

        # Validar campos
        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha usuário e senha!")
            return

        if not license_key:
            messagebox.showerror("Erro", "Por favor, informe a chave de licença!")
            return

        # Conectar ao banco de dados
        if not self.db_manager.connect():
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados!")
            return

        # Verificar licença
        if not self.db_manager.check_license(license_key):
            messagebox.showerror(
                "Licença Inválida",
                "A chave de licença informada é inválida ou está expirada!\n\n"
                "Por favor, entre em contato com o suporte."
            )
            return

        # Autenticar usuário
        if self.db_manager.authenticate_user(username, password):
            messagebox.showinfo("Sucesso", f"Bem-vindo, {username}!")
            self.root.destroy()
            self.on_login_success()
        else:
            messagebox.showerror(
                "Erro de Autenticação",
                "Usuário ou senha incorretos!\n\n"
                "Por favor, verifique suas credenciais e tente novamente."
            )

    def run(self):
        """Executa a janela de login"""
        self.root.mainloop()
