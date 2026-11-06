"""Teclado, cambio de modo (ENG/DIG), DEG/RAD y base del modo DIG."""
import customtkinter as ctk

from modes import MODULES


class KeypadMixin:
    def select_mode(self, name, win):
        self.calc_mode = name
        self.build_keypad_for_mode(name)

        if name == "DIG":
            if not hasattr(self, "base_mode_btn"):
                self.base_mode_btn = ctk.CTkButton(
                    self,
                    text=f"Base: {self.base_mode}",
                    width=120,
                    command=self.toggle_base_mode
                )
                self.base_mode_btn.pack(pady=4)
            else:
                self.base_mode_btn.configure(text=f"Base: {self.base_mode}")
            self.output_label.configure(text="PROGRAMMER MODE")
            if hasattr(self, "mode_indicator"):
                self.mode_indicator.configure(text="")
        else:
            if hasattr(self, "base_mode_btn"):
                try:
                    self.base_mode_btn.destroy()
                    del self.base_mode_btn
                except Exception:
                    pass
            self.output_label.configure(text="")
            if hasattr(self, "mode_indicator"):
                mode = "Degrees" if self.use_degrees else "Radians"
                self.mode_indicator.configure(text=f"Mode: {mode}")

        win.destroy()

    def build_keypad_for_mode(self, mode_name):
        for child in self.keypad_frame.winfo_children():
            child.destroy()
        layout = MODULES[mode_name]["layout"]
        for r, row in enumerate(layout):
            for c, txt in enumerate(row):
                if txt == "":
                    continue
                cmd = lambda val=txt: self.button_press(val)
                if mode_name == "DIG" and txt in ("DEL", "CLR", "="):
                    if txt == "DEL": cmd = lambda val=txt: self.button_press("DEL")
                    if txt == "CLR": cmd = lambda val=txt: self.button_press("CLR")
                    if txt == "=": cmd = lambda val=txt: self.button_press("=")
                elif mode_name == "DIG" and txt == "HEX":
                    cmd = lambda: self.toggle_base_mode()
                b = ctk.CTkButton(self.keypad_frame, text=txt, width=90, command=cmd)
                b.grid(row=r, column=c, padx=5, pady=5)

    def toggle_mode(self):
        self.use_degrees = not self.use_degrees
        mode = "Degrees" if self.use_degrees else "Radians"
        self.mode_btn.configure(text=f"Mode: {mode}")
        if hasattr(self, "mode_indicator"):
            self.mode_indicator.configure(text=f"Mode: {mode}")

    def button_press(self, key: str):
        if key == "Modes":
            self.open_modes_popup()
            return
        if key == "funct":
            self.show_functions_popup()
            return
        if key == "/" and self.calc_mode == "ENG":
            self.on_slash()
            return
        if self.calc_mode == "DIG" and key == "MODE":
            self.toggle_base_mode()
            return
        if key == "<":
            self.insert_text("<<")
            return
        if key == ">":
            self.insert_text(">>")
            return
        if key == "DEG" and self.calc_mode == "ENG":
            self.toggle_mode()
            return
        if key == "CLR":
            self.display.delete("1.0", "end")
            self.output_label.configure(text="")
            return
        if key == "DEL":
            self.delete_char()
            return
        if key == "=":
            self.evaluate()
            return
        self.insert_text(str(key))

    def toggle_base_mode(self):
        order = ["DEC", "HEX", "OCT", "BIN"]
        idx = order.index(self.base_mode)
        self.base_mode = order[(idx + 1) % len(order)]
        if hasattr(self, "base_mode_btn"):
            self.base_mode_btn.configure(text=f"Base: {self.base_mode}")
        self.output_label.configure(text=f"Switched to {self.base_mode}")
