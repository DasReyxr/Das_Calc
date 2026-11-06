"""Helper compartido por los editores de fracciones."""


def ensure_col(display, line_no: int, col_no: int):
    """Rellena con espacios la línea hasta llegar a col_no."""
    end_idx = display.index(f"{line_no}.end")
    cur_col = int(end_idx.split(".")[1])
    if cur_col < col_no:
        display.insert(end_idx, " " * (col_no - cur_col))
