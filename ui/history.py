"""Historial: clic y navegación con flechas."""
import tkinter as tk
import traceback


class HistoryMixin:
    def select_history(self, event):
        try:
            idx = self.history_box.index(f"@{event.x},{event.y}")
            line_no = idx.split(".")[0]
            line_text = self.history_box.get(f"{line_no}.0", f"{line_no}.end").strip()
            if not line_text:
                return
            expr_part = line_text.split(" = ", 1)[0] if " = " in line_text else line_text
            self.display.delete("1.0", "end")
            self.display.insert("1.0", expr_part)
            self.display.mark_set(tk.INSERT, "end-1c")
            for i, (e, r) in enumerate(self.history):
                if e == expr_part:
                    self.history_index = i
                    break
            else:
                self.history_index = len(self.history)
        except Exception:
            traceback.print_exc()

    def load_prev(self, event=None):
        if not self.history:
            return "break"
        if self.history_index is None:
            self.history_index = len(self.history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)
        expr, res = self.history[self.history_index]
        self.display.delete("1.0", "end")
        self.display.insert("1.0", expr)
        self.display.mark_set(tk.INSERT, "end-1c")
        return "break"

    def load_next(self, event=None):
        if not self.history or self.history_index is None:
            return "break"
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            expr, res = self.history[self.history_index]
            self.display.delete("1.0", "end")
            self.display.insert("1.0", expr)
            self.display.mark_set(tk.INSERT, "end-1c")
        else:
            self.history_index = None
            self.display.delete("1.0", "end")
        return "break"
