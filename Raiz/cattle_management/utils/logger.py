"""
Sistema de Log - AgroGestor - Sistema de Gestão de Rebanho
Registra atividades e erros do sistema
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class SystemLogger:
    """Gerencia o sistema de logs da aplicação"""

    def __init__(self, log_dir='cattle_management/logs'):
        self.log_dir = log_dir
        self.ensure_log_directory()
        self.loggers = {}

    def ensure_log_directory(self):
        """Garante que o diretório de logs existe"""
        os.makedirs(self.log_dir, exist_ok=True)

    def get_logger(self, name='system'):
        """Retorna um logger configurado"""
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Remove handlers existentes
        logger.handlers = []

        # Handler para arquivo diário
        log_file = os.path.join(self.log_dir, f'{name}.log')
        file_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)

        # Handler para erros
        error_file = os.path.join(self.log_dir, f'{name}_errors.log')
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)

        # Formato dos logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(error_handler)

        self.loggers[name] = logger
        return logger

    def log_user_activity(self, username, action, module, details=''):
        """Registra atividade de usuário"""
        logger = self.get_logger('user_activity')
        message = f"Usuário: {username} | Ação: {action} | Módulo: {module}"
        if details:
            message += f" | Detalhes: {details}"
        logger.info(message)

    def log_database_operation(self, operation, table, details=''):
        """Registra operação no banco de dados"""
        logger = self.get_logger('database')
        message = f"Operação: {operation} | Tabela: {table}"
        if details:
            message += f" | Detalhes: {details}"
        logger.info(message)

    def log_error(self, error, context=''):
        """Registra um erro"""
        logger = self.get_logger('errors')
        message = f"Erro: {str(error)}"
        if context:
            message += f" | Contexto: {context}"
        logger.error(message, exc_info=True)

    def log_warning(self, warning, context=''):
        """Registra um aviso"""
        logger = self.get_logger('warnings')
        message = f"Aviso: {warning}"
        if context:
            message += f" | Contexto: {context}"
        logger.warning(message)

    def log_info(self, info, module='system'):
        """Registra uma informação"""
        logger = self.get_logger(module)
        logger.info(info)

    def get_recent_logs(self, log_type='system', lines=100):
        """Retorna as últimas linhas de log"""
        log_file = os.path.join(self.log_dir, f'{log_type}.log')
        if not os.path.exists(log_file):
            return []

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except Exception as e:
            return [f"Erro ao ler log: {str(e)}"]

    def clear_old_logs(self, days=30):
        """Remove logs mais antigos que X dias"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)

        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_date:
                    try:
                        os.remove(file_path)
                        print(f"Log antigo removido: {filename}")
                    except Exception as e:
                        print(f"Erro ao remover log {filename}: {e}")


# Instância global do logger
_system_logger = None


def get_system_logger():
    """Retorna a instância global do logger"""
    global _system_logger
    if _system_logger is None:
        _system_logger = SystemLogger()
    return _system_logger
