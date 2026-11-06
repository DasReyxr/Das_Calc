"""Prefijos SI: '1k' -> 1000.0 (entrada) y 1000 -> '1k' (salida)."""
import math
import re

from .constants import ENG_PREFIXES


def Eng_Num_IN(expr: str) -> str:
    # número+prefijo seguido de 'i' (1ki, 1k i)
    pat_i = re.compile(r'(?<![A-Za-z0-9_.])([0-9]*\.?[0-9]+)\s*([TGMkmunpf])\s*i(?![A-Za-z0-9_])')
    def repl_i(m):
        try:
            return f"{float(m.group(1)) * ENG_PREFIXES[m.group(2)]}i"
        except Exception:
            return m.group(0)
    expr = pat_i.sub(repl_i, expr)

    # número+prefijo suelto (1k, 3.3u)
    pat = re.compile(r'(?<![A-Za-z0-9_.])([0-9]*\.?[0-9]+)\s*([TGMkmunpf])(?![A-Za-z0-9_\.])')
    def repl(m):
        try:
            return str(float(m.group(1)) * ENG_PREFIXES[m.group(2)])
        except Exception:
            return m.group(0)
    return pat.sub(repl, expr)


def Eng_Num_OUT(value: float) -> str:
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value)) / 3) * 3)
    exponent = max(min(exponent, 15), -15)
    scaled = value / (10 ** exponent)
    prefix_map = {
        12: "T", 9: "G", 6: "M", 3: "k",
        0: "",
        -3: "m", -6: "u", -9: "n", -12: "p"
    }
    prefix = prefix_map.get(exponent, f"e{exponent}")
    return f"{scaled:g}{prefix}"
