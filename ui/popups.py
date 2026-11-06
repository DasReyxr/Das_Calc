"""Popups de modos y de funciones."""
import customtkinter as ctk

from modes import MODULES


class PopupsMixin:
    def open_modes_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Select Mode")
        win.geometry("300x220")
        win.transient(self)
        ctk.CTkLabel(win, text="Choose a mode", font=("Arial", 14)).pack(pady=8)
        for name in MODULES.keys():
            b = ctk.CTkButton(win, text=name.capitalize(), command=lambda n=name, w=win: self.select_mode(n, w))
            b.pack(fill="x", padx=12, pady=6)
        win.grab_set()

    def show_functions_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Functions")
        win.geometry("320x400")
        win.transient(self)

        funcs = [
            ("sin(x)", "sin("), ("cos(x)", "cos("), ("tan(x)", "tan("),
            ("sqrt(x)", "sqrt("), ("ln(x)", "log("), ("log10(x)", "log("),
            ("exp(x)", "exp("), ("abs(x)", "abs("), ("pi", "pi"), ("e", "e"),
            ("rect(x,y)", "rect("), ("pol(r,θ)", "pol(")
        ]
        for name, ins in funcs:
            b = ctk.CTkButton(win, text=name, command=lambda t=ins: self.insert_func_from_popup(t, win))
            b.pack(pady=6, padx=8, fill="x")

    def insert_func_from_popup(self, s: str, win):
        try:
            self.insert_text(s)
        finally:
            win.destroy()
