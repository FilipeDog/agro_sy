# -*- coding: utf-8 -*-
"""Script para corrigir todos os erros de encoding nos arquivos Python"""
import os
import re

# Mapeamento completo de erros de encoding
replacements = {
    # Vogais acentuadas minúsculas
    'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
    'Ã': 'à', 'Ã¨': 'è', 'Ã¬': 'ì', 'Ã²': 'ò', 'Ã¹': 'ù',
    'Ã¢': 'â', 'Ãª': 'ê', 'Ã®': 'î', 'Ã´': 'ô', 'Ã»': 'û',
    'Ã£': 'ã', 'Ãµ': 'õ', 'Ã±': 'ñ',

    # Cedilha
    'Ã§': 'ç',

    # Combinações comuns
    'Ã§Ã£o': 'ção', 'Ã§Ãµes': 'ções',
    'CÃ³digo': 'Código', 'Cã³digo': 'Código',
    'NÃºmero': 'Número', 'Nãºmero': 'Número', 'Nãmero': 'Número',
    'DescriÃ§Ã£o': 'Descrição', 'Descriã§ã£o': 'Descrição',
    'ObservaÃ§Ãµes': 'Observações', 'Observaã§ãµes': 'Observações',
    'AdiÃ§Ã£o': 'Adição', 'Adiã§ã£o': 'Adição',
    'PrÃ³ximo': 'Próximo', 'Prã³ximo': 'Próximo',
    'PrÃ©vio': 'Prévio', 'Prã©vio': 'Prévio',
    'UltimaÃ§Ã£o': 'Ultimação', 'Ultimaã§ã£o': 'Ultimação',
    'MÃ©dia': 'Média', 'Mã©dia': 'Média',
    'CategoriÃ¡': 'Categoria', 'Categoriã¡': 'Categoria',
    'HÃ¡': 'Há', 'Hã¡': 'Há',
    'AtÃ©': 'Até', 'Atã©': 'Até',

    # Outras correções específicas
    'Nãºmero': 'Número',
    'cã³digo': 'código',
    'descriã§ã£o': 'descrição',
    'situaã§ã£o': 'situação',
    'operaã§ã£o': 'operação',
    'aplicaã§ã£o': 'aplicação',
    'transiã§ã£o': 'transição',
    'funã§ã£o': 'função',
    'seã§ã£o': 'seção',
    'produã§ã£o': 'produção',
    'reduã§ã£o': 'redução',
    'importaã§ã£o': 'importação',
    'exportaã§ã£o': 'exportação',
}

def fix_encoding_in_file(filepath):
    """Corrige encoding em um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content

        # Aplicar todas as substituições
        for bad, good in replacements.items():
            content = content.replace(bad, good)

        # Se houve mudanças, salvar
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}")
        return False

def main():
    """Função principal"""
    # Procurar todos os arquivos Python
    fixed_files = []
    checked_files = 0

    for root, dirs, files in os.walk('cattle_management'):
        # Ignorar __pycache__
        if '__pycache__' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                checked_files += 1
                if fix_encoding_in_file(filepath):
                    fixed_files.append(filepath)
                    print(f"✓ Corrigido: {filepath}")

    print(f"\n{'='*60}")
    print(f"Verificados: {checked_files} arquivos")
    print(f"Corrigidos: {len(fixed_files)} arquivos")
    print(f"{'='*60}")

    if fixed_files:
        print("\nArquivos corrigidos:")
        for f in fixed_files:
            print(f"  - {f}")
    else:
        print("\nNenhum arquivo precisou de correção!")

if __name__ == "__main__":
    main()
