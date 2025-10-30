# -*- coding: utf-8 -*-
"""
Tela de Boas-Vindas do Sistema
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


class WelcomeScreen:
    """Tela de boas-vindas com atalhos e indicadores"""

    def __init__(self, parent, db_manager, main_window):
        self.parent = parent
        self.db_manager = db_manager
        self.main_window = main_window
        self.create_widgets()
        self.load_quick_stats()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=X, padx=40, pady=30)

        ttk.Label(header_frame, text="🌾 AgroGestor",
                 font=("Helvetica", 24, "bold")).pack()
        ttk.Label(header_frame, text="Bem-vindo ao sistema completo de gestão",
                 font=("Helvetica", 12)).pack(pady=5)

        # Indicadores rápidos
        stats_frame = ttk.Frame(main_container)
        stats_frame.pack(fill=X, padx=40, pady=20)

        ttk.Label(stats_frame, text="Visão Geral", 
                 font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))

        indicators = ttk.Frame(stats_frame)
        indicators.pack(fill=X)

        # 4 indicadores
        self.create_indicator(indicators, "🐄 Animais Ativos", "0", 0)
        self.create_indicator(indicators, "💰 Saldo Total", "R$ 0,00", 1)
        self.create_indicator(indicators, "📦 Itens em Estoque", "0", 2)
        self.create_indicator(indicators, "🍌 Talhões Ativos", "0", 3)

        # Atalhos rápidos
        shortcuts_frame = ttk.LabelFrame(main_container, text="Atalhos Rápidos", padding=20)
        shortcuts_frame.pack(fill=BOTH, expand=YES, padx=40, pady=20)

        # Grid de botões
        buttons_frame = ttk.Frame(shortcuts_frame)
        buttons_frame.pack(expand=YES)

        shortcuts = [
            ("📊 Dashboard Gado", self.main_window.open_dashboard, 0, 0),
            ("🐄 Cadastro de Animais", self.main_window.open_animais, 0, 1),
            ("💰 Lançar Despesa", self.main_window.open_despesas, 0, 2),
            ("💵 Lançar Receita", self.main_window.open_receitas, 0, 3),
            
            ("🍌 Dashboard Bananas", self.main_window.open_dashboard_banana, 1, 0),
            ("🌱 Talhões", self.main_window.open_talhoes, 1, 1),
            ("📦 Inventário", self.main_window.open_inventario, 1, 2),
            ("👥 Clientes", self.main_window.open_clientes, 1, 3),
            
            ("📄 Relatórios", lambda: messagebox.showinfo("Info", "Use o menu Relatórios"), 2, 0),
            ("🏦 Contas Bancárias", self.main_window.open_contas_bancarias, 2, 1),
            ("📥 Importar Excel", self.main_window.open_excel_importer, 2, 2),
            ("⚙️ Configurações", lambda: messagebox.showinfo("Info", "Use o menu Utilitários"), 2, 3),
        ]

        for text, command, row, col in shortcuts:
            btn = ttk.Button(buttons_frame, text=text, command=command, width=25)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        # Footer
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(fill=X, padx=40, pady=20)

        ttk.Label(footer_frame, text=f"Sistema iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                 font=("Helvetica", 9)).pack(side=LEFT)
        ttk.Label(footer_frame, text="Versão 1.0.0 | © 2024",
                 font=("Helvetica", 9)).pack(side=RIGHT)

    def create_indicator(self, parent, label, value, column):
        """Cria um indicador de status"""
        frame = ttk.Frame(parent, relief=RAISED, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=5, sticky="ew")
        
        ttk.Label(frame, text=label, font=("Helvetica", 10)).pack(pady=(15, 5))
        lbl = ttk.Label(frame, text=value, font=("Helvetica", 18, "bold"))
        lbl.pack(pady=(0, 15))
        
        # Guardar referências
        if column == 0:
            self.ind_animais = lbl
        elif column == 1:
            self.ind_saldo = lbl
        elif column == 2:
            self.ind_estoque = lbl
        elif column == 3:
            self.ind_talhoes = lbl
        
        parent.columnconfigure(column, weight=1)

    def load_quick_stats(self):
        """Carrega estatísticas rápidas"""
        try:
            # Animais ativos
            animais = self.db_manager.execute_query(
                "SELECT COUNT(*) as total FROM animais WHERE status_id = (SELECT id FROM status_animal WHERE nome = 'Ativo')"
            )
            if animais:
                self.ind_animais.config(text=str(animais[0]['total'] or 0))

            # Saldo total
            saldo_result = self.db_manager.execute_query(
                "SELECT SUM(saldo_atual) as total FROM contas_bancarias WHERE ativo = 1"
            )
            saldo = saldo_result[0]['total'] if saldo_result and saldo_result[0]['total'] else 0
            self.ind_saldo.config(text=f"R$ {saldo:,.2f}")

            # Itens em estoque
            estoque = self.db_manager.execute_query(
                "SELECT COUNT(*) as total FROM inventario_itens WHERE ativo = 1"
            )
            if estoque:
                self.ind_estoque.config(text=str(estoque[0]['total'] or 0))

            # Talhões ativos
            talhoes = self.db_manager.execute_query(
                "SELECT COUNT(*) as total FROM talhoes WHERE situacao = 'Ativo'"
            )
            if talhoes:
                self.ind_talhoes.config(text=str(talhoes[0]['total'] or 0))

        except Exception as e:
            print(f"Erro ao carregar estatísticas: {e}")
