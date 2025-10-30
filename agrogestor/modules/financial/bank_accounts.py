"""
Gestão de Contas Bancárias
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


class BankAccountsWindow:
    """Janela de gestão de contas bancárias"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None
        self.create_widgets()
        self.load_accounts()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Contas Bancárias", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        form_frame = ttk.LabelFrame(main_container, text="Dados da Conta", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Nome da Conta:*").grid(row=row, column=0, sticky=W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        ttk.Label(form_frame, text="Banco:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.banco_entry = ttk.Entry(form_frame, width=25)
        self.banco_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Agência:").grid(row=row, column=0, sticky=W, pady=5)
        self.agencia_entry = ttk.Entry(form_frame, width=15)
        self.agencia_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Número:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.numero_entry = ttk.Entry(form_frame, width=20)
        self.numero_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Tipo:").grid(row=row, column=0, sticky=W, pady=5)
        self.tipo_combo = ttk.Combobox(form_frame, width=25, state="readonly",
                                       values=["Corrente", "Poupança", "Investimento", "Caixa (Dinheiro Físico)"])
        self.tipo_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.tipo_combo.set("Corrente")
        self.tipo_combo.bind('<<ComboboxSelected>>', self.on_tipo_changed)

        ttk.Label(form_frame, text="Saldo Inicial:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.saldo_entry = ttk.Entry(form_frame, width=15)
        self.saldo_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.saldo_entry.insert(0, "0.00")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=4, pady=15)
        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_account, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_account, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Contas Cadastradas", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para scrollbars
        table_frame = ttk.Frame(list_frame)
        table_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Nome", "Banco", "Agência", "Número", "Tipo", "Saldo Atual")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10,
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "Saldo Atual":
                self.tree.column(col, width=120, anchor=E)
            else:
                self.tree.column(col, width=120)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_accounts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        accounts = self.db_manager.select('contas_bancarias', where_clause='ativo = 1', order_by='nome_conta')

        for acc in accounts:
            values = (
                acc['id'],
                acc['nome_conta'],
                acc['banco'] or '',
                acc['agencia'] or '',
                acc['numero_conta'] or '',
                acc['tipo_conta'] or '',
                f"R$ {acc['saldo_atual']:,.2f}" if acc['saldo_atual'] else "R$ 0,00"
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        acc_id = item['values'][0]

        accounts = self.db_manager.select('contas_bancarias', where_clause='id = ?', where_params=[acc_id])
        if not accounts:
            return

        acc = accounts[0]
        self.selected_id = acc['id']

        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, acc['nome_conta'])

        self.banco_entry.delete(0, END)
        if acc['banco']:
            self.banco_entry.insert(0, acc['banco'])

        self.agencia_entry.delete(0, END)
        if acc['agencia']:
            self.agencia_entry.insert(0, acc['agencia'])

        self.numero_entry.delete(0, END)
        if acc['numero_conta']:
            self.numero_entry.insert(0, acc['numero_conta'])

        if acc['tipo_conta']:
            self.tipo_combo.set(acc['tipo_conta'])

        self.saldo_entry.delete(0, END)
        if acc['saldo_inicial'] is not None:
            self.saldo_entry.insert(0, str(acc['saldo_inicial']))

    def clear_form(self):
        self.selected_id = None
        self.nome_entry.delete(0, END)
        self.banco_entry.delete(0, END)
        self.agencia_entry.delete(0, END)
        self.numero_entry.delete(0, END)
        self.tipo_combo.set("Corrente")
        self.saldo_entry.delete(0, END)
        self.saldo_entry.insert(0, "0.00")
        self.on_tipo_changed()

    def on_tipo_changed(self, event=None):
        """Habilita/desabilita campos baseado no tipo de conta"""
        tipo = self.tipo_combo.get()

        if "Caixa" in tipo:
            # Para caixa, desabilitar campos bancários
            self.banco_entry.config(state=DISABLED)
            self.agencia_entry.config(state=DISABLED)
            self.numero_entry.config(state=DISABLED)

            # Limpar campos se estiverem preenchidos
            self.banco_entry.delete(0, END)
            self.agencia_entry.delete(0, END)
            self.numero_entry.delete(0, END)
        else:
            # Para contas bancárias, habilitar todos os campos
            self.banco_entry.config(state=NORMAL)
            self.agencia_entry.config(state=NORMAL)
            self.numero_entry.config(state=NORMAL)

    def save_account(self):
        if not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "Informe o nome da conta!")
            return

        try:
            saldo = float(self.saldo_entry.get().replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Saldo inválido!")
            return

        data = {
            'nome_conta': self.nome_entry.get().strip(),
            'banco': self.banco_entry.get().strip() or None,
            'agencia': self.agencia_entry.get().strip() or None,
            'numero_conta': self.numero_entry.get().strip() or None,
            'tipo_conta': self.tipo_combo.get(),
            'saldo_inicial': saldo,
            'saldo_atual': saldo if not self.selected_id else None,  # Apenas para nova conta
            'ativo': 1
        }

        try:
            if self.selected_id:
                # Não atualizar saldo_atual, apenas saldo_inicial
                data.pop('saldo_atual')
                self.db_manager.update('contas_bancarias', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Conta atualizada!")
            else:
                self.db_manager.insert('contas_bancarias', data)
                messagebox.showinfo("Sucesso", "Conta cadastrada!")

            self.clear_form()
            self.load_accounts()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_account(self):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma conta!")
            return

        if messagebox.askyesno("Confirmar", "Deseja inativar esta conta?"):
            try:
                self.db_manager.update('contas_bancarias', {'ativo': 0}, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Conta inativada!")
                self.clear_form()
                self.load_accounts()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")
