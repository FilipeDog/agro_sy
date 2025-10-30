"""
Calculadora Integrada - AgroGestor - Sistema de Gestão de Rebanho
Janela popup com calculadora funcional
"""
import tkinter as tk
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    from tkinter.constants import *
    import tkinter.ttk as ttk


class Calculator:
    """Janela de calculadora"""

    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Calculadora")
        self.window.geometry("300x400")
        self.window.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """Cria a interface da calculadora"""
        # Display
        display_frame = ttk.Frame(self.window, padding=10)
        display_frame.pack(fill=X)

        display = ttk.Entry(
            display_frame,
            textvariable=self.input_text,
            font=('Arial', 20),
            justify=RIGHT,
            state='readonly'
        )
        display.pack(fill=X, ipady=10)

        # Botões
        buttons_frame = ttk.Frame(self.window, padding=10)
        buttons_frame.pack(fill=BOTH, expand=YES)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C', '(', ')', '+']
        ]

        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                btn = ttk.Button(
                    buttons_frame,
                    text=btn_text,
                    command=lambda x=btn_text: self.on_button_click(x)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

                # Configurar tamanho das células
                buttons_frame.grid_rowconfigure(i, weight=1)
                buttons_frame.grid_columnconfigure(j, weight=1)

        # Instruções
        instructions = ttk.Label(
            self.window,
            text="Use o teclado ou clique nos botões",
            font=('Arial', 8)
        )
        instructions.pack(pady=5)

        # Bindings de teclado
        self.window.bind('<Key>', self.on_key_press)
        self.window.bind('<Return>', lambda e: self.on_button_click('='))
        self.window.bind('<Escape>', lambda e: self.window.destroy())

    def on_button_click(self, char):
        """Manipula cliques nos botões"""
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.clear()
        elif char == '+':
            self.backspace()
        else:
            self.expression += str(char)
            self.input_text.set(self.expression)

    def on_key_press(self, event):
        """Manipula teclas pressionadas"""
        key = event.char
        if key in '0123456789+-*/.()':
            self.expression += key
            self.input_text.set(self.expression)
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif key in ['c', 'C']:
            self.clear()

    def calculate(self):
        """Calcula a expressão"""
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception:
            self.input_text.set("Erro")
            self.expression = ""

    def clear(self):
        """Limpa a calculadora"""
        self.expression = ""
        self.input_text.set("")

    def backspace(self):
        """Remove o último caractere"""
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)

    def run(self):
        """Executa a calculadora"""
        self.window.mainloop()


def open_calculator(parent=None):
    """Abre a calculadora em uma nova janela"""
    calc = Calculator(parent)
    return calc
