"""Validación y conversión de tokens por base."""
import re

_BASES = {  # base: (patrón, radix)
    "HEX": (r"[0-9A-F]+", 16),
    "OCT": (r"[0-7]+", 8),
    "BIN": (r"[01]+", 2),
    "DEC": (r"[0-9]+", 10),
}


def DIG_IN(base_mode, ch):
    if base_mode == "HEX":
        return ch.upper() in "0123456789ABCDEF"
    if base_mode == "DEC":
        return ch in "0123456789"
    if base_mode == "OCT":
        return ch in "01234567"
    if base_mode == "BIN":
        return ch in "01"
    return False


def prog_token_to_decimal(token: str, base_mode: str):
    tok = token.upper()
    if base_mode in _BASES:
        pattern, radix = _BASES[base_mode]
        if re.fullmatch(pattern, tok):
            return str(int(tok, radix))
        raise ValueError(f"Invalid {base_mode} token: {token}")
    return token
