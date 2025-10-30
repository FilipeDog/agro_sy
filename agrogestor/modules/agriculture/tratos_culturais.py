"""
Tratos Culturais - Bananal
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


class TratosCulturaisWindow:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None
        self.create_widgets()
        self.load_talhoes()
        self.load_tratos()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Tratos Culturais", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        form_frame = ttk.LabelFrame(main_container, text="Registro de Trato Cultural", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Talhão:*").grid(row=row, column=0, sticky=W, pady=5)
        self.talhao_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.talhao_combo.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        ttk.Label(form_frame, text="Tipo:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.tipo_combo = ttk.Combobox(form_frame, width=20, state="readonly",
            values=["Adubação", "Irrigação", "Desbaste", "Desfolha", "Controle de Pragas", "Controle de Doenças", "Outro"])
        self.tipo_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Data:*").grid(row=row, column=0, sticky=W, pady=5)
        self.data_entry = ttk.Entry(form_frame, width=15)
        self.data_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        ttk.Label(form_frame, text="Produto:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.produto_entry = ttk.Entry(form_frame, width=25)
        self.produto_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Quantidade:").grid(row=row, column=0, sticky=W, pady=5)
        self.quantidade_entry = ttk.Entry(form_frame, width=15)
        self.quantidade_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Unidade:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.unidade_combo = ttk.Combobox(form_frame, width=10, state="readonly",
            values=["kg", "L", "ml", "g", "unidade", "saco"])
        self.unidade_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.unidade_combo.set("kg")

        row += 1
        ttk.Label(form_frame, text="Custo:").grid(row=row, column=0, sticky=W, pady=5)
        self.custo_entry = ttk.Entry(form_frame, width=15)
        self.custo_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Próxima Aplicação:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.proxima_entry = ttk.Entry(form_frame, width=15)
        self.proxima_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=4, pady=15)
        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_trato, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_trato, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Tratos Registrados", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        columns = ("ID", "Data", "Talhão", "Tipo", "Produto", "Qtd", "Un", "Custo", "Próxima")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col in ["Qtd", "Un"]:
                self.tree.column(col, width=60, anchor=CENTER)
            else:
                self.tree.column(col, width=100)

        vsb = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_talhoes(self):
        talhoes = self.db_manager.select('talhoes', order_by='codigo')
        talhao_list = [f"{t['codigo']} - {t['nome']}" for t in talhoes]
        self.talhao_combo['values'] = talhao_list

    def load_tratos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sql = """
            SELECT tc.*, t.codigo as talhao_codigo
            FROM tratos_culturais tc
            LEFT JOIN talhoes t ON tc.talhao_id = t.id
            ORDER BY tc.data_execucao DESC
            LIMIT 100
        """
        tratos = self.db_manager.execute_query(sql)

        for tr in tratos:
            values = (
                tr['id'],
                self.format_date_br(tr['data_execucao']),
                tr['talhao_codigo'],
                tr['tipo_trato'],
                tr['produto_utilizado'] or '',
                str(tr['quantidade']) if tr['quantidade'] else '',
                tr['unidade'] or '',
                f"R$ {tr['custo']:.2f}" if tr['custo'] else '',
                self.format_date_br(tr['proxima_aplicacao']) if tr['proxima_aplicacao'] else ''
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        # Similar ao método anterior - implementar se necessário
        pass

    def clear_form(self):
        self.selected_id = None
        self.talhao_combo.set('')
        self.tipo_combo.set('')
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.produto_entry.delete(0, END)
        self.quantidade_entry.delete(0, END)
        self.unidade_combo.set("kg")
        self.custo_entry.delete(0, END)
        self.proxima_entry.delete(0, END)

    def save_trato(self):
        if not self.talhao_combo.get() or not self.tipo_combo.get():
            messagebox.showerror("Erro", "Informe o talhão e tipo de trato!")
            return

        codigo = self.talhao_combo.get().split(' - ')[0]
        talhao = self.db_manager.select('talhoes', where_clause='codigo = ?', where_params=[codigo])
        if not talhao:
            messagebox.showerror("Erro", "Talhão não encontrado!")
            return

        try:
            data = {
                'talhao_id': talhao[0]['id'],
                'tipo_trato': self.tipo_combo.get(),
                'data_execucao': self.parse_date_br(self.data_entry.get()),
                'produto_utilizado': self.produto_entry.get().strip() or None,
                'quantidade': float(self.quantidade_entry.get().replace(',', '.')) if self.quantidade_entry.get() else None,
                'unidade': self.unidade_combo.get() if self.quantidade_entry.get() else None,
                'custo': float(self.custo_entry.get().replace(',', '.')) if self.custo_entry.get() else None,
                'proxima_aplicacao': self.parse_date_br(self.proxima_entry.get())
            }

            if self.selected_id:
                self.db_manager.update('tratos_culturais', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Trato atualizado!")
            else:
                self.db_manager.insert('tratos_culturais', data)
                messagebox.showinfo("Sucesso", "Trato registrado!")

            self.clear_form()
            self.load_tratos()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_trato(self):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um trato!")
            return

        if messagebox.askyesno("Confirmar", "Deseja excluir este trato?"):
            try:
                self.db_manager.delete('tratos_culturais', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Trato excluído!")
                self.clear_form()
                self.load_tratos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")

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
