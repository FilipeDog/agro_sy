"""
Interface Principal - AgroGestor
"""
import tkinter as tk
from tkinter import messagebox
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class MainWindow:
    """Janela principal do sistema"""

    def __init__(self, db_manager):
        """
        Inicializa a janela principal

        Args:
            db_manager: Instância do DatabaseManager
        """
        self.db_manager = db_manager

        # Criar janela principal
        try:
            self.root = ttk.Window(themename="darkly")
        except:
            self.root = tk.Tk()

        self.root.title("AgroGestor")
        self.root.geometry("1400x800")

        # Centralizar janela
        self.center_window()

        # Criar interface
        self.create_menu()
        self.create_widgets()

        # Variável para armazenar a tela atual
        self.current_frame = None

        # Atalhos de teclado globais
        self.setup_keyboard_shortcuts()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 1400
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self):
        """Cria o menu principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Cadastros
        cadastros_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=cadastros_menu)

        # Submenu Cadastros Secundários
        cadastros_sec_menu = tk.Menu(cadastros_menu, tearoff=0)
        cadastros_menu.add_cascade(label="Cadastros Secundários", menu=cadastros_sec_menu)
        cadastros_sec_menu.add_command(label="Tipos de Animal", command=lambda: self.open_generic_register("tipo_animal", "Tipos de Animal"))
        cadastros_sec_menu.add_command(label="Raças", command=lambda: self.open_generic_register("raca", "Raças"))
        cadastros_sec_menu.add_command(label="Pastos", command=lambda: self.open_generic_register("pastos", "Pastos"))
        cadastros_sec_menu.add_command(label="Status do Animal", command=lambda: self.open_generic_register("status_animal", "Status do Animal"))
        cadastros_sec_menu.add_command(label="Origem", command=lambda: self.open_generic_register("origem", "Origem"))
        cadastros_sec_menu.add_command(label="Causa da Morte", command=lambda: self.open_generic_register("causa_morte", "Causa da Morte"))
        cadastros_sec_menu.add_command(label="Medicamentos", command=self.open_medicamentos)
        cadastros_sec_menu.add_command(label="Tipos de Receita", command=lambda: self.open_generic_register("tipo_receita", "Tipos de Receita"))
        cadastros_sec_menu.add_command(label="Tipos de Despesa", command=lambda: self.open_generic_register("tipo_despesa", "Tipos de Despesa"))

        cadastros_menu.add_separator()

        # Cadastros Principais
        cadastros_menu.add_command(label="Animais", command=self.open_animais)
        cadastros_menu.add_command(label="Clientes", command=self.open_clientes)
        cadastros_menu.add_command(label="Fornecedores", command=self.open_fornecedores)
        cadastros_menu.add_separator()
        cadastros_menu.add_command(label="Funcionários", command=self.open_funcionarios)
        cadastros_menu.add_command(label="Contas Bancárias", command=self.open_contas_bancarias)
        cadastros_menu.add_command(label="Inventário", command=self.open_inventario)

        # Menu Lançamentos
        lancamentos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Lançamentos", menu=lancamentos_menu)
        lancamentos_menu.add_command(label="Despesas", command=self.open_despesas)
        lancamentos_menu.add_command(label="Receitas (Vendas)", command=self.open_receitas)
        lancamentos_menu.add_separator()
        lancamentos_menu.add_command(label="Aplicações (Sanidade)", command=self.open_aplicacoes)
        lancamentos_menu.add_command(label="Inseminações", command=self.open_inseminacoes)
        lancamentos_menu.add_command(label="Controle de Peso", command=self.open_controle_peso)

        # Menu Relatórios
        relatorios_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)

        # Relatórios de Cadastro
        relat_cad_menu = tk.Menu(relatorios_menu, tearoff=0)
        relatorios_menu.add_cascade(label="Relatórios de Cadastro", menu=relat_cad_menu)
        relat_cad_menu.add_command(label="Relatório de Animais", command=lambda: self.open_relatorio("animais"))
        relat_cad_menu.add_command(label="Animais por Status", command=lambda: self.open_relatorio("animais_status"))
        relat_cad_menu.add_command(label="Animais por Raça", command=lambda: self.open_relatorio("animais_raca"))
        relat_cad_menu.add_command(label="Animais por Pasto", command=lambda: self.open_relatorio("animais_pasto"))
        relat_cad_menu.add_command(label="Animais por Tipo", command=lambda: self.open_relatorio("animais_tipo"))
        relat_cad_menu.add_separator()
        relat_cad_menu.add_command(label="Clientes", command=lambda: self.open_relatorio("clientes"))
        relat_cad_menu.add_command(label="Fornecedores", command=lambda: self.open_relatorio("fornecedores"))

        # Relatórios de Movimentação
        relat_mov_menu = tk.Menu(relatorios_menu, tearoff=0)
        relatorios_menu.add_cascade(label="Relatórios de Movimentação", menu=relat_mov_menu)
        relat_mov_menu.add_command(label="Despesas por Fornecedor", command=lambda: self.open_relatorio("despesas_fornecedor"))
        relat_mov_menu.add_command(label="Despesas por Mês", command=lambda: self.open_relatorio("despesas_mes"))
        relat_mov_menu.add_command(label="Receitas por Cliente", command=lambda: self.open_relatorio("receitas_cliente"))
        relat_mov_menu.add_command(label="Receitas por Tipo", command=lambda: self.open_relatorio("receitas_tipo"))
        relat_mov_menu.add_separator()
        relat_mov_menu.add_command(label="Aplicações por Mês", command=lambda: self.open_relatorio("aplicacoes_mes"))
        relat_mov_menu.add_command(label="Inseminações por Mês", command=lambda: self.open_relatorio("inseminacoes_mes"))
        relat_mov_menu.add_command(label="Pesagens por Mês", command=lambda: self.open_relatorio("pesagens_mes"))
        relat_mov_menu.add_command(label="Mortes por Mês", command=lambda: self.open_relatorio("mortes_mes"))
        relat_mov_menu.add_separator()
        relat_mov_menu.add_command(label="Resultado Financeiro", command=lambda: self.open_relatorio("resultado_financeiro"))

        # Menu Dashboard
        dashboard_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dashboard", menu=dashboard_menu)
        dashboard_menu.add_command(label="📊 Dashboard Geral", command=self.open_dashboard)
        dashboard_menu.add_command(label="💰 Dashboard Financeiro", command=self.open_financial_dashboard)
        dashboard_menu.add_command(label="📈 Fluxo de Caixa Projetado", command=self.open_cash_flow)
        dashboard_menu.add_separator()
        dashboard_menu.add_command(label="🔔 Alertas e Lembretes", command=self.open_alerts)

        # Menu Bananal
        bananal_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bananal", menu=bananal_menu)
        bananal_menu.add_command(label="📊 Dashboard de Bananas", command=self.open_dashboard_banana)
        bananal_menu.add_separator()
        bananal_menu.add_command(label="Talhões", command=self.open_talhoes)
        bananal_menu.add_command(label="Tratos Culturais", command=self.open_tratos_culturais)
        bananal_menu.add_command(label="Colheitas", command=self.open_colheitas_banana)
        bananal_menu.add_separator()
        bananal_menu.add_command(label="Variedades de Banana", command=lambda: self.open_generic_register("variedades_banana", "Variedades de Banana"))
        bananal_menu.add_command(label="Pragas e Doenças", command=lambda: self.open_generic_register("pragas_doencas", "Pragas e Doenças"))

        # Menu Utilitários
        utils_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Utilitários", menu=utils_menu)
        utils_menu.add_command(label="🔍 Busca Global (Ctrl+F)", command=self.open_global_search)
        utils_menu.add_separator()
        utils_menu.add_command(label="Gestão de Usuários", command=self.open_users_management)
        utils_menu.add_command(label="Calculadora", command=self.open_calculator)
        utils_menu.add_separator()
        utils_menu.add_command(label="🎨 Alternar Tema (Escuro/Claro)", command=self.toggle_theme)
        utils_menu.add_separator()
        utils_menu.add_command(label="Importar de Excel", command=self.open_excel_importer)
        utils_menu.add_separator()
        utils_menu.add_command(label="Exportar Backup", command=self.create_backup)
        utils_menu.add_command(label="Importar Backup", command=self.restore_backup)
        utils_menu.add_separator()
        utils_menu.add_command(label="Sobre", command=self.show_about)
        utils_menu.add_command(label="Sair", command=self.quit_application)

    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame superior com título e botão home
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=X, padx=10, pady=10)

        # Botão Home
        home_btn = ttk.Button(
            header_frame,
            text="🏠 Início",
            command=self.show_welcome_screen,
            width=12
        )
        home_btn.pack(side=LEFT, padx=(0, 10))

        title_label = ttk.Label(
            header_frame,
            text="🌾 AgroGestor",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(side=LEFT)

        # Frame principal (área de trabalho)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=(0, 10))

        # Barra de status (DEVE SER CRIADA ANTES de show_welcome_screen)
        self.status_bar = ttk.Label(
            self.root,
            text="Sistema pronto. Selecione uma opção no menu.",
            relief=tk.SUNKEN,
            anchor=W
        )
        self.status_bar.pack(side=BOTTOM, fill=X)

        # Mostrar tela de boas-vindas
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Exibe a tela de boas-vindas completa"""
        from .welcome_screen import WelcomeScreen
        self.clear_main_frame()
        WelcomeScreen(self.main_frame, self.db_manager, self)
        self.update_status("Tela Inicial")

    def clear_main_frame(self):
        """Limpa o frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def update_status(self, message):
        """Atualiza a barra de status"""
        self.status_bar.config(text=message)

    # Métodos para abrir as telas
    def open_generic_register(self, table_name, title):
        """Abre um cadastro genérico (secundário)"""
        from .generic_register import GenericRegisterWindow
        self.clear_main_frame()
        GenericRegisterWindow(self.main_frame, self.db_manager, table_name, title)
        self.update_status(f"Cadastro: {title}")

    def open_medicamentos(self):
        """Abre cadastro de medicamentos"""
        self.open_generic_register("medicamentos", "Medicamentos")

    def open_animais(self):
        """Abre cadastro de animais"""
        from .animals_register import AnimalsRegisterWindow
        self.clear_main_frame()
        AnimalsRegisterWindow(self.main_frame, self.db_manager)
        self.update_status("Cadastro de Animais")

    def open_clientes(self):
        """Abre cadastro de clientes"""
        from .clients_register import ClientsRegisterWindow
        self.clear_main_frame()
        ClientsRegisterWindow(self.main_frame, self.db_manager)
        self.update_status("Cadastro de Clientes")

    def open_fornecedores(self):
        """Abre cadastro de fornecedores"""
        from .suppliers_register import SuppliersRegisterWindow
        self.clear_main_frame()
        SuppliersRegisterWindow(self.main_frame, self.db_manager)
        self.update_status("Cadastro de Fornecedores")

    def open_despesas(self):
        """Abre lançamento de despesas"""
        from .expenses import ExpensesWindow
        self.clear_main_frame()
        ExpensesWindow(self.main_frame, self.db_manager)
        self.update_status("Lançamento de Despesas")

    def open_receitas(self):
        """Abre lançamento de receitas"""
        from .revenues import RevenuesWindow
        self.clear_main_frame()
        RevenuesWindow(self.main_frame, self.db_manager)
        self.update_status("Lançamento de Receitas")

    def open_aplicacoes(self):
        """Abre lançamento de aplicações"""
        from .applications import ApplicationsWindow
        self.clear_main_frame()
        ApplicationsWindow(self.main_frame, self.db_manager)
        self.update_status("Lançamento de Aplicações (Sanidade)")

    def open_inseminacoes(self):
        """Abre lançamento de inseminações"""
        from .inseminations import InseminationsWindow
        self.clear_main_frame()
        InseminationsWindow(self.main_frame, self.db_manager)
        self.update_status("Lançamento de Inseminações")

    def open_controle_peso(self):
        """Abre controle de peso"""
        from .weight_control import WeightControlWindow
        self.clear_main_frame()
        WeightControlWindow(self.main_frame, self.db_manager)
        self.update_status("Controle de Peso")

    def open_relatorio(self, tipo):
        """Abre um relatório"""
        from .reports_window import ReportsWindow
        self.clear_main_frame()
        ReportsWindow(self.main_frame, self.db_manager, tipo)
        self.update_status(f"Relatório: {tipo}")

    def open_dashboard(self):
        """Abre o dashboard"""
        from .dashboard import DashboardWindow
        self.clear_main_frame()
        DashboardWindow(self.main_frame, self.db_manager)
        self.update_status("Dashboard - Indicadores")

    def open_financial_dashboard(self):
        """Abre o dashboard financeiro"""
        from .financial_dashboard import FinancialDashboard
        self.clear_main_frame()
        FinancialDashboard(self.main_frame, self.db_manager)
        self.update_status("Dashboard Financeiro - Análise Visual")

    def open_alerts(self):
        """Abre alertas e lembretes"""
        from .alerts_reminders import AlertsReminders
        self.clear_main_frame()
        AlertsReminders(self.main_frame, self.db_manager)
        self.update_status("Alertas e Lembretes")

    def open_cash_flow(self):
        """Abre fluxo de caixa projetado"""
        from .cash_flow_projection import CashFlowProjection
        self.clear_main_frame()
        CashFlowProjection(self.main_frame, self.db_manager)
        self.update_status("Fluxo de Caixa Projetado")

    def open_funcionarios(self):
        """Abre cadastro de funcionários"""
        from .employees_register import EmployeesRegisterWindow
        self.clear_main_frame()
        EmployeesRegisterWindow(self.main_frame, self.db_manager)
        self.update_status("Cadastro de Funcionários")

    def open_contas_bancarias(self):
        """Abre gestão de contas bancárias"""
        from .bank_accounts import BankAccountsWindow
        self.clear_main_frame()
        BankAccountsWindow(self.main_frame, self.db_manager)
        self.update_status("Contas Bancárias")

    def open_inventario(self):
        """Abre gestão de inventário"""
        from .inventory import InventoryWindow
        self.clear_main_frame()
        InventoryWindow(self.main_frame, self.db_manager)
        self.update_status("Inventário")

    def open_users_management(self):
        """Abre gestão de usuários"""
        from .users_management import UsersManagementWindow
        self.clear_main_frame()
        # TODO: Pass current_user information when implementing login system properly
        UsersManagementWindow(self.main_frame, self.db_manager)
        self.update_status("Gestão de Usuários")

    def open_calculator(self):
        """Abre calculadora"""
        from ..utils.calculator import open_calculator
        open_calculator(self.root)
        self.update_status("Calculadora aberta")

    def open_talhoes(self):
        """Abre cadastro de talhões"""
        from .talhoes_register import TalhoesRegisterWindow
        self.clear_main_frame()
        TalhoesRegisterWindow(self.main_frame, self.db_manager)
        self.update_status("Cadastro de Talhões")

    def open_tratos_culturais(self):
        """Abre tratos culturais"""
        from .tratos_culturais import TratosCulturaisWindow
        self.clear_main_frame()
        TratosCulturaisWindow(self.main_frame, self.db_manager)
        self.update_status("Tratos Culturais")

    def open_colheitas_banana(self):
        """Abre colheitas de banana"""
        from .colheitas_banana import ColheitasBananaWindow
        self.clear_main_frame()
        ColheitasBananaWindow(self.main_frame, self.db_manager)
        self.update_status("Colheitas de Banana")

    def open_dashboard_banana(self):
        """Abre dashboard de bananas"""
        from .dashboard_banana import DashboardBananaWindow
        self.clear_main_frame()
        DashboardBananaWindow(self.main_frame, self.db_manager)
        self.update_status("Dashboard de Bananas")

    def open_excel_importer(self):
        """Abre importador de Excel"""
        from ..utils.excel_importer import ExcelImporterWindow
        self.clear_main_frame()
        ExcelImporterWindow(self.main_frame, self.db_manager)
        self.update_status("Importar de Excel")

    def create_backup(self):
        """Cria backup do banco de dados"""
        try:
            from ..utils.backup_manager import BackupManager
            backup_mgr = BackupManager()
            result = backup_mgr.export_backup_dialog()
            if result:
                messagebox.showinfo("Sucesso", f"Backup exportado com sucesso!\n\n{result}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup: {str(e)}")

    def restore_backup(self):
        """Restaura backup do banco de dados"""
        try:
            from ..utils.backup_manager import BackupManager
            backup_mgr = BackupManager()
            success, current_backup = backup_mgr.import_backup_dialog()
            if success:
                messagebox.showinfo(
                    "Sucesso",
                    f"Backup restaurado com sucesso!\n\n"
                    f"Um backup do banco atual foi salvo em:\n{current_backup}\n\n"
                    f"Reinicie o sistema para aplicar as mudanças."
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup: {str(e)}")

    def toggle_theme(self):
        """Alterna entre tema claro e escuro INSTANTANEAMENTE"""
        try:
            from ..utils.theme_manager import ThemeManager
            theme_mgr = ThemeManager()

            # Alternar tema
            new_theme = theme_mgr.toggle_theme()

            # Aplicar instantaneamente
            try:
                import ttkbootstrap as ttk
                # Obter o style atual
                style = ttk.Style()

                # Aplicar novo tema
                theme_name = theme_mgr.get_ttkbootstrap_theme()
                style.theme_use(theme_name)

                messagebox.showinfo(
                    "Tema Alterado",
                    f"✓ Tema alterado para: {theme_mgr.get_theme_name()}\n\n"
                    "Aplicado instantaneamente!"
                )
            except Exception as e:
                # Se não conseguir aplicar instantaneamente, pedir reinício
                messagebox.showinfo(
                    "Tema Alterado",
                    f"Tema alterado para: {theme_mgr.get_theme_name()}\n\n"
                    "Por favor, reinicie o sistema para aplicar as mudanças."
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alternar tema: {str(e)}")

    def show_about(self):
        """Exibe informações sobre o sistema"""
        messagebox.showinfo(
            "Sobre - AgroGestor",
            "AgroGestor - Sistema Completo de Gestão Agropecuária\n"
            "Versão 1.0.0\n\n"
            "Sistema completo para gestão agropecuária\n"
            "com controle de animais, movimentações e relatórios.\n\n"
            "Desenvolvido em Python com interface gráfica moderna."
        )

    def quit_application(self):
        """Fecha o aplicativo"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.db_manager.disconnect()
            self.root.quit()

    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado globais"""
        # Ctrl+F - Busca Global
        self.root.bind('<Control-f>', lambda e: self.open_global_search())
        self.root.bind('<Control-F>', lambda e: self.open_global_search())

    def open_global_search(self):
        """Abre a janela de busca global"""
        try:
            from .global_search import GlobalSearch
            search = GlobalSearch(self.root, self.db_manager)
            search.show()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir busca global: {str(e)}")

    def run(self):
        """Executa a janela principal"""
        self.root.mainloop()
