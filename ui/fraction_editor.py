"""Editor de fracciones apiladas: '/', flechas, auto-expansión de la barra."""
import tkinter as tk

from core.constants import DIVISIONLINE
from .textutil import ensure_col


class FractionEditorMixin:
    def on_slash(self, event=None):
        if self.calc_mode != "ENG":
            return  # let normal DIVISIONLINE[0] in DIG
        if getattr(self, "inline_mode", False):
            return None   # "/" normal
        try:
            pos = self.display.index(tk.INSERT)
            line_s, col_s = pos.split(".")
            line = int(line_s)
            col = int(col_s)

            cur_line_text = self.display.get(f"{line}.0", f"{line}.end")
            prev_line_text = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            next_line_text = self.display.get(f"{line+1}.0", f"{line+1}.end")

            import re as _re
            
            # Check if we're on a numerator line (next line has DIVISIONLINE)
            on_numerator_line = DIVISIONLINE in next_line_text
            
            # Check if we're on a denominator line (previous line has DIVISIONLINE)
            on_denominator_line = DIVISIONLINE in prev_line_text
            
            # If on numerator or denominator line, just insert "/" inline (no new block)
            if on_numerator_line or on_denominator_line:
                self.display.insert(pos, "/")
                self.display.mark_set(tk.INSERT, f"{line}.{col+1}")
                return "break"
            
            # Selection takes priority for numerator
            numerator_sel = None
            if self.display.tag_ranges("sel"):
                numerator_sel = self.display.get("sel.first", "sel.last")
                self.display.delete("sel.first", "sel.last")

            # Detect if we're on a division line (contains DIVISIONLINE anywhere)
            on_dash_line = (DIVISIONLINE in cur_line_text)

            if on_dash_line and line > 1:
                # Inline add another fraction at current column
                # Determine numerator: from selection or from token just left of caret on current line
                if numerator_sel is not None:
                    numerator = numerator_sel
                else:
                    left_segment = self.display.get(f"{line}.0", pos)
                    # Only capture the number (not the operator before it)
                    m = _re.search(r"(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                    if m and m.group(1):
                        numerator = m.group(1)
                        start_col = len(left_segment) - len(numerator)
                        # remove that token from current (dash) line
                        self.display.delete(f"{line}.{start_col}", pos)
                        col = start_col  # align to token start
                    else:
                        numerator = "1"

                # Align cells by matching number of tabs before insertion point
                left_mid = self.display.get(f"{line}.0", f"{line}.{col}")
                tabs_before = left_mid.count("\t")
                # Advance to next cell boundary if we're not at start of one (by inserting a tab)
                if not left_mid.endswith("\t") and not left_mid.endswith(" "):
                    self.display.insert(f"{line}.{col}", "\t")
                    col += 1
                # Ensure top and bottom lines have the same number of tabs
                def ensure_tabs(line_no: int, n_tabs: int):
                    line_text = self.display.get(f"{line_no}.0", f"{line_no}.end")
                    cur_tabs = line_text.count("\t")
                    if cur_tabs < n_tabs:
                        self.display.insert(f"{line_no}.end", "\t" * (n_tabs - cur_tabs))
                ensure_tabs(line-1, tabs_before)
                ensure_tabs(line+1, tabs_before)
                # Fallback padding with spaces if still short by columns
                ensure_col(self.display, line-1, col)
                ensure_col(self.display, line+1, col)

                # Insert components aligned at column
                self.display.insert(f"{line-1}.{col}", numerator)
                self.display.insert(f"{line}.{col}", DIVISIONLINE)
                self.display.insert(f"{line+1}.{col}", "D")
                # Move caret to denominator position to keep typing
                self.display.mark_set(tk.INSERT, f"{line+1}.{col}")
                return "break"
            else:
                # Fallback: create a new vertical fraction block
                txt = self.get_selection_or_word()
                if txt is None:
                    # Try to capture numeric token immediately before caret on the same line
                    left_segment = self.display.get(f"{line}.0", pos)
                    # Only capture the number (not the operator before it)
                    # Use \d to start, so -5 after 2 becomes just 5, leaving "2-" 
                    m = _re.search(r"(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                    if m:
                        numerator = m.group(1)
                        start_col = len(left_segment) - len(m.group(1))
                        self.display.delete(f"{line}.{start_col}", pos)
                    else:
                        # Check for standalone negative number at start of line
                        m2 = _re.search(r"^([+\-]?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                        if m2:
                            numerator = m2.group(1)
                            start_col = 0
                            self.display.delete(f"{line}.{start_col}", pos)
                        else:
                            numerator = "N"
                else:
                    numerator = txt
                    self.display.delete("sel.first", "sel.last")

                insert_at = self.display.index(tk.INSERT)
                # Indent dash/D lines to current column so the dashes align under the numerator,
                # keeping any left-side terms (e.g., '2-') outside the fraction but parseable.
                if col>4:
                    indent = " " * (col)
                else:
                    indent = ""
                block = f"{numerator}\n{indent}{DIVISIONLINE}\n{indent}D"
                self.display.insert(insert_at, block)
                # place cursor at start of D line at same column
                line2, col2 = map(int, insert_at.split("."))
                den_line_index = f"{line2+2}.{col}"
                self.display.mark_set(tk.INSERT, den_line_index)
                return "break"
        except Exception:
            return "break"

    def on_up(self, event=None):
        # If we're around a fraction block, move to numerator line
        if self.move_between_fraction_lines(direction="up"):
            return "break"
        # default caret move
        return None

    def on_down(self, event=None):
        # If we're around a fraction block, move to denominator line
        if self.move_between_fraction_lines(direction="down"):
            return "break"
        # default caret move
        return None

    def on_right(self, event=None):
        # If caret is at end of a denominator line, jump to dash line end
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            cur_line = self.display.get(f"{line}.0", f"{line}.end")
            # denominator line if previous line starts with '////'
            prev_line = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            if prev_line.lstrip().startswith(DIVISIONLINE):
                # at end?
                line_end = self.display.index(f"{line}.end")
                if pos == line_end:
                    # Move caret to end of dash line; insert a space if not present
                    dash_end = self.display.index(f"{line-1}.end")
                    # ensure a space after dashes if last char isn't space
                    last_char = self.display.get(f"{line-1}.end-1c", f"{line-1}.end")
                    if last_char != " ":
                        self.display.insert(dash_end, " ")
                        dash_end = self.display.index(f"{line-1}.end")
                    self.display.mark_set(tk.INSERT, dash_end)
                    return "break"
        except Exception:
            pass
        # default behavior
        return None

    def move_between_fraction_lines(self, direction: str) -> bool:
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            cur = self.display.get(f"{line}.0", f"{line}.end")
            above = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            below = self.display.get(f"{line+1}.0", f"{line+1}.end")

            # If on middle line '---', jump accordingly
            if cur.lstrip().startswith(DIVISIONLINE):
                target_line = line-1 if direction == "up" else line+1
                self.display.mark_set(tk.INSERT, f"{target_line}.end")
                return True

            # If on numerator with next line '---' and going down
            if below.lstrip().startswith(DIVISIONLINE) and direction == "down":
                self.display.mark_set(tk.INSERT, f"{line+2}.end")
                return True

            # If on denominator with previous line '---' and going up
            if above.lstrip().startswith(DIVISIONLINE) and direction == "up":
                self.display.mark_set(tk.INSERT, f"{line-2}.end")
                return True
        except Exception:
            return False
        return False

    def on_key_release(self, event=None):
        """Auto-expande la barra bajo el numerador donde está el cursor."""
        if self.calc_mode != "ENG" or getattr(self, "inline_mode", False):
            return None
        if event and event.keysym in ("Up", "Down", "Left", "Right", "Home", "End"):
            return None
        try:
            DASH = DIVISIONLINE[0]
            line, col = map(int, self.display.index(tk.INSERT).split("."))
            div_line = line + 1
            div = self.display.get(f"{div_line}.0", f"{div_line}.end")
            if DIVISIONLINE not in div:
                return None
            cur = self.display.get(f"{line}.0", f"{line}.end")

            # token del numerador bajo el cursor
            a = min(col, len(cur))
            while a > 0 and not cur[a - 1].isspace():
                a -= 1
            b = min(col, len(cur))
            while b < len(cur) and not cur[b].isspace():
                b += 1

            # barra que empieza en la columna del numerador
            if a >= len(div) or div[a] != DASH:
                return None
            e = a
            while e < len(div) and div[e] == DASH:
                e += 1

            need = max(len(DIVISIONLINE), b - a)
            if need > e - a:
                self.display.insert(f"{div_line}.{e}", DASH * (need - (e - a)))
        except Exception:
            pass
        return None
