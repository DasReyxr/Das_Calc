"""Modo DIG (programador): registro."""
from .format import programmer_format_result, programmer_prepare_env
from .layout import DIG_LAYOUT

DIG_MODE = {
    "layout": DIG_LAYOUT,
    "prepare_env": programmer_prepare_env,
    "format_result": programmer_format_result,
}
