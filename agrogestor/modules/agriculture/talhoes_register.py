"""
Cadastro de Talhões/Lotes de Bananal
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


class TalhoesRegisterWindow:
    """Janela de cadastro de talhões"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None
        self.create_widgets()
        self.load_variedades()
        self.load_talhoes()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Cadastro de Talhões", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        # Frame com abas
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Aba 1: Formulário
        form_tab = ttk.Frame(notebook)
        notebook.add(form_tab, text="Dados do Talhão")

        form_frame = ttk.LabelFrame(form_tab, text="Informações do Talhão", padding=20)
        form_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        row = 0
        ttk.Label(form_frame, text="Código:*").grid(row=row, column=0, sticky=W, pady=5)
        self.codigo_entry = ttk.Entry(form_frame, width=20)
        self.codigo_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Nome:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Localização:").grid(row=row, column=0, sticky=W, pady=5)
        self.localizacao_entry = ttk.Entry(form_frame, width=40)
        self.localizacao_entry.grid(row=row, column=1, columnspan=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="àrea (ha):*").grid(row=row, column=0, sticky=W, pady=5)
        self.area_entry = ttk.Entry(form_frame, width=15)
        self.area_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Variedade:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.variedade_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.variedade_combo.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Data de Plantio:").grid(row=row, column=0, sticky=W, pady=5)
        self.data_plantio_entry = ttk.Entry(form_frame, width=15)
        self.data_plantio_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        ttk.Label(form_frame, text="(DD/MM/AAAA)").grid(row=row, column=2, sticky=W, pady=5)

        row += 1
        ttk.Label(form_frame, text="Espaçamento:").grid(row=row, column=0, sticky=W, pady=5)
        self.espacamento_entry = ttk.Entry(form_frame, width=15)
        self.espacamento_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        ttk.Label(form_frame, text="Ex: 3m x 2m").grid(row=row, column=2, sticky=W, pady=5)

        ttk.Label(form_frame, text="Densidade (plantas/ha):").grid(row=row, column=3, sticky=E, pady=5)
        self.densidade_entry = ttk.Entry(form_frame, width=15)
        self.densidade_entry.grid(row=row, column=4, sticky=W, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Situação:").grid(row=row, column=0, sticky=W, pady=5)
        self.situacao_combo = ttk.Combobox(form_frame, width=15, state="readonly",
            values=["Ativo", "Colhido", "Replantio", "Inativo"])
        self.situacao_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.situacao_combo.set("Ativo")

        row += 1
        ttk.Label(form_frame, text="Observações:").grid(row=row, column=0, sticky=W+N, pady=5)
        self.obs_text = tk.Text(form_frame, height=4, width=40)
        self.obs_text.grid(row=row, column=1, columnspan=4, sticky=W+E, pady=5, padx=5)

        form_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=5, pady=15)
        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_talhao, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_talhao, width=12).pack(side=LEFT, padx=5)

        # Aba 2: Lista de talhões
        list_tab = ttk.Frame(notebook)
        notebook.add(list_tab, text="Talhões Cadastrados")

        list_frame = ttk.Frame(list_tab, padding=10)
        list_frame.pack(fill=BOTH, expand=YES)

        columns = ("ID", "Código", "Nome", "àrea (ha)", "Variedade", "Data de Plantio", "Situação")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col == "àrea (ha)":
                self.tree.column(col, width=80, anchor=CENTER)
            else:
                self.tree.column(col, width=120)

        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_variedades(self):
        variedades = self.db_manager.select('variedades_banana', order_by='nome')
        var_list = [v['nome'] for v in variedades]
        self.variedade_combo['values'] = var_list
        if var_list:
            self.variedade_combo.set(var_list[0])

    def load_talhoes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sql = """
            SELECT t.*, v.nome as variedade_nome
            FROM talhoes t
            LEFT JOIN variedades_banana v ON t.variedade_id = v.id
            ORDER BY t.codigo
        """
        talhoes = self.db_manager.execute_query(sql)

        for t in talhoes:
            values = (
                t['id'],
                t['codigo'],
                t['nome'],
                f"{t['area_hectares']:.2f}",
                t['variedade_nome'] or '',
                self.format_date_br(t['data_plantio']) if t['data_plantio'] else '',
                t['situacao']
            )
            self.tree.insert('', END, values=values)

    def load_selected(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        talhao_id = item['values'][0]

        talhoes = self.db_manager.select('talhoes', where_clause='id = ?', where_params=[talhao_id])
        if not talhoes:
            return

        t = talhoes[0]
        self.selected_id = t['id']

        self.codigo_entry.delete(0, END)
        self.codigo_entry.insert(0, t['codigo'])

        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, t['nome'])

        self.localizacao_entry.delete(0, END)
        if t['localizacao']:
            self.localizacao_entry.insert(0, t['localizacao'])

        self.area_entry.delete(0, END)
        self.area_entry.insert(0, str(t['area_hectares']))

        if t['variedade_id']:
            var = self.db_manager.select('variedades_banana', where_clause='id = ?', where_params=[t['variedade_id']])
            if var:
                self.variedade_combo.set(var[0]['nome'])

        self.data_plantio_entry.delete(0, END)
        if t['data_plantio']:
            self.data_plantio_entry.insert(0, self.format_date_br(t['data_plantio']))

        self.espacamento_entry.delete(0, END)
        if t['espacamento']:
            self.espacamento_entry.insert(0, t['espacamento'])

        self.densidade_entry.delete(0, END)
        if t['densidade_plantas_ha']:
            self.densidade_entry.insert(0, str(t['densidade_plantas_ha']))

        self.situacao_combo.set(t['situacao'])

        self.obs_text.delete('1.0', END)
        if t['observacoes']:
            self.obs_text.insert('1.0', t['observacoes'])

    def clear_form(self):
        self.selected_id = None
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.localizacao_entry.delete(0, END)
        self.area_entry.delete(0, END)
        self.data_plantio_entry.delete(0, END)
        self.espacamento_entry.delete(0, END)
        self.densidade_entry.delete(0, END)
        self.situacao_combo.set("Ativo")
        self.obs_text.delete('1.0', END)

    def save_talhao(self):
        if not self.codigo_entry.get().strip() or not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "Informe o código e nome do talhão!")
            return

        try:
            area = float(self.area_entry.get().replace(',', '.'))
        except:
            messagebox.showerror("Erro", "àrea inválida!")
            return

        # Buscar ID da variedade
        variedade_id = None
        if self.variedade_combo.get():
            var = self.db_manager.select('variedades_banana', where_clause='nome = ?', 
                where_params=[self.variedade_combo.get()])
            if var:
                variedade_id = var[0]['id']

        densidade = None
        if self.densidade_entry.get().strip():
            try:
                densidade = int(self.densidade_entry.get())
            except:
                pass

        data = {
            'codigo': self.codigo_entry.get().strip(),
            'nome': self.nome_entry.get().strip(),
            'localizacao': self.localizacao_entry.get().strip() or None,
            'area_hectares': area,
            'variedade_id': variedade_id,
            'data_plantio': self.parse_date_br(self.data_plantio_entry.get()),
            'espacamento': self.espacamento_entry.get().strip() or None,
            'densidade_plantas_ha': densidade,
            'situacao': self.situacao_combo.get(),
            'observacoes': self.obs_text.get('1.0', END).strip() or None
        }

        try:
            if self.selected_id:
                self.db_manager.update('talhoes', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Talhão atualizado!")
            else:
                self.db_manager.insert('talhoes', data)
                messagebox.showinfo("Sucesso", "Talhão cadastrado!")

            self.clear_form()
            self.load_talhoes()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_talhao(self):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um talhão!")
            return

        if messagebox.askyesno("Confirmar", "Deseja excluir este talhão?"):
            try:
                self.db_manager.delete('talhoes', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Talhão excluído!")
                self.clear_form()
                self.load_talhoes()
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
