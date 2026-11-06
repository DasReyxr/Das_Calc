"""Evaluación del modo DIG: tokeniza, convierte a decimal según la base y evalúa con enteros."""
import re

from .format import format_bin, format_hex
from .tokens import prog_token_to_decimal

_OPS = ("<<", ">>", "&", "|", "^", "+", "-", "*", "/", "(", ")")
_TOKEN_RE = re.compile(r"([0-9A-Fa-f]+|<<|>>|<|>|[&\|\^\+\-\*\/\(\)])")


def _pack(val: int) -> dict:
    return {"DEC": str(val), "HEX": format_hex(val), "OCT": oct(val)[2:], "BIN": format_bin(val)}


def evaluate_programmer(expr: str, base_mode: str) -> dict:
    expr = expr.replace(" ", "")
    expr = expr.replace("<<", " __SHIFT_L__ ").replace(">>", " __SHIFT_R__ ")
    expr = re.sub(r"(?<!__SHIFT_L__)(?<!__SHIFT_R__)<", " < ", expr)
    expr = re.sub(r"(?<!__SHIFT_L__)(?<!__SHIFT_R__)>", " > ", expr)
    expr = expr.replace("__SHIFT_L__", "<<").replace("__SHIFT_R__", ">>")

    if expr == "<":
        return _pack(1 << 1)
    if expr == ">":
        return _pack(1 >> 1)

    tokens = _TOKEN_RE.findall(expr)
    out_tokens = [t if t in _OPS else prog_token_to_decimal(t, base_mode) for t in tokens]
    raw = eval(" ".join(out_tokens), {"__builtins__": None}, {})
    return _pack(int(raw))
