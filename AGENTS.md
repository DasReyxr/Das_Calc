# AGENTS.md — Das Calculator

Calculadora de ingeniería (complejos, prefijos SI, polar/rect, fracciones apiladas) y modo programador (DEC/HEX/OCT/BIN). GUI con `customtkinter`.

## Regla de oro
**Abre solo el módulo que vas a tocar.** Un archivo = una responsabilidad (~150 líneas máx.). Dependencias solo hacia abajo: `ui → modes → core`. `core` nunca importa `ui` ni `modes`.

## Tree
```
main.py                 entrada: llama ui.app.run()
DasCalculator.spec      PyInstaller (entrada main.py, assets/ como datas)
assets/                 ALU.ico, ALU.png
core/                   lógica ENG pura, sin tkinter
modes/                  modos de calculadora (registro MODULES)
ui/                     GUI: un mixin por funcionalidad
```

## core/ (probar sin GUI)
| Archivo | Responsabilidad | Símbolos |
|---|---|---|
| `constants.py` | Constantes compartidas | `BASE_FUNCS`, `ENG_PREFIXES`, `DIVISIONLINE` |
| `prefixes.py` | Prefijos SI (1k↔1000) | `Eng_Num_IN`, `Eng_Num_OUT` |
| `parser.py` | Normaliza expresión: `^`→`**`, `i`→`j`, mult. implícita, `r L θ`→`pol(r,θ)` | `Input_Clean`, `insert_implicit_multiplication`, `polar_literal_to_func` |
| `env.py` | Entorno de `eval`: trig en grados/radianes, `rect`, `pol`, `toRect` | `deg_wrap`, `engineering_prepare_env`, `build_env(use_degrees)` |
| `formatting.py` | Resultado ENG en líneas `Rect:` y `Pol:` | `eng_format_result` |
| `frac_blocks.py` | Bloque de fracción multilínea → `(num)/(den)` | `replace_fraction_blocks` |
| `evaluator.py` | Pipeline ENG completo | `evaluate_eng(raw_expr, use_degrees) -> (expr, resultado)` |

## modes/
| Archivo | Responsabilidad |
|---|---|
| `__init__.py` | Registro `MODULES = {"ENG", "DIG"}` (layout, prepare_env, format_result) |
| `eng.py` | `ENG_LAYOUT` + entrada del registro |
| `dig/__init__.py` | Entrada del registro DIG |
| `dig/layout.py` | `DIG_LAYOUT` |
| `dig/tokens.py` | `DIG_IN`, `prog_token_to_decimal` (token de una base → decimal) |
| `dig/evaluate.py` | `evaluate_programmer(expr, base_mode)` → dict `DEC/HEX/OCT/BIN` |
| `dig/format.py` | `format_bin` (8 bits), `format_hex` (4 dígitos), `programmer_format_result`, `programmer_prepare_env` |

Modo nuevo: crear `modes/<nombre>/` y registrarlo en `modes/__init__.py`.

## ui/ (cada archivo es un mixin de `EngCalculator`)
| Archivo | Métodos |
|---|---|
| `app.py` | `EngCalculator.__init__` (construye widgets y bindings) + `run()`. Solo composición |
| `window.py` | `_set_windows_app_id`, `_set_window_icon` (lee `assets/`), `configure_tab_grid` |
| `theme.py` | `setup_colors`, `toggle_theme`, `apply_dark_mode_colors`, `_get_all_widgets` |
| `keypad.py` | `select_mode`, `build_keypad_for_mode`, `toggle_mode` (DEG/RAD), `button_press`, `toggle_base_mode` |
| `display.py` | `insert_text`, `delete_char`, `get_selection_or_word`, `enter` |
| `history.py` | `select_history`, `load_prev`, `load_next` |
| `popups.py` | `open_modes_popup`, `show_functions_popup`, `insert_func_from_popup` |
| `evaluate.py` | `evaluate`: delega en `core.evaluator` o `modes.dig.evaluate`; actualiza salida e historial |
| `fraction_editor.py` | `on_slash`, `on_up`, `on_down`, `on_right`, `move_between_fraction_lines`, `on_key_release` |
| `fraction_delete.py` | `on_backspace`, `on_delete_key`, helpers `_dash_run`, `_delete_fraction_at`, `token_span` |
| `operators.py` | `on_operator` (+ − * sobre la barra), `on_ctrl_slash`, `on_less_than`, `on_greater_than` |
| `latex_export.py` | `expr_to_latex`, `export_latex` |
| `textutil.py` | `ensure_col(display, línea, col)` compartido por los editores de fracciones |

## ¿Dónde toco para…?
- Nueva función matemática → `core/constants.py` (`BASE_FUNCS`) o `core/env.py`; si va en el popup, `ui/popups.py`.
- Cambiar cómo se muestra un resultado → `core/formatting.py` (ENG) o `modes/dig/format.py` (DIG).
- Nueva sintaxis de entrada → `core/parser.py`.
- Atajo de teclado → binding en `ui/app.py`, handler en el mixin que corresponda. Botón → layout en `modes/` y acción en `ui/keypad.py` (`button_press`).
- Colores → `ui/theme.py`.

## Bugs conocidos (NO corregidos; la reorganización solo movió código)
1. `programmer_format_result` compara `base == "hex"/"bin"` en minúscula pero `base_mode` usa `"HEX"/"BIN"/"OCT"`: esas ramas no se alcanzan y devuelve `None`. (Hoy no afecta: el modo DIG usa `evaluate_programmer`.)
2. `insert_implicit_multiplication` hace `replace("e", "*e")` global si hay dígito seguido de `e`: puede romper nombres como `exp`.
3. `export_latex` existe pero ningún botón lo llama.

5. `evaluate_eng` conserva dos `print("DEBUG ...")` del código original.

## Reglas para cambios
- Mover ≠ corregir: los bugs se arreglan en un cambio aparte.
- No agregues lógica a `ui/app.py`; va en el mixin o módulo que corresponda.
- Lógica nueva sin tkinter → `core/` o `modes/`, para poder probarla sin GUI.
