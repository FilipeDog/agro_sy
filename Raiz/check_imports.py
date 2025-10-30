#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar imports sem executar GUI"""

import sys
import ast
import os

def check_imports_in_file(filepath):
    """Verifica os imports de um arquivo sem executá-lo"""
    errors = []
    warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content, filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    # Ignorar tkinter (não disponível em ambiente headless)
                    if module_name.startswith('tkinter') or module_name.startswith('ttkbootstrap'):
                        continue
                    # Ignorar imports locais
                    if module_name.startswith('cattle_management'):
                        continue
                    # Tentar importar
                    try:
                        __import__(module_name.split('.')[0])
                    except ImportError:
                        errors.append(f"Import não encontrado: {module_name}")

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module
                    # Ignorar tkinter
                    if module_name.startswith('tkinter') or module_name.startswith('ttkbootstrap'):
                        continue
                    # Ignorar imports locais
                    if module_name.startswith('cattle_management'):
                        continue
                    # Tentar importar
                    try:
                        __import__(module_name.split('.')[0])
                    except ImportError:
                        errors.append(f"Import não encontrado: from {module_name}")

        return errors, warnings

    except SyntaxError as e:
        return [f"Erro de sintaxe: {e}"], []
    except Exception as e:
        return [f"Erro ao processar: {e}"], []

def check_all_imports(directory):
    """Verifica imports de todos os arquivos Python"""
    total_errors = []
    total_warnings = []
    checked = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv']]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                checked += 1
                errors, warnings = check_imports_in_file(filepath)

                if errors:
                    print(f"✗ {filepath}")
                    for error in errors:
                        print(f"  - {error}")
                    total_errors.extend([(filepath, e) for e in errors])
                else:
                    print(f"✓ {filepath}")

                if warnings:
                    for warning in warnings:
                        print(f"  ⚠ {warning}")
                    total_warnings.extend([(filepath, w) for w in warnings])

    print(f"\n{'='*60}")
    print(f"Total de arquivos verificados: {checked}")
    print(f"Arquivos com erro: {len(set([e[0] for e in total_errors]))}")
    print(f"Total de erros: {len(total_errors)}")
    print(f"Total de avisos: {len(total_warnings)}")
    print(f"{'='*60}\n")

    if total_errors:
        print("❌ RESUMO DE ERROS:\n")
        for filepath, error in total_errors:
            print(f"{filepath}: {error}")
        return False
    else:
        print("✅ Todos os imports estão corretos!")
        return True

if __name__ == "__main__":
    directory = "/home/user/gado"
    success = check_all_imports(directory)
    sys.exit(0 if success else 1)
