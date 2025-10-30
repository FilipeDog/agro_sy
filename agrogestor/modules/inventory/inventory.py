"""
Gestão de Inventário
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


class InventoryWindow:
    """Janela de gestão de inventário"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_id = None
        self.create_widgets()
        self.load_items()

    def create_widgets(self):
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=YES)

        ttk.Label(main_container, text="Inventário", font=("Helvetica", 16, "bold")).pack(padx=20, pady=10)

        form_frame = ttk.LabelFrame(main_container, text="Item do Inventário", padding=20)
        form_frame.pack(fill=X, padx=20, pady=10)

        row = 0
        ttk.Label(form_frame, text="Código:").grid(row=row, column=0, sticky=W, pady=5)
        self.codigo_entry = ttk.Entry(form_frame, width=20)
        self.codigo_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        ttk.Label(form_frame, text="Nome:*").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=row, column=3, sticky=W+E, pady=5, padx=5)

        row += 1
        ttk.Label(form_frame, text="Categoria:").grid(row=row, column=0, sticky=W, pady=5)
        self.categoria_combo = ttk.Combobox(form_frame, width=18, state="readonly",
            values=["Medicamentos", "Insumos", "Ferramentas", "Equipamentos", "Alimentos"])
        self.categoria_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.categoria_combo.set("Insumos")

        ttk.Label(form_frame, text="Unidade:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.unidade_combo = ttk.Combobox(form_frame, width=15, state="readonly",
            values=["kg", "L", "unidade", "saco", "caixa", "ml", "g"])
        self.unidade_combo.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.unidade_combo.set("unidade")

        row += 1
        ttk.Label(form_frame, text="Estoque Mínimo:").grid(row=row, column=0, sticky=W, pady=5)
        self.estoque_min_entry = ttk.Entry(form_frame, width=10)
        self.estoque_min_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        self.estoque_min_entry.insert(0, "0")

        ttk.Label(form_frame, text="Valor Unitário:").grid(row=row, column=2, sticky=W, pady=5, padx=(20, 0))
        self.valor_entry = ttk.Entry(form_frame, width=15)
        self.valor_entry.grid(row=row, column=3, sticky=W, pady=5, padx=5)
        self.valor_entry.insert(0, "0.00")

        form_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=4, pady=15)
        ttk.Button(btn_frame, text="Novo", command=self.clear_form, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self.save_item, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_item, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Entrada/Saída", command=self.show_movement, width=15).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Histórico", command=self.show_history, width=12).pack(side=LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_container, text="Itens do Inventário", padding=20)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Frame para TreeView e scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        columns = ("ID", "Código", "Nome", "Categoria", "Estoque Atual", "Est. Mínimo", "Unidade", "Valor Unit.")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10,
                                yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor=CENTER)
            elif col in ["Estoque Atual", "Est. Mínimo"]:
                self.tree.column(col, width=100, anchor=CENTER)
            else:
                self.tree.column(col, width=120)

        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind('<Double-1>', lambda e: self.load_selected())

    def load_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        items = self.db_manager.select('inventario_itens', where_clause='ativo = 1', order_by='nome')

        for it in items:
            # Marcar em vermelho se estoque baixo
            estoque_atual = it['estoque_atual'] or 0
            estoque_minimo = it['estoque_minimo'] or 0
            
            values = (
                it['id'],
                it['codigo'] or '',
                it['nome'],
                it['categoria'] or '',
                f"{estoque_atual:.2f}",
                f"{estoque_minimo:.2f}",
                it['unidade'] or '',
                f"R$ {it['valor_unitario']:,.2f}" if it['valor_unitario'] else ''
            )
            item_id = self.tree.insert('', END, values=values)
            
            # Destacar itens com estoque baixo
            if estoque_atual <= estoque_minimo:
                self.tree.item(item_id, tags=('low_stock',))

        self.tree.tag_configure('low_stock', background='#ffcccc')

    def load_selected(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        item_id = item['values'][0]

        items = self.db_manager.select('inventario_itens', where_clause='id = ?', where_params=[item_id])
        if not items:
            return

        it = items[0]
        self.selected_id = it['id']

        self.codigo_entry.delete(0, END)
        if it['codigo']:
            self.codigo_entry.insert(0, it['codigo'])

        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, it['nome'])

        if it['categoria']:
            self.categoria_combo.set(it['categoria'])

        if it['unidade']:
            self.unidade_combo.set(it['unidade'])

        self.estoque_min_entry.delete(0, END)
        self.estoque_min_entry.insert(0, str(it['estoque_minimo'] or 0))

        self.valor_entry.delete(0, END)
        self.valor_entry.insert(0, str(it['valor_unitario'] or 0))

    def clear_form(self):
        self.selected_id = None
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.categoria_combo.set("Insumos")
        self.unidade_combo.set("unidade")
        self.estoque_min_entry.delete(0, END)
        self.estoque_min_entry.insert(0, "0")
        self.valor_entry.delete(0, END)
        self.valor_entry.insert(0, "0.00")

    def save_item(self):
        if not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "Informe o nome do item!")
            return

        try:
            estoque_min = float(self.estoque_min_entry.get().replace(',', '.'))
            valor = float(self.valor_entry.get().replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
            return

        data = {
            'codigo': self.codigo_entry.get().strip() or None,
            'nome': self.nome_entry.get().strip(),
            'categoria': self.categoria_combo.get(),
            'unidade': self.unidade_combo.get(),
            'estoque_minimo': estoque_min,
            'valor_unitario': valor,
            'ativo': 1
        }

        try:
            if self.selected_id:
                self.db_manager.update('inventario_itens', data, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Item atualizado!")
            else:
                data['estoque_atual'] = 0
                self.db_manager.insert('inventario_itens', data)
                messagebox.showinfo("Sucesso", "Item cadastrado!")

            self.clear_form()
            self.load_items()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {str(e)}")

    def delete_item(self):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um item!")
            return

        if messagebox.askyesno("Confirmar", "Deseja inativar este item?"):
            try:
                self.db_manager.update('inventario_itens', {'ativo': 0}, 'id = ?', [self.selected_id])
                messagebox.showinfo("Sucesso", "Item inativado!")
                self.clear_form()
                self.load_items()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")

    def show_movement(self):
        """Mostra janela de entrada/saída de estoque"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um item para movimentar!")
            return

        # Buscar item selecionado
        items = self.db_manager.select('inventario_itens', where_clause='id = ?', where_params=[self.selected_id])
        if not items:
            return

        item = items[0]

        # Criar janela de movimentação
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Movimentar Estoque - {item['nome']}")
        dialog.geometry("500x400")
        dialog.transient(self.parent)
        dialog.grab_set()

        # Cabeçalho
        header_frame = ttk.Frame(dialog, padding=10)
        header_frame.pack(fill=X)

        ttk.Label(header_frame, text=f"Item: {item['nome']}", font=("Helvetica", 12, "bold")).pack(anchor=W)
        ttk.Label(header_frame, text=f"Estoque Atual: {item['estoque_atual']:.2f} {item['unidade']}",
                 font=("Helvetica", 10)).pack(anchor=W)

        # Formulário
        form_frame = ttk.LabelFrame(dialog, text="Dados da Movimentação", padding=20)
        form_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        row = 0
        # Tipo
        ttk.Label(form_frame, text="Tipo:*").grid(row=row, column=0, sticky=W, pady=5)
        tipo_combo = ttk.Combobox(form_frame, width=25, state="readonly", values=["Entrada", "Saída"])
        tipo_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        tipo_combo.set("Entrada")

        row += 1
        # Data
        ttk.Label(form_frame, text="Data:*").grid(row=row, column=0, sticky=W, pady=5)
        data_entry = ttk.Entry(form_frame, width=27)
        data_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        row += 1
        # Quantidade
        ttk.Label(form_frame, text="Quantidade:*").grid(row=row, column=0, sticky=W, pady=5)
        qtd_entry = ttk.Entry(form_frame, width=27)
        qtd_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        row += 1
        # Valor Unitário
        ttk.Label(form_frame, text="Valor Unitário:").grid(row=row, column=0, sticky=W, pady=5)
        valor_entry = ttk.Entry(form_frame, width=27)
        valor_entry.grid(row=row, column=1, sticky=W, pady=5, padx=5)

        row += 1
        # Motivo
        ttk.Label(form_frame, text="Motivo/Observação:").grid(row=row, column=0, sticky=W+N, pady=5)
        motivo_text = tk.Text(form_frame, height=4, width=30)
        motivo_text.grid(row=row, column=1, sticky=W+E, pady=5, padx=5)

        def salvar_movimentacao():
            """Salva movimentação"""
            if not tipo_combo.get():
                messagebox.showerror("Erro", "Selecione o tipo!")
                return

            if not qtd_entry.get().strip():
                messagebox.showerror("Erro", "Informe a quantidade!")
                return

            try:
                qtd = float(qtd_entry.get().replace(',', '.'))
                if qtd <= 0:
                    messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                    return
            except:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return

            # Verificar saída maior que estoque
            if tipo_combo.get() == "Saída" and qtd > item['estoque_atual']:
                messagebox.showerror("Erro", f"Quantidade de saída ({qtd}) é maior que o estoque atual ({item['estoque_atual']})!")
                return

            # Calcular novo saldo
            saldo_anterior = item['estoque_atual']
            if tipo_combo.get() == "Entrada":
                saldo_novo = saldo_anterior + qtd
            else:
                saldo_novo = saldo_anterior - qtd

            # Valor unitário
            valor_unit = None
            if valor_entry.get().strip():
                try:
                    valor_unit = float(valor_entry.get().replace(',', '.'))
                except:
                    pass

            # Salvar movimentação
            try:
                # Registrar movimentação
                mov_data = {
                    'item_id': item['id'],
                    'tipo': tipo_combo.get(),
                    'quantidade': qtd,
                    'valor_unitario': valor_unit,
                    'data': self.parse_date_br(data_entry.get()),
                    'motivo': motivo_text.get('1.0', END).strip() or None,
                    'saldo_anterior': saldo_anterior,
                    'saldo_novo': saldo_novo
                }
                self.db_manager.insert('movimentacoes_inventario', mov_data)

                # Atualizar estoque do item
                self.db_manager.update('inventario_itens',
                    {'estoque_atual': saldo_novo},
                    'id = ?', [item['id']])

                messagebox.showinfo("Sucesso", f"Movimentação registrada com sucesso!\nNovo estoque: {saldo_novo:.2f}")
                dialog.destroy()
                self.load_items()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Salvar", command=salvar_movimentacao, width=12).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=12).pack(side=LEFT, padx=5)

    def show_history(self):
        """Mostra histórico de movimentações do item selecionado"""
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Selecione um item para ver o histórico!")
            return

        # Buscar item
        items = self.db_manager.select('inventario_itens', where_clause='id = ?', where_params=[self.selected_id])
        if not items:
            return

        item = items[0]

        # Criar janela de histórico
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Histórico de Movimentações - {item['nome']}")
        dialog.geometry("900x500")
        dialog.transient(self.parent)
        dialog.grab_set()

        # Cabeçalho
        header_frame = ttk.Frame(dialog, padding=10)
        header_frame.pack(fill=X)

        ttk.Label(header_frame, text=f"Item: {item['nome']}", font=("Helvetica", 12, "bold")).pack(anchor=W)
        ttk.Label(header_frame, text=f"Estoque Atual: {item['estoque_atual']:.2f} {item['unidade']}",
                 font=("Helvetica", 10)).pack(anchor=W)

        # Lista
        list_frame = ttk.Frame(dialog, padding=10)
        list_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(list_frame, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)

        scrollbar_h = ttk.Scrollbar(list_frame, orient=HORIZONTAL)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        # Treeview
        columns = ("ID", "Data", "Tipo", "Quantidade", "Valor Unit.", "Saldo Anterior", "Saldo Novo", "Motivo")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=tree.yview)
        scrollbar_h.config(command=tree.xview)

        for col in columns:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50, anchor=CENTER)
            elif col in ["Data", "Tipo"]:
                tree.column(col, width=100, anchor=CENTER)
            elif col in ["Quantidade", "Valor Unit.", "Saldo Anterior", "Saldo Novo"]:
                tree.column(col, width=100, anchor=CENTER)
            else:
                tree.column(col, width=200)

        tree.pack(fill=BOTH, expand=YES)

        # Carregar movimentações
        movs = self.db_manager.select('movimentacoes_inventario',
                                       where_clause='item_id = ?',
                                       where_params=[item['id']],
                                       order_by='data DESC, id DESC')

        for mov in movs:
            motivo = mov['motivo'] or ''
            if len(motivo) > 50:
                motivo = motivo[:47] + '...'

            values = (
                mov['id'],
                self.format_date_br(mov['data']),
                mov['tipo'],
                f"{mov['quantidade']:.2f}",
                f"R$ {mov['valor_unitario']:.2f}" if mov['valor_unitario'] else '',
                f"{mov['saldo_anterior']:.2f}",
                f"{mov['saldo_novo']:.2f}",
                motivo
            )
            tree.insert('', END, values=values)

        # Botão fechar
        ttk.Button(dialog, text="Fechar", command=dialog.destroy, width=12).pack(pady=10)

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
