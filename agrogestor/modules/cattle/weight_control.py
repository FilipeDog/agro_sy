"""
Controle de Peso
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


class WeightControlWindow:
    """Janela de controle de peso"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_combo_data()
        self.load_weights()

    def create_widgets(self):
        """Cria interface"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Controle de Peso", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10, anchor=W)

        form_frame = ttk.LabelFrame(main_container, text="Dados da Pesagem", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Brinco Animal:*").grid(row=row, column=0, sticky=W, pady=5)
        self.brinco_combo = ttk.Combobox(form_frame, width=20)
        self.brinco_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Data Pesagem:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.data_entry = ttk.Entry(form_frame, width=15)
        self.data_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        ttk.Label(form_frame, text="Peso (kg):*").grid(row=row, column=0, sticky=W, pady=5)
        self.peso_entry = ttk.Entry(form_frame, width=15)
        self.peso_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Observações:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.obs_entry = ttk.Entry(form_frame, width=40)
        self.obs_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row+1, column=0, columnspan=4, pady=15)

        ttk.Button(buttons_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Salvar", command=self.save_weight, width=12).pack(side=LEFT, padx=5)
        ttk.Button(buttons_frame, text="Excluir", command=self.delete_weight, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Pesagens Registradas", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para TreeView e scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Data", "Brinco", "Peso (kg)", "Observações")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "Peso (kg)":
                self.tree.column(col, width=100, anchor=CENTER)
            else:
                self.tree.column(col, width=150)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_combo_data(self):
        """Carrega dados"""
        animals = self.db_manager.select('animais', order_by='brinco')
        self.brinco_combo['values'] = [a['brinco'] for a in animals]
        self.brinco_data = {a['brinco']: a['id'] for a in animals}

    def load_weights(self):
        """Carrega pesagens"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        weights = self.db_manager.select('controle_peso', order_by='data_pesagem DESC')

        for weight in weights:
            values = (
                weight['id'],
                self.format_date_br(weight['data_pesagem']),
                weight['brinco'] or '',
                f"{weight['peso']:.1f}" if weight['peso'] else '',
                weight['observacoes'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        """Carrega pesagem selecionada"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        weight_id = item['values'][0]

        weights = self.db_manager.select('controle_peso', where_clause='id = ?', where_params=[weight_id])
        if not weights:
            return

        weight = weights[0]
        self.selected_id = weight['id']

        self.brinco_combo.set(weight['brinco'] or '')

        self.data_entry.delete(0, END)
        self.data_entry.insert(0, self.format_date_br(weight['data_pesagem']))

        self.peso_entry.delete(0, END)
        if weight['peso']:
            self.peso_entry.insert(0, str(weight['peso']))

        self.obs_entry.delete(0, END)
        if weight['observacoes']:
            self.obs_entry.insert(0, weight['observacoes'])

    def clear_form(self):
        """Limpa formulário"""
        self.selected_id = None
        self.brinco_combo.set('')
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.peso_entry.delete(0, END)
        self.obs_entry.delete(0, END)

    def save_weight(self):
        """Salva pesagem"""
        if not self.brinco_combo.get().strip():
            messagebox.showerror("Erro", "Informe o brinco do animal!")
            return

        if not self.peso_entry.get().strip():
            messagebox.showerror("Erro", "Informe o peso!")
            return

        try:
            peso = float(self.peso_entry.get().replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Peso inválido!")
            return

        data = {
            'brinco': self.brinco_combo.get().strip(),
            'animal_id': self.brinco_data.get(self.brinco_combo.get()),
            'data_pesagem': self.parse_date_br(self.data_entry.get()),
            'peso': peso,
            'observacoes': self.obs_entry.get().strip() or None
        }

        try:
            if self.selected_id:
                self.db_manager.update('controle_peso', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Pesagem atualizada com sucesso!")

                # Atualizar peso atual do animal
                if data['animal_id']:
                    self.db_manager.update('animais', {'peso_atual': peso}, 'id = ?', [data['animal_id']])
            else:
                self.db_manager.insert('controle_peso', data)
                messagebox.showinfo("Sucesso", "Pesagem registrada com sucesso!")

                # Atualizar peso atual do animal
                if data['animal_id']:
                    self.db_manager.update('animais', {'peso_atual': peso}, 'id = ?', [data['animal_id']])

            self.clear_form()
            self.load_weights()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_weight(self):
        """Exclui pesagem"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma pesagem para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta pesagem?"):
            try:
                self.db_manager.delete('controle_peso', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Pesagem excluída com sucesso!")
                self.clear_form()
                self.load_weights()
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
