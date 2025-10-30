#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar schema do banco de dados"""

import sqlite3
import os

def test_database_schema():
    """Testa se o schema SQL é válido"""
    print("="*60)
    print("VERIFICAÇÃO DO SCHEMA DO BANCO DE DADOS")
    print("="*60)

    schema_path = "/home/user/gado/cattle_management/database/schema.sql"
    test_db = "/tmp/test_agrogestor.db"

    # Remover banco de teste se existir
    if os.path.exists(test_db):
        os.remove(test_db)

    try:
        # Ler schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        print(f"\n✓ Schema lido com sucesso: {len(schema_sql)} bytes")

        # Criar banco de teste
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        # Executar schema
        cursor.executescript(schema_sql)

        print("✓ Schema executado com sucesso")

        # Verificar tabelas criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        print(f"\n✓ Total de tabelas criadas: {len(tables)}")
        print("\nTabelas no banco:")
        for i, (table_name,) in enumerate(tables, 1):
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            # Obter estrutura
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            print(f"  {i:2d}. {table_name:30s} - {len(columns)} colunas, {count} registros")

        conn.close()
        os.remove(test_db)

        print("\n" + "="*60)
        print("✅ SCHEMA VALIDADO COM SUCESSO!")
        print("="*60)
        return True

    except sqlite3.Error as e:
        print(f"\n❌ ERRO SQL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = test_database_schema()
    sys.exit(0 if success else 1)
