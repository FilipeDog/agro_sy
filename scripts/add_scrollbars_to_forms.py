# -*- coding: utf-8 -*-
"""Script para adicionar scrollbars aos formulários de cadastro"""
import os
import re

files_to_update = [
    'cattle_management/ui/suppliers_register.py',
    'cattle_management/ui/employees_register.py',
    'cattle_management/ui/animals_register.py',
]

# Padrão para encontrar a seção do formulário
pattern_to_find = r'''        # Coluna esquerda - Formulário
        left_frame = ttk\.LabelFrame\(content_frame, text="Dados do (.+?)", padding=20\)
        left_frame\.pack\(side=LEFT, fill=BOTH, expand=YES, padx=\(0, 10\)\)

        row = 0'''

replacement = r'''        # Coluna esquerda - Formulário com Scrollbar
        left_outer_frame = ttk.LabelFrame(content_frame, text="Dados do \1", padding=10)
        left_outer_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Canvas e Scrollbar para o formulário
        canvas = tk.Canvas(left_outer_frame, highlightthickness=0)
        scrollbar_form = ttk.Scrollbar(left_outer_frame, orient=VERTICAL, command=canvas.yview)
        left_frame = ttk.Frame(canvas)

        left_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=left_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_form.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar_form.pack(side=RIGHT, fill=Y)

        # Habilitar scroll com mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Frame interno com padding
        form_inner = ttk.Frame(left_frame, padding=10)
        form_inner.pack(fill=BOTH, expand=YES)

        row = 0'''

def add_scrollbar_to_file(filepath):
    """Adiciona scrollbar a um arquivo de formulário"""
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar se já tem scrollbar
        if 'scrollbar_form' in content or 'form_inner' in content:
            print(f"✓ {filepath} já tem scrollbar")
            return False

        # Encontrar e substituir o padrão
        new_content = re.sub(pattern_to_find, replacement, content, flags=re.MULTILINE)

        if new_content == content:
            print(f"✗ Padrão não encontrado em {filepath}")
            return False

        # Substituir todas as referências left_frame por form_inner nos campos do formulário
        # Mas manter left_frame.columnconfigure e buttons_frame
        lines = new_content.split('\n')
        new_lines = []
        in_form_section = False

        for i, line in enumerate(lines):
            if 'form_inner = ttk.Frame(left_frame, padding=10)' in line:
                in_form_section = True
                new_lines.append(line)
                continue

            if in_form_section and 'left_frame.columnconfigure' in line:
                new_lines.append(line.replace('left_frame.columnconfigure', 'form_inner.columnconfigure'))
                continue

            if in_form_section and 'ttk.Frame(left_frame)' in line:
                new_lines.append(line.replace('ttk.Frame(left_frame)', 'ttk.Frame(form_inner)'))
                continue

            if in_form_section and ('ttk.Label(left_frame,' in line or
                                     'ttk.Entry(left_frame,' in line or
                                     'ttk.Combobox(left_frame,' in line or
                                     'tk.Text(left_frame,' in line or
                                     'ttk.Checkbutton(left_frame,' in line):
                new_lines.append(line.replace('left_frame,', 'form_inner,'))
                continue

            new_lines.append(line)

        new_content = '\n'.join(new_lines)

        # Salvar arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ Scrollbar adicionado: {filepath}")
        return True

    except Exception as e:
        print(f"✗ Erro ao processar {filepath}: {e}")
        return False

def main():
    """Função principal"""
    print("Adicionando scrollbars aos formulários de cadastro...\n")

    updated = 0
    for filepath in files_to_update:
        if add_scrollbar_to_file(filepath):
            updated += 1

    print(f"\n{'='*60}")
    print(f"Total atualizado: {updated} de {len(files_to_update)} arquivos")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
