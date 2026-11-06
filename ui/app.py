"""Clase principal: solo compone los mixins. No agregues lógica aquí."""
import customtkinter as ctk

from .display import DisplayMixin
from .evaluate import EvaluateMixin
from .fraction_delete import FractionDeleteMixin
from .fraction_editor import FractionEditorMixin
from .history import HistoryMixin
from .keypad import KeypadMixin
from .latex_export import LatexExportMixin
from .operators import OperatorsMixin
from .popups import PopupsMixin
from .theme import ThemeMixin
from .window import WindowMixin

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class EngCalculator(WindowMixin, ThemeMixin, KeypadMixin, DisplayMixin, HistoryMixin, PopupsMixin,
                    FractionEditorMixin, FractionDeleteMixin, OperatorsMixin, EvaluateMixin,
                    LatexExportMixin, ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_windows_app_id()
        self.title("Das Calculator")
        self.geometry("900x300")
        self.resizable(False, False)
        self._set_window_icon()

        # ------ THEME SETUP ---------
        self.setup_colors()
        self.current_mode = "dark"
        self.current_colors = self.colors_dark.copy()

        # ------ HISTORY ---------
        self.history = []  # list of (expr, result)
        self.history_index = None
        self.use_degrees = True

        # ------ DISPLAY ---------
        self.display = ctk.CTkTextbox(self, width=860, height=180, font=("Consolas", 28))
        self.display.pack(pady=10)
        self.display.insert("1.0", "")
        # Configure tab-based grid cells so each term can sit in its own "box"
        self.configure_tab_grid(cell_chars=6, max_cells=40)

        # History navigation will be conditional; fractions use arrows locally
        self.display.bind("<Up>", self.on_up)
        self.display.bind("<Down>", self.on_down)
        self.display.bind("<Return>", self.enter)
        # Fraction template on DIVISIONLINE[0]
        self.display.bind("/", self.on_slash)
        # Literal inline division: Ctrl + /
        self.display.bind("<Control-slash>", self.on_ctrl_slash)
        self.display.bind("<KP_Divide>", self.on_ctrl_slash)
        # Exit denominator with Right arrow
        self.display.bind("<Right>", self.on_right)
        # Operators on dash line between fractions
        self.display.bind("+", self.on_operator)
        self.display.bind("<KP_Add>", self.on_operator)
        self.display.bind("-", self.on_operator)
        self.display.bind("<KP_Subtract>", self.on_operator)
        self.display.bind("*", self.on_operator)
        self.display.bind("<KP_Multiply>", self.on_operator)
        # Delete entire fraction when deleting a dash
        self.display.bind("<BackSpace>", self.on_backspace)
        self.display.bind("<Delete>", self.on_delete_key)
        # History with Shift + arrows
        self.display.bind("<Shift-Up>", self.load_prev)
        self.display.bind("<Shift-Down>", self.load_next)
        # Shift operators (keyboard < and > insert << and >>)
        self.display.bind("<less>", self.on_less_than)
        self.display.bind("<greater>", self.on_greater_than)
        # Auto-expand division line when typing in numerator
        self.display.bind("<KeyRelease>", self.on_key_release)

        # ------ OUTPUT LABEL ---------
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.output_label.pack(pady=5)


        # ------ CONTROLS ROW ---------
        self.inline_mode = True          # activado por defecto
        self.keypad_visible = False      # teclado oculto al inicio

        self.controls = ctk.CTkFrame(self, fg_color="transparent")
        self.controls.pack(pady=(10, 6))

        self.mode_switch = ctk.CTkSwitch(
            self.controls,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="pink",
        )
        self.mode_switch.select()
        self.mode_switch.pack(side="left", padx=10)

        self.inline_switch = ctk.CTkSwitch(
            self.controls,
            text="Inline Mode",
            command=self.sync_inline_mode,
        )
        self.inline_switch.select()
        self.inline_switch.pack(side="left", padx=10)

        self.keypad_toggle_btn = ctk.CTkButton(
            self.controls,
            text="Show Keyboard",
            width=150,
            command=self.toggle_keypad,
        )
        self.keypad_toggle_btn.pack(side="left", padx=10)

        self.mode_btn = ctk.CTkButton(
            self.controls,
            text="Change Mode",
            width=150,
            command=self.toggle_mode,
        )
        self.mode_btn.pack(side="left", padx=10)

        # ------ FRAMES ---------
        self.main_frame = ctk.CTkFrame(self)
        # NO se empaqueta aquí: el teclado inicia oculto

        self.keypad_frame = ctk.CTkFrame(self.main_frame)
        self.keypad_frame.grid(row=0, column=0, padx=10)

        history_frame = ctk.CTkFrame(self.main_frame)
        history_frame.grid(row=0, column=1)

        ctk.CTkLabel(history_frame, text="History", font=("Arial", 16)).pack()
        self.history_box = ctk.CTkTextbox(history_frame, width=300, height=420, font=("Consolas", 11))
        self.history_box.pack(padx=4, pady=4)
        self.history_box.bind("<Button-1>", self.select_history)

    
        # ----- MODES ---------
        self.calc_mode = "ENG"
        self.base_mode = "DEC"  # only used in programmer mode

                
        
        self.display.bind("<Control-z>", self.undo)
        self.display.bind("<Control-Z>", self.undo)   # con Bloq Mayús
        self.display.bind("<Control-y>", self.redo)
        self.display.bind("<Control-Y>", self.redo)

        self.display.bind("<Control-a>", self.select_all)
        self.display.bind("<Control-A>", self.select_all)  # con Bloq Mayús
        self.build_keypad_for_mode(self.calc_mode)
        self.apply_dark_mode_colors()
        self.after(100, self._set_window_icon)







def run():
    EngCalculator().mainloop()
