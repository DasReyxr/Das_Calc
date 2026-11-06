"""Formato de resultados ENG: siempre Rect y Pol."""
import math

from .prefixes import Eng_Num_OUT


def eng_format_result(raw_result, use_degrees: bool = True):
    try:
        if isinstance(raw_result, (int, float, complex)):
            z = complex(raw_result)
            real, imag = z.real, z.imag
            if abs(real) < 1e-12: real = 0.0
            if abs(imag) < 1e-12: imag = 0.0
            if imag == 0.0:
                rect = f"{Eng_Num_OUT(float(real))}"
            elif real == 0.0:
                rect = f"{Eng_Num_OUT(float(imag))}i"
            else:
                sign = "+" if imag >= 0 else "-"
                rect = f"{Eng_Num_OUT(float(real))} {sign} {Eng_Num_OUT(float(abs(imag)))}i"

            r = abs(z)
            theta = math.atan2(z.imag, z.real)
            if use_degrees:
                pol = f"{Eng_Num_OUT(r)} L {math.degrees(theta):g}°"
            else:
                pol = f"{Eng_Num_OUT(r)} L {theta:g}"
            return f"Rect: {rect}\nPol:  {pol}"
        return str(raw_result)
    except Exception:
        return str(raw_result)
