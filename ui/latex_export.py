"""Exportar historial a LaTeX."""
import customtkinter as ctk

from core.frac_blocks import replace_fraction_blocks


class LatexExportMixin:
    def expr_to_latex(self, expr: str) -> str:
        """Convert a math expression to LaTeX format."""
        import re as _re
        
        # Convert fractions like (num)/(den) to \frac{num}{den}
        def replace_frac(m):
            num = m.group(1)
            den = m.group(2)
            return f"\\frac{{{num}}}{{{den}}}"
        
        latex = expr
        # Match (...)/(...)
        latex = _re.sub(r'\(([^()]+)\)/\(([^()]+)\)', replace_frac, latex)
        
        # Convert simple a/b fractions
        latex = _re.sub(r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)', r'\\frac{\1}{\2}', latex)
        
        # Convert functions
        latex = latex.replace('sqrt(', '\\sqrt{').replace('sin(', '\\sin(').replace('cos(', '\\cos(').replace('tan(', '\\tan(')
        latex = latex.replace('log(', '\\log(').replace('exp(', '\\exp(')
        
        # Convert sqrt closing ) to }
        latex = _re.sub(r'\\sqrt\{([^}]+)\)', r'\\sqrt{\1}', latex)
        
        # Convert pi and e
        latex = latex.replace('pi', '\\pi').replace(' e ', ' e ')
        
        # Convert multiplication
        latex = latex.replace('*', ' \\cdot ')
        
        # Convert angle notation (L angle)
        latex = _re.sub(r'(\d+(?:\.\d+)?(?:[munpkMG])?)\s*L\s*(-?\d+(?:\.\d+)?)', r'\1 \\angle \2^\\circ', latex)
        
        return latex

    def export_latex(self):
        """Export history to LaTeX and copy to clipboard."""
        if not self.history:
            self.output_label.configure(text="No history to export")
            return
        
        latex_lines = ["\\begin{align*}"]
        for expr, result in self.history:
            # Convert multi-line fraction to single line first
            expr_single = replace_fraction_blocks(expr)
            latex_expr = self.expr_to_latex(expr_single)
            
            # Parse result - take first line (Rect value)
            result_first = result.split('\n')[0] if '\n' in result else result
            result_first = result_first.replace('Rect:', '').strip()
            
            latex_lines.append(f"  {latex_expr} &= {result_first} \\\\")
        
        latex_lines.append("\\end{align*}")
        latex_output = "\n".join(latex_lines)
        
        # Copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(latex_output)
        
        # Show confirmation
        self.output_label.configure(text="LaTeX copied to clipboard!")
        
        # Also show in a popup
        win = ctk.CTkToplevel(self)
        win.title("LaTeX Export")
        win.geometry("500x400")
        win.transient(self)
        
        ctk.CTkLabel(win, text="LaTeX Output (copied to clipboard):", font=("Arial", 12)).pack(pady=5)
        
        text_box = ctk.CTkTextbox(win, width=460, height=320, font=("Consolas", 11))
        text_box.pack(padx=10, pady=5)
        text_box.insert("1.0", latex_output)
        
        ctk.CTkButton(win, text="Close", command=win.destroy).pack(pady=5)
