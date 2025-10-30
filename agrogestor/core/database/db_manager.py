"""
Gerenciador de Banco de Dados - AgroGestor - Sistema de Gestão de Rebanho
"""
import sqlite3
import os
from datetime import datetime
import hashlib


class DatabaseManager:
    """Classe para gerenciar todas as operações com o banco de dados"""

    def __init__(self, db_path=None):
        """Inicializa o gerenciador de banco de dados"""
        if db_path is None:
            # Usar caminho padrão relativo à estrutura do projeto
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            db_path = os.path.join(base_dir, 'agrogestor', 'core', 'database', 'gado.db')
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Cria todas as tabelas do banco de dados"""
        try:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            self.cursor.executescript(schema_sql)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            return False

    def initialize_database(self):
        """Inicializa o banco de dados com dados padrão"""
        try:
            # Inserir dados padrão para cadastros secundários

            # Tipos de Animal
            tipos_animal = [
                ('Bezerro',), ('Bezerra',), ('Novilha',),
                ('Garrote',), ('Boi',), ('Touro',), ('Vaca',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO tipo_animal (nome) VALUES (?)",
                tipos_animal
            )

            # Status do Animal
            status = [
                ('Ativo',), ('Morto',), ('Abatido',), ('Vendido',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO status_animal (nome) VALUES (?)",
                status
            )

            # Origens
            origens = [
                ('Compra',), ('Nascimento',), ('Troca',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO origem (nome) VALUES (?)",
                origens
            )

            # Raças
            racas = [
                ('Angus',), ('Nelore',), ('Brahman',), ('Hereford',),
                ('Simental',), ('Charolês',), ('Limousin',), ('Gir',),
                ('Guzerá',), ('Tabapuã',), ('Mestiço',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO raca (nome) VALUES (?)",
                racas
            )

            # Pastos
            pastos = [
                ('Pasto Norte',), ('Pasto Sul',),
                ('Pasto Leste',), ('Pasto Oeste',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO pastos (nome) VALUES (?)",
                pastos
            )

            # Causa da Morte
            causas = [
                ('Doença',), ('Aborto',), ('Causas Externas',),
                ('Acidente',), ('Predador',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO causa_morte (nome) VALUES (?)",
                causas
            )

            # Tipos de Receita
            tipos_receita = [
                ('Venda de Animal',), ('Venda de Leite',),
                ('Venda de Carne',), ('Prestação de Serviço',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO tipo_receita (nome) VALUES (?)",
                tipos_receita
            )

            # Tipos de Despesa
            tipos_despesa = [
                ('Salário',), ('Medicamento',), ('Vacina',),
                ('Transporte',), ('Veterinário',), ('Ração',),
                ('Suplemento',), ('Manutenção',), ('Energia',), ('Água',)
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO tipo_despesa (nome) VALUES (?)",
                tipos_despesa
            )

            # Medicamentos básicos
            medicamentos = [
                ('Ivermectina', 'Vermífugo', 'ml'),
                ('Vitamina ADE', 'Medicamento', 'ml'),
                ('Vacina Aftosa', 'Vacina', 'dose'),
                ('Vacina Brucelose', 'Vacina', 'dose'),
                ('Antibiótico', 'Medicamento', 'ml'),
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO medicamentos (nome, tipo, unidade) VALUES (?, ?, ?)",
                medicamentos
            )

            # Criar usuário admin padrão
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            self.cursor.execute(
                "INSERT OR IGNORE INTO usuarios (username, password, nome_completo, nivel_acesso, primeiro_acesso) VALUES (?, ?, ?, ?, ?)",
                ('admin', password_hash, 'Administrador', 'Admin', 0)
            )

            # Criar licença padrão (válida por 1 ano)
            from datetime import datetime, timedelta
            data_expiracao = datetime.now() + timedelta(days=365)
            self.cursor.execute(
                "INSERT OR IGNORE INTO licencas (chave_licenca, data_ativacao, data_expiracao, ativo) VALUES (?, ?, ?, ?)",
                ('DEMO-2024-GADO-CTRL', datetime.now(), data_expiracao, 1)
            )

            # Dados iniciais do módulo de bananal
            # Variedades de banana
            variedades = [
                ('Banana Nanica', 'Variedade mais comum no Brasil', 360, 25.0),
                ('Banana Prata', 'Segunda variedade mais cultivada', 420, 18.0),
                ('Banana Maçã', 'Doce e aromática', 480, 12.0),
                ('Banana da Terra', 'Para cozinhar', 540, 30.0),
                ('Banana Ouro', 'Pequena e muito doce', 360, 8.0),
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO variedades_banana (nome, descricao, ciclo_medio_dias, producao_media_ton_ha) VALUES (?, ?, ?, ?)",
                variedades
            )

            # Pragas e doenças comuns
            pragas = [
                ('Sigatoka Negra', 'Doença', 'Manchas nas folhas', 'Fungicidas'),
                ('Sigatoka Amarela', 'Doença', 'Manchas amarelas', 'Fungicidas'),
                ('Moko da Bananeira', 'Bactéria', 'Murcha e podridão', 'Erradicação'),
                ('Broca da Bananeira', 'Praga', 'Larvas no pseudocaule', 'Armadilhas'),
                ('Tripes', 'Praga', 'Manchas nos frutos', 'Inseticidas'),
            ]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO pragas_doencas (nome, tipo, sintomas, tratamento_recomendado) VALUES (?, ?, ?, ?)",
                pragas
            )

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            self.conn.rollback()
            return False

    # Métodos CRUD genéricos

    def insert(self, table, data):
        """Insere um registro em uma tabela"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, list(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            error_msg = f"Erro de integridade ao inserir em '{table}': {e}\nDados: {data}"
            print(error_msg)
            self.conn.rollback()
            raise ValueError(error_msg)
        except sqlite3.OperationalError as e:
            error_msg = f"Erro operacional ao inserir em '{table}': {e}\nColunas tentadas: {list(data.keys())}"
            print(error_msg)
            self.conn.rollback()
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Erro desconhecido ao inserir em '{table}': {e}\nDados: {data}"
            print(error_msg)
            self.conn.rollback()
            raise ValueError(error_msg)

    def update(self, table, data, where_clause, where_params):
        """Atualiza registros em uma tabela"""
        try:
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(sql, list(data.values()) + where_params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
            self.conn.rollback()
            return 0

    def delete(self, table, where_clause, where_params):
        """Deleta registros de uma tabela"""
        try:
            sql = f"DELETE FROM {table} WHERE {where_clause}"
            self.cursor.execute(sql, where_params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Erro ao deletar dados: {e}")
            self.conn.rollback()
            return 0

    def select(self, table, columns='*', where_clause=None, where_params=None, order_by=None):
        """Seleciona registros de uma tabela"""
        try:
            sql = f"SELECT {columns} FROM {table}"
            if where_clause:
                sql += f" WHERE {where_clause}"
            if order_by:
                sql += f" ORDER BY {order_by}"

            if where_params:
                self.cursor.execute(sql, where_params)
            else:
                self.cursor.execute(sql)

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao selecionar dados: {e}")
            return []

    def execute_query(self, sql, params=None):
        """Executa uma query SQL personalizada"""
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)

            if sql.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor.rowcount
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            self.conn.rollback()
            return None

    # Métodos específicos para o sistema

    def authenticate_user(self, username, password):
        """Autentica um usuário e retorna informações completas"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        result = self.select(
            'usuarios',
            where_clause='username = ? AND password = ? AND ativo = 1',
            where_params=[username, password_hash]
        )
        if result:
            # Atualizar último login
            self.update(
                'usuarios',
                {'ultimo_login': datetime.now()},
                'id = ?',
                [result[0]['id']]
            )
            return dict(result[0])
        return None

    def check_license(self, license_key):
        """Verifica se uma licença é válida"""
        result = self.select(
            'licencas',
            where_clause='chave_licenca = ? AND ativo = 1 AND data_expiracao > ?',
            where_params=[license_key, datetime.now()]
        )
        return len(result) > 0

    def get_animal_by_brinco(self, brinco):
        """Busca um animal pelo número do brinco"""
        result = self.select('animais', where_clause='brinco = ?', where_params=[brinco])
        return result[0] if result else None

    def calculate_animal_age(self, data_nascimento):
        """Calcula a idade do animal em meses"""
        if not data_nascimento:
            return None

        from datetime import datetime
        try:
            birth_date = datetime.strptime(data_nascimento, '%Y-%m-%d')
            today = datetime.now()
            months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
            return months
        except:
            return None

    def get_all_animals(self):
        """Retorna todos os animais com informações completas"""
        sql = """
            SELECT a.*,
                   ta.nome as tipo_nome,
                   s.nome as status_nome,
                   p.nome as pasto_nome,
                   r.nome as raca_nome,
                   o.nome as origem_nome,
                   cm.nome as causa_morte_nome
            FROM animais a
            LEFT JOIN tipo_animal ta ON a.tipo_id = ta.id
            LEFT JOIN status_animal s ON a.status_id = s.id
            LEFT JOIN pastos p ON a.pasto_id = p.id
            LEFT JOIN raca r ON a.raca_id = r.id
            LEFT JOIN origem o ON a.origem_id = o.id
            LEFT JOIN causa_morte cm ON a.causa_morte_id = cm.id
            ORDER BY a.brinco
        """
        return self.execute_query(sql)

    def log_activity(self, usuario_id, usuario_nome, acao, modulo, descricao='', ip_address=''):
        """Registra uma atividade no log"""
        try:
            data = {
                'usuario_id': usuario_id,
                'usuario_nome': usuario_nome,
                'acao': acao,
                'modulo': modulo,
                'descricao': descricao,
                'ip_address': ip_address
            }
            return self.insert('log_atividades', data)
        except Exception as e:
            print(f"Erro ao registrar log: {e}")
            return None

    def update_account_balance(self, conta_id, valor, operacao='add'):
        """Atualiza o saldo de uma conta bancária"""
        try:
            conta = self.select('contas_bancarias', where_clause='id = ?', where_params=[conta_id])
            if conta:
                saldo_atual = conta[0]['saldo_atual'] or 0
                if operacao == 'add':
                    novo_saldo = saldo_atual + valor
                else:
                    novo_saldo = saldo_atual - valor

                self.update('contas_bancarias', {'saldo_atual': novo_saldo}, 'id = ?', [conta_id])
                return novo_saldo
            return None
        except Exception as e:
            print(f"Erro ao atualizar saldo da conta: {e}")
            return None

    def update_inventory_stock(self, item_id, quantidade, operacao='add'):
        """Atualiza o estoque de um item do inventário"""
        try:
            item = self.select('inventario_itens', where_clause='id = ?', where_params=[item_id])
            if item:
                estoque_atual = item[0]['estoque_atual'] or 0
                if operacao == 'add':
                    novo_estoque = estoque_atual + quantidade
                else:
                    novo_estoque = estoque_atual - quantidade

                self.update('inventario_itens', {'estoque_atual': novo_estoque}, 'id = ?', [item_id])
                return novo_estoque
            return None
        except Exception as e:
            print(f"Erro ao atualizar estoque: {e}")
            return None

    def get_low_stock_items(self):
        """Retorna itens com estoque abaixo do mínimo"""
        sql = """
            SELECT * FROM inventario_itens
            WHERE ativo = 1 AND estoque_atual <= estoque_minimo
            ORDER BY estoque_atual ASC
        """
        return self.execute_query(sql)

    def get_financial_summary(self, data_inicio=None, data_fim=None):
        """Retorna resumo financeiro do período"""
        where_despesas = ""
        where_receitas = ""
        params_despesas = []
        params_receitas = []

        if data_inicio and data_fim:
            where_despesas = "WHERE data_gasto BETWEEN ? AND ?"
            where_receitas = "WHERE data_venda BETWEEN ? AND ?"
            params_despesas = [data_inicio, data_fim]
            params_receitas = [data_inicio, data_fim]

        sql_despesas = f"SELECT SUM(valor_final) as total FROM despesas {where_despesas}"
        sql_receitas = f"SELECT SUM(valor_total) as total FROM receitas {where_receitas}"

        despesas = self.execute_query(sql_despesas, params_despesas)
        receitas = self.execute_query(sql_receitas, params_receitas)

        total_despesas = despesas[0]['total'] if despesas and despesas[0]['total'] else 0
        total_receitas = receitas[0]['total'] if receitas and receitas[0]['total'] else 0

        return {
            'despesas': total_despesas,
            'receitas': total_receitas,
            'saldo': total_receitas - total_despesas
        }

    def change_user_password(self, user_id, new_password):
        """Altera a senha de um usuário"""
        try:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            self.update(
                'usuarios',
                {'password': password_hash, 'primeiro_acesso': 0},
                'id = ?',
                [user_id]
            )
            return True
        except Exception as e:
            print(f"Erro ao alterar senha: {e}")
            return False

    def backup_database(self, backup_path):
        """Cria um backup do banco de dados"""
        try:
            import shutil
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_path, f'backup_gado_{timestamp}.db')
            shutil.copy2(self.db_path, backup_file)
            return backup_file
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return None
