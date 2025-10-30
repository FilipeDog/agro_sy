# -*- coding: utf-8 -*-
"""
Fluxo de Caixa Projetado
Projeção de saldo futuro baseado em receitas e despesas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from collections import defaultdict


class CashFlowProjection:
    """Fluxo de caixa projetado"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.create_ui()

    def create_ui(self):
        """Cria interface"""
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.parent, bg='#6610f2', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="📈 FLUXO DE CAIXA PROJETADO",
                        bg='#6610f2', fg='white',
                        font=('Arial', 20, 'bold'))
        title.pack(pady=10)

        subtitle = tk.Label(header, text="Projeção do saldo futuro com base em receitas e despesas pendentes",
                           bg='#6610f2', fg='white',
                           font=('Arial', 11))
        subtitle.pack()

        # Filter frame
        filter_frame = tk.Frame(self.parent, bg='white', height=80)
        filter_frame.pack(fill=tk.X, padx=20, pady=20)
        filter_frame.pack_propagate(False)

        filter_container = tk.Frame(filter_frame, bg='white')
        filter_container.pack(expand=True)

        tk.Label(filter_container, text="Projeção para:",
                font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT, padx=10)

        # Period selection
        self.period_var = tk.StringVar(value='30')
        periods = [
            ('30 dias', '30'),
            ('60 dias', '60'),
            ('90 dias', '90'),
            ('6 meses', '180'),
            ('1 ano', '365')
        ]

        for text, value in periods:
            tk.Radiobutton(filter_container, text=text, variable=self.period_var,
                          value=value, bg='white', font=('Arial', 10),
                          command=self.load_projection).pack(side=tk.LEFT, padx=5)

        # Main container
        main_container = tk.Frame(self.parent, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container, bg='#f5f5f5')
        scrollbar = tk.Scrollbar(main_container, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Load projection
        self.load_projection()

    def load_projection(self):
        """Carrega e exibe projeção"""
        # Clear
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        days = int(self.period_var.get())
        today = datetime.now().date()
        end_date = today + timedelta(days=days)

        # Get current balances
        current_balance = self.get_total_balance()

        # Get pending transactions
        pending_expenses = self.get_pending_expenses(today, end_date)
        pending_revenues = self.get_pending_revenues(today, end_date)

        # Calculate projections
        projections = self.calculate_projections(
            current_balance,
            pending_expenses,
            pending_revenues,
            today,
            end_date
        )

        # Row 1: Current situation
        current_frame = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
        current_frame.pack(fill=tk.X, padx=10, pady=10)

        self.create_indicator_card(current_frame, "💰 Saldo Atual",
                                   f"R$ {current_balance:,.2f}",
                                   '#17a2b8', 0)

        total_pending_exp = sum(e['valor'] for e in pending_expenses)
        self.create_indicator_card(current_frame, "💸 Despesas Pendentes",
                                   f"R$ {total_pending_exp:,.2f}",
                                   '#dc3545', 1)

        total_pending_rev = sum(r['valor'] for r in pending_revenues)
        self.create_indicator_card(current_frame, "💵 Receitas Pendentes",
                                   f"R$ {total_pending_rev:,.2f}",
                                   '#28a745', 2)

        projected_balance = current_balance + total_pending_rev - total_pending_exp
        color = '#28a745' if projected_balance >= 0 else '#dc3545'
        self.create_indicator_card(current_frame, f"📊 Saldo Projetado ({days} dias)",
                                   f"R$ {projected_balance:,.2f}",
                                   color, 3)

        # Row 2: Projection chart
        chart_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RIDGE, bd=2)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(chart_frame, text="📈 Evolução do Saldo Projetado",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)

        self.create_projection_chart(chart_frame, projections)

        # Row 3: Two lists side by side
        lists_frame = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
        lists_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pending expenses list
        exp_frame = tk.Frame(lists_frame, bg='white', relief=tk.RIDGE, bd=2)
        exp_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(exp_frame, text="💸 Despesas Pendentes",
                font=('Arial', 12, 'bold'), bg='white', fg='#dc3545').pack(pady=10)

        self.create_transactions_list(exp_frame, pending_expenses, 'expense')

        # Pending revenues list
        rev_frame = tk.Frame(lists_frame, bg='white', relief=tk.RIDGE, bd=2)
        rev_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(rev_frame, text="💵 Receitas Pendentes",
                font=('Arial', 12, 'bold'), bg='white', fg='#28a745').pack(pady=10)

        self.create_transactions_list(rev_frame, pending_revenues, 'revenue')

        # Row 4: Warnings
        if projected_balance < 0:
            warning_frame = tk.Frame(self.scrollable_frame, bg='#fff3cd', relief=tk.RIDGE, bd=2)
            warning_frame.pack(fill=tk.X, padx=10, pady=10)

            tk.Label(warning_frame, text="⚠️", font=('Arial', 40), bg='#fff3cd').pack(pady=10)
            tk.Label(warning_frame, text="ATENÇÃO: Saldo Projetado Negativo!",
                    font=('Arial', 14, 'bold'), bg='#fff3cd', fg='#856404').pack()
            tk.Label(warning_frame,
                    text=f"O saldo ficará negativo em R$ {abs(projected_balance):,.2f} nos próximos {days} dias.",
                    font=('Arial', 11), bg='#fff3cd', fg='#856404').pack(pady=(5, 15))

        # Find critical dates (when balance goes negative)
        critical_dates = [p for p in projections if p['balance'] < 0]
        if critical_dates:
            first_negative = critical_dates[0]
            warning_frame2 = tk.Frame(self.scrollable_frame, bg='#f8d7da', relief=tk.RIDGE, bd=2)
            warning_frame2.pack(fill=tk.X, padx=10, pady=10)

            tk.Label(warning_frame2, text="🔴 Data Crítica",
                    font=('Arial', 12, 'bold'), bg='#f8d7da', fg='#721c24').pack(pady=10)
            tk.Label(warning_frame2,
                    text=f"O saldo ficará negativo pela primeira vez em {first_negative['date'].strftime('%d/%m/%Y')}",
                    font=('Arial', 10), bg='#f8d7da', fg='#721c24').pack(pady=(0, 10))

    def create_indicator_card(self, parent, title, value, color, col):
        """Cria um card de indicador"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=3)
        card.grid(row=0, column=col, padx=10, pady=10, sticky='nsew')
        parent.columnconfigure(col, weight=1)

        tk.Label(card, text=title, bg=color, fg='white',
                font=('Arial', 10, 'bold')).pack(pady=(15, 5))

        tk.Label(card, text=value, bg=color, fg='white',
                font=('Arial', 16, 'bold')).pack(pady=(5, 15))

        card.config(height=90)

    def get_total_balance(self):
        """Calcula saldo total de todas as contas"""
        try:
            sql = "SELECT SUM(saldo_atual) as total FROM contas_bancarias WHERE ativo = 1"
            result = self.db_manager.execute_query(sql)
            if result and result[0]['total']:
                return float(result[0]['total'])
            return 0.0
        except:
            return 0.0

    def get_pending_expenses(self, start_date, end_date):
        """Busca despesas pendentes"""
        try:
            sql = """
                SELECT d.data_vencimento as data, d.descricao, d.valor, f.nome as fornecedor
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE d.pago = 0
                  AND d.data_vencimento BETWEEN ? AND ?
                ORDER BY d.data_vencimento
            """
            return self.db_manager.execute_query(
                sql,
                [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
            )
        except:
            return []

    def get_pending_revenues(self, start_date, end_date):
        """Busca receitas pendentes"""
        try:
            sql = """
                SELECT r.data_vencimento as data, r.descricao, r.valor_total as valor, c.nome as cliente
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE r.pago = 0
                  AND r.data_vencimento BETWEEN ? AND ?
                ORDER BY r.data_vencimento
            """
            return self.db_manager.execute_query(
                sql,
                [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
            )
        except:
            return []

    def calculate_projections(self, initial_balance, expenses, revenues, start_date, end_date):
        """Calcula projeções diárias"""
        projections = []
        current_balance = initial_balance

        # Group transactions by date
        transactions_by_date = defaultdict(lambda: {'expenses': 0, 'revenues': 0})

        for exp in expenses:
            date = datetime.strptime(exp['data'], '%Y-%m-%d').date()
            transactions_by_date[date]['expenses'] += float(exp['valor'])

        for rev in revenues:
            date = datetime.strptime(rev['data'], '%Y-%m-%d').date()
            transactions_by_date[date]['revenues'] += float(rev['valor'])

        # Calculate daily balance
        current_date = start_date
        while current_date <= end_date:
            if current_date in transactions_by_date:
                trans = transactions_by_date[current_date]
                current_balance += trans['revenues'] - trans['expenses']

            projections.append({
                'date': current_date,
                'balance': current_balance,
                'expenses': transactions_by_date[current_date]['expenses'] if current_date in transactions_by_date else 0,
                'revenues': transactions_by_date[current_date]['revenues'] if current_date in transactions_by_date else 0
            })

            current_date += timedelta(days=1)

        return projections

    def create_projection_chart(self, parent, projections):
        """Cria gráfico de projeção"""
        chart_canvas = tk.Canvas(parent, bg='white', height=350)
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        if not projections:
            tk.Label(parent, text="Sem dados", bg='white',
                    font=('Arial', 10), fg='#999').pack(pady=50)
            return

        # Find min and max balance
        balances = [p['balance'] for p in projections]
        min_balance = min(balances)
        max_balance = max(balances)

        # Add padding
        balance_range = max_balance - min_balance
        if balance_range == 0:
            balance_range = abs(max_balance) if max_balance != 0 else 1000

        min_balance -= balance_range * 0.1
        max_balance += balance_range * 0.1

        # Chart dimensions
        chart_width = max(800, len(projections) * 3)
        chart_canvas.config(width=chart_width)

        x_start = 60
        y_top = 30
        y_bottom = 300
        chart_height = y_bottom - y_top

        # Draw zero line if applicable
        if min_balance < 0 < max_balance:
            zero_y = y_bottom - ((0 - min_balance) / (max_balance - min_balance)) * chart_height
            chart_canvas.create_line(
                x_start, zero_y, x_start + len(projections) * 3, zero_y,
                fill='#dc3545', width=2, dash=(5, 5)
            )
            chart_canvas.create_text(
                x_start - 10, zero_y, text='R$ 0',
                anchor='e', font=('Arial', 9), fill='#dc3545'
            )

        # Draw line
        points = []
        for i, proj in enumerate(projections):
            x = x_start + i * 3
            balance_norm = (proj['balance'] - min_balance) / (max_balance - min_balance)
            y = y_bottom - (balance_norm * chart_height)
            points.extend([x, y])

            # Mark negative points
            if proj['balance'] < 0:
                chart_canvas.create_oval(x-3, y-3, x+3, y+3, fill='#dc3545', outline='#dc3545')

        # Draw line
        if len(points) >= 4:
            chart_canvas.create_line(points, fill='#6610f2', width=2, smooth=True)

        # Draw axes labels
        num_labels = 5
        for i in range(num_labels):
            value = min_balance + (max_balance - min_balance) * (i / (num_labels - 1))
            y = y_bottom - (i / (num_labels - 1)) * chart_height
            chart_canvas.create_text(
                x_start - 10, y, text=f'R$ {value:,.0f}',
                anchor='e', font=('Arial', 8)
            )
            chart_canvas.create_line(x_start - 5, y, x_start, y, fill='#999')

        # Date labels (show every 7 days or so)
        step = max(1, len(projections) // 10)
        for i in range(0, len(projections), step):
            proj = projections[i]
            x = x_start + i * 3
            label = proj['date'].strftime('%d/%m')
            chart_canvas.create_text(
                x, y_bottom + 15, text=label,
                font=('Arial', 8), angle=0
            )

    def create_transactions_list(self, parent, transactions, trans_type):
        """Cria lista de transações"""
        # Scrollbars
        scroll_y = tk.Scrollbar(parent, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # TreeView
        columns = ['Data', 'Descrição', 'Fornecedor/Cliente', 'Valor']
        tree = ttk.Treeview(parent, columns=columns, show='headings',
                           height=10,
                           yscrollcommand=scroll_y.set,
                           xscrollcommand=scroll_x.set)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        # Configure columns
        tree.heading('Data', text='Data')
        tree.column('Data', width=100, anchor='center')

        tree.heading('Descrição', text='Descrição')
        tree.column('Descrição', width=200)

        if trans_type == 'expense':
            tree.heading('Fornecedor/Cliente', text='Fornecedor')
        else:
            tree.heading('Fornecedor/Cliente', text='Cliente')
        tree.column('Fornecedor/Cliente', width=150)

        tree.heading('Valor', text='Valor')
        tree.column('Valor', width=120, anchor='center')

        # Insert data
        for trans in transactions:
            date_str = datetime.strptime(trans['data'], '%Y-%m-%d').strftime('%d/%m/%Y')
            partner = trans.get('fornecedor') or trans.get('cliente') or 'N/A'
            value_str = f"R$ {float(trans['valor']):,.2f}"

            tree.insert('', tk.END, values=[
                date_str,
                trans['descricao'],
                partner,
                value_str
            ])

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Summary
        total = sum(float(t['valor']) for t in transactions)
        summary = tk.Label(parent, text=f"Total: R$ {total:,.2f}",
                          font=('Arial', 10, 'bold'), bg='white')
        summary.pack(pady=(0, 10))
