"""Borrar una fracción completa (num, barra, den) con Backspace/Delete sobre la barra."""
import tkinter as tk

from core.constants import DIVISIONLINE


def token_span(s, idx):
    s2 = s.replace('\t', '      ')
    k = idx
    while k < len(s2) and s2[k].isspace():
        k += 1
    a = k
    while k < len(s2) and not s2[k].isspace():
        k += 1
    return a, k


class FractionDeleteMixin:
    def _dash_run(self, line, start, end):
        """Expande [start,end) sobre los guiones contiguos; None si no hay barra válida."""
        full_line = self.display.get(f"{line}.0", f"{line}.end")
        if DIVISIONLINE not in full_line:
            return None
        while start > 0 and full_line[start - 1] == DIVISIONLINE[0]:
            start -= 1
        while end < len(full_line) and full_line[end] == DIVISIONLINE[0]:
            end += 1
        return (start, end) if end - start >= len(DIVISIONLINE) else None

    def _delete_fraction_at(self, line, start, end):
        d = self.display
        top = d.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
        bot = d.get(f"{line+1}.0", f"{line+1}.end")
        a_top, b_top = token_span(top, start)
        a_bot, b_bot = token_span(bot, start)
        if line > 1 and b_top > a_top:
            d.delete(f"{line-1}.{a_top}", f"{line-1}.{b_top}")
        d.delete(f"{line}.{start}", f"{line}.{end}")
        if b_bot > a_bot:
            d.delete(f"{line+1}.{a_bot}", f"{line+1}.{b_bot}")
        d.mark_set(tk.INSERT, f"{line}.{start}")

    def on_backspace(self, event=None):
        try:
            line, col = map(int, self.display.index(tk.INSERT).split("."))
            if col == 0:
                return None
            if self.display.get(f"{line}.{col-1}", f"{line}.{col}") == DIVISIONLINE[0]:
                run = self._dash_run(line, col - 1, col)
                if run:
                    self._delete_fraction_at(line, *run)
                    return "break"
        except Exception:
            pass
        return None

    def on_delete_key(self, event=None):
        try:
            line, col = map(int, self.display.index(tk.INSERT).split("."))
            if self.display.get(f"{line}.{col}", f"{line}.{col+1}") == DIVISIONLINE[0]:
                run = self._dash_run(line, col, col)
                if run:
                    self._delete_fraction_at(line, *run)
                    return "break"
        except Exception:
            pass
        return None
