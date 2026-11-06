"""Convierte bloques de fracción multilínea (num / ---- / den) a '(num)/(den)'."""
from .constants import DIVISIONLINE

DASH = DIVISIONLINE[0]


def read_token_around(s, div_start):
    """Token no vacío (sin espacios) que cubre la columna div_start."""
    token_start = div_start
    while token_start > 0 and not s[token_start - 1].isspace():
        token_start -= 1
    token_end = div_start
    while token_end < len(s) and not s[token_end].isspace():
        token_end += 1
    return s[token_start:token_end].strip()


def replace_fraction_blocks(text: str) -> str:
    lines = text.splitlines()
    out_parts = []
    i = 0
    divlen = len(DIVISIONLINE)
    while i < len(lines):
        if i + 2 < len(lines) and DIVISIONLINE in lines[i + 1]:
            top, mid, bot = lines[i], lines[i + 1], lines[i + 2]
            maxlen = max(len(top), len(mid), len(bot))
            top, mid, bot = top.ljust(maxlen), mid.ljust(maxlen), bot.ljust(maxlen)
            j = 0
            expr = []
            while j < maxlen:
                if mid.startswith(DIVISIONLINE, j):
                    start = j
                    num = read_token_around(top, start) or "0"
                    den = read_token_around(bot, start) or "1"
                    expr.append(f"({num})/({den})")
                    # saltar toda la barra contigua
                    while j < maxlen and mid[j] == DASH:
                        j += 1
                    if j == start:      # seguro anti-cuelgue
                        j = start + divlen
                else:
                    ch = mid[j]
                    if ch != DASH and not ch.isspace() and ch != '/':
                        expr.append(ch)
                    j += 1
            out_parts.append(''.join(expr))
            i += 3
        else:
            out_parts.append(lines[i])
            i += 1
    return ' '.join(p for p in out_parts if p.strip())