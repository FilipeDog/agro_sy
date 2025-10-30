#!/usr/bin/env python3
"""
AgroGestor - Sistema de Gestão Agropecuária
Arquivo Principal de Execução

Para executar o sistema, execute este arquivo:
    python main.py
ou
    python3 main.py
"""

import sys
import os

# Adicionar diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cattle_management.database.db_manager import DatabaseManager
from cattle_management.ui.login import LoginWindow
from cattle_management.ui.main_window import MainWindow


def initialize_system():
    """Inicializa o sistema"""
    print("=" * 60)
    print("🌾 AgroGestor - Sistema de Gestão Agropecuária")
    print("Versão 1.0.0")
    print("=" * 60)
    print()

    # Verificar e criar diretórios necessários
    print("Verificando estrutura de diretórios...")
    os.makedirs('cattle_management/database', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    print("✓ Diretórios verificados")

    # Inicializar banco de dados
    print("\nInicializando banco de dados...")
    db_manager = DatabaseManager('cattle_management/database/gado.db')

    if not db_manager.connect():
        print("✗ ERRO: Não foi possível conectar ao banco de dados!")
        sys.exit(1)

    print("✓ Conexão com banco de dados estabelecida")

    # Criar tabelas
    print("\nCriando tabelas...")
    if not db_manager.create_tables():
        print("✗ ERRO: Não foi possível criar as tabelas!")
        sys.exit(1)

    print("✓ Tabelas criadas/verificadas")

    # Inicializar dados padrão
    print("\nInicializando dados padrão...")
    if not db_manager.initialize_database():
        print("✗ ERRO: Não foi possível inicializar dados padrão!")
        sys.exit(1)

    print("✓ Dados padrão inicializados")

    print("\n" + "=" * 60)
    print("Sistema inicializado com sucesso!")
    print("=" * 60)
    print()
    print("Credenciais padrão:")
    print("  Usuário: admin")
    print("  Senha: admin123")
    print("  Licença: DEMO-2024-GADO-CTRL")
    print()
    print("=" * 60)
    print()

    return db_manager


def start_application(db_manager):
    """Inicia a aplicação"""
    def on_login_success():
        """Callback chamado após login bem-sucedido"""
        main_window = MainWindow(db_manager)
        main_window.run()

    # Mostrar tela de login
    login_window = LoginWindow(db_manager, on_login_success)
    login_window.run()


def main():
    """Função principal"""
    try:
        # Inicializar sistema
        db_manager = initialize_system()

        # Iniciar aplicação
        print("Iniciando interface gráfica...")
        start_application(db_manager)

    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
        sys.exit(0)

    except Exception as e:
        print(f"\n\n✗ ERRO FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        print("\nEncerrando sistema...")


if __name__ == "__main__":
    main()
