"""
Lançamento de Aplicações (Sanidade)
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


class ApplicationsWindow:
    """Janela de lançamento de aplicações"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_combo_data()
        self.load_applications()

    def create_widgets(self):
        """Cria interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Aplicações (Sanidade)", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10, anchor=W)

        form_frame = ttk.LabelFrame(main_container, text="Dados da Aplicação", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Brinco Animal:*").grid(row=row, column=0, sticky=W, pady=5)
        self.brinco_combo = ttk.Combobox(form_frame, width=20)
        self.brinco_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Medicamento:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.medicamento_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.medicamento_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Data Aplicação:*").grid(row=row, column=0, sticky=W, pady=5)
        self.data_entry = ttk.Entry(form_frame, width=15)
        self.data_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        ttk.Label(form_frame, text="Quantidade:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.qtd_entry = ttk.Entry(form_frame, width=15)
        self.qtd_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Status:").grid(row=row, column=0, sticky=W, pady=5)
        self.status_combo = ttk.Combobox(form_frame, width=18, state="readonly", values=["Concluído", "Pendente"])
        self.status_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.status_combo.set("Concluído")

        ttk.Label(form_frame, text="Dose:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.dose_entry = ttk.Entry(form_frame, width=15)
        self.dose_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(buttons_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Salvar", command=self.save_application, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Excluir", command=self.delete_application, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Aplicações Registradas", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para TreeView e scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Data", "Brinco", "Medicamento", "Quantidade", "Dose", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            else:
                self.tree.column(col, width=120)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_combo_data(self):
        """Carrega dados"""
        animals = self.db_manager.select('animais', order_by='brinco')
        self.brinco_combo['values'] = [a['brinco'] for a in animals]
        self.brinco_data = {a['brinco']: a['id'] for a in animals}

        medicamentos = self.db_manager.select('medicamentos', order_by='nome')
        self.medicamento_combo['values'] = [m['nome'] for m in medicamentos]
        self.medicamento_data = {m['nome']: m['id'] for m in medicamentos}

    def load_applications(self):
        """Carrega aplicações"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        sql = """
            SELECT a.*, m.nome as medicamento_nome
            FROM aplicacoes a
            LEFT JOIN medicamentos m ON a.medicamento_id = m.id
            ORDER BY a.data_aplicacao DESC
        """

        applications = self.db_manager.execute_query(sql)

        for app in applications:
            values = (
                app['id'],
                self.format_date_br(app['data_aplicacao']),
                app['brinco'] or '',
                app['medicamento_nome'] or '',
                app['quantidade'] or '',
                app['dose'] or '',
                app['status'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        """Carrega aplicação selecionada"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        app_id = item['values'][0]

        applications = self.db_manager.select('aplicacoes', where_clause='id = ?', where_params=[app_id])
        if not applications:
            return

        app = applications[0]
        self.selected_id = app['id']

        self.brinco_combo.set(app['brinco'] or '')

        if app['medicamento_id']:
            med = self.db_manager.select('medicamentos', where_clause='id = ?', where_params=[app['medicamento_id']])
            if med:
                self.medicamento_combo.set(med[0]['nome'])

        self.data_entry.delete(0, END)
        self.data_entry.insert(0, self.format_date_br(app['data_aplicacao']))

        self.qtd_entry.delete(0, END)
        if app['quantidade']:
            self.qtd_entry.insert(0, str(app['quantidade']))

        self.dose_entry.delete(0, END)
        if app['dose']:
            self.dose_entry.insert(0, app['dose'])

        if app['status']:
            self.status_combo.set(app['status'])

    def clear_form(self):
        """Limpa formulário"""
        self.selected_id = None
        self.brinco_combo.set('')
        self.medicamento_combo.set('')
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.qtd_entry.delete(0, END)
        self.dose_entry.delete(0, END)
        self.status_combo.set('Concluído')

    def save_application(self):
        """Salva aplicação"""
        if not self.brinco_combo.get().strip():
            messagebox.showerror("Erro", "Informe o brinco do animal!")
            return

        if not self.medicamento_combo.get():
            messagebox.showerror("Erro", "Selecione o medicamento!")
            return

        data = {
            'brinco': self.brinco_combo.get().strip(),
            'animal_id': self.brinco_data.get(self.brinco_combo.get()),
            'medicamento_id': self.medicamento_data.get(self.medicamento_combo.get()),
            'data_aplicacao': self.parse_date_br(self.data_entry.get()),
            'quantidade': float(self.qtd_entry.get()) if self.qtd_entry.get().strip() else None,
            'dose': self.dose_entry.get().strip() or None,
            'status': self.status_combo.get()
        }

        try:
            if self.selected_id:
                self.db_manager.update('aplicacoes', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Aplicação atualizada com sucesso!")
            else:
                self.db_manager.insert('aplicacoes', data)
                messagebox.showinfo("Sucesso", "Aplicação registrada com sucesso!")

            self.clear_form()
            self.load_applications()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_application(self):
        """Exclui aplicação"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma aplicação para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta aplicação?"):
            try:
                self.db_manager.delete('aplicacoes', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Aplicação excluída com sucesso!")
                self.clear_form()
                self.load_applications()
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
