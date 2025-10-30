"""
Registro de Colheitas de Banana
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


class ColheitasBananaWindow:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None
        self.create_widgets()
        self.load_talhoes()
        self.load_funcionarios()
        self.load_colheitas()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Colheitas de Banana", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        form_frame = ttk.LabelFrame(main_container, text="Registro de Colheita", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Talhão:*").grid(row=row, column=0, sticky=W, pady=5)
        self.talhao_combo = ttk.Combobox(form_frame, width=30, state="readonly")
        self.talhao_combo.grid(row=row, column=1, columnspan=2, sticky=W+E, pady=5, padx=5)

        ttk.Label(form_frame, text="Data:*").grid(row=row, column=3, sticky=W, pady=5, padx=(20, 0))
        self.data_entry = ttk.Entry(form_frame, width=15)
        self.data_entry.grid(row=row, column=4, sticky=W, pady=5, padx=5)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        ttk.Label(form_frame, text="Qtd Total (kg):*").grid(row=row, column=0, sticky=W, pady=5)
        self.qtd_kg_entry = ttk.Entry(form_frame, width=15)
        self.qtd_kg_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Caixas:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.caixas_entry = ttk.Entry(form_frame, width=10)
        self.caixas_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Peso Médio Cacho:").grid(row=row, column=4, sticky=W, pady=5)
        self.peso_cacho_entry = ttk.Entry(form_frame, width=10)
        self.peso_cacho_entry.grid(row=row, column=5, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Classificação A (kg):").grid(row=row, column=0, sticky=W, pady=5)
        self.class_a_entry = ttk.Entry(form_frame, width=15)
        self.class_a_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.class_a_entry.insert(0, "0")

        ttk.Label(form_frame, text="Classe B (kg):").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.class_b_entry = ttk.Entry(form_frame, width=15)
        self.class_b_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.class_b_entry.insert(0, "0")

        ttk.Label(form_frame, text="Descarte (kg):").grid(row=row, column=4, sticky=W, pady=5)
        self.class_c_entry = ttk.Entry(form_frame, width=15)
        self.class_c_entry.grid(row=row, column=5, sticky=W, pady=5, padx=5)
        self.class_c_entry.insert(0, "0")

        row += 1
        ttk.Label(form_frame, text="Custo Colheita:").grid(row=row, column=0, sticky=W, pady=5)
        self.custo_entry = ttk.Entry(form_frame, width=15)
        self.custo_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Responsável:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.responsavel_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.responsavel_combo.grid(row=row, column=3, columnspan=2, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Destino:").grid(row=row, column=0, sticky=W, pady=5)
        self.destino_combo = ttk.Combobox(form_frame, width=20, state="readonly",
            values=["Venda", "Consumo Próprio", "Doação", "Outro"])
        self.destino_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.destino_combo.set("Venda")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=6, pady=15)
        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_colheita, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_colheita, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Colheitas Registradas", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        columns = ("ID", "Data", "Talhão", "Qtd (kg)", "Classe A", "Classe B", "Descarte", "Destino")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            else:
                self.tree.column(col, width=100, anchor=CENTER)

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

    def load_funcionarios(self):
        funcs = self.db_manager.select('funcionarios', where_clause='ativo = 1', order_by='nome')
        func_list = [""] + [f['nome'] for f in funcs]
        self.responsavel_combo['values'] = func_list

    def load_colheitas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sql = """
            SELECT c.*, t.codigo as talhao_codigo, t.nome as talhao_nome
            FROM colheitas_banana c
            LEFT JOIN talhoes t ON c.talhao_id = t.id
            ORDER BY c.data_colheita DESC
            LIMIT 100
        """
        colheitas = self.db_manager.execute_query(sql)

        for c in colheitas:
            values = (
                c['id'],
                self.format_date_br(c['data_colheita']),
                c['talhao_codigo'],
                f"{c['quantidade_kg']:.2f}",
                f"{c['classificacao_a_kg']:.2f}",
                f"{c['classificacao_b_kg']:.2f}",
                f"{c['classificacao_c_kg']:.2f}",
                c['destino'] or ''
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        colheita_id = item['values'][0]

        colheitas = self.db_manager.select('colheitas_banana', where_clause='id = ?', where_params=[colheita_id])
        if not colheitas:
            return

        c = colheitas[0]
        self.selected_id = c['id']

        # Carregar talhão
        talhao = self.db_manager.select('talhoes', where_clause='id = ?', where_params=[c['talhao_id']])
        if talhao:
            self.talhao_combo.set(f"{talhao[0]['codigo']} - {talhao[0]['nome']}")

        self.data_entry.delete(0, END)
        self.data_entry.insert(0, self.format_date_br(c['data_colheita']))

        self.qtd_kg_entry.delete(0, END)
        self.qtd_kg_entry.insert(0, str(c['quantidade_kg']))

        self.caixas_entry.delete(0, END)
        if c['quantidade_caixas']:
            self.caixas_entry.insert(0, str(c['quantidade_caixas']))

        self.peso_cacho_entry.delete(0, END)
        if c['peso_medio_cacho']:
            self.peso_cacho_entry.insert(0, str(c['peso_medio_cacho']))

        self.class_a_entry.delete(0, END)
        self.class_a_entry.insert(0, str(c['classificacao_a_kg']))

        self.class_b_entry.delete(0, END)
        self.class_b_entry.insert(0, str(c['classificacao_b_kg']))

        self.class_c_entry.delete(0, END)
        self.class_c_entry.insert(0, str(c['classificacao_c_kg']))

        self.custo_entry.delete(0, END)
        if c['custo_colheita']:
            self.custo_entry.insert(0, str(c['custo_colheita']))

        if c['destino']:
            self.destino_combo.set(c['destino'])

    def clear_form(self):
        self.selected_id = None
        self.talhao_combo.set('')
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.qtd_kg_entry.delete(0, END)
        self.caixas_entry.delete(0, END)
        self.peso_cacho_entry.delete(0, END)
        self.class_a_entry.delete(0, END)
        self.class_a_entry.insert(0, "0")
        self.class_b_entry.delete(0, END)
        self.class_b_entry.insert(0, "0")
        self.class_c_entry.delete(0, END)
        self.class_c_entry.insert(0, "0")
        self.custo_entry.delete(0, END)
        self.responsavel_combo.set('')
        self.destino_combo.set("Venda")

    def save_colheita(self):
        if not self.talhao_combo.get() or not self.qtd_kg_entry.get():
            messagebox.showerror("Erro", "Informe o talhão e quantidade!")
            return

        # Buscar ID do talhão
        codigo = self.talhao_combo.get().split(' - ')[0]
        talhao = self.db_manager.select('talhoes', where_clause='codigo = ?', where_params=[codigo])
        if not talhao:
            messagebox.showerror("Erro", "Talhão não encontrado!")
            return

        try:
            data = {
                'talhao_id': talhao[0]['id'],
                'data_colheita': self.parse_date_br(self.data_entry.get()),
                'quantidade_kg': float(self.qtd_kg_entry.get().replace(',', '.')),
                'quantidade_caixas': int(self.caixas_entry.get()) if self.caixas_entry.get() else None,
                'peso_medio_cacho': float(self.peso_cacho_entry.get().replace(',', '.')) if self.peso_cacho_entry.get() else None,
                'classificacao_a_kg': float(self.class_a_entry.get().replace(',', '.')),
                'classificacao_b_kg': float(self.class_b_entry.get().replace(',', '.')),
                'classificacao_c_kg': float(self.class_c_entry.get().replace(',', '.')),
                'custo_colheita': float(self.custo_entry.get().replace(',', '.')) if self.custo_entry.get() else None,
                'destino': self.destino_combo.get()
            }

            if self.selected_id:
                self.db_manager.update('colheitas_banana', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Colheita atualizada!")
            else:
                self.db_manager.insert('colheitas_banana', data)
                messagebox.showinfo("Sucesso", "Colheita registrada!")

            self.clear_form()
            self.load_colheitas()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_colheita(self):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione uma colheita!")
            return

        if messagebox.askyesno("Confirmar", "Deseja excluir esta colheita?"):
            try:
                self.db_manager.delete('colheitas_banana', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Colheita excluída!")
                self.clear_form()
                self.load_colheitas()
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
