"""Formato de salida del modo DIG."""
from core.prefixes import Eng_Num_OUT


def programmer_prepare_env(local_env):
    local_env.update({"int": int, "bin": bin, "hex": hex, "abs": abs, "pow": pow})


def _group(digits: str, size: int) -> str:
    digits = "0" * ((size - len(digits) % size) % size) + digits
    return " ".join(digits[i:i + size] for i in range(0, len(digits), size))


def format_bin(val: int) -> str:
    """Binario agrupado de 8 en 8 bits."""
    return _group(bin(val)[2:], 8)


def format_hex(val: int) -> str:
    """Hex agrupado de 4 en 4 dígitos."""
    return _group(hex(val)[2:].upper(), 4)


def programmer_format_result(raw_result, base):
    try:
        if isinstance(raw_result, complex):
            real = raw_result.real; imag = raw_result.imag
            if abs(imag) < 1e-12: imag = 0
            if abs(real) < 1e-12: real = 0
            if imag == 0: return str(int(real)) if float(real).is_integer() else str(real)
            if real == 0: return f"{imag}i"
            sign = "+" if imag >= 0 else "-"
            return f"{real} {sign} {abs(imag)}i"
        if isinstance(raw_result, (int,)) or (isinstance(raw_result, float) and float(raw_result).is_integer()):
            val = int(raw_result)
            if base == "DEC": return str(val)
            elif base == "hex": return format_hex(val)
            elif base == "bin": return format_bin(val)
        else:
            return Eng_Num_OUT(float(raw_result))
    except Exception:
        return str(raw_result)
