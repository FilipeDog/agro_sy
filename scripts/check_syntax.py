#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar sintaxe de todos os arquivos Python"""

import os
import py_compile
import sys

def check_python_files(directory):
    """Verifica sintaxe de todos os arquivos Python"""
    errors = []
    checked = []

    for root, dirs, files in os.walk(directory):
        # Ignorar diretórios .git e __pycache__
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv']]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                checked.append(filepath)
                try:
                    py_compile.compile(filepath, doraise=True)
                    print(f"✓ {filepath}")
                except py_compile.PyCompileError as e:
                    print(f"✗ {filepath}")
                    errors.append((filepath, str(e)))
                except SyntaxError as e:
                    print(f"✗ {filepath}")
                    errors.append((filepath, str(e)))

    print(f"\n{'='*60}")
    print(f"Total de arquivos verificados: {len(checked)}")
    print(f"Arquivos com erro: {len(errors)}")
    print(f"{'='*60}\n")

    if errors:
        print("ERROS ENCONTRADOS:\n")
        for filepath, error in errors:
            print(f"Arquivo: {filepath}")
            print(f"Erro: {error}")
            print("-" * 60)
        return False
    else:
        print("✓ Todos os arquivos estão sem erros de sintaxe!")
        return True

if __name__ == "__main__":
    directory = "/home/user/gado"
    success = check_python_files(directory)
    sys.exit(0 if success else 1)
