"""Entorno de eval para ENG: funciones complejas, trig en grados/radianes, rect/pol."""
import math

from .constants import BASE_FUNCS


def deg_wrap(fn):
    return lambda x: fn(math.radians(x))


def engineering_prepare_env(local_env):
    local_env.update(BASE_FUNCS.copy())


def build_env(use_degrees: bool) -> dict:
    env = {}
    engineering_prepare_env(env)
    if use_degrees:
        env.update({"sin": deg_wrap(math.sin), "cos": deg_wrap(math.cos), "tan": deg_wrap(math.tan)})
    else:
        env.update({"sin": math.sin, "cos": math.cos, "tan": math.tan})
    # rect/pol siguen el sin/cos activo (grados o radianes)
    env.update({
        "rect": lambda x, y: complex(x, y),
        "pol": lambda r, th: r * (complex(env["cos"](th), env["sin"](th))),
        "toRect": lambda r, th: r * (complex(env["cos"](th), env["sin"](th))),
    })
    return env
