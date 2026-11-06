"""Registro de modos. Para agregar uno: crear modes/<nombre>/ y añadirlo aquí."""
from .dig import DIG_MODE
from .eng import ENG_MODE

MODULES = {"ENG": ENG_MODE, "DIG": DIG_MODE}
