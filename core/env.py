"""Entorno de eval para ENG: funciones complejas, trig en grados/radianes, rect/pol."""
import cmath
import math

from .constants import BASE_FUNCS

_INVERSE = {"asin": cmath.asin, "acos": cmath.acos, "atan": cmath.atan}


def _real_if_possible(r):
    r = complex(r)
    return r.real if r.imag == 0 else r


def ln(x):
    return _real_if_possible(cmath.log(x))


def log10(x):
    return _real_if_possible(cmath.log10(x))


def log(x, base=None):
    """log(x) = ln(x); log(x, b) = log base b de x."""
    if base is None or base == 10:
        return log10(x)
    if base == 2 and not isinstance(x, complex) and x > 0:
        return math.log2(x)  # exacto para potencias de 2
    return _real_if_possible(cmath.log(x) / cmath.log(base))


def deg_wrap(fn):
    return lambda x: fn(math.radians(x))


def inv_wrap(fn, use_degrees):
    """Inversa trig: la salida es un ángulo, se convierte a grados si use_degrees."""
    def wrapped(x):
        r = fn(x)
        if use_degrees:
            r = r * 180 / math.pi
        return _real_if_possible(r)
    return wrapped


def engineering_prepare_env(local_env):
    local_env.update(BASE_FUNCS.copy())
    local_env.update({"ln": ln, "log10": log10, "log": log})


def build_env(use_degrees: bool) -> dict:
    env = {}
    engineering_prepare_env(env)
    if use_degrees:
        env.update({"sin": deg_wrap(math.sin), "cos": deg_wrap(math.cos), "tan": deg_wrap(math.tan)})
    else:
        env.update({"sin": math.sin, "cos": math.cos, "tan": math.tan})
    for name, fn in _INVERSE.items():
        f = inv_wrap(fn, use_degrees)
        env[name] = f
        env["arc" + name[1:]] = f
    env.update({
        "rect": lambda x, y: complex(x, y),
        "pol": lambda r, th: r * (complex(env["cos"](th), env["sin"](th))),
        "toRect": lambda r, th: r * (complex(env["cos"](th), env["sin"](th))),
    })
    return env