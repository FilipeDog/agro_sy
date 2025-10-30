"""
Lançamento de Inseminações
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


class InseminationsWindow:
    """Janela de lançamento de inseminações"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_combo_data()
        self.load_inseminations()

    def create_widgets(self):
        """Cria interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Controle de Inseminações", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10, anchor=W)

        form_frame = ttk.LabelFrame(main_container, text="Dados da Inseminação", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Brinco Animal:*").grid(row=row, column=0, sticky=W, pady=5)
        self.brinco_combo = ttk.Combobox(form_frame, width=20)
        self.brinco_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Data Inseminação:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_entry = ttk.Entry(form_frame, width=15)
        self.data_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        ttk.Label(form_frame, text="Status:").grid(row=row, column=0, sticky=W, pady=5)
        self.status_combo = ttk.Combobox(form_frame, width=18, state="readonly", values=["Em processo", "Concluído"])
        self.status_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.status_combo.set("Em processo")

        ttk.Label(form_frame, text="Touro Reprodutor:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.touro_entry = ttk.Entry(form_frame, width=20)
        self.touro_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        self.efetivou_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Efetivou (gerou cria)?", variable=self.efetivou_var).grid(row=row, column=0, columnspan=2, sticky=W, pady=5)

        ttk.Label(form_frame, text="Data da Cria:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_cria_entry = ttk.Entry(form_frame, width=15)
        self.data_cria_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Qtd. Crias:").grid(row=row, column=0, sticky=W, pady=5)
        self.qtd_entry = ttk.Entry(form_frame, width=10)
        self.qtd_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(buttons_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Salvar", command=self.save_insemination, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Excluir", command=self.delete_insemination, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Inseminações Registradas", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para TreeView e scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Data", "Brinco", "Status", "Efetivou", "Data Cria", "Qtd Crias", "Touro")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            else:
                self.tree.column(col, width=100)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_combo_data(self):
        """Carrega dados"""
        animals = self.db_manager.select('animais', where_clause="sexo = 'Fêmea'", order_by='brinco')
        self.brinco_combo['values'] = [a['brinco'] for a in animals]
        self.brinco_data = {a['brinco']: a['id'] for a in animals}

    def load_inseminations(self):
        """Carrega inseminações"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        inseminations = self.db_manager.select('inseminacoes', order_by='data_inseminacao DESC')

        for ins in inseminations:
            values = (
                ins['id'],
                self.format_date_br(ins['data_inseminacao']),
                ins['brinco'] or '',
                ins['status'] or '',
                "Sim" if ins['efetivou'] else "Não",
                self.format_date_br(ins['data_cria']) if ins['data_cria'] else '',
                ins['quantidade_crias'] or '',
                ins['touro_reprodutor'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        """Carrega inseminação selecionada"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        ins_id = item['values'][0]

        inseminations = self.db_manager.select('inseminacoes', where_clause='id = ?', where_params=[ins_id])
        if not inseminations:
            return

        ins = inseminations[0]
        self.selected_id = ins['id']

        self.brinco_combo.set(ins['brinco'] or '')
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, self.format_date_br(ins['data_inseminacao']))

        if ins['status']:
            self.status_combo.set(ins['status'])

        self.touro_entry.delete(0, END)
        if ins['touro_reprodutor']:
            self.touro_entry.insert(0, ins['touro_reprodutor'])

        self.efetivou_var.set(ins['efetivou'] or 0)

        self.data_cria_entry.delete(0, END)
        if ins['data_cria']:
            self.data_cria_entry.insert(0, self.format_date_br(ins['data_cria']))

        self.qtd_entry.delete(0, END)
        if ins['quantidade_crias']:
            self.qtd_entry.insert(0, str(ins['quantidade_crias']))

    def clear_form(self):
        """Limpa formulário"""
        self.selected_id = None
        self.brinco_combo.set('')
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.status_combo.set('Em processo')
        self.touro_entry.delete(0, END)
        self.efetivou_var.set(0)
        self.data_cria_entry.delete(0, END)
        self.qtd_entry.delete(0, END)

    def save_insemination(self):
        """Salva inseminação"""
        if not self.brinco_combo.get().strip():
            messagebox.showerror("Erro", "Informe o brinco do animal!")
            return

        data = {
            'brinco': self.brinco_combo.get().strip(),
            'animal_id': self.brinco_data.get(self.brinco_combo.get()),
            'data_inseminacao': self.parse_date_br(self.data_entry.get()),
            'status': self.status_combo.get(),
            'touro_reprodutor': self.touro_entry.get().strip() or None,
            'efetivou': self.efetivou_var.get(),
            'data_cria': self.parse_date_br(self.data_cria_entry.get()),
            'quantidade_crias': int(self.qtd_entry.get()) if self.qtd_entry.get().strip() else None
        }

        try:
            if self.selected_id:
                self.db_manager.update('inseminacoes', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Inseminação atualizada com sucesso!")
            else:
                self.db_manager.insert('inseminacoes', data)
                messagebox.showinfo("Sucesso", "Inseminação registrada com sucesso!")

            self.clear_form()
            self.load_inseminations()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_insemination(self):
        """Exclui inseminação"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma inseminação para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta inseminação?"):
            try:
                self.db_manager.delete('inseminacoes', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Inseminação excluída com sucesso!")
                self.clear_form()
                self.load_inseminations()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

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
