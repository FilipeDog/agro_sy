# -*- coding: utf-8 -*-
"""
Gerenciador de Temas do Sistema
Permite alternar entre tema claro e escuro
"""
import json
import os

class ThemeManager:
    """Gerencia temas do aplicativo"""

    THEMES = {
        'light': {
            'name': 'Claro',
            'bg': '#f0f0f0',
            'fg': '#000000',
            'selectbg': '#0078d7',
            'selectfg': '#ffffff',
            'fieldbg': '#ffffff',
            'ttktheme': 'flatly'
        },
        'dark': {
            'name': 'Escuro',
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'selectbg': '#0078d7',
            'selectfg': '#ffffff',
            'fieldbg': '#3c3c3c',
            'ttktheme': 'darkly'
        }
    }

    def __init__(self, config_file='cattle_management/config/theme_config.json'):
        self.config_file = config_file
        self.current_theme = self.load_theme()

    def load_theme(self):
        """Carrega tema salvo ou usa padrão"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('theme', 'light')
        except:
            pass
        return 'light'

    def save_theme(self, theme):
        """Salva tema selecionado"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump({'theme': theme}, f)
            self.current_theme = theme
            return True
        except Exception as e:
            print(f"Erro ao salvar tema: {e}")
            return False

    def get_theme(self):
        """Retorna configurações do tema atual"""
        return self.THEMES.get(self.current_theme, self.THEMES['light'])

    def get_theme_name(self):
        """Retorna nome do tema atual"""
        return self.get_theme()['name']

    def toggle_theme(self):
        """Alterna entre temas"""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_theme(new_theme)
        return new_theme

    def set_theme(self, theme):
        """Define tema específico"""
        if theme in self.THEMES:
            self.save_theme(theme)
            return True
        return False

    def get_ttkbootstrap_theme(self):
        """Retorna nome do tema ttkbootstrap"""
        return self.get_theme()['ttktheme']
