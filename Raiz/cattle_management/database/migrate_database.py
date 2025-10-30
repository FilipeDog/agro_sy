# -*- coding: utf-8 -*-
"""
Script de Migração do Banco de Dados
Atualiza bancos antigos para a nova estrutura ou cria novo
"""
import sqlite3
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


def create_new_database(db_path):
    """Cria um novo banco de dados com estrutura completa"""
    print("Criando novo banco de dados...")

    try:
        from cattle_management.database.db_manager import DatabaseManager

        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        db = DatabaseManager(db_path)
        db.connect()

        # Criar tabelas
        if db.create_tables():
            print("✓ Tabelas criadas com sucesso")

        # Inicializar dados padrão
        if db.initialize_database():
            print("✓ Dados iniciais inseridos com sucesso")

        db.disconnect()
        print("\n✓ Banco de dados criado com sucesso!")
        return True

    except Exception as e:
        print(f"✗ Erro ao criar banco de dados: {e}")
        import traceback
        traceback.print_exc()
        return False


def migrate_database(db_path='cattle_management/database/gado.db'):
    """Migra banco de dados antigo para nova estrutura ou cria novo"""

    # Se o banco não existe, criar um novo
    if not os.path.exists(db_path):
        return create_new_database(db_path)
    
    print("Iniciando migração do banco de dados...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    migrations = []
    
    # Verificar e adicionar colunas na tabela usuarios
    try:
        cursor.execute("SELECT nivel_acesso FROM usuarios LIMIT 1")
    except:
        migrations.append(("usuarios", "ALTER TABLE usuarios ADD COLUMN nivel_acesso TEXT DEFAULT 'Operador'"))
        migrations.append(("usuarios", "ALTER TABLE usuarios ADD COLUMN primeiro_acesso INTEGER DEFAULT 1"))
        migrations.append(("usuarios", "ALTER TABLE usuarios ADD COLUMN ultimo_login TIMESTAMP"))
    
    # Verificar e adicionar colunas na tabela despesas
    try:
        cursor.execute("SELECT quantidade FROM despesas LIMIT 1")
    except:
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN quantidade REAL DEFAULT 1"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN valor_unitario REAL"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN desconto REAL DEFAULT 0"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN valor_final REAL"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN data_vencimento DATE"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN forma_pagamento TEXT"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN numero_nota TEXT"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN pago_por INTEGER"))
        migrations.append(("despesas", "ALTER TABLE despesas ADD COLUMN conta_bancaria_id INTEGER"))
    
    # Verificar e adicionar colunas na tabela receitas
    try:
        cursor.execute("SELECT numero_nota FROM receitas LIMIT 1")
    except:
        migrations.append(("receitas", "ALTER TABLE receitas ADD COLUMN numero_nota TEXT"))
        migrations.append(("receitas", "ALTER TABLE receitas ADD COLUMN desconto REAL DEFAULT 0"))
        migrations.append(("receitas", "ALTER TABLE receitas ADD COLUMN valor_final REAL"))
        migrations.append(("receitas", "ALTER TABLE receitas ADD COLUMN forma_pagamento TEXT"))
        migrations.append(("receitas", "ALTER TABLE receitas ADD COLUMN recebido_por INTEGER"))
        migrations.append(("receitas", "ALTER TABLE receitas ADD COLUMN conta_bancaria_id INTEGER"))
    
    # Executar migrações
    for table, sql in migrations:
        try:
            cursor.execute(sql)
            print(f"✓ Migração aplicada em {table}")
        except Exception as e:
            print(f"✗ Erro em {table}: {e}")
    
    # Criar novas tabelas se não existirem
    new_tables = [
        ("funcionarios", """
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE,
                rg TEXT,
                data_nascimento DATE,
                telefone TEXT,
                email TEXT,
                cargo TEXT,
                setor TEXT,
                salario REAL,
                data_admissao DATE,
                data_demissao DATE,
                ativo INTEGER DEFAULT 1,
                endereco TEXT,
                cidade TEXT,
                uf TEXT,
                cep TEXT,
                observacoes TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("contas_bancarias", """
            CREATE TABLE IF NOT EXISTS contas_bancarias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_conta TEXT NOT NULL,
                banco TEXT,
                agencia TEXT,
                numero_conta TEXT,
                tipo_conta TEXT,
                saldo_inicial REAL DEFAULT 0,
                saldo_atual REAL DEFAULT 0,
                data_abertura DATE,
                ativo INTEGER DEFAULT 1,
                observacoes TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("inventario_itens", """
            CREATE TABLE IF NOT EXISTS inventario_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE,
                nome TEXT NOT NULL,
                categoria TEXT,
                unidade TEXT,
                estoque_minimo REAL DEFAULT 0,
                estoque_atual REAL DEFAULT 0,
                valor_unitario REAL,
                localizacao TEXT,
                fornecedor_id INTEGER,
                ativo INTEGER DEFAULT 1,
                observacoes TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("variedades_banana", """
            CREATE TABLE IF NOT EXISTS variedades_banana (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT,
                ciclo_medio_dias INTEGER,
                producao_media_ton_ha REAL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("talhoes", """
            CREATE TABLE IF NOT EXISTS talhoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                localizacao TEXT,
                area_hectares REAL NOT NULL,
                variedade_id INTEGER,
                data_plantio DATE,
                espacamento TEXT,
                densidade_plantas_ha INTEGER,
                situacao TEXT DEFAULT 'Ativo',
                observacoes TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("colheitas_banana", """
            CREATE TABLE IF NOT EXISTS colheitas_banana (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                talhao_id INTEGER NOT NULL,
                data_colheita DATE NOT NULL,
                quantidade_kg REAL NOT NULL,
                quantidade_caixas INTEGER,
                peso_medio_cacho REAL,
                classificacao_a_kg REAL DEFAULT 0,
                classificacao_b_kg REAL DEFAULT 0,
                classificacao_c_kg REAL DEFAULT 0,
                custo_colheita REAL,
                responsavel_id INTEGER,
                destino TEXT,
                observacoes TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("tratos_culturais", """
            CREATE TABLE IF NOT EXISTS tratos_culturais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                talhao_id INTEGER NOT NULL,
                tipo_trato TEXT NOT NULL,
                data_execucao DATE NOT NULL,
                produto_utilizado TEXT,
                quantidade REAL,
                unidade TEXT,
                custo REAL,
                responsavel_id INTEGER,
                observacoes TEXT,
                proxima_aplicacao DATE,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("pragas_doencas", """
            CREATE TABLE IF NOT EXISTS pragas_doencas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                tipo TEXT,
                sintomas TEXT,
                tratamento_recomendado TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
    ]
    
    for table_name, create_sql in new_tables:
        try:
            cursor.execute(create_sql)
            print(f"✓ Tabela {table_name} verificada/criada")
        except Exception as e:
            print(f"✗ Erro ao criar {table_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✓ Migração concluída com sucesso!")
    return True


if __name__ == "__main__":
    migrate_database()
