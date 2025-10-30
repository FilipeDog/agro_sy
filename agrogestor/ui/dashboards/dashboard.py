"""
Dashboard - Indicadores e Estatísticas
"""
import tkinter as tk
from tkinter import messagebox
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class DashboardWindow:
    """Janela de dashboard com indicadores"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        """Cria interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(
            title_frame,
            text="Dashboard - Indicadores do Rebanho",
            font=("Helvetica", 18, "bold")
        ).pack(side=LEFT)

        ttk.Button(
            title_frame,
            text="Atualizar",
            command=self.load_data
        ).pack(side=RIGHT)

        # Cards de indicadores
        cards_frame = ttk.Frame(main_container)
        cards_frame.pack(fill=X, padx=20, pady=10)

        # Linha 1 de cards
        row1 = ttk.Frame(cards_frame)
        row1.pack(fill=X, pady=5)

        self.card_total_animais = self.create_card(row1, "Total de Animais", "0", "info")
        self.card_total_animais.pack(side=LEFT, padx=5, fill=X, expand=YES)

        self.card_peso_total = self.create_card(row1, "Peso Total", "0 kg", "success")
        self.card_peso_total.pack(side=LEFT, padx=5, fill=X, expand=YES)

        self.card_total_receitas = self.create_card(row1, "Total Receitas", "R$ 0,00", "success")
        self.card_total_receitas.pack(side=LEFT, padx=5, fill=X, expand=YES)

        self.card_total_despesas = self.create_card(row1, "Total Despesas", "R$ 0,00", "danger")
        self.card_total_despesas.pack(side=LEFT, padx=5, fill=X, expand=YES)

        # Seção de gráficos/tabelas
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Coluna esquerda
        left_col = ttk.Frame(content_frame)
        left_col.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Animais por Status
        status_frame = ttk.LabelFrame(left_col, text="Animais por Status", padding=10)
        status_frame.pack(fill=BOTH, expand=YES, pady=5)

        # Frame para TreeView e scrollbars
        status_tree_frame = ttk.Frame(status_frame)
        status_tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        status_scrollbar_v = ttk.Scrollbar(status_tree_frame, orient=VERTICAL)
        status_scrollbar_v.pack(side=RIGHT, fill=Y)

        status_scrollbar_h = ttk.Scrollbar(status_tree_frame, orient=HORIZONTAL)
        status_scrollbar_h.pack(side=BOTTOM, fill=X)

        self.status_tree = ttk.Treeview(
            status_tree_frame,
            columns=("Status", "Quantidade", "Percentual"),
            show="headings",
            height=6,
            yscrollcommand=status_scrollbar_v.set,
            xscrollcommand=status_scrollbar_h.set
        )

        status_scrollbar_v.config(command=self.status_tree.yview)
        status_scrollbar_h.config(command=self.status_tree.xview)

        for col in ["Status", "Quantidade", "Percentual"]:
            self.status_tree.heading(col, text=col)
            self.status_tree.column(col, width=100, anchor=CENTER)

        self.status_tree.pack(fill=BOTH, expand=YES)

        # Animais por Raça
        raca_frame = ttk.LabelFrame(left_col, text="Animais por Raça", padding=10)
        raca_frame.pack(fill=BOTH, expand=YES, pady=5)

        # Frame para TreeView e scrollbars
        raca_tree_frame = ttk.Frame(raca_frame)
        raca_tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        raca_scrollbar_v = ttk.Scrollbar(raca_tree_frame, orient=VERTICAL)
        raca_scrollbar_v.pack(side=RIGHT, fill=Y)

        raca_scrollbar_h = ttk.Scrollbar(raca_tree_frame, orient=HORIZONTAL)
        raca_scrollbar_h.pack(side=BOTTOM, fill=X)

        self.raca_tree = ttk.Treeview(
            raca_tree_frame,
            columns=("Raça", "Quantidade"),
            show="headings",
            height=6,
            yscrollcommand=raca_scrollbar_v.set,
            xscrollcommand=raca_scrollbar_h.set
        )

        raca_scrollbar_v.config(command=self.raca_tree.yview)
        raca_scrollbar_h.config(command=self.raca_tree.xview)

        for col in ["Raça", "Quantidade"]:
            self.raca_tree.heading(col, text=col)
            self.raca_tree.column(col, width=150, anchor=CENTER)

        self.raca_tree.pack(fill=BOTH, expand=YES)

        # Coluna direita
        right_col = ttk.Frame(content_frame)
        right_col.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Top 10 Clientes
        clientes_frame = ttk.LabelFrame(right_col, text="Top 10 Clientes", padding=10)
        clientes_frame.pack(fill=BOTH, expand=YES, pady=5)

        # Frame para TreeView e scrollbars
        clientes_tree_frame = ttk.Frame(clientes_frame)
        clientes_tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        clientes_scrollbar_v = ttk.Scrollbar(clientes_tree_frame, orient=VERTICAL)
        clientes_scrollbar_v.pack(side=RIGHT, fill=Y)

        clientes_scrollbar_h = ttk.Scrollbar(clientes_tree_frame, orient=HORIZONTAL)
        clientes_scrollbar_h.pack(side=BOTTOM, fill=X)

        self.clientes_tree = ttk.Treeview(
            clientes_tree_frame,
            columns=("Cliente", "Total Compras"),
            show="headings",
            height=6,
            yscrollcommand=clientes_scrollbar_v.set,
            xscrollcommand=clientes_scrollbar_h.set
        )

        clientes_scrollbar_v.config(command=self.clientes_tree.yview)
        clientes_scrollbar_h.config(command=self.clientes_tree.xview)

        for col in ["Cliente", "Total Compras"]:
            self.clientes_tree.heading(col, text=col)
            self.clientes_tree.column(col, width=150, anchor=CENTER if col == "Total Compras" else W)

        self.clientes_tree.pack(fill=BOTH, expand=YES)

        # Resultado Mensal
        resultado_frame = ttk.LabelFrame(right_col, text="Resultado Mensal (Últimos 6 meses)", padding=10)
        resultado_frame.pack(fill=BOTH, expand=YES, pady=5)

        # Frame para TreeView e scrollbars
        resultado_tree_frame = ttk.Frame(resultado_frame)
        resultado_tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        resultado_scrollbar_v = ttk.Scrollbar(resultado_tree_frame, orient=VERTICAL)
        resultado_scrollbar_v.pack(side=RIGHT, fill=Y)

        resultado_scrollbar_h = ttk.Scrollbar(resultado_tree_frame, orient=HORIZONTAL)
        resultado_scrollbar_h.pack(side=BOTTOM, fill=X)

        self.resultado_tree = ttk.Treeview(
            resultado_tree_frame,
            columns=("Mês", "Receitas", "Despesas", "Saldo"),
            show="headings",
            height=6,
            yscrollcommand=resultado_scrollbar_v.set,
            xscrollcommand=resultado_scrollbar_h.set
        )

        resultado_scrollbar_v.config(command=self.resultado_tree.yview)
        resultado_scrollbar_h.config(command=self.resultado_tree.xview)

        for col in ["Mês", "Receitas", "Despesas", "Saldo"]:
            self.resultado_tree.heading(col, text=col)
            self.resultado_tree.column(col, width=100, anchor=CENTER)

        self.resultado_tree.pack(fill=BOTH, expand=YES)

    def create_card(self, parent, title, value, style="info"):
        """Cria um card de indicador"""
        try:
            card = ttk.Frame(parent, bootstyle=style)
        except:
            card = ttk.Frame(parent)

        card_inner = ttk.Frame(card, padding=20)
        card_inner.pack(fill=BOTH, expand=YES)

        title_label = ttk.Label(
            card_inner,
            text=title,
            font=("Helvetica", 10)
        )
        title_label.pack()

        value_label = ttk.Label(
            card_inner,
            text=value,
            font=("Helvetica", 20, "bold")
        )
        value_label.pack(pady=(10, 0))

        # Guardar referência do label de valor
        card.value_label = value_label

        return card

    def load_data(self):
        """Carrega todos os dados do dashboard"""
        # Total de Animais
        sql = "SELECT COUNT(*) as total FROM animais WHERE status_id IN (SELECT id FROM status_animal WHERE nome = 'Ativo')"
        result = self.db_manager.execute_query(sql)
        total_animais = result[0]['total'] if result else 0
        self.card_total_animais.value_label.config(text=str(total_animais))

        # Peso Total
        sql = "SELECT SUM(peso_atual) as total FROM animais WHERE status_id IN (SELECT id FROM status_animal WHERE nome = 'Ativo')"
        result = self.db_manager.execute_query(sql)
        peso_total = result[0]['total'] if result and result[0]['total'] else 0
        self.card_peso_total.value_label.config(text=f"{peso_total:,.1f} kg")

        # Total Receitas
        sql = "SELECT SUM(valor_total) as total FROM receitas"
        result = self.db_manager.execute_query(sql)
        total_receitas = result[0]['total'] if result and result[0]['total'] else 0
        self.card_total_receitas.value_label.config(text=f"R$ {total_receitas:,.2f}")

        # Total Despesas
        sql = "SELECT SUM(valor) as total FROM despesas"
        result = self.db_manager.execute_query(sql)
        total_despesas = result[0]['total'] if result and result[0]['total'] else 0
        self.card_total_despesas.value_label.config(text=f"R$ {total_despesas:,.2f}")

        # Animais por Status
        self.load_status_data(total_animais)

        # Animais por Raça
        self.load_raca_data()

        # Top 10 Clientes
        self.load_top_clientes()

        # Resultado Mensal
        self.load_resultado_mensal()

    def load_status_data(self, total):
        """Carrega animais por status"""
        for item in self.status_tree.get_children():
            self.status_tree.delete(item)

        sql = """
            SELECT s.nome as status, COUNT(a.id) as quantidade
            FROM status_animal s
            LEFT JOIN animais a ON a.status_id = s.id
            GROUP BY s.id, s.nome
            ORDER BY quantidade DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            qtd = row['quantidade']
            percentual = (qtd / total * 100) if total > 0 else 0
            self.status_tree.insert('', END, values=(
                row['status'],
                qtd,
                f"{percentual:.1f}%"
            ))

    def load_raca_data(self):
        """Carrega animais por raça"""
        for item in self.raca_tree.get_children():
            self.raca_tree.delete(item)

        sql = """
            SELECT r.nome as raca, COUNT(a.id) as quantidade
            FROM raca r
            LEFT JOIN animais a ON a.raca_id = r.id
            GROUP BY r.id, r.nome
            HAVING quantidade > 0
            ORDER BY quantidade DESC
            LIMIT 10
        """

        results = self.db_manager.execute_query(sql)

        if results:
            for row in results:
                self.raca_tree.insert('', END, values=(row['raca'], row['quantidade']))

    def load_top_clientes(self):
        """Carrega top 10 clientes"""
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)

        sql = """
            SELECT c.nome, SUM(r.valor_total) as total
            FROM receitas r
            LEFT JOIN clientes c ON r.cliente_id = c.id
            WHERE c.nome IS NOT NULL
            GROUP BY c.id, c.nome
            ORDER BY total DESC
            LIMIT 10
        """

        results = self.db_manager.execute_query(sql)

        if results:
            for row in results:
                self.clientes_tree.insert('', END, values=(
                    row['nome'],
                    f"R$ {row['total']:,.2f}"
                ))

    def load_resultado_mensal(self):
        """Carrega resultado mensal"""
        for item in self.resultado_tree.get_children():
            self.resultado_tree.delete(item)

        sql = """
            SELECT
                strftime('%m/%Y', data) as mes,
                SUM(CASE WHEN tipo = 'D' THEN valor ELSE 0 END) as despesas,
                SUM(CASE WHEN tipo = 'R' THEN valor ELSE 0 END) as receitas
            FROM (
                SELECT data_gasto as data, valor, 'D' as tipo FROM despesas
                UNION ALL
                SELECT data_venda as data, valor_total as valor, 'R' as tipo FROM receitas
            )
            GROUP BY strftime('%m/%Y', data)
            ORDER BY data DESC
            LIMIT 6
        """

        results = self.db_manager.execute_query(sql)

        if results:
            for row in results:
                despesas = row['despesas'] or 0
                receitas = row['receitas'] or 0
                saldo = receitas - despesas
                self.resultado_tree.insert('', END, values=(
                    row['mes'],
                    f"R$ {receitas:,.2f}",
                    f"R$ {despesas:,.2f}",
                    f"R$ {saldo:,.2f}"
                ))
