"""Botón de actualización."""
import threading
import webbrowser
from tkinter import messagebox

from core import updater


class UpdateMixin:
    def check_for_updates(self):
        self.update_btn.configure(state="disabled", text="Checking...")
        threading.Thread(target=self._check_worker, daemon=True).start()

    def _reset_update_btn(self):
        self.update_btn.configure(state="normal", text="Update")

    def _check_worker(self):
        try:
            info = updater.check_latest()
        except Exception as e:
            self.after(0, lambda: (self._reset_update_btn(),
                                   messagebox.showerror("Update", f"No se pudo consultar: {e}")))
            return
        self.after(0, lambda: self._on_update_result(info))

    def _on_update_result(self, info):
        self._reset_update_btn()
        if info is None:
            messagebox.showinfo("Update", "Ya tienes la última versión.")
            return
        if not (updater.can_self_update() and info["asset_url"]):
            if messagebox.askyesno("Update", f"Hay una versión {info['version']}. ¿Abrir la página de descarga?"):
                webbrowser.open(info["page"])
            return
        if messagebox.askyesno("Update", f"Versión {info['version']} disponible. ¿Actualizar ahora?"):
            self.update_btn.configure(state="disabled", text="Updating...")
            threading.Thread(target=self._download_worker, args=(info["asset_url"],), daemon=True).start()

    def _download_worker(self, url):
        try:
            updater.download_and_replace(url)  # si tiene éxito, reinicia y no regresa
        except Exception as e:
            self.after(0, lambda: (self._reset_update_btn(),
                                   messagebox.showerror("Update", f"Falló la actualización: {e}")))