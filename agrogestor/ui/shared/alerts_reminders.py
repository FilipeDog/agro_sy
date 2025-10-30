# -*- coding: utf-8 -*-
"""
Sistema de Alertas e Lembretes
Notificações e tarefas pendentes
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class AlertsReminders:
    """Sistema de alertas e lembretes"""

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
        header = tk.Frame(self.parent, bg='#ff6b6b', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="🔔 ALERTAS E LEMBRETES",
                        bg='#ff6b6b', fg='white',
                        font=('Arial', 20, 'bold'))
        title.pack(pady=10)

        subtitle = tk.Label(header, text="Fique por dentro de tudo que precisa da sua atenção",
                           bg='#ff6b6b', fg='white',
                           font=('Arial', 11))
        subtitle.pack()

        # Summary frame
        summary_frame = tk.Frame(self.parent, bg='white', height=100)
        summary_frame.pack(fill=tk.X, padx=20, pady=20)
        summary_frame.pack_propagate(False)

        # Count alerts
        alerts_data = self.get_all_alerts()
        total_alerts = sum(len(alerts) for alerts in alerts_data.values())

        summary_container = tk.Frame(summary_frame, bg='white')
        summary_container.pack(expand=True)

        # Alert icon and count
        tk.Label(summary_container, text="⚠️", font=('Arial', 40), bg='white').pack(side=tk.LEFT, padx=20)

        count_frame = tk.Frame(summary_container, bg='white')
        count_frame.pack(side=tk.LEFT)

        tk.Label(count_frame, text=f"{total_alerts}",
                font=('Arial', 32, 'bold'), fg='#ff6b6b', bg='white').pack()
        tk.Label(count_frame, text="Alertas Ativos",
                font=('Arial', 12), fg='#666', bg='white').pack()

        # Refresh button
        refresh_btn = tk.Button(summary_container, text="🔄 Atualizar",
                               command=self.load_alerts,
                               font=('Arial', 11, 'bold'), bg='#17a2b8', fg='white',
                               relief=tk.FLAT, cursor='hand2', padx=20, pady=10)
        refresh_btn.pack(side=tk.LEFT, padx=30)

        # Main container with scrollbar
        main_container = tk.Frame(self.parent, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

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

        # Load alerts
        self.load_alerts()

    def get_all_alerts(self):
        """Coleta todos os alertas"""
        alerts = {
            'expenses': self.get_pending_expenses(),
            'revenues': self.get_pending_revenues(),
            'overdue_expenses': self.get_overdue_expenses(),
            'overdue_revenues': self.get_overdue_revenues(),
            'low_weight': self.get_animals_without_weight(),
            'no_applications': self.get_animals_without_applications()
        }
        return alerts

    def load_alerts(self):
        """Carrega e exibe alertas"""
        # Clear
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        alerts_data = self.get_all_alerts()

        # Overdue expenses
        if alerts_data['overdue_expenses']:
            self.create_alert_section(
                "🔴 DESPESAS VENCIDAS",
                f"{len(alerts_data['overdue_expenses'])} despesa(s) vencida(s) e não paga(s)",
                '#dc3545',
                alerts_data['overdue_expenses'],
                ['Data Venc.', 'Descrição', 'Fornecedor', 'Valor', 'Dias Vencido']
            )

        # Overdue revenues
        if alerts_data['overdue_revenues']:
            self.create_alert_section(
                "🔴 RECEITAS VENCIDAS",
                f"{len(alerts_data['overdue_revenues'])} receita(s) vencida(s) e não recebida(s)",
                '#dc3545',
                alerts_data['overdue_revenues'],
                ['Data Venc.', 'Descrição', 'Cliente', 'Valor', 'Dias Vencido']
            )

        # Upcoming expenses (next 7 days)
        if alerts_data['expenses']:
            self.create_alert_section(
                "🟡 DESPESAS A VENCER (próximos 7 dias)",
                f"{len(alerts_data['expenses'])} despesa(s) para pagar",
                '#ffc107',
                alerts_data['expenses'],
                ['Data Venc.', 'Descrição', 'Fornecedor', 'Valor', 'Dias até Venc.']
            )

        # Upcoming revenues (next 7 days)
        if alerts_data['revenues']:
            self.create_alert_section(
                "🟡 RECEITAS A RECEBER (próximos 7 dias)",
                f"{len(alerts_data['revenues'])} receita(s) para receber",
                '#ffc107',
                alerts_data['revenues'],
                ['Data Venc.', 'Descrição', 'Cliente', 'Valor', 'Dias até Rec.']
            )

        # Animals without recent weight
        if alerts_data['low_weight']:
            self.create_alert_section(
                "🟠 ANIMAIS SEM PESAGEM RECENTE",
                f"{len(alerts_data['low_weight'])} animal(is) sem pesagem há mais de 60 dias",
                '#ff8800',
                alerts_data['low_weight'],
                ['Brinco', 'Tipo', 'Status', 'Última Pesagem', 'Dias']
            )

        # Animals without applications
        if alerts_data['no_applications']:
            self.create_alert_section(
                "🟠 ANIMAIS SEM APLICAÇÕES RECENTES",
                f"{len(alerts_data['no_applications'])} animal(is) sem aplicações há mais de 90 dias",
                '#ff8800',
                alerts_data['no_applications'],
                ['Brinco', 'Tipo', 'Status', 'Última Aplicação', 'Dias']
            )

        # No alerts message
        if sum(len(alerts) for alerts in alerts_data.values()) == 0:
            no_alerts_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RIDGE, bd=2)
            no_alerts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            tk.Label(no_alerts_frame, text="✅",
                    font=('Arial', 60), bg='white').pack(pady=30)
            tk.Label(no_alerts_frame, text="Tudo em Ordem!",
                    font=('Arial', 18, 'bold'), bg='white', fg='#28a745').pack()
            tk.Label(no_alerts_frame, text="Não há alertas ou lembretes no momento.",
                    font=('Arial', 12), bg='white', fg='#666').pack(pady=10)

    def create_alert_section(self, title, subtitle, color, data, columns):
        """Cria uma seção de alertas"""
        section_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RIDGE, bd=2)
        section_frame.pack(fill=tk.X, padx=10, pady=10)

        # Header
        header = tk.Frame(section_frame, bg=color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text=title, bg=color, fg='white',
                font=('Arial', 14, 'bold')).pack(pady=(10, 0))
        tk.Label(header, text=subtitle, bg=color, fg='white',
                font=('Arial', 10)).pack(pady=(5, 10))

        # Table
        table_frame = tk.Frame(section_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # TreeView
        tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                           height=min(len(data), 5),
                           yscrollcommand=scroll_y.set,
                           xscrollcommand=scroll_x.set)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            if 'Data' in col or 'Dias' in col or 'Valor' in col:
                tree.column(col, width=120, anchor='center')
            else:
                tree.column(col, width=200)

        # Insert data
        for row in data:
            tree.insert('', tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True)

    def get_pending_expenses(self):
        """Busca despesas a vencer nos próximos 7 dias"""
        try:
            today = datetime.now().date()
            future = (datetime.now() + timedelta(days=7)).date()

            sql = """
                SELECT d.data_vencimento as data, d.descricao, f.nome, d.valor
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE d.pago = 0
                  AND d.data_vencimento BETWEEN ? AND ?
                ORDER BY d.data_vencimento
            """

            results = self.db_manager.execute_query(
                sql,
                [today.strftime('%Y-%m-%d'), future.strftime('%Y-%m-%d')]
            )

            formatted = []
            for row in results:
                date = datetime.strptime(row['data'], '%Y-%m-%d').date()
                days_until = (date - today).days

                formatted.append([
                    datetime.strptime(row['data'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    row['descricao'],
                    row['nome'] if row['nome'] else 'N/A',
                    f"R$ {float(row['valor']):,.2f}",
                    f"{days_until} dia(s)"
                ])

            return formatted
        except:
            return []

    def get_pending_revenues(self):
        """Busca receitas a receber nos próximos 7 dias"""
        try:
            today = datetime.now().date()
            future = (datetime.now() + timedelta(days=7)).date()

            sql = """
                SELECT r.data_vencimento as data, r.descricao, c.nome, r.valor_total
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE r.pago = 0
                  AND r.data_vencimento BETWEEN ? AND ?
                ORDER BY r.data_vencimento
            """

            results = self.db_manager.execute_query(
                sql,
                [today.strftime('%Y-%m-%d'), future.strftime('%Y-%m-%d')]
            )

            formatted = []
            for row in results:
                date = datetime.strptime(row['data'], '%Y-%m-%d').date()
                days_until = (date - today).days

                formatted.append([
                    datetime.strptime(row['data'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    row['descricao'],
                    row['nome'] if row['nome'] else 'N/A',
                    f"R$ {float(row['valor_total']):,.2f}",
                    f"{days_until} dia(s)"
                ])

            return formatted
        except:
            return []

    def get_overdue_expenses(self):
        """Busca despesas vencidas"""
        try:
            today = datetime.now().date()

            sql = """
                SELECT d.data_vencimento as data, d.descricao, f.nome, d.valor
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE d.pago = 0
                  AND d.data_vencimento < ?
                ORDER BY d.data_vencimento
            """

            results = self.db_manager.execute_query(sql, [today.strftime('%Y-%m-%d')])

            formatted = []
            for row in results:
                date = datetime.strptime(row['data'], '%Y-%m-%d').date()
                days_overdue = (today - date).days

                formatted.append([
                    datetime.strptime(row['data'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    row['descricao'],
                    row['nome'] if row['nome'] else 'N/A',
                    f"R$ {float(row['valor']):,.2f}",
                    f"{days_overdue} dia(s)"
                ])

            return formatted
        except:
            return []

    def get_overdue_revenues(self):
        """Busca receitas vencidas"""
        try:
            today = datetime.now().date()

            sql = """
                SELECT r.data_vencimento as data, r.descricao, c.nome, r.valor_total
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE r.pago = 0
                  AND r.data_vencimento < ?
                ORDER BY r.data_vencimento
            """

            results = self.db_manager.execute_query(sql, [today.strftime('%Y-%m-%d')])

            formatted = []
            for row in results:
                date = datetime.strptime(row['data'], '%Y-%m-%d').date()
                days_overdue = (today - date).days

                formatted.append([
                    datetime.strptime(row['data'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    row['descricao'],
                    row['nome'] if row['nome'] else 'N/A',
                    f"R$ {float(row['valor_total']):,.2f}",
                    f"{days_overdue} dia(s)"
                ])

            return formatted
        except:
            return []

    def get_animals_without_weight(self):
        """Busca animais sem pesagem recente (60 dias)"""
        try:
            sql = """
                SELECT a.brinco, t.nome as tipo, s.nome as status,
                       MAX(p.data_pesagem) as ultima_pesagem
                FROM animais a
                LEFT JOIN tipo_animal t ON a.tipo_id = t.id
                LEFT JOIN status_animal s ON a.status_id = s.id
                LEFT JOIN controle_peso p ON a.id = p.animal_id
                WHERE s.nome NOT IN ('Vendido', 'Morto')
                GROUP BY a.id
                HAVING ultima_pesagem IS NULL OR ultima_pesagem < date('now', '-60 days')
                ORDER BY ultima_pesagem
                LIMIT 20
            """

            results = self.db_manager.execute_query(sql)

            formatted = []
            for row in results:
                if row['ultima_pesagem']:
                    try:
                        date = datetime.strptime(row['ultima_pesagem'], '%Y-%m-%d').date()
                        days_ago = (datetime.now().date() - date).days
                        last_weight = date.strftime('%d/%m/%Y')
                    except:
                        last_weight = 'N/A'
                        days_ago = '-'
                else:
                    last_weight = 'Nunca'
                    days_ago = '-'

                formatted.append([
                    row['brinco'],
                    row['tipo'] or 'N/A',
                    row['status'] or 'N/A',
                    last_weight,
                    f"{days_ago} dia(s)" if days_ago != '-' else '-'
                ])

            return formatted
        except:
            return []

    def get_animals_without_applications(self):
        """Busca animais sem aplicações recentes (90 dias)"""
        try:
            sql = """
                SELECT a.brinco, t.nome as tipo, s.nome as status,
                       MAX(ap.data_aplicacao) as ultima_aplicacao
                FROM animais a
                LEFT JOIN tipo_animal t ON a.tipo_id = t.id
                LEFT JOIN status_animal s ON a.status_id = s.id
                LEFT JOIN aplicacoes ap ON a.id = ap.animal_id
                WHERE s.nome NOT IN ('Vendido', 'Morto')
                GROUP BY a.id
                HAVING ultima_aplicacao IS NULL OR ultima_aplicacao < date('now', '-90 days')
                ORDER BY ultima_aplicacao
                LIMIT 20
            """

            results = self.db_manager.execute_query(sql)

            formatted = []
            for row in results:
                if row['ultima_aplicacao']:
                    try:
                        date = datetime.strptime(row['ultima_aplicacao'], '%Y-%m-%d').date()
                        days_ago = (datetime.now().date() - date).days
                        last_app = date.strftime('%d/%m/%Y')
                    except:
                        last_app = 'N/A'
                        days_ago = '-'
                else:
                    last_app = 'Nunca'
                    days_ago = '-'

                formatted.append([
                    row['brinco'],
                    row['tipo'] or 'N/A',
                    row['status'] or 'N/A',
                    last_app,
                    f"{days_ago} dia(s)" if days_ago != '-' else '-'
                ])

            return formatted
        except:
            return []
