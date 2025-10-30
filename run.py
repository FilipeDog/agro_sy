#!/usr/bin/env python3
"""
Script de entrada para executar o AgroGestor
"""
import sys
import os

# Adicionar diretório do projeto ao path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Importar e executar o main
from agrogestor.main import main

if __name__ == "__main__":
    main()
