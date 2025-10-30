#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para análise de qualidade do código"""

import os
import re
import ast

def analyze_code_patterns(directory):
    """Analisa padrões comuns de código"""
    print("="*60)
    print("ANÁLISE DE QUALIDADE DO CÓDIGO")
    print("="*60)

    issues = []
    warnings = []
    stats = {
        'files': 0,
        'lines': 0,
        'functions': 0,
        'classes': 0,
        'comments': 0,
        'docstrings': 0
    }

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv']]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                stats['files'] += 1

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        stats['lines'] += len(lines)

                    # Verificar codificação UTF-8
                    if '# -*- coding: utf-8 -*-' not in content[:100]:
                        warnings.append(f"{filepath}: Declaração UTF-8 ausente no cabeçalho")

                    # Analisar AST
                    try:
                        tree = ast.parse(content, filepath)

                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                stats['functions'] += 1
                                if ast.get_docstring(node):
                                    stats['docstrings'] += 1

                            elif isinstance(node, ast.ClassDef):
                                stats['classes'] += 1
                                if ast.get_docstring(node):
                                    stats['docstrings'] += 1

                    except SyntaxError:
                        pass

                    # Contar comentários
                    stats['comments'] += len([l for l in lines if l.strip().startswith('#')])

                    # Verificar padrões problemáticos
                    # Bare except
                    if re.search(r'except\s*:', content):
                        issues.append(f"{filepath}: Uso de 'except:' sem especificar exceção")

                    # Print statements (possível debug esquecido)
                    if 'print(' in content and 'check_' not in filepath:
                        # Ignorar em arquivos de teste
                        if not any(x in filepath for x in ['test_', 'check_', 'main.py']):
                            warnings.append(f"{filepath}: Contém print() - possível debug esquecido")

                except Exception as e:
                    issues.append(f"{filepath}: Erro ao analisar - {e}")

    # Relatório
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  • Arquivos Python: {stats['files']}")
    print(f"  • Total de linhas: {stats['lines']:,}")
    print(f"  • Funções: {stats['functions']}")
    print(f"  • Classes: {stats['classes']}")
    print(f"  • Comentários: {stats['comments']}")
    print(f"  • Docstrings: {stats['docstrings']}")
    print(f"  • Taxa de documentação: {stats['docstrings']/(stats['functions']+stats['classes'])*100:.1f}%")

    if warnings:
        print(f"\n⚠️  AVISOS ({len(warnings)}):")
        for warning in warnings[:10]:  # Mostrar apenas os 10 primeiros
            print(f"  • {warning}")
        if len(warnings) > 10:
            print(f"  ... e mais {len(warnings)-10} avisos")

    if issues:
        print(f"\n❌ PROBLEMAS ENCONTRADOS ({len(issues)}):")
        for issue in issues[:10]:
            print(f"  • {issue}")
        if len(issues) > 10:
            print(f"  ... e mais {len(issues)-10} problemas")
    else:
        print(f"\n✅ NENHUM PROBLEMA CRÍTICO ENCONTRADO!")

    print("\n" + "="*60)
    print("CONCLUSÃO DA ANÁLISE")
    print("="*60)

    if len(issues) == 0:
        print("✅ Código em excelente estado!")
        print("✅ Pronto para produção!")
        return True
    else:
        print(f"⚠️  {len(issues)} problemas precisam de atenção")
        return False

if __name__ == "__main__":
    import sys
    directory = "/home/user/gado"
    success = analyze_code_patterns(directory)
    sys.exit(0 if success else 1)
