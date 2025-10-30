# -*- coding: utf-8 -*-
"""
Busca Global do Sistema
Permite buscar em todos os módulos com Ctrl+F
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class GlobalSearch:
    """Janela de busca global"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.window = None

    def show(self):
        """Mostra janela de busca"""
        if self.window and self.window.winfo_exists():
            self.window.focus()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("🔍 Busca Global - Pesquisar em Todo o Sistema")
        self.window.geometry("1000x600")

        # Header
        header = tk.Frame(self.window, bg='#0078d7', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="🔍 BUSCA GLOBAL",
                        bg='#0078d7', fg='white',
                        font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        subtitle = tk.Label(header, text="Digite para buscar em: Animais, Clientes, Fornecedores, Funcionários, Despesas e Receitas",
                           bg='#0078d7', fg='white',
                           font=('Arial', 10))
        subtitle.pack()

        # Search frame
        search_frame = tk.Frame(self.window, bg='white', height=80)
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        search_frame.pack_propagate(False)

        # Search entry (large)
        search_container = tk.Frame(search_frame, bg='white')
        search_container.pack(expand=True)

        tk.Label(search_container, text="🔍", font=('Arial', 20), bg='white').pack(side=tk.LEFT, padx=10)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.perform_search())

        self.search_entry = tk.Entry(search_container, textvariable=self.search_var,
                               font=('Arial', 14), width=60, relief=tk.FLAT,
                               bg='#f5f5f5')
        self.search_entry.pack(side=tk.LEFT, ipady=8, padx=5)
        self.search_entry.focus()

        # Bind Enter key to perform search
        self.search_entry.bind('<Return>', lambda e: self.perform_search())

        # Search button
        search_btn = tk.Button(search_container, text="🔍 Buscar",
                             command=self.perform_search,
                             font=('Arial', 10), bg='#28a745', fg='white',
                             relief=tk.FLAT, cursor='hand2', padx=15, pady=5)
        search_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        clear_btn = tk.Button(search_container, text="✕ Limpar",
                             command=self.clear_search,
                             font=('Arial', 10), bg='#dc3545', fg='white',
                             relief=tk.FLAT, cursor='hand2', padx=15, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=10)

        # Results count
        self.results_label = tk.Label(self.window, text="Digite algo para buscar...",
                                     font=('Arial', 10), fg='#666')
        self.results_label.pack(pady=(0, 10))

        # Notebook for categories
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Create tabs
        self.tabs = {}
        self.trees = {}

        categories = [
            ('animals', '🐄 Animais',
             ['ID', 'Brinco', 'Lote', 'Tipo', 'Sexo', 'Raça', 'Status']),
            ('clients', '👥 Clientes',
             ['ID', 'Nome', 'CPF/CNPJ', 'Telefone', 'Cidade']),
            ('suppliers', '🏪 Fornecedores',
             ['ID', 'Nome', 'CNPJ/CPF', 'Telefone', 'Cidade']),
            ('employees', '👔 Funcionários',
             ['ID', 'Nome', 'CPF', 'Cargo', 'Telefone']),
            ('expenses', '💰 Despesas',
             ['ID', 'Data', 'Descrição', 'Fornecedor', 'Valor', 'Pago']),
            ('revenues', '💵 Receitas',
             ['ID', 'Data', 'Descrição', 'Cliente', 'Valor', 'Recebido'])
        ]

        for key, title, columns in categories:
            self.create_tab(key, title, columns)

        # Footer
        footer = tk.Frame(self.window, bg='#f8f9fa', height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        footer_text = tk.Label(footer,
                              text="💡 Dica: Clique duas vezes em um resultado para abrir o registro | ESC para fechar",
                              bg='#f8f9fa', fg='#666', font=('Arial', 9))
        footer_text.pack(pady=10)

        # Keyboard shortcuts
        self.window.bind('<Escape>', lambda e: self.window.destroy())
        self.window.bind('<Control-w>', lambda e: self.window.destroy())

    def create_tab(self, key, title, columns):
        """Cria uma aba de resultados"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        self.tabs[key] = frame

        # Scrollbars
        scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # TreeView
        tree = ttk.Treeview(frame, columns=columns, show='headings',
                           yscrollcommand=scroll_y.set,
                           xscrollcommand=scroll_x.set)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            if col == 'ID':
                tree.column(col, width=50, anchor='center')
            elif col in ['Valor', 'Pago', 'Recebido']:
                tree.column(col, width=100, anchor='center')
            elif col in ['Data']:
                tree.column(col, width=100, anchor='center')
            else:
                tree.column(col, width=150)

        tree.pack(fill=tk.BOTH, expand=True)

        # Bind double click
        tree.bind('<Double-1>', lambda e: self.open_record(key))

        self.trees[key] = tree

    def clear_search(self):
        """Limpa busca"""
        self.search_var.set('')
        for tree in self.trees.values():
            tree.delete(*tree.get_children())
        self.results_label.config(text="Digite algo para buscar...")

    def perform_search(self):
        """Executa busca em tempo real"""
        query = self.search_var.get().strip()

        if len(query) < 2:
            self.clear_search()
            return

        # Clear all trees
        for tree in self.trees.values():
            tree.delete(*tree.get_children())

        total_results = 0

        # Search in each category
        total_results += self.search_animals(query)
        total_results += self.search_clients(query)
        total_results += self.search_suppliers(query)
        total_results += self.search_employees(query)
        total_results += self.search_expenses(query)
        total_results += self.search_revenues(query)

        # Update results label
        if total_results == 0:
            self.results_label.config(text=f"❌ Nenhum resultado encontrado para '{query}'",
                                     fg='#dc3545')
        else:
            self.results_label.config(text=f"✓ {total_results} resultado(s) encontrado(s) para '{query}'",
                                     fg='#28a745')

    def search_animals(self, query):
        """Busca em animais"""
        try:
            sql = """
                SELECT a.id, a.brinco, a.lote, t.nome as tipo, a.sexo, r.nome as raca, s.nome as status
                FROM animais a
                LEFT JOIN tipo_animal t ON a.tipo_id = t.id
                LEFT JOIN raca r ON a.raca_id = r.id
                LEFT JOIN status_animal s ON a.status_id = s.id
                WHERE LOWER(a.brinco) LIKE ?
                   OR LOWER(a.lote) LIKE ?
                   OR LOWER(t.nome) LIKE ?
                   OR LOWER(r.nome) LIKE ?
                LIMIT 100
            """
            pattern = f'%{query.lower()}%'
            results = self.db_manager.execute_query(sql, [pattern, pattern, pattern, pattern])

            tree = self.trees['animals']
            for row in results:
                tree.insert('', tk.END, values=row)

            return len(results)
        except:
            return 0

    def search_clients(self, query):
        """Busca em clientes"""
        try:
            sql = """
                SELECT id, nome, cpf_cnpj, telefone, cidade
                FROM clientes
                WHERE LOWER(nome) LIKE ?
                   OR LOWER(cpf_cnpj) LIKE ?
                   OR LOWER(telefone) LIKE ?
                LIMIT 100
            """
            pattern = f'%{query.lower()}%'
            results = self.db_manager.execute_query(sql, [pattern, pattern, pattern])

            tree = self.trees['clients']
            for row in results:
                tree.insert('', tk.END, values=row)

            return len(results)
        except:
            return 0

    def search_suppliers(self, query):
        """Busca em fornecedores"""
        try:
            sql = """
                SELECT id, nome, cpf_cnpj, telefone, cidade
                FROM fornecedores
                WHERE LOWER(nome) LIKE ?
                   OR LOWER(cpf_cnpj) LIKE ?
                   OR LOWER(telefone) LIKE ?
                LIMIT 100
            """
            pattern = f'%{query.lower()}%'
            results = self.db_manager.execute_query(sql, [pattern, pattern, pattern])

            tree = self.trees['suppliers']
            for row in results:
                tree.insert('', tk.END, values=row)

            return len(results)
        except:
            return 0

    def search_employees(self, query):
        """Busca em funcionários"""
        try:
            sql = """
                SELECT id, nome, cpf, cargo, telefone
                FROM funcionarios
                WHERE LOWER(nome) LIKE ?
                   OR LOWER(cpf) LIKE ?
                   OR LOWER(cargo) LIKE ?
                LIMIT 100
            """
            pattern = f'%{query.lower()}%'
            results = self.db_manager.execute_query(sql, [pattern, pattern, pattern])

            tree = self.trees['employees']
            for row in results:
                tree.insert('', tk.END, values=row)

            return len(results)
        except:
            return 0

    def search_expenses(self, query):
        """Busca em despesas"""
        try:
            sql = """
                SELECT d.id, d.data_gasto as data, d.descricao, f.nome as fornecedor, d.valor,
                       CASE WHEN d.pago = 1 THEN 'Sim' ELSE 'Não' END as pago
                FROM despesas d
                LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
                WHERE LOWER(d.descricao) LIKE ?
                   OR LOWER(f.nome) LIKE ?
                ORDER BY d.data_gasto DESC
                LIMIT 100
            """
            pattern = f'%{query.lower()}%'
            results = self.db_manager.execute_query(sql, [pattern, pattern])

            tree = self.trees['expenses']
            for row in results:
                # Format date and value
                formatted_row = list(row)
                if formatted_row[1]:
                    try:
                        date_obj = datetime.strptime(formatted_row[1], '%Y-%m-%d')
                        formatted_row[1] = date_obj.strftime('%d/%m/%Y')
                    except:
                        pass
                if formatted_row[4]:
                    formatted_row[4] = f'R$ {float(formatted_row[4]):,.2f}'

                tree.insert('', tk.END, values=formatted_row)

            return len(results)
        except:
            return 0

    def search_revenues(self, query):
        """Busca em receitas"""
        try:
            sql = """
                SELECT r.id, r.data_venda as data, r.descricao, c.nome as cliente, r.valor_total,
                       CASE WHEN r.pago = 1 THEN 'Sim' ELSE 'Não' END as recebido
                FROM receitas r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                WHERE LOWER(r.descricao) LIKE ?
                   OR LOWER(c.nome) LIKE ?
                ORDER BY r.data_venda DESC
                LIMIT 100
            """
            pattern = f'%{query.lower()}%'
            results = self.db_manager.execute_query(sql, [pattern, pattern])

            tree = self.trees['revenues']
            for row in results:
                # Format date and value
                formatted_row = list(row)
                if formatted_row[1]:
                    try:
                        date_obj = datetime.strptime(formatted_row[1], '%Y-%m-%d')
                        formatted_row[1] = date_obj.strftime('%d/%m/%Y')
                    except:
                        pass
                if formatted_row[4]:
                    formatted_row[4] = f'R$ {float(formatted_row[4]):,.2f}'

                tree.insert('', tk.END, values=formatted_row)

            return len(results)
        except:
            return 0

    def open_record(self, category):
        """Abre o registro selecionado no módulo apropriado"""
        tree = self.trees[category]
        selection = tree.selection()

        if not selection:
            return

        item = tree.item(selection[0])
        record_id = item['values'][0]

        # Show message (in real implementation, would open the actual module)
        category_names = {
            'animals': 'Animais',
            'clients': 'Clientes',
            'suppliers': 'Fornecedores',
            'employees': 'Funcionários',
            'expenses': 'Despesas',
            'revenues': 'Receitas'
        }

        messagebox.showinfo("Abrir Registro",
                           f"Abrindo {category_names[category]} - ID: {record_id}\n\n"
                           "Funcionalidade de navegação será implementada em breve!")
