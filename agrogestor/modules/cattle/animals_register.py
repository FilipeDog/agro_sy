"""
Cadastro de Animais - Padrão Unificado
Formulário e lista na mesma tela
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


class AnimalsRegisterWindow:
    """Janela de cadastro de animais com padrão unificado"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None

        self.create_widgets()
        self.load_combo_data()
        self.load_animals()

    def create_widgets(self):
        """Cria interface unificada - formulário + lista"""
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        # Título
        ttk.Label(main_container, text="Cadastro de Animais",
                 font=("Helvetica", 16, "bold")).pack(padx=20, pady=10, anchor=W)

        # Área de formulário
        form_frame = ttk.LabelFrame(main_container, text="Dados do Animal", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        # DADOS BÁSICOS
        row = 0
        # Linha 1
        ttk.Label(form_frame, text="Brinco:*").grid(row=row, column=0, sticky=W, pady=5)
        self.brinco_entry = ttk.Entry(form_frame, width=15)
        self.brinco_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Lote:").grid(row=row, column=2, sticky=W, pady=5, padx=(20,0))
        self.lote_entry = ttk.Entry(form_frame, width=15)
        self.lote_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Data Nasc.:").grid(row=row, column=4, sticky=W, pady=5, padx=(20,0))
        self.data_nasc_entry = ttk.Entry(form_frame, width=12)
        self.data_nasc_entry.grid(row=row, column=5, sticky=W, pady=5, padx=5)

        # Linha 2
        row += 1
        ttk.Label(form_frame, text="Tipo:*").grid(row=row, column=0, sticky=W, pady=5)
        self.tipo_combo = ttk.Combobox(form_frame, width=13, state="readonly")
        self.tipo_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Sexo:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20,0))
        self.sexo_combo = ttk.Combobox(form_frame, width=13, state="readonly", values=["Macho", "Fêmea"])
        self.sexo_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Raça:*").grid(row=row, column=4, sticky=W, pady=5, padx=(20,0))
        self.raca_combo = ttk.Combobox(form_frame, width=13, state="readonly")
        self.raca_combo.grid(row=row, column=5, sticky=W, pady=5, padx=5)

        # Linha 3
        row += 1
        ttk.Label(form_frame, text="Status:*").grid(row=row, column=0, sticky=W, pady=5)
        self.status_combo = ttk.Combobox(form_frame, width=13, state="readonly")
        self.status_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Pasto:").grid(row=row, column=2, sticky=W, pady=5, padx=(20,0))
        self.pasto_combo = ttk.Combobox(form_frame, width=13, state="readonly")
        self.pasto_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Peso Atual (kg):").grid(row=row, column=4, sticky=W, pady=5, padx=(20,0))
        self.peso_entry = ttk.Entry(form_frame, width=12)
        self.peso_entry.grid(row=row, column=5, sticky=W, pady=5, padx=5)

        # Linha 4 - Reprodução
        row += 1
        ttk.Label(form_frame, text="Pai (Brinco):").grid(row=row, column=0, sticky=W, pady=5)
        self.pai_combo = ttk.Combobox(form_frame, width=13, state="readonly")
        self.pai_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Mãe (Brinco):").grid(row=row, column=2, sticky=W, pady=5, padx=(20,0))
        self.mae_combo = ttk.Combobox(form_frame, width=13, state="readonly")
        self.mae_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)

        # Linha 5 - Observações
        row += 1
        ttk.Label(form_frame, text="Observações:").grid(row=row, column=0, sticky=NW, pady=5)
        self.obs_text = tk.Text(form_frame, width=60, height=3)
        self.obs_text.grid(row=row, column=1, columnspan=5, sticky=W+E, pady=5, padx=5)

        # Botões
        row += 1
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row, column=0, columnspan=6, pady=15)

        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_animal, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_animal, width=12).pack(side=LEFT, padx=5)

        # LISTA DE ANIMAIS
        list_frame = ttk.LabelFrame(main_container, text="Animais Cadastrados", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para busca
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(search_frame, text="Buscar:").pack(side=LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_animals())

        ttk.Button(search_frame, text="Limpar", command=self.clear_search).pack(side=LEFT, padx=5)
        ttk.Button(search_frame, text="Atualizar (F5)", command=self.load_animals).pack(side=LEFT, padx=5)

        # TreeView com scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("Brinco", "Lote", "Tipo", "Sexo", "Raça", "Status", "Pasto", "Peso", "Data Nasc.", "Idade", "Pai", "Mãe")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)
            if col in ["Brinco", "Lote", "Sexo", "Peso"]:
                self.tree.column(col, width=80, anchor=CENTER)
            elif col in ["Data Nasc.", "Idade"]:
                self.tree.column(col, width=100, anchor=CENTER)
            else:
                self.tree.column(col, width=120)

        self.tree.pack(fill=BOTH, expand=YES)

        # Duplo clique para editar
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_selected())

        # Atalhos de teclado
        self.parent.bind('<F5>', lambda e: self.load_animals())
        self.parent.bind('<Control-n>', lambda e: self.clear_form())
        self.parent.bind('<Control-s>', lambda e: self.save_animal())
        self.parent.bind('<Control-e>', lambda e: self.edit_selected())
        self.parent.bind('<Delete>', lambda e: self.delete_animal())

    def load_combo_data(self):
        """Carrega dados dos comboboxes"""
        # Tipos
        tipos = self.db_manager.select('tipo_animal', order_by='nome')
        self.tipo_combo['values'] = [t['nome'] for t in tipos]
        self.tipo_data = {t['nome']: t['id'] for t in tipos}

        # Raças
        racas = self.db_manager.select('raca', order_by='nome')
        self.raca_combo['values'] = [r['nome'] for r in racas]
        self.raca_data = {r['nome']: r['id'] for r in racas}

        # Status
        status = self.db_manager.select('status_animal', order_by='nome')
        self.status_combo['values'] = [s['nome'] for s in status]
        self.status_data = {s['nome']: s['id'] for s in status}

        # Pastos
        pastos = self.db_manager.select('pastos', order_by='nome')
        self.pasto_combo['values'] = [''] + [p['nome'] for p in pastos]
        self.pasto_data = {p['nome']: p['id'] for p in pastos}

        # Animais para pai/mãe
        machos = self.db_manager.select('animais', where_clause="sexo = 'Macho'", order_by='brinco')
        self.pai_combo['values'] = [''] + [m['brinco'] for m in machos]
        self.pai_data = {m['brinco']: m['id'] for m in machos}

        femeas = self.db_manager.select('animais', where_clause="sexo = 'Fêmea'", order_by='brinco')
        self.mae_combo['values'] = [''] + [f['brinco'] for f in femeas]
        self.mae_data = {f['brinco']: f['id'] for f in femeas}

    def load_animals(self):
        """Carrega lista de animais com busca"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca
        search_term = self.search_entry.get().strip()

        animals = self.db_manager.get_all_animals()

        for row in animals:
            # Converter sqlite3.Row para dict para poder usar .get()
            animal = dict(row)

            # Filtrar pela busca
            if search_term:
                search_lower = search_term.lower()
                if not any([
                    search_lower in str(animal.get('brinco', '')).lower(),
                    search_lower in str(animal.get('lote', '')).lower(),
                    search_lower in str(animal.get('tipo_nome', '')).lower(),
                    search_lower in str(animal.get('raca_nome', '')).lower(),
                    search_lower in str(animal.get('status_nome', '')).lower(),
                ]):
                    continue

            # Calcular idade
            idade = ""
            if animal.get('data_nascimento'):
                try:
                    nasc = datetime.strptime(animal['data_nascimento'], '%Y-%m-%d')
                    hoje = datetime.now()
                    meses = (hoje.year - nasc.year) * 12 + (hoje.month - nasc.month)
                    if meses < 12:
                        idade = f"{meses}m"
                    else:
                        anos = meses // 12
                        meses_resto = meses % 12
                        idade = f"{anos}a {meses_resto}m" if meses_resto > 0 else f"{anos}a"
                except:
                    pass

            # Buscar brincos de pai e mãe (já estão no schema como strings)
            pai_brinco = animal.get('brinco_pai', '') or ''
            mae_brinco = animal.get('brinco_mae', '') or ''

            values = (
                animal['brinco'],
                animal.get('lote', ''),
                animal.get('tipo_nome', ''),
                animal.get('sexo', ''),
                animal.get('raca_nome', ''),
                animal.get('status_nome', ''),
                animal.get('pasto_nome', ''),
                f"{animal['peso_atual']:.1f}" if animal.get('peso_atual') else '',
                self.format_date_br(animal['data_nascimento']) if animal.get('data_nascimento') else '',
                idade,
                pai_brinco,
                mae_brinco
            )
            self.tree.insert('', END, values=values, tags=(animal['id'],))

    def edit_selected(self):
        """Método unificado para edição por duplo clique ou Ctrl+E"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um animal na lista!")
            return

        item = self.tree.item(selection[0])
        animal_id = item['tags'][0]

        animals = self.db_manager.select('animais', where_clause='id = ?', where_params=[animal_id])
        if not animals:
            return

        animal = animals[0]
        self.selected_id = animal['id']

        # Preencher formulário
        self.brinco_entry.delete(0, END)
        self.brinco_entry.insert(0, animal['brinco'])

        self.lote_entry.delete(0, END)
        if animal.get('lote'):
            self.lote_entry.insert(0, animal['lote'])

        # Tipo
        if animal.get('tipo_id'):
            tipo = self.db_manager.select('tipo_animal', where_clause='id = ?', where_params=[animal['tipo_id']])
            if tipo:
                self.tipo_combo.set(tipo[0]['nome'])

        # Sexo
        if animal.get('sexo'):
            self.sexo_combo.set(animal['sexo'])

        # Raça
        if animal.get('raca_id'):
            raca = self.db_manager.select('raca', where_clause='id = ?', where_params=[animal['raca_id']])
            if raca:
                self.raca_combo.set(raca[0]['nome'])

        # Status
        if animal.get('status_id'):
            status = self.db_manager.select('status_animal', where_clause='id = ?', where_params=[animal['status_id']])
            if status:
                self.status_combo.set(status[0]['nome'])

        # Pasto
        self.pasto_combo.set('')
        if animal.get('pasto_id'):
            pasto = self.db_manager.select('pastos', where_clause='id = ?', where_params=[animal['pasto_id']])
            if pasto:
                self.pasto_combo.set(pasto[0]['nome'])

        # Peso
        self.peso_entry.delete(0, END)
        if animal.get('peso_atual'):
            self.peso_entry.insert(0, str(animal['peso_atual']))

        # Data nascimento
        self.data_nasc_entry.delete(0, END)
        if animal.get('data_nascimento'):
            self.data_nasc_entry.insert(0, self.format_date_br(animal['data_nascimento']))

        # Pai (brinco_pai é string no schema)
        self.pai_combo.set('')
        if animal.get('brinco_pai'):
            self.pai_combo.set(animal['brinco_pai'])

        # Mãe (brinco_mae é string no schema)
        self.mae_combo.set('')
        if animal.get('brinco_mae'):
            self.mae_combo.set(animal['brinco_mae'])

        # Observações
        self.obs_text.delete('1.0', END)
        if animal.get('observacao'):
            self.obs_text.insert('1.0', animal['observacao'])

        messagebox.showinfo("Editar", "Registro carregado para edicao! Modifique os dados e clique em Salvar.")

    def clear_form(self):
        """Limpa formulário"""
        self.selected_id = None
        self.brinco_entry.delete(0, END)
        self.lote_entry.delete(0, END)
        self.tipo_combo.set('')
        self.sexo_combo.set('')
        self.raca_combo.set('')
        self.status_combo.set('')
        self.pasto_combo.set('')
        self.peso_entry.delete(0, END)
        self.data_nasc_entry.delete(0, END)
        self.pai_combo.set('')
        self.mae_combo.set('')
        self.obs_text.delete('1.0', END)

    def clear_search(self):
        """Limpa busca"""
        self.search_entry.delete(0, END)
        self.load_animals()

    def save_animal(self):
        """Salva animal"""
        if not self.brinco_entry.get().strip():
            messagebox.showerror("Erro", "Informe o brinco!")
            return

        if not self.tipo_combo.get():
            messagebox.showerror("Erro", "Selecione o tipo!")
            return

        if not self.sexo_combo.get():
            messagebox.showerror("Erro", "Selecione o sexo!")
            return

        if not self.raca_combo.get():
            messagebox.showerror("Erro", "Selecione a raça!")
            return

        if not self.status_combo.get():
            messagebox.showerror("Erro", "Selecione o status!")
            return

        data = {
            'brinco': self.brinco_entry.get().strip(),
            'lote': self.lote_entry.get().strip() or None,
            'tipo_id': self.tipo_data.get(self.tipo_combo.get()),
            'sexo': self.sexo_combo.get(),
            'raca_id': self.raca_data.get(self.raca_combo.get()),
            'status_id': self.status_data.get(self.status_combo.get()),
            'pasto_id': self.pasto_data.get(self.pasto_combo.get()) if self.pasto_combo.get() else None,
            'peso_atual': float(self.peso_entry.get().replace(',', '.')) if self.peso_entry.get().strip() else None,
            'data_nascimento': self.parse_date_br(self.data_nasc_entry.get()),
            'brinco_pai': self.pai_combo.get() if self.pai_combo.get() else None,
            'brinco_mae': self.mae_combo.get() if self.mae_combo.get() else None,
            'observacao': self.obs_text.get('1.0', END).strip() or None
        }

        try:
            if self.selected_id:
                self.db_manager.update('animais', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Animal atualizado com sucesso!")
            else:
                self.db_manager.insert('animais', data)
                messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")

            self.clear_form()
            self.load_animals()
            self.load_combo_data()  # Recarregar para atualizar pai/mãe

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def delete_animal(self):
        """Exclui animal"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um animal para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este animal?"):
            try:
                self.db_manager.delete('animais', 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Animal excluído com sucesso!")
                self.clear_form()
                self.load_animals()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    def format_date_br(self, date_str):
        """Converte data SQL para BR"""
        if not date_str:
            return ''
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            return date_str

    def parse_date_br(self, date_str):
        """Converte data BR para SQL"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        except:
            return None
