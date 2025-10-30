"""
Lançamento de Despesas
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


class ExpensesWindow:
    """Janela de lançamento de despesas"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        # Inicializar dicionários para evitar erros
        self.tipo_data = {}
        self.fornecedor_data = {}
        self.conta_data = {}

        self.create_widgets()
        self.load_combo_data()
        self.load_expenses()

    def create_widgets(self):
        """Cria os widgets da interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(title_frame, text="Lançamento de Despesas", font=("Helvetica", 16, "bold")).pack(side=LEFT)

        # Frame dividido
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Formulário
        form_frame = ttk.LabelFrame(content_frame, text="Dados da Despesa", padding=20)
        form_frame.pack(side=TOP, fill=X, pady=(0, 10))

        row = 0
        # Tipo de Despesa
        ttk.Label(form_frame, text="Tipo de Despesa:*").grid(row=row, column=0, sticky=W, pady=5)
        self.tipo_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.tipo_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Fornecedor
        ttk.Label(form_frame, text="Fornecedor:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.fornecedor_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.fornecedor_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        # Descrição
        ttk.Label(form_frame, text="Descrição:").grid(row=row, column=0, sticky=W, pady=5)
        self.descricao_entry = ttk.Entry(form_frame, width=60)
        self.descricao_entry.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        row += 1
        # Valor
        ttk.Label(form_frame, text="Valor:*").grid(row=row, column=0, sticky=W, pady=5)
        self.valor_entry = ttk.Entry(form_frame, width=20)
        self.valor_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Data do Gasto
        ttk.Label(form_frame, text="Data do Gasto:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_gasto_entry = ttk.Entry(form_frame, width=15)
        self.data_gasto_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.data_gasto_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        # Conta Bancária
        ttk.Label(form_frame, text="Conta/Caixa:").grid(row=row, column=0, sticky=W, pady=5)
        self.conta_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.conta_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Data do Pagamento
        ttk.Label(form_frame, text="Data Pagamento:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_pgto_entry = ttk.Entry(form_frame, width=15)
        self.data_pgto_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        # Pago
        self.pago_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Já foi pago?", variable=self.pago_var,
                       command=self.on_pago_changed).grid(row=row, column=0, sticky=W, pady=5)

        # Parcelar
        self.parcelar_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Parcelar?", variable=self.parcelar_var,
                       command=self.on_parcelar_changed).grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Número de Parcelas
        ttk.Label(form_frame, text="Nº Parcelas:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.num_parcelas_entry = ttk.Entry(form_frame, width=10, state=DISABLED)
        self.num_parcelas_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.num_parcelas_entry.insert(0, "2")

        row += 1
        # Adicionar ao Inventário
        self.add_inventario_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Adicionar ao Inventário 📦", variable=self.add_inventario_var,
                       command=self.on_inventario_changed).grid(row=row, column=0, columnspan=2, sticky=W, pady=5)

        # Quantidade
        ttk.Label(form_frame, text="Quantidade:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.quantidade_entry = ttk.Entry(form_frame, width=10, state=DISABLED)
        self.quantidade_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        # Unidade
        ttk.Label(form_frame, text="Unidade:").grid(row=row, column=0, sticky=W, pady=5)
        self.unidade_combo = ttk.Combobox(form_frame, width=15, state=DISABLED,
                                         values=["kg", "L", "unidade", "saco", "caixa", "m", "m²", "m³"])
        self.unidade_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.unidade_combo.set("kg")

        # Categoria do Item
        ttk.Label(form_frame, text="Categoria:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.categoria_combo = ttk.Combobox(form_frame, width=20, state=DISABLED,
                                           values=["Medicamentos", "Insumos", "Ferramentas", "Equipamentos", "Alimentos", "Outros"])
        self.categoria_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.categoria_combo.set("Insumos")

        row += 1
        # Observações
        ttk.Label(form_frame, text="Observações:").grid(row=row, column=0, sticky=W+N, pady=5)
        self.obs_text = tk.Text(form_frame, height=3, width=60)
        self.obs_text.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        # Botões
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(buttons_frame, text="Novo (Ctrl+N)", command=self.clear_form, width=15).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Salvar (Ctrl+S)", command=self.save_expense, width=15).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Excluir (Del)", command=self.delete_expense, width=15).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Marcar como Pago", command=self.mark_as_paid, width=15).pack(side=LEFT, padx=5)

        # Lista
        list_frame = ttk.LabelFrame(content_frame, text="Despesas Lançadas", padding=20)
        list_frame.pack(side=TOP, fill=BOTH, expand=YES)

        # Filtros
        filter_frame = ttk.Frame(list_frame)
        filter_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(filter_frame, text="Período:").pack(side=LEFT, padx=5)
        self.data_inicio_entry = ttk.Entry(filter_frame, width=12)
        self.data_inicio_entry.pack(side=LEFT, padx=5)
        ttk.Label(filter_frame, text="até").pack(side=LEFT, padx=5)
        self.data_fim_entry = ttk.Entry(filter_frame, width=12)
        self.data_fim_entry.pack(side=LEFT, padx=5)

        ttk.Label(filter_frame, text="Status:").pack(side=LEFT, padx=(20, 5))
        self.status_combo = ttk.Combobox(filter_frame, width=15, state="readonly", values=["Todos", "Em Aberto", "Pagos"])
        self.status_combo.set("Todos")
        self.status_combo.pack(side=LEFT, padx=5)

        ttk.Button(filter_frame, text="Filtrar", command=self.load_expenses).pack(side=LEFT, padx=5)

        # Tabela
        table_frame = ttk.Frame(list_frame)
        table_frame.pack(fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Data", "Tipo", "Fornecedor", "Descrição", "Valor", "Pagamento", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_h.set)
        scrollbar.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col in ["Data", "Valor", "Pagamento", "Status"]:
                self.tree.column(col, width=100, anchor=CENTER)
            else:
                self.tree.column(col, width=150)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_selected())

        # Atalhos de teclado
        self.parent.bind('<Control-n>', lambda e: self.clear_form())
        self.parent.bind('<Control-s>', lambda e: self.save_expense())
        self.parent.bind('<Control-e>', lambda e: self.edit_selected())
        self.parent.bind('<Delete>', lambda e: self.delete_expense())

        # Carregar dados dos comboboxes na inicialização
        self.load_combo_data()

    def load_combo_data(self):
        """Carrega dados dos comboboxes"""
        try:
            # Tipos de Despesa
            tipos = self.db_manager.select('tipo_despesa', order_by='nome')
            tipo_values = [t['nome'] for t in tipos]
            self.tipo_combo['values'] = tipo_values
            self.tipo_data = {t['nome']: t['id'] for t in tipos}

            # Fornecedores
            fornecedores = self.db_manager.select('fornecedores', where_clause='ativo = 1', order_by='nome')
            fornecedor_values = [''] + [f['nome'] for f in fornecedores]
            self.fornecedor_combo['values'] = fornecedor_values
            self.fornecedor_data = {f['nome']: f['id'] for f in fornecedores}

            # Contas Bancárias / Caixa
            contas = self.db_manager.select('contas_bancarias', where_clause='ativo = 1', order_by='nome_conta')
            conta_values = [''] + [c['nome_conta'] for c in contas]
            self.conta_combo['values'] = conta_values
            self.conta_data = {c['nome_conta']: c['id'] for c in contas}
        except Exception as e:
            print(f"Erro ao carregar comboboxes: {e}")

    def load_expenses(self):
        """Carrega lista de despesas"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Montar query com filtros
        where_parts = []
        where_params = []

        if self.data_inicio_entry.get().strip():
            data_inicio = self.parse_date_br(self.data_inicio_entry.get())
            if data_inicio:
                where_parts.append("data_gasto >= ?")
                where_params.append(data_inicio)

        if self.data_fim_entry.get().strip():
            data_fim = self.parse_date_br(self.data_fim_entry.get())
            if data_fim:
                where_parts.append("data_gasto <= ?")
                where_params.append(data_fim)

        status = self.status_combo.get()
        if status == "Em Aberto":
            where_parts.append("pago = 0")
        elif status == "Pagos":
            where_parts.append("pago = 1")

        where_clause = " AND ".join(where_parts) if where_parts else None

        sql = """
            SELECT d.*, td.nome as tipo_nome, f.nome as fornecedor_nome
            FROM despesas d
            LEFT JOIN tipo_despesa td ON d.tipo_despesa_id = td.id
            LEFT JOIN fornecedores f ON d.fornecedor_id = f.id
        """

        if where_clause:
            sql += f" WHERE {where_clause}"

        sql += " ORDER BY d.data_gasto DESC"

        expenses = self.db_manager.execute_query(sql, where_params if where_params else None)

        for expense in expenses:
            values = (
                expense['id'],
                self.format_date_br(expense['data_gasto']),
                expense['tipo_nome'] or '',
                expense['fornecedor_nome'] or '',
                expense['descricao'] or '',
                f"R$ {expense['valor']:.2f}",
                self.format_date_br(expense['data_pagamento']) if expense['data_pagamento'] else '',
                "Pago" if expense['pago'] else "Em Aberto"
            )
            self.tree.insert('', END, values=values)

    def edit_selected(self):
        """Método unificado para edição por duplo clique ou Ctrl+E"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma despesa na lista!")
            return

        item = self.tree.item(selection[0])
        expense_id = item['values'][0]

        expenses = self.db_manager.select('despesas', where_clause='id = ?', where_params=[expense_id])
        if not expenses:
            return

        expense = expenses[0]
        self.selected_id = expense['id']

        # Tipo
        if expense['tipo_despesa_id']:
            tipo = self.db_manager.select('tipo_despesa', where_clause='id = ?', where_params=[expense['tipo_despesa_id']])
            if tipo:
                self.tipo_combo.set(tipo[0]['nome'])

        # Fornecedor
        if expense['fornecedor_id']:
            fornecedor = self.db_manager.select('fornecedores', where_clause='id = ?', where_params=[expense['fornecedor_id']])
            if fornecedor:
                self.fornecedor_combo.set(fornecedor[0]['nome'])

        self.descricao_entry.delete(0, END)
        if expense['descricao']:
            self.descricao_entry.insert(0, expense['descricao'])

        self.valor_entry.delete(0, END)
        self.valor_entry.insert(0, str(expense['valor']))

        self.data_gasto_entry.delete(0, END)
        self.data_gasto_entry.insert(0, self.format_date_br(expense['data_gasto']))

        self.data_pgto_entry.delete(0, END)
        if expense['data_pagamento']:
            self.data_pgto_entry.insert(0, self.format_date_br(expense['data_pagamento']))

        self.pago_var.set(expense['pago'])

        # Conta Bancária
        self.conta_combo.set('')
        if expense.get('conta_bancaria_id'):
            conta = self.db_manager.select('contas_bancarias', where_clause='id = ?', where_params=[expense['conta_bancaria_id']])
            if conta:
                self.conta_combo.set(conta[0]['nome_conta'])

        self.obs_text.delete('1.0', END)
        if expense['observacoes']:
            self.obs_text.insert('1.0', expense['observacoes'])

        messagebox.showinfo("Editar", "Registro carregado para edicao! Modifique os dados e clique em Salvar.")

    def clear_form(self):
        """Limpa o formulário"""
        self.selected_id = None
        self.tipo_combo.set('')
        self.fornecedor_combo.set('')
        self.descricao_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        self.data_gasto_entry.delete(0, END)
        self.data_gasto_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.data_pgto_entry.delete(0, END)
        self.pago_var.set(0)
        self.parcelar_var.set(0)
        self.num_parcelas_entry.delete(0, END)
        self.num_parcelas_entry.insert(0, "2")
        self.num_parcelas_entry.config(state=DISABLED)
        self.conta_combo.set('')
        self.obs_text.delete('1.0', END)
        # Limpar campos de inventário
        self.add_inventario_var.set(0)
        self.quantidade_entry.delete(0, END)
        self.quantidade_entry.config(state=DISABLED)
        self.unidade_combo.set("kg")
        self.unidade_combo.config(state=DISABLED)
        self.categoria_combo.set("Insumos")
        self.categoria_combo.config(state=DISABLED)

    def save_expense(self):
        """Salva a despesa"""
        if not self.tipo_combo.get():
            messagebox.showerror("Erro", "Selecione o tipo de despesa!")
            return

        if not self.valor_entry.get().strip():
            messagebox.showerror("Erro", "Informe o valor!")
            return

        if not self.data_gasto_entry.get().strip():
            messagebox.showerror("Erro", "Informe a data do gasto!")
            return

        try:
            valor = float(self.valor_entry.get().replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Valor inválido!")
            return

        # Verificar se precisa parcelar
        is_parcelado = self.parcelar_var.get() == 1
        num_parcelas = 1

        if is_parcelado:
            try:
                num_parcelas = int(self.num_parcelas_entry.get())
                if num_parcelas < 2:
                    messagebox.showerror("Erro", "Número de parcelas deve ser 2 ou mais!")
                    return
            except:
                messagebox.showerror("Erro", "Número de parcelas inválido!")
                return

        # Obter conta bancária se selecionada
        conta_id = None
        if self.conta_combo.get():
            conta_id = self.conta_data.get(self.conta_combo.get())

        # Preparar dados base
        base_data = {
            'tipo_despesa_id': self.tipo_data.get(self.tipo_combo.get()),
            'fornecedor_id': self.fornecedor_data.get(self.fornecedor_combo.get()),
            'descricao': self.descricao_entry.get().strip() or None,
            'conta_bancaria_id': conta_id,
            'observacoes': self.obs_text.get('1.0', END).strip() or None
        }

        try:
            if self.selected_id:
                # Atualização de despesa existente (não parcelar em edição)
                data = base_data.copy()
                data.update({
                    'valor': valor,
                    'data_gasto': self.parse_date_br(self.data_gasto_entry.get()),
                    'data_pagamento': self.parse_date_br(self.data_pgto_entry.get()),
                    'pago': self.pago_var.get()
                })

                self.db_manager.update('despesas', data, 'id = ?', [self.selected_id])

                # Atualizar saldo da conta se foi pago
                if self.pago_var.get() == 1 and conta_id:
                    self.update_account_balance(conta_id, -valor)

                messagebox.showinfo("Sucesso", "Despesa atualizada com sucesso!")
            else:
                # Nova despesa
                if is_parcelado:
                    # Gerar parcelas
                    valor_parcela = valor / num_parcelas
                    data_gasto = datetime.strptime(self.data_gasto_entry.get(), '%d/%m/%Y')

                    for i in range(num_parcelas):
                        data = base_data.copy()

                        # Data de cada parcela (adiciona meses)
                        mes = data_gasto.month + i
                        ano = data_gasto.year
                        while mes > 12:
                            mes -= 12
                            ano += 1

                        # Ajustar dia se necessário
                        try:
                            data_parcela = data_gasto.replace(year=ano, month=mes)
                        except ValueError:
                            # Se dia não existe no mês (ex: 31 em fevereiro), usar último dia do mês
                            import calendar
                            ultimo_dia = calendar.monthrange(ano, mes)[1]
                            data_parcela = data_gasto.replace(year=ano, month=mes, day=ultimo_dia)

                        data.update({
                            'valor': valor_parcela,
                            'data_gasto': data_parcela.strftime('%Y-%m-%d'),
                            'data_pagamento': None,
                            'pago': 0,
                            'descricao': f"{base_data['descricao'] or ''} - Parcela {i+1}/{num_parcelas}".strip()
                        })

                        self.db_manager.insert('despesas', data)

                    messagebox.showinfo("Sucesso", f"Despesa parcelada em {num_parcelas}x com sucesso!")
                else:
                    # Despesa única
                    data = base_data.copy()
                    data.update({
                        'valor': valor,
                        'data_gasto': self.parse_date_br(self.data_gasto_entry.get()),
                        'data_pagamento': self.parse_date_br(self.data_pgto_entry.get()),
                        'pago': self.pago_var.get()
                    })

                    despesa_id = self.db_manager.insert('despesas', data)

                    # Adicionar ao inventário se checkbox estiver marcado
                    if self.add_inventario_var.get() == 1:
                        self.add_to_inventory(despesa_id, valor)

                    # Atualizar saldo da conta se foi pago
                    if self.pago_var.get() == 1 and conta_id:
                        self.update_account_balance(conta_id, -valor)

                    messagebox.showinfo("Sucesso", "Despesa lançada com sucesso!")

            self.clear_form()
            self.load_expenses()
            self.load_combo_data()  # Recarregar comboboxes após salvar

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_expense(self):
        """Exclui a despesa"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma despesa para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta despesa?"):
            try:
                self.db_manager.delete('despesas', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")
                self.clear_form()
                self.load_expenses()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    def mark_as_paid(self):
        """Marca despesa como paga"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma despesa na lista!")
            return

        # Pegar ID da despesa selecionada
        item = self.tree.item(selection[0])
        expense_id = item['values'][0]

        # Buscar despesa
        expenses = self.db_manager.select('despesas', where_clause='id = ?', where_params=[expense_id])
        if not expenses:
            return

        expense = expenses[0]

        # Verificar se já está paga
        if expense['pago'] == 1:
            # Desmarcar como pago
            if messagebox.askyesno("Desmarcar como Pago", "Esta despesa já está marcada como paga.\nDeseja desmarcar e estornar o valor na conta?"):
                try:
                    # Estornar saldo
                    if expense.get('conta_bancaria_id'):
                        self.update_account_balance(expense['conta_bancaria_id'], expense['valor'])

                    # Atualizar despesa
                    self.db_manager.update('despesas',
                        {'pago': 0, 'data_pagamento': None},
                        'id = ?', [expense_id])

                    messagebox.showinfo("Sucesso", "Despesa desmarcada como paga!")
                    self.load_expenses()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao desmarcar: {str(e)}")
        else:
            # Marcar como pago - abrir diálogo
            dialog = tk.Toplevel(self.parent)
            dialog.title("Marcar como Pago")
            dialog.geometry("400x250")
            dialog.transient(self.parent)
            dialog.grab_set()

            ttk.Label(dialog, text="Marcar Despesa como Paga", font=("Helvetica", 12, "bold")).pack(pady=10)

            frame = ttk.Frame(dialog, padding=20)
            frame.pack(fill=BOTH, expand=YES)

            # Conta bancária
            ttk.Label(frame, text="Conta/Caixa:*").grid(row=0, column=0, sticky=W, pady=5)
            conta_combo = ttk.Combobox(frame, width=25, state="readonly")
            conta_combo.grid(row=0, column=1, sticky=W, pady=5, padx=5)

            # Carregar contas
            contas = self.db_manager.select('contas_bancarias', where_clause='ativo = 1', order_by='nome_conta')
            conta_combo['values'] = [c['nome_conta'] for c in contas]
            conta_data = {c['nome_conta']: c['id'] for c in contas}

            # Se despesa já tinha conta, selecionar
            if expense.get('conta_bancaria_id'):
                conta = self.db_manager.select('contas_bancarias', where_clause='id = ?', where_params=[expense['conta_bancaria_id']])
                if conta:
                    conta_combo.set(conta[0]['nome_conta'])

            # Data pagamento
            ttk.Label(frame, text="Data Pagamento:*").grid(row=1, column=0, sticky=W, pady=5)
            data_pgto_entry = ttk.Entry(frame, width=27)
            data_pgto_entry.grid(row=1, column=1, sticky=W, pady=5, padx=5)
            data_pgto_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

            # Valor
            ttk.Label(frame, text="Valor:").grid(row=2, column=0, sticky=W, pady=5)
            ttk.Label(frame, text=f"R$ {expense['valor']:,.2f}", font=("Helvetica", 10, "bold")).grid(row=2, column=1, sticky=W, pady=5, padx=5)

            def confirmar():
                if not conta_combo.get():
                    messagebox.showerror("Erro", "Selecione uma conta!")
                    return

                if not data_pgto_entry.get():
                    messagebox.showerror("Erro", "Informe a data de pagamento!")
                    return

                try:
                    conta_id = conta_data[conta_combo.get()]

                    # Atualizar despesa
                    data_pagamento = datetime.strptime(data_pgto_entry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')

                    self.db_manager.update('despesas',
                        {'pago': 1, 'data_pagamento': data_pagamento, 'conta_bancaria_id': conta_id},
                        'id = ?', [expense_id])

                    # Atualizar saldo da conta (débito)
                    self.update_account_balance(conta_id, -expense['valor'])

                    messagebox.showinfo("Sucesso", "Despesa marcada como paga!\nSaldo da conta atualizado.")
                    dialog.destroy()
                    self.load_expenses()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao marcar como pago: {str(e)}")

            # Botões
            btn_frame = ttk.Frame(frame)
            btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

            ttk.Button(btn_frame, text="Confirmar", command=confirmar, width=12).pack(side=LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=12).pack(side=LEFT, padx=5)

    def on_pago_changed(self):
        """Callback quando checkbox 'Já foi pago?' muda"""
        if self.pago_var.get() == 1:
            # Se está marcado como pago, habilita data de pagamento e exige
            self.data_pgto_entry.config(state=NORMAL)
            if not self.data_pgto_entry.get():
                self.data_pgto_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        else:
            # Se não está pago, limpa e desabilita data de pagamento
            self.data_pgto_entry.delete(0, END)
            self.data_pgto_entry.config(state=NORMAL)  # Manter habilitado para permitir entrada manual

    def on_parcelar_changed(self):
        """Callback quando checkbox 'Parcelar?' muda"""
        if self.parcelar_var.get() == 1:
            # Se está marcado parcelar, habilita número de parcelas
            self.num_parcelas_entry.config(state=NORMAL)
        else:
            # Se não vai parcelar, desabilita número de parcelas
            self.num_parcelas_entry.config(state=DISABLED)

    def on_inventario_changed(self):
        """Callback quando checkbox 'Adicionar ao Inventário' muda"""
        if self.add_inventario_var.get() == 1:
            # Se está marcado, habilita campos de inventário
            self.quantidade_entry.config(state=NORMAL)
            self.unidade_combo.config(state="readonly")
            self.categoria_combo.config(state="readonly")
        else:
            # Se não está marcado, desabilita campos de inventário
            self.quantidade_entry.config(state=DISABLED)
            self.unidade_combo.config(state=DISABLED)
            self.categoria_combo.config(state=DISABLED)

    def update_account_balance(self, conta_id, valor):
        """Atualiza saldo da conta bancária"""
        try:
            contas = self.db_manager.select('contas_bancarias', where_clause='id = ?', where_params=[conta_id])
            if contas:
                saldo_atual = contas[0].get('saldo_atual', 0) or 0
                novo_saldo = saldo_atual + valor

                self.db_manager.update('contas_bancarias',
                    {'saldo_atual': novo_saldo},
                    'id = ?',
                    [conta_id])
        except Exception as e:
            print(f"Erro ao atualizar saldo da conta: {e}")

    def add_to_inventory(self, despesa_id, valor_total):
        """Adiciona item ao inventário baseado na despesa"""
        try:
            # Validar campos de inventário
            if not self.quantidade_entry.get().strip():
                messagebox.showwarning("Aviso", "Quantidade não informada. Item não adicionado ao inventário.")
                return

            try:
                quantidade = float(self.quantidade_entry.get().replace(',', '.'))
            except:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return

            # Calcular valor unitário
            valor_unitario = valor_total / quantidade if quantidade > 0 else valor_total

            # Obter descrição do item (usar descrição da despesa ou tipo)
            nome_item = self.descricao_entry.get().strip()
            if not nome_item:
                nome_item = self.tipo_combo.get()

            # Gerar código único para o item
            import random
            import string
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            # Verificar se item já existe com mesmo nome
            existing = self.db_manager.select('inventario_itens',
                                             where_clause='LOWER(nome) = LOWER(?)',
                                             where_params=[nome_item])

            if existing:
                # Item já existe, apenas adicionar quantidade
                item_id = existing[0]['id']
                estoque_atual = existing[0]['estoque_atual'] or 0
                novo_estoque = estoque_atual + quantidade

                self.db_manager.update('inventario_itens',
                                      {'estoque_atual': novo_estoque,
                                       'valor_unitario': valor_unitario},
                                      'id = ?',
                                      [item_id])

                # Registrar movimentação
                self.db_manager.insert('inventario_movimentacoes', {
                    'item_id': item_id,
                    'tipo': 'Entrada',
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'saldo_anterior': estoque_atual,
                    'saldo_novo': novo_estoque,
                    'motivo': f'Compra - Despesa #{despesa_id}',
                    'data_movimentacao': datetime.now().strftime('%Y-%m-%d'),
                    'responsavel': 'Sistema'
                })

                messagebox.showinfo("Inventário", f"Quantidade adicionada ao item existente '{nome_item}'!")
            else:
                # Criar novo item no inventário
                fornecedor_id = self.fornecedor_data.get(self.fornecedor_combo.get())

                item_data = {
                    'codigo': codigo,
                    'nome': nome_item,
                    'categoria': self.categoria_combo.get(),
                    'unidade': self.unidade_combo.get(),
                    'estoque_minimo': 0,
                    'estoque_atual': quantidade,
                    'valor_unitario': valor_unitario,
                    'fornecedor_id': fornecedor_id,
                    'ativo': 1,
                    'observacoes': f'Adicionado automaticamente da despesa #{despesa_id}'
                }

                item_id = self.db_manager.insert('inventario_itens', item_data)

                # Registrar movimentação inicial
                self.db_manager.insert('inventario_movimentacoes', {
                    'item_id': item_id,
                    'tipo': 'Entrada',
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'saldo_anterior': 0,
                    'saldo_novo': quantidade,
                    'motivo': f'Compra - Despesa #{despesa_id}',
                    'data_movimentacao': datetime.now().strftime('%Y-%m-%d'),
                    'responsavel': 'Sistema'
                })

                messagebox.showinfo("Inventário", f"Novo item '{nome_item}' adicionado ao inventário com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar ao inventário: {str(e)}")
            print(f"Erro detalhado: {e}")

    def format_date_br(self, date_str):
        """Converte data SQL para BR"""
        if not date_str:
            return ''
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%Y')
        except:
            return date_str

    def parse_date_br(self, date_str):
        """Converte data BR para SQL"""
        if not date_str:
            return None
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        except:
            return None
