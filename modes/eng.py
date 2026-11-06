"""Modo ENG: teclado y registro."""
from core.env import engineering_prepare_env
from core.formatting import eng_format_result

ENG_LAYOUT = [
    ["DEG", "Modes", "funct", "(", ")"],
    ["7", "8", "9", "/", "^"],
    ["4", "5", "6", "*", "DEL"],
    ["1", "2", "3", "-", "CLR"],
    [".", "0", "i", "+", "="]
]

ENG_MODE = {
    "layout": ENG_LAYOUT,
    "prepare_env": engineering_prepare_env,
    "format_result": eng_format_result,
}
