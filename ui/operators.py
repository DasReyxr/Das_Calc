"""Operadores de teclado: +,-,* sobre la barra de fracción, Ctrl+/, < y > (DIG)."""
import tkinter as tk

from core.constants import DIVISIONLINE
from .textutil import ensure_col


class OperatorsMixin:
    def on_ctrl_slash(self, event=None):
        # Insert a literal DIVISIONLINE[0]: allows inline divisions like 1/2/3/4
        try:
            pos = self.display.index(tk.INSERT)
            self.display.insert(pos, "/")
            line, col = map(int, pos.split("."))
            self.display.mark_set(tk.INSERT, f"{line}.{col+1}")
            return "break"
        except Exception:
            return "break"

    def on_less_than(self, event=None):
        # Insert << when user types <
        if self.calc_mode == "DIG":
            self.display.insert(tk.INSERT, "<<")
            return "break"
        return None  # Allow normal < in ENG mode

    def on_greater_than(self, event=None):
        # Insert >> when user types >
        if self.calc_mode == "DIG":
            self.display.insert(tk.INSERT, ">>")
            return "break"
        return None  # Allow normal > in ENG mode


    def on_operator(self, event=None):
        """+, -, * sobre la barra de fracción cuando el cursor está en una fracción."""
        if self.calc_mode != "ENG":
            return None
        op = event.char if event and event.char else "+"
        d = self.display
        try:
            line, col = map(int, d.index(tk.INSERT).split("."))
            cur_line = d.get(f"{line}.0", f"{line}.end")
            prev_line = d.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            next_line = d.get(f"{line+1}.0", f"{line+1}.end")

            if DIVISIONLINE in next_line:      # en el numerador
                div_line = line + 1
            elif DIVISIONLINE in prev_line:    # en el denominador
                div_line = line - 1
            elif DIVISIONLINE in cur_line:     # ya en la barra: solo alinear
                ensure_col(d, line - 1, col)
                ensure_col(d, line + 1, col)
                return None
            else:
                return None

            new_col = max(col, len(cur_line)) + 1
            for ln in (div_line - 1, div_line, div_line + 1):
                ensure_col(d, ln, new_col)
            d.insert(f"{div_line}.{new_col}", op)
            d.mark_set(tk.INSERT, f"{div_line}.{new_col + 1}")
            return "break"
        except Exception:
            pass
        return None
