"""Ventana: app id de Windows, icono y rejilla de tabs del display."""
import ctypes
import sys
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path


class WindowMixin:
    def _set_windows_app_id(self):
        if sys.platform != "win32":
            return
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AufDas.DasCalculator")
        except Exception:
            pass

    def _set_window_icon(self):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)) / "assets"
        icon_ico = base_dir / "ALU.ico"
        icon_png = base_dir / "ALU.png"

        try:
            if icon_ico.exists():
                self.iconbitmap(default=str(icon_ico))
                self.iconbitmap(str(icon_ico))
                return
        except Exception:
            pass

        try:
            if not icon_png.exists():
                return

            self._app_icon = tk.PhotoImage(file=str(icon_png))
            w = max(1, self._app_icon.width())
            h = max(1, self._app_icon.height())
            subsample_32 = max(1, min(w // 32, h // 32))
            subsample_16 = max(1, min(w // 16, h // 16))
            self._app_icon_32 = self._app_icon.subsample(subsample_32, subsample_32)
            self._app_icon_16 = self._app_icon.subsample(subsample_16, subsample_16)
            self.iconphoto(True, self._app_icon, self._app_icon_32, self._app_icon_16)
            self.wm_iconphoto(True, self._app_icon, self._app_icon_32, self._app_icon_16)
        except Exception:
            pass

    def configure_tab_grid(self, cell_chars=6, max_cells=40):
        try:
            f = tkfont.Font(font=("Consolas", 28))
            cell_px = f.measure(" " * cell_chars)
            # Build a list of tab stops in pixels
            stops = tuple((i+1) * cell_px for i in range(max_cells))
            # CTkTextbox is tk.Text under the hood; we can set tabs option
            self.display.configure(tabs=stops)
        except Exception:
            pass
