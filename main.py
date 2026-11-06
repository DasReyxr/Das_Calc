"""
Das Calculator — punto de entrada. Ver AGENTS.md para el mapa de módulos.
PyInstaller (desde esta carpeta): python -m PyInstaller --noconfirm --clean DasCalculator.spec
"""
from ui.app import run

if __name__ == "__main__":
    run()
