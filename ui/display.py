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
