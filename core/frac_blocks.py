"""Convierte bloques de fracción multilínea (num / ---- / den) a '(num)/(den)'."""
from .constants import DIVISIONLINE


def replace_fraction_blocks(text: str) -> str:
    """Parse multi-line fractions possibly placed side-by-side.
    For any triplet of lines where the middle contains DIVISIONLINE, scan left-to-right and
    reconstruct an expression by converting each DIVISIONLINE column span into (NUM)/(DEN),
    where NUM and DEN are the contiguous non-space tokens starting at the same column
    on the lines above and below.
    Non-fraction operators/tokens are taken from the middle line.
    Other lines without DIVISIONLINE are appended as-is.
    """
    lines = text.splitlines()
    out_parts = []
    i = 0
    divlen = len(DIVISIONLINE)  # Length of the division marker
    while i < len(lines):
        if i + 2 < len(lines) and DIVISIONLINE in lines[i+1]:
            top = lines[i]
            mid = lines[i+1]
            bot = lines[i+2]
            # Normalize lengths
            maxlen = max(len(top), len(mid), len(bot))
            top = top.ljust(maxlen)
            mid = mid.ljust(maxlen)
            bot = bot.ljust(maxlen)
            j = 0
            expr = []
            while j < maxlen:
                if mid.startswith(DIVISIONLINE, j):
                    start = j
                    end = j + divlen

                    # Read token that overlaps with the division line region
                    # The token could start before 'start' and extend into/past the ---- region
                    def read_token_around(s, div_start, div_end):
                        # Find the token that covers the division line area
                        # Look backwards from div_start to find token start
                        token_start = div_start
                        while token_start > 0 and s[token_start - 1] != ' ':
                            token_start -= 1
                        # Look forwards from div_start to find token end
                        token_end = div_start
                        while token_end < len(s) and s[token_end] != ' ':
                            token_end += 1
                        token = s[token_start:token_end].strip()
                        return token

                    num = read_token_around(top, start, end)
                    den = read_token_around(bot, start, end)

                    if not num:
                        num = "0"
                    if not den:
                        den = "1"
                    expr.append(f"({num})/({den})")
                    # Skip ALL consecutive dashes (not just divlen)
                    while j < maxlen and mid[j] == '-':
                        j += 1
                else:
                    ch = mid[j]
                    # Skip dash characters and spaces, only add operators
                    if ch != '-' and not ch.isspace() and ch != '/':
                        expr.append(ch)
                    j += 1
            out_parts.append(''.join(expr))
            i += 3
        else:
            out_parts.append(lines[i])
            i += 1
    return ' '.join([p for p in out_parts if p.strip()])
