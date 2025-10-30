# -*- coding: utf-8 -*-
"""
Dashboard Financeiro com Gráficos
Análise visual completa das finanças
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class FinancialDashboard:
    """Dashboard financeiro com gráficos"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.create_ui()

    def create_ui(self):
        """Cria interface do dashboard"""
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.parent, bg='#0078d7', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="💰 DASHBOARD FINANCEIRO",
                        bg='#0078d7', fg='white',
                        font=('Arial', 20, 'bold'))
        title.pack(pady=10)

        subtitle = tk.Label(header, text="Análise Visual Completa das Finanças do Sistema",
                           bg='#0078d7', fg='white',
                           font=('Arial', 11))
        subtitle.pack()

        # Filter frame
        filter_frame = tk.Frame(self.parent, bg='white', height=80)
        filter_frame.pack(fill=tk.X, padx=20, pady=20)
        filter_frame.pack_propagate(False)

        filter_container = tk.Frame(filter_frame, bg='white')
        filter_container.pack(expand=True)

        tk.Label(filter_container, text="Período:",
                font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT, padx=10)

        # Period selection
        self.period_var = tk.StringVar(value='30')
        periods = [
            ('Últimos 7 dias', '7'),
            ('Últimos 30 dias', '30'),
            ('Últimos 90 dias', '90'),
            ('Últimos 12 meses', '365'),
            ('Este ano', 'year'),
            ('Todo período', 'all')
        ]

        for text, value in periods:
            tk.Radiobutton(filter_container, text=text, variable=self.period_var,
                          value=value, bg='white', font=('Arial', 9),
                          command=self.load_data).pack(side=tk.LEFT, padx=5)

        # Main container
        main_container = tk.Frame(self.parent, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container, bg='#f5f5f5')
        scrollbar = tk.Scrollbar(main_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.scrollable_frame = scrollable_frame

        # Load data
        self.load_data()

    def load_data(self):
        """Carrega e exibe dados financeiros"""
        # Clear scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get date range
        period = self.period_var.get()
        today = datetime.now()

        if period == 'all':
            start_date = '2000-01-01'
        elif period == 'year':
            start_date = f'{today.year}-01-01'
        else:
            days = int(period)
            start_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')

        end_date = today.strftime('%Y-%m-%d')

        # Get financial data
        expenses_data = self.get_expenses_data(start_date, end_date)
        revenues_data = self.get_revenues_data(start_date, end_date)

        # Row 1: Main indicators
        indicators_frame = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
        indicators_frame.pack(fill=tk.X, padx=10, pady=10)

        total_expenses = sum(exp['valor'] for exp in expenses_data)
        total_revenues = sum(rev['valor'] for rev in revenues_data)
        balance = total_revenues - total_expenses

        self.create_indicator_card(indicators_frame, "💸 Total Despesas",
                                   f"R$ {total_expenses:,.2f}",
                                   '#dc3545', 0)
        self.create_indicator_card(indicators_frame, "💰 Total Receitas",
                                   f"R$ {total_revenues:,.2f}",
                                   '#28a745', 1)
        self.create_indicator_card(indicators_frame, "📊 Resultado",
                                   f"R$ {balance:,.2f}",
                                   '#28a745' if balance >= 0 else '#dc3545', 2)
        self.create_indicator_card(indicators_frame, "📈 Margem",
                                   f"{(balance/total_revenues*100) if total_revenues > 0 else 0:.1f}%",
                                   '#17a2b8', 3)

        # Row 1.5: Pie Charts (if matplotlib available)
        if MATPLOTLIB_AVAILABLE:
            # Title for pie charts section
            pie_title_frame = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
            pie_title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

            tk.Label(pie_title_frame, text="📊 ANÁLISE POR CATEGORIAS",
                    font=('Arial', 14, 'bold'), bg='#f5f5f5', fg='#333').pack()

            # Row with 4 pie charts (2x2 grid)
            pie_row1 = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
            pie_row1.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Despesas por Categoria
            pie_frame1 = tk.Frame(pie_row1, bg='white', relief=tk.RIDGE, bd=2)
            pie_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            self.create_expenses_by_category_pie(pie_frame1, start_date, end_date)

            # Receitas por Categoria
            pie_frame2 = tk.Frame(pie_row1, bg='white', relief=tk.RIDGE, bd=2)
            pie_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
            self.create_revenues_by_category_pie(pie_frame2, start_date, end_date)

            pie_row2 = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
            pie_row2.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Top Fornecedores (Pizza)
            pie_frame3 = tk.Frame(pie_row2, bg='white', relief=tk.RIDGE, bd=2)
            pie_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            self.create_suppliers_pie(pie_frame3, start_date, end_date)

            # Top Clientes (Pizza)
            pie_frame4 = tk.Frame(pie_row2, bg='white', relief=tk.RIDGE, bd=2)
            pie_frame4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
            self.create_clients_pie(pie_frame4, start_date, end_date)

        # Row 2: Monthly comparison chart
        chart_frame1 = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RIDGE, bd=2)
        chart_frame1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(chart_frame1, text="📊 Receitas vs Despesas por Mês",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)

        self.create_monthly_chart(chart_frame1, expenses_data, revenues_data)

        # Row 3: Two charts side by side
        row3 = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
        row3.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Expenses by supplier chart
        chart_frame2 = tk.Frame(row3, bg='white', relief=tk.RIDGE, bd=2)
        chart_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(chart_frame2, text="🏪 Top 5 Fornecedores (Despesas)",
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

        self.create_supplier_chart(chart_frame2, start_date, end_date)

        # Revenues by client chart
        chart_frame3 = tk.Frame(row3, bg='white', relief=tk.RIDGE, bd=2)
        chart_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(chart_frame3, text="👥 Top 5 Clientes (Receitas)",
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

        self.create_client_chart(chart_frame3, start_date, end_date)

        # Row 4: Payment status
        row4 = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
        row4.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Expenses payment status
        status_frame1 = tk.Frame(row4, bg='white', relief=tk.RIDGE, bd=2)
        status_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(status_frame1, text="💳 Status de Pagamento - Despesas",
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

        self.create_payment_status_chart(status_frame1, 'expenses', start_date, end_date)

        # Revenues receipt status
        status_frame2 = tk.Frame(row4, bg='white', relief=tk.RIDGE, bd=2)
        status_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(status_frame2, text="💵 Status de Recebimento - Receitas",
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

        self.create_payment_status_chart(status_frame2, 'revenues', start_date, end_date)

    def create_indicator_card(self, parent, title, value, color, col):
        """Cria um card de indicador"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=3)
        card.grid(row=0, column=col, padx=10, pady=10, sticky='nsew')
        parent.columnconfigure(col, weight=1)

        tk.Label(card, text=title, bg=color, fg='white',
                font=('Arial', 11, 'bold')).pack(pady=(15, 5))

        tk.Label(card, text=value, bg=color, fg='white',
                font=('Arial', 18, 'bold')).pack(pady=(5, 15))

        card.config(height=100)

    def get_expenses_data(self, start_date, end_date):
        """Busca dados de despesas"""
        try:
            sql = """
                SELECT d.*, f.nome as fornecedor_nome
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE d.data_gasto BETWEEN ? AND ?
                ORDER BY d.data_gasto
            """
            return self.db_manager.execute_query(sql, [start_date, end_date])
        except:
            return []

    def get_revenues_data(self, start_date, end_date):
        """Busca dados de receitas"""
        try:
            sql = """
                SELECT r.*, c.nome as cliente_nome
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE r.data_venda BETWEEN ? AND ?
                ORDER BY r.data_venda
            """
            results = self.db_manager.execute_query(sql, [start_date, end_date])
            # Rename valor_total to valor for consistency
            for r in results:
                r['valor'] = r.get('valor_total', 0)
            return results
        except:
            return []

    def create_monthly_chart(self, parent, expenses, revenues):
        """Cria gráfico de barras mensal"""
        # Group by month
        monthly_expenses = {}
        monthly_revenues = {}

        for exp in expenses:
            try:
                date = datetime.strptime(exp['data_gasto'], '%Y-%m-%d')
                month_key = date.strftime('%Y-%m')
                monthly_expenses[month_key] = monthly_expenses.get(month_key, 0) + float(exp['valor'])
            except:
                pass

        for rev in revenues:
            try:
                date = datetime.strptime(rev['data_venda'], '%Y-%m-%d')
                month_key = date.strftime('%Y-%m')
                monthly_revenues[month_key] = monthly_revenues.get(month_key, 0) + float(rev['valor'])
            except:
                pass

        # Get all months
        all_months = sorted(set(list(monthly_expenses.keys()) + list(monthly_revenues.keys())))

        if not all_months:
            tk.Label(parent, text="Sem dados para exibir", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=50)
            return

        # Create chart frame
        chart_canvas = tk.Canvas(parent, bg='white', height=300)
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Calculate max value
        max_value = max(
            max(monthly_expenses.values(), default=0),
            max(monthly_revenues.values(), default=0)
        )

        if max_value == 0:
            max_value = 1

        # Draw bars
        num_months = len(all_months)
        bar_width = min(40, 600 // (num_months * 2 + 1))
        spacing = 10

        canvas_width = (bar_width * 2 + spacing) * num_months + 100
        chart_canvas.config(width=canvas_width)

        x_start = 50
        y_base = 250
        chart_height = 200

        for i, month in enumerate(all_months):
            x = x_start + i * (bar_width * 2 + spacing)

            # Expense bar
            exp_value = monthly_expenses.get(month, 0)
            exp_height = (exp_value / max_value) * chart_height if max_value > 0 else 0
            chart_canvas.create_rectangle(
                x, y_base - exp_height, x + bar_width, y_base,
                fill='#dc3545', outline='#c82333'
            )
            if exp_height > 20:
                chart_canvas.create_text(
                    x + bar_width//2, y_base - exp_height - 10,
                    text=f'R${exp_value:,.0f}', font=('Arial', 8)
                )

            # Revenue bar
            rev_value = monthly_revenues.get(month, 0)
            rev_height = (rev_value / max_value) * chart_height if max_value > 0 else 0
            chart_canvas.create_rectangle(
                x + bar_width + 5, y_base - rev_height,
                x + bar_width * 2 + 5, y_base,
                fill='#28a745', outline='#218838'
            )
            if rev_height > 20:
                chart_canvas.create_text(
                    x + bar_width * 1.5 + 5, y_base - rev_height - 10,
                    text=f'R${rev_value:,.0f}', font=('Arial', 8)
                )

            # Month label
            try:
                date_obj = datetime.strptime(month, '%Y-%m')
                month_label = date_obj.strftime('%b/%y')
            except:
                month_label = month

            chart_canvas.create_text(
                x + bar_width, y_base + 15,
                text=month_label, font=('Arial', 8), angle=0
            )

        # Legend
        legend_y = 20
        chart_canvas.create_rectangle(canvas_width - 180, legend_y, canvas_width - 165, legend_y + 15,
                                      fill='#dc3545', outline='#c82333')
        chart_canvas.create_text(canvas_width - 155, legend_y + 7, text='Despesas',
                                anchor='w', font=('Arial', 9))

        chart_canvas.create_rectangle(canvas_width - 180, legend_y + 25, canvas_width - 165, legend_y + 40,
                                      fill='#28a745', outline='#218838')
        chart_canvas.create_text(canvas_width - 155, legend_y + 32, text='Receitas',
                                anchor='w', font=('Arial', 9))

    def create_supplier_chart(self, parent, start_date, end_date):
        """Cria gráfico de top fornecedores"""
        try:
            sql = """
                SELECT f.nome, SUM(d.valor) as total
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE d.data_gasto BETWEEN ? AND ?
                GROUP BY f.id
                ORDER BY total DESC
                LIMIT 5
            """
            results = self.db_manager.execute_query(sql, [start_date, end_date])

            if not results:
                tk.Label(parent, text="Sem dados", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=50)
                return

            self.create_horizontal_bar_chart(parent, results, '#dc3545')
        except:
            tk.Label(parent, text="Erro ao carregar", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=50)

    def create_client_chart(self, parent, start_date, end_date):
        """Cria gráfico de top clientes"""
        try:
            sql = """
                SELECT c.nome, SUM(r.valor_total) as total
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE r.data_venda BETWEEN ? AND ?
                GROUP BY c.id
                ORDER BY total DESC
                LIMIT 5
            """
            results = self.db_manager.execute_query(sql, [start_date, end_date])

            if not results:
                tk.Label(parent, text="Sem dados", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=50)
                return

            self.create_horizontal_bar_chart(parent, results, '#28a745')
        except:
            tk.Label(parent, text="Erro ao carregar", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=50)

    def create_horizontal_bar_chart(self, parent, data, color):
        """Cria gráfico de barras horizontal"""
        chart_canvas = tk.Canvas(parent, bg='white', height=250)
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        if not data:
            return

        max_value = max(row['total'] for row in data)
        if max_value == 0:
            max_value = 1

        y_start = 20
        bar_height = 30
        spacing = 10

        for i, row in enumerate(data):
            y = y_start + i * (bar_height + spacing)
            value = float(row['total'])
            bar_width = (value / max_value) * 300

            # Bar
            chart_canvas.create_rectangle(
                150, y, 150 + bar_width, y + bar_height,
                fill=color, outline=''
            )

            # Label
            name = row['nome'] if row['nome'] else 'Sem nome'
            if len(name) > 20:
                name = name[:17] + '...'

            chart_canvas.create_text(
                145, y + bar_height//2, text=name,
                anchor='e', font=('Arial', 9)
            )

            # Value
            chart_canvas.create_text(
                160 + bar_width, y + bar_height//2,
                text=f'R$ {value:,.2f}',
                anchor='w', font=('Arial', 9, 'bold')
            )

    def create_payment_status_chart(self, parent, type_name, start_date, end_date):
        """Cria gráfico de status de pagamento"""
        try:
            if type_name == 'expenses':
                table = 'despesas'
                value_field = 'valor'
                date_field = 'data_gasto'
            else:
                table = 'receitas'
                value_field = 'valor_total'
                date_field = 'data_venda'

            sql = f"""
                SELECT
                    SUM(CASE WHEN pago = 1 THEN {value_field} ELSE 0 END) as paid,
                    SUM(CASE WHEN pago = 0 THEN {value_field} ELSE 0 END) as pending
                FROM {table}
                WHERE {date_field} BETWEEN ? AND ?
            """
            result = self.db_manager.execute_query(sql, [start_date, end_date])

            if not result or not result[0]:
                tk.Label(parent, text="Sem dados", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=50)
                return

            paid = float(result[0]['paid'] or 0)
            pending = float(result[0]['pending'] or 0)
            total = paid + pending

            if total == 0:
                tk.Label(parent, text="Sem dados", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=50)
                return

            # Create pie chart (simple version with rectangles)
            chart_canvas = tk.Canvas(parent, bg='white', height=200)
            chart_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Calculate percentages
            paid_pct = (paid / total) * 100
            pending_pct = (pending / total) * 100

            # Draw bars
            y = 80
            bar_height = 40

            # Paid bar
            paid_width = (paid / total) * 300 if total > 0 else 0
            chart_canvas.create_rectangle(
                100, y, 100 + paid_width, y + bar_height,
                fill='#28a745', outline=''
            )
            if paid_width > 50:
                chart_canvas.create_text(
                    100 + paid_width//2, y + bar_height//2,
                    text=f'{paid_pct:.1f}%\nR$ {paid:,.2f}',
                    fill='white', font=('Arial', 9, 'bold')
                )

            # Pending bar
            pending_width = (pending / total) * 300 if total > 0 else 0
            chart_canvas.create_rectangle(
                100 + paid_width, y, 100 + paid_width + pending_width, y + bar_height,
                fill='#ffc107', outline=''
            )
            if pending_width > 50:
                chart_canvas.create_text(
                    100 + paid_width + pending_width//2, y + bar_height//2,
                    text=f'{pending_pct:.1f}%\nR$ {pending:,.2f}',
                    fill='white', font=('Arial', 9, 'bold')
                )

            # Legend
            legend_y = 150
            chart_canvas.create_rectangle(150, legend_y, 165, legend_y + 15,
                                          fill='#28a745')
            chart_canvas.create_text(170, legend_y + 7, text='Pago/Recebido',
                                    anchor='w', font=('Arial', 9))

            chart_canvas.create_rectangle(270, legend_y, 285, legend_y + 15,
                                          fill='#ffc107')
            chart_canvas.create_text(290, legend_y + 7, text='Pendente',
                                    anchor='w', font=('Arial', 9))

        except Exception as e:
            tk.Label(parent, text=f"Erro: {str(e)}", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=50)

    def create_expenses_by_category_pie(self, parent, start_date, end_date):
        """Cria gráfico de pizza de despesas por categoria"""
        try:
            tk.Label(parent, text="💸 Despesas por Categoria",
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

            # Query data
            sql = """
                SELECT td.nome as categoria, SUM(d.valor) as total
                FROM despesas d
                LEFT JOIN tipo_despesa td ON d.tipo_despesa_id = td.id
                WHERE d.data_gasto BETWEEN ? AND ?
                GROUP BY td.nome
                ORDER BY total DESC
            """
            data = self.db_manager.execute_query(sql, [start_date, end_date])

            if not data or sum(row['total'] or 0 for row in data) == 0:
                tk.Label(parent, text="Sem dados no período", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=30)
                return

            # Prepare data
            labels = [row['categoria'] or 'Sem categoria' for row in data]
            sizes = [row['total'] for row in data]
            colors = ['#dc3545', '#ff6b6b', '#ffa502', '#ff7979', '#ee5a6f',
                     '#ff6348', '#ff4757', '#fd7272', '#fc5c65', '#ff3838']

            # Create pie chart
            fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)

            wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%',
                                              startangle=90, colors=colors[:len(sizes)],
                                              textprops={'color': 'white', 'weight': 'bold'})

            # Legend
            ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                     fontsize=8)

            ax.set_title("", fontsize=10)

            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        except Exception as e:
            tk.Label(parent, text=f"Erro: {str(e)}", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=30)

    def create_revenues_by_category_pie(self, parent, start_date, end_date):
        """Cria gráfico de pizza de receitas por categoria"""
        try:
            tk.Label(parent, text="💰 Receitas por Categoria",
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

            # Query data
            sql = """
                SELECT tr.nome as categoria, SUM(r.valor_total) as total
                FROM receitas r
                LEFT JOIN tipo_receita tr ON r.tipo_receita_id = tr.id
                WHERE r.data_venda BETWEEN ? AND ?
                GROUP BY tr.nome
                ORDER BY total DESC
            """
            data = self.db_manager.execute_query(sql, [start_date, end_date])

            if not data or sum(row['total'] or 0 for row in data) == 0:
                tk.Label(parent, text="Sem dados no período", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=30)
                return

            # Prepare data
            labels = [row['categoria'] or 'Sem categoria' for row in data]
            sizes = [row['total'] for row in data]
            colors = ['#28a745', '#38c172', '#4cd964', '#51cf66', '#5cd85a',
                     '#6bdb6b', '#7ee07e', '#8be68b', '#99eb99', '#a5f0a5']

            # Create pie chart
            fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)

            wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%',
                                              startangle=90, colors=colors[:len(sizes)],
                                              textprops={'color': 'white', 'weight': 'bold'})

            # Legend
            ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                     fontsize=8)

            ax.set_title("", fontsize=10)

            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        except Exception as e:
            tk.Label(parent, text=f"Erro: {str(e)}", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=30)

    def create_suppliers_pie(self, parent, start_date, end_date):
        """Cria gráfico de pizza de fornecedores"""
        try:
            tk.Label(parent, text="🏪 Top Fornecedores",
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

            # Query data
            sql = """
                SELECT f.nome as fornecedor, SUM(d.valor) as total
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE d.data_gasto BETWEEN ? AND ?
                  AND f.nome IS NOT NULL
                GROUP BY f.nome
                ORDER BY total DESC
                LIMIT 5
            """
            data = self.db_manager.execute_query(sql, [start_date, end_date])

            if not data or sum(row['total'] or 0 for row in data) == 0:
                tk.Label(parent, text="Sem dados no período", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=30)
                return

            # Prepare data
            labels = [row['fornecedor'] for row in data]
            sizes = [row['total'] for row in data]
            colors = ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff']

            # Create pie chart
            fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)

            wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%',
                                              startangle=90, colors=colors[:len(sizes)],
                                              textprops={'color': 'white', 'weight': 'bold'})

            # Legend
            ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                     fontsize=8)

            ax.set_title("", fontsize=10)

            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        except Exception as e:
            tk.Label(parent, text=f"Erro: {str(e)}", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=30)

    def create_clients_pie(self, parent, start_date, end_date):
        """Cria gráfico de pizza de clientes"""
        try:
            tk.Label(parent, text="👥 Top Clientes",
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)

            # Query data
            sql = """
                SELECT c.nome as cliente, SUM(r.valor_total) as total
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE r.data_venda BETWEEN ? AND ?
                  AND c.nome IS NOT NULL
                GROUP BY c.nome
                ORDER BY total DESC
                LIMIT 5
            """
            data = self.db_manager.execute_query(sql, [start_date, end_date])

            if not data or sum(row['total'] or 0 for row in data) == 0:
                tk.Label(parent, text="Sem dados no período", bg='white',
                        font=('Arial', 10), fg='#999').pack(pady=30)
                return

            # Prepare data
            labels = [row['cliente'] for row in data]
            sizes = [row['total'] for row in data]
            colors = ['#66bb6a', '#42a5f5', '#ffa726', '#ab47bc', '#26c6da']

            # Create pie chart
            fig = Figure(figsize=(5, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)

            wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%',
                                              startangle=90, colors=colors[:len(sizes)],
                                              textprops={'color': 'white', 'weight': 'bold'})

            # Legend
            ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                     fontsize=8)

            ax.set_title("", fontsize=10)

            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        except Exception as e:
            tk.Label(parent, text=f"Erro: {str(e)}", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=30)
