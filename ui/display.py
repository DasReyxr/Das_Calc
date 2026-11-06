"""Edición básica del display."""
import tkinter as tk
import traceback


class DisplayMixin:
    def insert_text(self, s: str):
        self.display.insert(tk.INSERT, s)
        self.display.focus_set()

    def delete_char(self):
        try:
            if self.display.tag_ranges("sel"):
                start = self.display.index("sel.first")
                end = self.display.index("sel.last")
                self.display.delete(start, end)
            else:
                pos = self.display.index(tk.INSERT)
                if pos != "1.0":
                    self.display.delete(f"{pos}-1c")
        except Exception:
            traceback.print_exc()

    def get_selection_or_word(self):
        try:
            if self.display.tag_ranges("sel"):
                return self.display.get("sel.first", "sel.last")
        except Exception:
            pass
        return None

    def enter(self, event=None):
        self.evaluate()
        return "break"

    def select_all(self, event=None):
        """Ctrl+A: selecciona todo el contenido del display."""
        self.display.tag_add("sel", "1.0", "end-1c")
        self.display.mark_set(tk.INSERT, "end-1c")
        self.display.see(tk.INSERT)
        return "break"

    def undo(self, event=None):
        try:
            self.display.edit_undo()
        except tk.TclError:
            pass   # nada que deshacer
        return "break"

    def redo(self, event=None):
        try:
            self.display.edit_redo()
        except tk.TclError:
            pass   # nada que rehacer
        return "break"