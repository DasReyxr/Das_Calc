"""Botón '=' / Enter: delega en core (ENG) o modes.dig (DIG) y actualiza salida e historial."""
from core.evaluator import evaluate_eng
from modes.dig.evaluate import evaluate_programmer


class EvaluateMixin:
    def evaluate(self):
        raw_expr = self.display.get("1.0", "end-1c").strip()
        if not raw_expr:
            return

        if self.calc_mode == "DIG":
            try:
                r = evaluate_programmer(raw_expr, self.base_mode)
                out = f"DEC: {r['DEC']}\nHEX: {r['HEX']}\nOCT: {r['OCT']}\nBIN: {r['BIN']}"
                self.output_label.configure(text=out)
                self.history.append((raw_expr, out))
                self.history_box.insert("end", raw_expr + " = " + r["DEC"] + "\n")
                self.history_box.see("end")
            except Exception as e:
                print("Programmer Mode Error:", e)
                self.output_label.configure(text="Math Error")
            return

        try:
            expr, result_str = evaluate_eng(raw_expr, self.use_degrees)
        except ZeroDivisionError:
            self.output_label.configure(text="Math Error")
            return
        except Exception:
            self.output_label.configure(text="Error")
            return

        self.output_label.configure(text=result_str)
        # Se guarda la expresión RAW para conservar los bloques de fracción al recuperar el historial
        self.history.append((raw_expr, result_str))
        self.history_box.insert("end", f"{expr} = {result_str}\n")
        self.history_box.see("end")
        self.history_index = len(self.history)
