"""Pipeline ENG: fracciones -> polar -> prefijos -> limpieza -> eval -> formato."""
from .env import build_env
from .formatting import eng_format_result
from .frac_blocks import replace_fraction_blocks
from .parser import Input_Clean, insert_implicit_multiplication, polar_literal_to_func
from .prefixes import Eng_Num_IN


def evaluate_eng(raw_expr: str, use_degrees: bool):
    """Devuelve (expr_en_una_línea, resultado_str). Propaga errores de eval (p.ej. ZeroDivisionError)."""
    print(f"DEBUG raw_expr:\n{repr(raw_expr)}")
    expr = replace_fraction_blocks(raw_expr)
    print(f"DEBUG after replace_fraction_blocks: {repr(expr)}")
    expr = polar_literal_to_func(expr)

    expr_for_eval = insert_implicit_multiplication(Input_Clean(Eng_Num_IN(expr)))
    raw_result = eval(expr_for_eval, {"__builtins__": None}, build_env(use_degrees))
    try:
        result_str = eng_format_result(raw_result, use_degrees)
    except Exception:
        result_str = str(raw_result)
    return expr, result_str
