"""
Gerenciador de Backup e Restore
"""
import shutil
import os
from datetime import datetime
from tkinter import filedialog, messagebox
import sqlite3


class BackupManager:
    """Gerencia backups e restauraçàµes do banco de dados"""

    def __init__(self, db_path='cattle_management/database/gado.db'):
        self.db_path = db_path
        self.backup_dir = 'cattle_management/backups'
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, custom_path=None):
        """Cria um backup do banco de dados"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if custom_path:
                backup_file = custom_path
            else:
                backup_filename = f'backup_gado_{timestamp}.db'
                backup_file = os.path.join(self.backup_dir, backup_filename)

            # Copiar arquivo do banco
            shutil.copy2(self.db_path, backup_file)

            # Criar arquivo de informaçàµes
            info_file = backup_file.replace('.db', '_info.txt')
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"Backup criado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Banco de dados: {self.db_path}\n")
                f.write(f"Tamanho: {os.path.getsize(backup_file) / 1024:.2f} KB\n")
                
                # Contar registros
                conn = sqlite3.connect(backup_file)
                cursor = conn.cursor()
                
                tables = ['animais', 'clientes', 'fornecedores', 'funcionarios', 
                         'despesas', 'receitas', 'talhoes', 'colheitas_banana']
                
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        f.write(f"{table}: {count} registros\n")
                    except:
                        pass
                
                conn.close()

            return backup_file

        except Exception as e:
            raise Exception(f"Erro ao criar backup: {str(e)}")

    def restore_backup(self, backup_path):
        """Restaura um backup do banco de dados"""
        try:
            if not os.path.exists(backup_path):
                raise Exception("Arquivo de backup não encontrado!")

            # Criar backup do banco atual antes de restaurar
            current_backup = self.create_backup()

            # Fechar conexàµes existentes
            # (Em produção, deveria fechar todas as conexàµes ativas)

            # Restaurar backup
            shutil.copy2(backup_path, self.db_path)

            return True, current_backup

        except Exception as e:
            raise Exception(f"Erro ao restaurar backup: {str(e)}")

    def list_backups(self):
        """Lista todos os backups disponíveis"""
        backups = []
        try:
            for filename in sorted(os.listdir(self.backup_dir), reverse=True):
                if filename.endswith('.db'):
                    filepath = os.path.join(self.backup_dir, filename)
                    size = os.path.getsize(filepath) / 1024  # KB
                    mtime = os.path.getmtime(filepath)
                    date = datetime.fromtimestamp(mtime)
                    
                    backups.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size_kb': size,
                        'date': date
                    })
        except Exception as e:
            print(f"Erro ao listar backups: {e}")
        
        return backups

    def delete_backup(self, backup_path):
        """Deleta um arquivo de backup"""
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
                
                # Remover arquivo de informaçàµes se existir
                info_file = backup_path.replace('.db', '_info.txt')
                if os.path.exists(info_file):
                    os.remove(info_file)
                
                return True
        except Exception as e:
            raise Exception(f"Erro ao deletar backup: {str(e)}")

    def export_backup_dialog(self):
        """Abre diálogo para exportar backup"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_name = f'backup_gado_{timestamp}.db'
            
            filepath = filedialog.asksaveasfilename(
                title="Exportar Backup",
                defaultextension=".db",
                initialfile=default_name,
                filetypes=[("Banco de Dados", "*.db"), ("Todos os arquivos", "*.*")]
            )
            
            if filepath:
                return self.create_backup(filepath)
            
            return None

        except Exception as e:
            raise Exception(f"Erro ao exportar backup: {str(e)}")

    def import_backup_dialog(self):
        """Abre diálogo para importar backup"""
        try:
            filepath = filedialog.askopenfilename(
                title="Importar Backup",
                filetypes=[("Banco de Dados", "*.db"), ("Todos os arquivos", "*.*")]
            )
            
            if filepath:
                # Confirmar restauração
                response = messagebox.askyesno(
                    "Confirmar Restauração",
                    "ATENààO: Esta ação irá substituir todos os dados atuais!\n\n"
                    "Um backup automático do banco atual será criado antes da restauração.\n\n"
                    "Deseja continuar?"
                )
                
                if response:
                    success, current_backup = self.restore_backup(filepath)
                    return True, current_backup
            
            return False, None

        except Exception as e:
            raise Exception(f"Erro ao importar backup: {str(e)}")
