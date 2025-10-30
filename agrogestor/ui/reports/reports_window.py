"""
Janela de Relatórios
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class ReportsWindow:
    """Janela de relatórios"""

    def __init__(self, parent, db_manager, report_type):
        self.parent = parent
        self.db_manager = db_manager
        self.report_type = report_type

        self.create_widgets()
        self.load_report()

    def create_widgets(self):
        """Cria interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(
            title_frame,
            text=f"Relatório: {self.get_report_title()}",
            font=("Helvetica", 16, "bold")
        ).pack(side=LEFT)

        # Filtros
        filter_frame = ttk.LabelFrame(main_container, text="Filtros", padding=10)
        filter_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(filter_frame, text="Data Início:").pack(side=LEFT, padx=5)
        self.data_inicio = ttk.Entry(filter_frame, width=12)
        self.data_inicio.pack(side=LEFT, padx=5)

        ttk.Label(filter_frame, text="Data Fim:").pack(side=LEFT, padx=5)
        self.data_fim = ttk.Entry(filter_frame, width=12)
        self.data_fim.pack(side=LEFT, padx=5)

        ttk.Button(filter_frame, text="Filtrar", command=self.load_report).pack(side=LEFT, padx=10)
        ttk.Button(filter_frame, text="Exportar Excel", command=self.export_excel).pack(side=LEFT, padx=5)

        # Tabela
        table_frame = ttk.Frame(main_container)
        table_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            table_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def get_report_title(self):
        """Retorna título do relatório"""
        titles = {
            'animais': 'Todos os Animais',
            'animais_status': 'Animais por Status',
            'animais_raca': 'Animais por Raça',
            'animais_pasto': 'Animais por Pasto',
            'animais_tipo': 'Animais por Tipo',
            'clientes': 'Clientes',
            'fornecedores': 'Fornecedores',
            'despesas_fornecedor': 'Despesas por Fornecedor',
            'despesas_mes': 'Despesas por Mês',
            'receitas_cliente': 'Receitas por Cliente',
            'receitas_tipo': 'Receitas por Tipo',
            'aplicacoes_mes': 'Aplicações por Mês',
            'inseminacoes_mes': 'Inseminações por Mês',
            'pesagens_mes': 'Pesagens por Mês',
            'mortes_mes': 'Mortes por Mês',
            'resultado_financeiro': 'Resultado Financeiro (Despesas vs Receitas)'
        }
        return titles.get(self.report_type, 'Relatório')

    def load_report(self):
        """Carrega dados do relatório"""
        # Verificar se tree foi criado
        if not hasattr(self, 'tree'):
            return

        # Limpar árvore
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Buscar dados baseado no tipo
        if self.report_type == 'animais':
            self.load_animals_report()
        elif self.report_type == 'animais_status':
            self.load_animals_by_status()
        elif self.report_type == 'animais_raca':
            self.load_animals_by_race()
        elif self.report_type == 'animais_pasto':
            self.load_animals_by_pasto()
        elif self.report_type == 'animais_tipo':
            self.load_animals_by_type()
        elif self.report_type == 'clientes':
            self.load_clients_report()
        elif self.report_type == 'fornecedores':
            self.load_suppliers_report()
        elif self.report_type == 'despesas_fornecedor':
            self.load_expenses_by_supplier()
        elif self.report_type == 'despesas_mes':
            self.load_expenses_by_month()
        elif self.report_type == 'receitas_cliente':
            self.load_revenues_by_client()
        elif self.report_type == 'receitas_tipo':
            self.load_revenues_by_type()
        elif self.report_type == 'aplicacoes_mes':
            self.load_applications_by_month()
        elif self.report_type == 'inseminacoes_mes':
            self.load_inseminations_by_month()
        elif self.report_type == 'pesagens_mes':
            self.load_weighings_by_month()
        elif self.report_type == 'mortes_mes':
            self.load_deaths_by_month()
        elif self.report_type == 'resultado_financeiro':
            self.load_financial_result()
        else:
            messagebox.showinfo("Info", "Relatório em desenvolvimento")

    def load_animals_report(self):
        """Relatório de animais"""
        self.tree['columns'] = ("Brinco", "Tipo", "Sexo", "Raça", "Status", "Pasto", "Peso", "Data Nasc.")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        animals = self.db_manager.get_all_animals()

        for animal in animals:
            values = (
                animal['brinco'],
                animal['tipo_nome'] or '',
                animal['sexo'] or '',
                animal['raca_nome'] or '',
                animal['status_nome'] or '',
                animal['pasto_nome'] or '',
                f"{animal['peso_atual']:.1f}" if animal['peso_atual'] else '',
                animal['data_nascimento'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_animals_by_status(self):
        """Animais por status"""
        self.tree['columns'] = ("Status", "Quantidade")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT s.nome as status, COUNT(a.id) as quantidade
            FROM status_animal s
            LEFT JOIN animais a ON a.status_id = s.id
            GROUP BY s.id, s.nome
            ORDER BY quantidade DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            self.tree.insert('', END, values=(row['status'], row['quantidade']))

    def load_animals_by_race(self):
        """Animais por raça"""
        self.tree['columns'] = ("Raça", "Quantidade")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT r.nome as raca, COUNT(a.id) as quantidade
            FROM raca r
            LEFT JOIN animais a ON a.raca_id = r.id
            GROUP BY r.id, r.nome
            ORDER BY quantidade DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            self.tree.insert('', END, values=(row['raca'], row['quantidade']))

    def load_clients_report(self):
        """Relatório de clientes"""
        self.tree['columns'] = ("Nome", "CPF/CNPJ", "Telefone", "Cidade", "UF")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        clients = self.db_manager.select('clientes', where_clause='ativo = 1', order_by='nome')

        for client in clients:
            values = (
                client['nome'],
                client['cpf_cnpj'] or '',
                client['telefone'] or '',
                client['cidade'] or '',
                client['uf'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_suppliers_report(self):
        """Relatório de fornecedores"""
        self.tree['columns'] = ("Nome", "CPF/CNPJ", "Telefone", "Cidade", "UF")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        suppliers = self.db_manager.select('fornecedores', where_clause='ativo = 1', order_by='nome')

        for supplier in suppliers:
            values = (
                supplier['nome'],
                supplier['cpf_cnpj'] or '',
                supplier['telefone'] or '',
                supplier['cidade'] or '',
                supplier['uf'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_expenses_by_month(self):
        """Despesas por mês"""
        self.tree['columns'] = ("Mês/Ano", "Total Despesas")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT strftime('%m/%Y', data_gasto) as mes, SUM(valor) as total
            FROM despesas
            GROUP BY strftime('%m/%Y', data_gasto)
            ORDER BY data_gasto DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            self.tree.insert('', END, values=(row['mes'], f"R$ {row['total']:,.2f}"))

    def load_revenues_by_client(self):
        """Receitas por cliente"""
        self.tree['columns'] = ("Cliente", "Total Vendas", "Qtd Vendas")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT c.nome, SUM(r.valor_total) as total, COUNT(r.id) as qtd
            FROM receitas r
            LEFT JOIN clientes c ON r.cliente_id = c.id
            GROUP BY c.nome
            ORDER BY total DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            nome = row['nome'] if row['nome'] else 'Sem Cliente'
            self.tree.insert('', END, values=(nome, f"R$ {row['total']:,.2f}", row['qtd']))

    def load_animals_by_pasto(self):
        """Animais por pasto"""
        self.tree['columns'] = ("Pasto", "Quantidade")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT p.nome as pasto, COUNT(a.id) as quantidade
            FROM pastos p
            LEFT JOIN animais a ON a.pasto_id = p.id
            GROUP BY p.id, p.nome
            ORDER BY quantidade DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            pasto = row['pasto'] if row['pasto'] else 'Sem Pasto'
            self.tree.insert('', END, values=(pasto, row['quantidade']))

    def load_animals_by_type(self):
        """Animais por tipo"""
        self.tree['columns'] = ("Tipo", "Quantidade")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT t.nome as tipo, COUNT(a.id) as quantidade
            FROM tipo_animal t
            LEFT JOIN animais a ON a.tipo_id = t.id
            GROUP BY t.id, t.nome
            ORDER BY quantidade DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            self.tree.insert('', END, values=(row['tipo'], row['quantidade']))

    def load_expenses_by_supplier(self):
        """Despesas por fornecedor"""
        self.tree['columns'] = ("Fornecedor", "Total Despesas", "Qtd Compras")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT f.nome, SUM(d.valor) as total, COUNT(d.id) as qtd
            FROM despesas d
            LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
            GROUP BY f.nome
            ORDER BY total DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            nome = row['nome'] if row['nome'] else 'Sem Fornecedor'
            total = row['total'] or 0
            self.tree.insert('', END, values=(nome, f"R$ {total:,.2f}", row['qtd']))

    def load_revenues_by_type(self):
        """Receitas por tipo"""
        self.tree['columns'] = ("Tipo Receita", "Total", "Qtd Vendas")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT t.nome, SUM(r.valor_total) as total, COUNT(r.id) as qtd
            FROM receitas r
            LEFT JOIN tipo_receita t ON r.tipo_receita_id = t.id
            GROUP BY t.nome
            ORDER BY total DESC
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            nome = row['nome'] if row['nome'] else 'Sem Tipo'
            total = row['total'] or 0
            self.tree.insert('', END, values=(nome, f"R$ {total:,.2f}", row['qtd']))

    def load_applications_by_month(self):
        """Aplicações por mês"""
        self.tree['columns'] = ("Mês/Ano", "Quantidade")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT strftime('%m/%Y', data_aplicacao) as mes,
                   COUNT(id) as quantidade
            FROM aplicacoes
            GROUP BY strftime('%m/%Y', data_aplicacao)
            ORDER BY data_aplicacao DESC
        """

        try:
            results = self.db_manager.execute_query(sql)
            for row in results:
                self.tree.insert('', END, values=(row['mes'], row['quantidade']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar aplicações: {str(e)}")

    def load_inseminations_by_month(self):
        """Inseminações por mês"""
        self.tree['columns'] = ("Mês/Ano", "Quantidade")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT strftime('%m/%Y', data_inseminacao) as mes,
                   COUNT(id) as quantidade
            FROM inseminacoes
            GROUP BY strftime('%m/%Y', data_inseminacao)
            ORDER BY data_inseminacao DESC
        """

        try:
            results = self.db_manager.execute_query(sql)
            for row in results:
                self.tree.insert('', END, values=(row['mes'], row['quantidade']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar inseminações: {str(e)}")

    def load_weighings_by_month(self):
        """Pesagens por mês"""
        self.tree['columns'] = ("Mês/Ano", "Quantidade", "Peso Médio")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT strftime('%m/%Y', data_pesagem) as mes,
                   COUNT(id) as quantidade,
                   AVG(peso) as peso_medio
            FROM controle_peso
            GROUP BY strftime('%m/%Y', data_pesagem)
            ORDER BY data_pesagem DESC
        """

        try:
            results = self.db_manager.execute_query(sql)
            for row in results:
                peso = row['peso_medio'] or 0
                self.tree.insert('', END, values=(row['mes'], row['quantidade'], f"{peso:.1f} kg"))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar pesagens: {str(e)}")

    def load_deaths_by_month(self):
        """Mortes por mês"""
        self.tree['columns'] = ("Mês/Ano", "Quantidade", "Motivo Principal")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        sql = """
            SELECT strftime('%m/%Y', a.data_morte) as mes,
                   COUNT(a.id) as quantidade,
                   cm.nome as motivo
            FROM animais a
            LEFT JOIN causa_morte cm ON a.causa_morte_id = cm.id
            WHERE a.data_morte IS NOT NULL
            GROUP BY strftime('%m/%Y', a.data_morte), cm.nome
            ORDER BY a.data_morte DESC
        """

        try:
            results = self.db_manager.execute_query(sql)
            for row in results:
                motivo = row['motivo'] if row['motivo'] else 'Diversos'
                self.tree.insert('', END, values=(row['mes'], row['quantidade'], motivo))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar mortes: {str(e)}")

    def load_financial_result(self):
        """Resultado financeiro"""
        self.tree['columns'] = ("Mês/Ano", "Despesas", "Receitas", "Resultado")
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

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
        """

        results = self.db_manager.execute_query(sql)

        for row in results:
            despesas = row['despesas'] or 0
            receitas = row['receitas'] or 0
            resultado = receitas - despesas
            self.tree.insert('', END, values=(
                row['mes'],
                f"R$ {despesas:,.2f}",
                f"R$ {receitas:,.2f}",
                f"R$ {resultado:,.2f}"
            ))

    def export_excel(self):
        """Exporta para Excel"""
        try:
            import openpyxl
            from openpyxl import Workbook

            # Criar workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Relatório"

            # Cabeçalhos
            headers = list(self.tree['columns'])
            ws.append(headers)

            # Dados
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                ws.append(values)

            # Salvar
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )

            if filename:
                wb.save(filename)
                messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filename}")

        except ImportError:
            messagebox.showerror("Erro", "Biblioteca openpyxl não instalada!\nInstale com: pip install openpyxl")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
