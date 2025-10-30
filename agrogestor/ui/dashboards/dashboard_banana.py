# -*- coding: utf-8 -*-
"""
Dashboard de Produção de Bananas
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class DashboardBananaWindow:
    """Dashboard para visualização de dados do bananal"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Dashboard - Produção de Bananas", 
                 font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        # Indicadores
        indicators_frame = ttk.Frame(main_container)
        indicators_frame.pack(fill=X, padx=20, pady=10)

        self.create_indicator(indicators_frame, "Total de Talhões", "0", 0)
        self.create_indicator(indicators_frame, "Área Total (ha)", "0", 1)
        self.create_indicator(indicators_frame, "Produção Mês (kg)", "0", 2)
        self.create_indicator(indicators_frame, "Colheitas Mês", "0", 3)

        # Gráficos e tabelas
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Produção por talhão
        left_frame = ttk.LabelFrame(content_frame, text="Produção por Talhão (Último Mês)", padding=15)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Frame para TreeView e scrollbars
        prod_tree_frame = ttk.Frame(left_frame)
        prod_tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        prod_scrollbar_v = ttk.Scrollbar(prod_tree_frame, orient=VERTICAL)
        prod_scrollbar_v.pack(side=RIGHT, fill=Y)

        prod_scrollbar_h = ttk.Scrollbar(prod_tree_frame, orient=HORIZONTAL)
        prod_scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("Talhão", "Área (ha)", "Produção (kg)", "Kg/ha")
        self.prod_tree = ttk.Treeview(prod_tree_frame, columns=columns, show="headings", height=10,
                                     yscrollcommand=prod_scrollbar_v.set, xscrollcommand=prod_scrollbar_h.set)

        prod_scrollbar_v.config(command=self.prod_tree.yview)
        prod_scrollbar_h.config(command=self.prod_tree.xview)

        for col in columns:
            self.prod_tree.heading(col, text=col)
            self.prod_tree.column(col, width=100, anchor=CENTER)

        self.prod_tree.pack(fill=BOTH, expand=YES)

        # Talhões ativos
        right_frame = ttk.LabelFrame(content_frame, text="Talhões Ativos", padding=15)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Frame para TreeView e scrollbars
        talhao_tree_frame = ttk.Frame(right_frame)
        talhao_tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        talhao_scrollbar_v = ttk.Scrollbar(talhao_tree_frame, orient=VERTICAL)
        talhao_scrollbar_v.pack(side=RIGHT, fill=Y)

        talhao_scrollbar_h = ttk.Scrollbar(talhao_tree_frame, orient=HORIZONTAL)
        talhao_scrollbar_h.pack(side=BOTTOM, fill=X)

        columns2 = ("Código", "Nome", "Variedade", "Situação")
        self.talhao_tree = ttk.Treeview(talhao_tree_frame, columns=columns2, show="headings", height=10,
                                       yscrollcommand=talhao_scrollbar_v.set, xscrollcommand=talhao_scrollbar_h.set)

        talhao_scrollbar_v.config(command=self.talhao_tree.yview)
        talhao_scrollbar_h.config(command=self.talhao_tree.xview)

        for col in columns2:
            self.talhao_tree.heading(col, text=col)
            self.talhao_tree.column(col, width=120)

        self.talhao_tree.pack(fill=BOTH, expand=YES)

        # Botão atualizar
        ttk.Button(main_container, text="🔄 Atualizar Dados", 
                  command=self.load_data).pack(pady=10)

    def create_indicator(self, parent, label, value, column):
        """Cria um indicador visual"""
        frame = ttk.Frame(parent, relief=RAISED, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        
        ttk.Label(frame, text=label, font=("Helvetica", 10)).pack(pady=(10, 5))
        lbl = ttk.Label(frame, text=value, font=("Helvetica", 24, "bold"))
        lbl.pack(pady=(0, 10))
        
        # Guardar referência
        if column == 0:
            self.ind_talhoes = lbl
        elif column == 1:
            self.ind_area = lbl
        elif column == 2:
            self.ind_producao = lbl
        elif column == 3:
            self.ind_colheitas = lbl
        
        parent.columnconfigure(column, weight=1)

    def load_data(self):
        """Carrega dados do dashboard"""
        try:
            # Total de talhões
            talhoes = self.db_manager.select('talhoes', where_clause="situacao = 'Ativo'")
            self.ind_talhoes.config(text=str(len(talhoes)))

            # Área total
            area_total = sum(t['area_hectares'] or 0 for t in talhoes)
            self.ind_area.config(text=f"{area_total:.1f}")

            # Produção do mês
            data_inicio = (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
            sql_producao = """
                SELECT SUM(quantidade_kg) as total
                FROM colheitas_banana
                WHERE data_colheita >= ?
            """
            result = self.db_manager.execute_query(sql_producao, [data_inicio])
            producao = result[0]['total'] if result and result[0]['total'] else 0
            self.ind_producao.config(text=f"{producao:,.0f}")

            # Colheitas do mês
            sql_colheitas = """
                SELECT COUNT(*) as total
                FROM colheitas_banana
                WHERE data_colheita >= ?
            """
            result = self.db_manager.execute_query(sql_colheitas, [data_inicio])
            colheitas = result[0]['total'] if result and result[0]['total'] else 0
            self.ind_colheitas.config(text=str(colheitas))

            # Produção por talhão
            self.load_producao_talhao(data_inicio)

            # Talhões ativos
            self.load_talhoes_ativos()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")

    def load_producao_talhao(self, data_inicio):
        """Carrega produção por talhão"""
        self.prod_tree.delete(*self.prod_tree.get_children())

        sql = """
            SELECT t.nome, t.area_hectares, SUM(c.quantidade_kg) as producao
            FROM talhoes t
            LEFT JOIN colheitas_banana c ON t.id = c.talhao_id AND c.data_colheita >= ?
            WHERE t.situacao = 'Ativo'
            GROUP BY t.id
            HAVING producao > 0
            ORDER BY producao DESC
        """
        
        results = self.db_manager.execute_query(sql, [data_inicio])
        if results:
            for row in results:
                area = row['area_hectares'] or 1
                producao = row['producao'] or 0
                kg_ha = producao / area if area > 0 else 0
                
                self.prod_tree.insert('', END, values=(
                    row['nome'],
                    f"{area:.2f}",
                    f"{producao:,.0f}",
                    f"{kg_ha:,.0f}"
                ))

    def load_talhoes_ativos(self):
        """Carrega lista de talhões ativos"""
        self.talhao_tree.delete(*self.talhao_tree.get_children())

        sql = """
            SELECT t.codigo, t.nome, v.nome as variedade, t.situacao
            FROM talhoes t
            LEFT JOIN variedades_banana v ON t.variedade_id = v.id
            WHERE t.situacao = 'Ativo'
            ORDER BY t.codigo
        """
        
        results = self.db_manager.execute_query(sql)
        if results:
            for row in results:
                self.talhao_tree.insert('', END, values=(
                    row['codigo'],
                    row['nome'],
                    row['variedade'] or 'Não definida',
                    row['situacao']
                ))
