"""Constantes compartidas por ENG y la UI."""
import cmath

BASE_FUNCS = {
    "abs": abs,
    "sin": cmath.sin,
    "cos": cmath.cos,
    "tan": cmath.tan,
    "sqrt": cmath.sqrt,
    "log": cmath.log,
    "exp": cmath.exp,
    "pi": cmath.pi,
    "e": cmath.e,
    "j": 1j,
}

ENG_PREFIXES = {
    'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3,
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9,
    'p': 1e-12, 'f': 1e-15
}

DIVISIONLINE = "----"
