"""
Lançamento de Receitas (Vendas)
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


class RevenuesWindow:
    """Janela de lançamento de receitas"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_combo_data()
        self.load_revenues()

    def create_widgets(self):
        """Cria os widgets da interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Lançamento de Receitas (Vendas)", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10, anchor=W)

        # Formulário
        form_frame = ttk.LabelFrame(main_container, text="Dados da Receita", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Tipo Receita:*").grid(row=row, column=0, sticky=W, pady=5)
        self.tipo_combo = ttk.Combobox(form_frame, width=20, state="readonly")
        self.tipo_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Cliente:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.cliente_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.cliente_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Descrição:").grid(row=row, column=0, sticky=W, pady=5)
        self.descricao_entry = ttk.Entry(form_frame, width=60)
        self.descricao_entry.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Quantidade:").grid(row=row, column=0, sticky=W, pady=5)
        self.qtd_entry = ttk.Entry(form_frame, width=15)
        self.qtd_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.qtd_entry.bind('<KeyRelease>', lambda e: self.calculate_total())

        ttk.Label(form_frame, text="Valor Unit.:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.valor_unit_entry = ttk.Entry(form_frame, width=15)
        self.valor_unit_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.valor_unit_entry.bind('<KeyRelease>', lambda e: self.calculate_total())

        row += 1
        ttk.Label(form_frame, text="Valor Total:").grid(row=row, column=0, sticky=W, pady=5)
        self.valor_total_label = ttk.Label(form_frame, text="R$ 0,00", font=("Helvetica", 11, "bold"))
        self.valor_total_label.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Data Venda:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_venda_entry = ttk.Entry(form_frame, width=15)
        self.data_venda_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.data_venda_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        # Conta Bancária
        ttk.Label(form_frame, text="Conta/Caixa:").grid(row=row, column=0, sticky=W, pady=5)
        self.conta_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.conta_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        # Data Pagamento
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

        # Botões
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(buttons_frame, text="Novo (Ctrl+N)", command=self.clear_form, width=15).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Salvar (Ctrl+S)", command=self.save_revenue, width=15).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Excluir (Del)", command=self.delete_revenue, width=15).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Marcar como Recebido", command=self.mark_as_received, width=18).pack(side=LEFT, padx=5)

        # Lista
        list_frame = ttk.LabelFrame(main_container, text="Receitas Lançadas", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        table_frame = ttk.Frame(list_frame)
        table_frame.pack(fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Data", "Tipo", "Cliente", "Descrição", "Qtd", "Valor Unit.", "Total", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_h.set)
        scrollbar.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col in ["Data", "Qtd", "Status"]:
                self.tree.column(col, width=80, anchor=CENTER)
            elif col in ["Valor Unit.", "Total"]:
                self.tree.column(col, width=100, anchor=CENTER)
            else:
                self.tree.column(col, width=150)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_selected())

        # Atalhos de teclado
        self.parent.bind('<Control-n>', lambda e: self.clear_form())
        self.parent.bind('<Control-s>', lambda e: self.save_revenue())
        self.parent.bind('<Control-e>', lambda e: self.edit_selected())
        self.parent.bind('<Delete>', lambda e: self.delete_revenue())

    def load_combo_data(self):
        """Carrega dados dos comboboxes"""
        tipos = self.db_manager.select('tipo_receita', order_by='nome')
        self.tipo_combo['values'] = [t['nome'] for t in tipos]
        self.tipo_data = {t['nome']: t['id'] for t in tipos}

        clientes = self.db_manager.select('clientes', where_clause='ativo = 1', order_by='nome')
        self.cliente_combo['values'] = [''] + [c['nome'] for c in clientes]
        self.cliente_data = {c['nome']: c['id'] for c in clientes}

        # Contas Bancárias / Caixa
        contas = self.db_manager.select('contas_bancarias', where_clause='ativo = 1', order_by='nome_conta')
        self.conta_combo['values'] = [''] + [c['nome_conta'] for c in contas]
        self.conta_data = {c['nome_conta']: c['id'] for c in contas}

    def calculate_total(self):
        """Calcula o valor total"""
        try:
            qtd = float(self.qtd_entry.get().replace(',', '.')) if self.qtd_entry.get().strip() else 0
            valor_unit = float(self.valor_unit_entry.get().replace(',', '.')) if self.valor_unit_entry.get().strip() else 0
            total = qtd * valor_unit
            self.valor_total_label.config(text=f"R$ {total:,.2f}")
        except:
            self.valor_total_label.config(text="R$ 0,00")

    def load_revenues(self):
        """Carrega lista de receitas"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        sql = """
            SELECT r.*, tr.nome as tipo_nome, c.nome as cliente_nome
            FROM receitas r
            LEFT JOIN tipo_receita tr ON r.tipo_receita_id = tr.id
            LEFT JOIN clientes c ON r.cliente_id = c.id
            ORDER BY r.data_venda DESC
        """

        revenues = self.db_manager.execute_query(sql)

        for revenue in revenues:
            values = (
                revenue['id'],
                self.format_date_br(revenue['data_venda']),
                revenue['tipo_nome'] or '',
                revenue['cliente_nome'] or '',
                revenue['descricao'] or '',
                revenue['quantidade'] or '',
                f"R$ {revenue['valor_unitario']:.2f}" if revenue['valor_unitario'] else '',
                f"R$ {revenue['valor_total']:.2f}" if revenue['valor_total'] else '',
                "Pago" if revenue['pago'] else "Em Aberto"
            )
            self.tree.insert('', END, values=values)

    def edit_selected(self):
        """Método unificado para edição por duplo clique ou Ctrl+E"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma receita na lista!")
            return

        item = self.tree.item(selection[0])
        revenue_id = item['values'][0]

        revenues = self.db_manager.select('receitas', where_clause='id = ?', where_params=[revenue_id])
        if not revenues:
            return

        revenue = revenues[0]
        self.selected_id = revenue['id']

        if revenue['tipo_receita_id']:
            tipo = self.db_manager.select('tipo_receita', where_clause='id = ?', where_params=[revenue['tipo_receita_id']])
            if tipo:
                self.tipo_combo.set(tipo[0]['nome'])

        if revenue['cliente_id']:
            cliente = self.db_manager.select('clientes', where_clause='id = ?', where_params=[revenue['cliente_id']])
            if cliente:
                self.cliente_combo.set(cliente[0]['nome'])

        self.descricao_entry.delete(0, END)
        if revenue['descricao']:
            self.descricao_entry.insert(0, revenue['descricao'])

        self.qtd_entry.delete(0, END)
        if revenue['quantidade']:
            self.qtd_entry.insert(0, str(revenue['quantidade']))

        self.valor_unit_entry.delete(0, END)
        if revenue['valor_unitario']:
            self.valor_unit_entry.insert(0, str(revenue['valor_unitario']))

        self.data_venda_entry.delete(0, END)
        self.data_venda_entry.insert(0, self.format_date_br(revenue['data_venda']))

        self.data_pgto_entry.delete(0, END)
        if revenue['data_pagamento']:
            self.data_pgto_entry.insert(0, self.format_date_br(revenue['data_pagamento']))

        self.pago_var.set(revenue['pago'])

        # Conta Bancária
        self.conta_combo.set('')
        if revenue.get('conta_bancaria_id'):
            conta = self.db_manager.select('contas_bancarias', where_clause='id = ?', where_params=[revenue['conta_bancaria_id']])
            if conta:
                self.conta_combo.set(conta[0]['nome_conta'])

        self.calculate_total()

        messagebox.showinfo("Editar", "Registro carregado para edicao! Modifique os dados e clique em Salvar.")

    def clear_form(self):
        """Limpa o formulário"""
        self.selected_id = None
        self.tipo_combo.set('')
        self.cliente_combo.set('')
        self.descricao_entry.delete(0, END)
        self.qtd_entry.delete(0, END)
        self.valor_unit_entry.delete(0, END)
        self.data_venda_entry.delete(0, END)
        self.data_venda_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.data_pgto_entry.delete(0, END)
        self.pago_var.set(0)
        self.parcelar_var.set(0)
        self.num_parcelas_entry.delete(0, END)
        self.num_parcelas_entry.insert(0, "2")
        self.num_parcelas_entry.config(state=DISABLED)
        self.conta_combo.set('')
        self.valor_total_label.config(text="R$ 0,00")

    def save_revenue(self):
        """Salva a receita"""
        if not self.tipo_combo.get():
            messagebox.showerror("Erro", "Selecione o tipo de receita!")
            return

        if not self.valor_unit_entry.get().strip():
            messagebox.showerror("Erro", "Informe o valor unitário!")
            return

        try:
            qtd = float(self.qtd_entry.get().replace(',', '.')) if self.qtd_entry.get().strip() else 1
            valor_unit = float(self.valor_unit_entry.get().replace(',', '.'))
            valor_total = qtd * valor_unit
        except:
            messagebox.showerror("Erro", "Valores inválidos!")
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
            'tipo_receita_id': self.tipo_data.get(self.tipo_combo.get()),
            'cliente_id': self.cliente_data.get(self.cliente_combo.get()),
            'descricao': self.descricao_entry.get().strip() or None,
            'conta_bancaria_id': conta_id
        }

        try:
            if self.selected_id:
                # Atualização de receita existente (não parcelar em edição)
                data = base_data.copy()
                data.update({
                    'quantidade': qtd,
                    'valor_unitario': valor_unit,
                    'valor_total': valor_total,
                    'data_venda': self.parse_date_br(self.data_venda_entry.get()),
                    'data_pagamento': self.parse_date_br(self.data_pgto_entry.get()),
                    'pago': self.pago_var.get()
                })

                self.db_manager.update('receitas', data, 'id = ?', [self.selected_id])

                # Atualizar saldo da conta se foi pago (receita = positivo)
                if self.pago_var.get() == 1 and conta_id:
                    self.update_account_balance(conta_id, valor_total)

                messagebox.showinfo("Sucesso", "Receita atualizada com sucesso!")
            else:
                # Nova receita
                if is_parcelado:
                    # Gerar parcelas
                    valor_parcela = valor_total / num_parcelas
                    qtd_parcela = qtd / num_parcelas
                    data_venda = datetime.strptime(self.data_venda_entry.get(), '%d/%m/%Y')

                    for i in range(num_parcelas):
                        data = base_data.copy()

                        # Data de cada parcela (adiciona meses)
                        mes = data_venda.month + i
                        ano = data_venda.year
                        while mes > 12:
                            mes -= 12
                            ano += 1

                        # Ajustar dia se necessário
                        try:
                            data_parcela = data_venda.replace(year=ano, month=mes)
                        except ValueError:
                            # Se dia não existe no mês (ex: 31 em fevereiro), usar último dia do mês
                            import calendar
                            ultimo_dia = calendar.monthrange(ano, mes)[1]
                            data_parcela = data_venda.replace(year=ano, month=mes, day=ultimo_dia)

                        data.update({
                            'quantidade': qtd_parcela,
                            'valor_unitario': valor_unit,
                            'valor_total': valor_parcela,
                            'data_venda': data_parcela.strftime('%Y-%m-%d'),
                            'data_pagamento': None,
                            'pago': 0,
                            'descricao': f"{base_data['descricao'] or ''} - Parcela {i+1}/{num_parcelas}".strip()
                        })

                        self.db_manager.insert('receitas', data)

                    messagebox.showinfo("Sucesso", f"Receita parcelada em {num_parcelas}x com sucesso!")
                else:
                    # Receita única
                    data = base_data.copy()
                    data.update({
                        'quantidade': qtd,
                        'valor_unitario': valor_unit,
                        'valor_total': valor_total,
                        'data_venda': self.parse_date_br(self.data_venda_entry.get()),
                        'data_pagamento': self.parse_date_br(self.data_pgto_entry.get()),
                        'pago': self.pago_var.get()
                    })

                    self.db_manager.insert('receitas', data)

                    # Atualizar saldo da conta se foi pago (receita = positivo)
                    if self.pago_var.get() == 1 and conta_id:
                        self.update_account_balance(conta_id, valor_total)

                    messagebox.showinfo("Sucesso", "Receita lançada com sucesso!")

            self.clear_form()
            self.load_revenues()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_revenue(self):
        """Exclui a receita"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma receita para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta receita?"):
            try:
                self.db_manager.delete('receitas', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Receita excluída com sucesso!")
                self.clear_form()
                self.load_revenues()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    def mark_as_received(self):
        """Marca receita como recebida"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma receita na lista!")
            return

        # Pegar ID da receita selecionada
        item = self.tree.item(selection[0])
        revenue_id = item['values'][0]

        # Buscar receita
        revenues = self.db_manager.select('receitas', where_clause='id = ?', where_params=[revenue_id])
        if not revenues:
            return

        revenue = revenues[0]

        # Verificar se já está recebida
        if revenue['pago'] == 1:
            # Desmarcar como recebido
            if messagebox.askyesno("Desmarcar como Recebido", "Esta receita já está marcada como recebida.\nDeseja desmarcar e estornar o valor na conta?"):
                try:
                    # Estornar saldo (subtrair porque é estorno de receita)
                    if revenue.get('conta_bancaria_id'):
                        self.update_account_balance(revenue['conta_bancaria_id'], -revenue['valor_total'])

                    # Atualizar receita
                    self.db_manager.update('receitas',
                        {'pago': 0, 'data_pagamento': None},
                        'id = ?', [revenue_id])

                    messagebox.showinfo("Sucesso", "Receita desmarcada como recebida!")
                    self.load_revenues()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao desmarcar: {str(e)}")
        else:
            # Marcar como recebido - abrir diálogo
            dialog = tk.Toplevel(self.parent)
            dialog.title("Marcar como Recebido")
            dialog.geometry("400x250")
            dialog.transient(self.parent)
            dialog.grab_set()

            ttk.Label(dialog, text="Marcar Receita como Recebida", font=("Helvetica", 12, "bold")).pack(pady=10)

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

            # Se receita já tinha conta, selecionar
            if revenue.get('conta_bancaria_id'):
                conta = self.db_manager.select('contas_bancarias', where_clause='id = ?', where_params=[revenue['conta_bancaria_id']])
                if conta:
                    conta_combo.set(conta[0]['nome_conta'])

            # Data pagamento
            ttk.Label(frame, text="Data Recebimento:*").grid(row=1, column=0, sticky=W, pady=5)
            data_pgto_entry = ttk.Entry(frame, width=27)
            data_pgto_entry.grid(row=1, column=1, sticky=W, pady=5, padx=5)
            data_pgto_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

            # Valor
            ttk.Label(frame, text="Valor:").grid(row=2, column=0, sticky=W, pady=5)
            ttk.Label(frame, text=f"R$ {revenue['valor_total']:,.2f}", font=("Helvetica", 10, "bold")).grid(row=2, column=1, sticky=W, pady=5, padx=5)

            def confirmar():
                if not conta_combo.get():
                    messagebox.showerror("Erro", "Selecione uma conta!")
                    return

                if not data_pgto_entry.get():
                    messagebox.showerror("Erro", "Informe a data de recebimento!")
                    return

                try:
                    conta_id = conta_data[conta_combo.get()]

                    # Atualizar receita
                    data_pagamento = datetime.strptime(data_pgto_entry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')

                    self.db_manager.update('receitas',
                        {'pago': 1, 'data_pagamento': data_pagamento, 'conta_bancaria_id': conta_id},
                        'id = ?', [revenue_id])

                    # Atualizar saldo da conta (crédito - adiciona dinheiro)
                    self.update_account_balance(conta_id, revenue['valor_total'])

                    messagebox.showinfo("Sucesso", "Receita marcada como recebida!\nSaldo da conta atualizado.")
                    dialog.destroy()
                    self.load_revenues()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao marcar como recebido: {str(e)}")

            # Botões
            btn_frame = ttk.Frame(frame)
            btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

            ttk.Button(btn_frame, text="Confirmar", command=confirmar, width=12).pack(side=LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=12).pack(side=LEFT, padx=5)

    def on_pago_changed(self):
        """Callback quando checkbox 'Já foi pago?' muda"""
        if self.pago_var.get() == 1:
            # Se está marcado como pago, habilita data de pagamento
            self.data_pgto_entry.config(state=NORMAL)
            if not self.data_pgto_entry.get():
                self.data_pgto_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        else:
            # Se não está pago, limpa data de pagamento
            self.data_pgto_entry.delete(0, END)

    def on_parcelar_changed(self):
        """Callback quando checkbox 'Parcelar?' muda"""
        if self.parcelar_var.get() == 1:
            # Se está marcado parcelar, habilita número de parcelas
            self.num_parcelas_entry.config(state=NORMAL)
        else:
            # Se não vai parcelar, desabilita número de parcelas
            self.num_parcelas_entry.config(state=DISABLED)

    def update_account_balance(self, conta_id, valor):
        """Atualiza saldo da conta bancária (positivo para receita)"""
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

    def format_date_br(self, date_str):
        if not date_str:
            return ''
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            return date_str

    def parse_date_br(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        except:
            return None
