"""Normalización de expresiones ENG: símbolos, 'i'->j, multiplicación implícita, polar 'r L θ'."""
import re


def Input_Clean(expr: str) -> str:
    expr = expr.strip()
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("^", "**")
    num_pat = r'(?<![A-Za-z0-9_\.])((?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?)'
    expr = re.sub(num_pat + r'\s*i(?![A-Za-z0-9_])', r'(\1)*j', expr)
    expr = re.sub(num_pat + r'i(?![A-Za-z0-9_])', r'(\1)*j', expr)
    expr = re.sub(r'(?<![a-zA-Z0-9_])i(?![a-zA-Z0-9_])', '1*j', expr)
    return expr


def insert_implicit_multiplication(expr: str):
    expr = re.sub(r'(\d|\))\s*\(', r'\1*(', expr)
    expr = re.sub(r'\)\s*(\d|[a-zA-Z])', r')*\1', expr)
    expr = re.sub(r'(\d)\s*([a-zA-Z])', r'\1*\2', expr)
    expr = expr.replace("pi", "*pi") if re.search(r'\dpi', expr) else expr
    expr = expr.replace("e", "*e") if re.search(r'\de', expr) else expr
    expr = expr.replace("*pi", "pi", 1) if expr.startswith("*pi") else expr
    expr = expr.replace("*e", "e", 1) if expr.startswith("*e") else expr
    return expr


def polar_literal_to_func(expr: str) -> str:
    """'r L theta' (opcional °) -> 'pol(r,theta)'. Soporta varias ocurrencias."""
    number = r"[+\-]?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?"
    pat = re.compile(rf"(?<![A-Za-z0-9_\.])\s*({number})\s*[L]\s*({number})(?:°)?(?![A-Za-z0-9_\.])")
    prev = None
    out = expr
    while prev != out:
        prev = out
        out = pat.sub(lambda m: f"pol({m.group(1)},{m.group(2)})", out)
    return out
