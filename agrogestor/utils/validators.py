"""
Validadores - AgroGestor - Sistema de Gestão de Rebanho
Funções para validação de dados
"""
import re
from datetime import datetime


class Validators:
    """Classe com métodos de validação"""

    @staticmethod
    def validate_cpf(cpf):
        """Valida um CPF brasileiro"""
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)

        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False

        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False

        # Valida primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10

        if int(cpf[9]) != digito1:
            return False

        # Valida segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10

        if int(cpf[10]) != digito2:
            return False

        return True

    @staticmethod
    def validate_cnpj(cnpj):
        """Valida um CNPJ brasileiro"""
        # Remove caracteres não numéricos
        cnpj = re.sub(r'\D', '', cnpj)

        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False

        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False

        # Valida primeiro dígito verificador
        peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * peso[i] for i in range(12))
        digito1 = 11 - (soma % 11)
        digito1 = 0 if digito1 >= 10 else digito1

        if int(cnpj[12]) != digito1:
            return False

        # Valida segundo dígito verificador
        peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * peso[i] for i in range(13))
        digito2 = 11 - (soma % 11)
        digito2 = 0 if digito2 >= 10 else digito2

        if int(cnpj[13]) != digito2:
            return False

        return True

    @staticmethod
    def validate_cpf_cnpj(doc):
        """Valida CPF ou CNPJ automaticamente"""
        doc = re.sub(r'\D', '', doc)
        if len(doc) == 11:
            return Validators.validate_cpf(doc)
        elif len(doc) == 14:
            return Validators.validate_cnpj(doc)
        return False

    @staticmethod
    def validate_email(email):
        """Valida um endereço de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Valida um telefone brasileiro"""
        # Remove caracteres não numéricos
        phone = re.sub(r'\D', '', phone)

        # Aceita telefones com 10 ou 11 dígitos
        return len(phone) in [10, 11]

    @staticmethod
    def validate_date(date_str, date_format='%d/%m/%Y'):
        """Valida uma data"""
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_number(value, allow_negative=False, allow_decimal=True):
        """Valida se é um número"""
        try:
            num = float(value) if allow_decimal else int(value)
            if not allow_negative and num < 0:
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_cep(cep):
        """Valida um CEP brasileiro"""
        cep = re.sub(r'\D', '', cep)
        return len(cep) == 8

    @staticmethod
    def format_cpf(cpf):
        """Formata um CPF"""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf

    @staticmethod
    def format_cnpj(cnpj):
        """Formata um CNPJ"""
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj

    @staticmethod
    def format_phone(phone):
        """Formata um telefone"""
        phone = re.sub(r'\D', '', phone)
        if len(phone) == 11:
            return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
        elif len(phone) == 10:
            return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
        return phone

    @staticmethod
    def format_cep(cep):
        """Formata um CEP"""
        cep = re.sub(r'\D', '', cep)
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep

    @staticmethod
    def validate_required_fields(data, required_fields):
        """Valida se todos os campos obrigatórios estão preenchidos"""
        missing = []
        for field in required_fields:
            if field not in data or not data[field] or str(data[field]).strip() == '':
                missing.append(field)
        return len(missing) == 0, missing
