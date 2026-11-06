"""Temas dark/pink."""
import customtkinter as ctk


class ThemeMixin:
    def setup_colors(self):
        """Define color palettes for dark and pink modes."""
        self.colors_dark = {
            "bg": "#0f0f10",
            "frame": "#1f1f20",
            "text": "#FFFFFF",
            "button": "#3a3a3a",
            "button_hover": "#4a4a4a",
            "entry": "#191919",
            "entry_text": "#FFFFFF",
            "border": "#333333",
            "textbox": "#141414",
            "label_text": "#FFFFFF",
            "button_text": "#FFFFFF",
        }

        self.colors_pink = {
            "bg": "#FFE4F0",
            "frame": "#FFF0F5",
            "text": "#8B4789",
            "button": "#FF69B4",
            "button_hover": "#FF1493",
            "entry": "#FFFFFF",
            "entry_text": "#8B4789",
            "border": "#FFB6D9",
            "textbox": "#FFFFFF",
            "label_text": "#8B4789",
            "button_text": "#FFFFFF",
        }

    def toggle_theme(self):
        """Switch between dark and pink modes."""
        # If switch text says "Dark Mode", user just switched OFF (to pink)
        # If switch text says "Pink Mode", user just switched ON (to dark)
        if self.current_mode == "dark":
            self.current_mode = "pink"
            self.current_colors = self.colors_pink.copy()
            self.mode_switch.configure(text="Pink Mode")
        else:
            self.current_mode = "dark"
            self.current_colors = self.colors_dark.copy()
            self.mode_switch.configure(text="Dark Mode")

        self.apply_dark_mode_colors()

    def apply_dark_mode_colors(self):
        """Apply current color scheme to all widgets."""
        self.configure(fg_color=self.current_colors["bg"])
        self.mode_switch.configure(
            text="Dark Mode" if self.current_mode == "dark" else "Pink Mode",
            fg_color=self.current_colors["frame"],
            text_color=self.current_colors["text"],
            button_color=self.current_colors["button"],
            progress_color=self.current_colors["button"]
        )

        # Apply colors to all widgets recursively
        for widget in self._get_all_widgets(self):
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=self.current_colors["frame"])
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(
                    fg_color="transparent",
                    text_color=self.current_colors["label_text"]
                )
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                    hover_color=self.current_colors["button_hover"]
                )
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(
                    fg_color=self.current_colors["entry"],
                    text_color=self.current_colors["entry_text"],
                    border_color=self.current_colors["border"]
                )
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(
                    fg_color=self.current_colors["textbox"],
                    text_color=self.current_colors["text"]
                )

    def _get_all_widgets(self, parent):
        """Recursively get all widgets from parent."""
        widgets = []
        for widget in parent.winfo_children():
            widgets.append(widget)
            widgets.extend(self._get_all_widgets(widget))
        return widgets
