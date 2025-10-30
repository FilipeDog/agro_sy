"""
Utilitários de Interface - Helpers para compatibilidade tkinter/ttkbootstrap
"""
import tkinter as tk

# Detectar se ttkbootstrap está disponível
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    import tkinter.ttk as ttk
    from tkinter.constants import *
    TTKBOOTSTRAP_AVAILABLE = False


def create_button(parent, text, command, width=None, style=None, **kwargs):
    """
    Cria um botão compatível com tkinter e ttkbootstrap

    Args:
        parent: Widget pai
        text: Texto do botão
        command: Função callback
        width: Largura do botão
        style: Estilo do botão (success, danger, primary, etc.) - ignorado se ttkbootstrap não disponível
        **kwargs: Outros parâmetros do botão

    Returns:
        Button widget
    """
    button_kwargs = {
        'text': text,
        'command': command,
        **kwargs
    }

    if width:
        button_kwargs['width'] = width

    # Usar bootstyle apenas se ttkbootstrap estiver disponível
    if TTKBOOTSTRAP_AVAILABLE and style:
        button_kwargs['bootstyle'] = style

    return ttk.Button(parent, **button_kwargs)


def create_window(title="", theme="darkly"):
    """
    Cria uma janela compatível

    Args:
        title: Título da janela
        theme: Tema (usado apenas com ttkbootstrap)

    Returns:
        Window ou Tk
    """
    if TTKBOOTSTRAP_AVAILABLE:
        try:
            root = ttk.Window(themename=theme)
        except:
            root = tk.Tk()
    else:
        root = tk.Tk()

    if title:
        root.title(title)

    return root


def create_frame(parent, style=None, **kwargs):
    """
    Cria um frame compatível

    Args:
        parent: Widget pai
        style: Estilo do frame (usado apenas com ttkbootstrap)
        **kwargs: Outros parâmetros

    Returns:
        Frame widget
    """
    frame_kwargs = dict(kwargs)

    if TTKBOOTSTRAP_AVAILABLE and style:
        frame_kwargs['bootstyle'] = style

    return ttk.Frame(parent, **frame_kwargs)
