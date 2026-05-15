# Paleta de colores para toda la aplicación
BG_DARK    = "#0A0A0F"
BG_CARD    = "#13131A"
BG_SIDEBAR = "#0F0F16"
BG_HOVER   = "#1E1E2A"
ACCENT     = "#7C5CBF"       # púrpura profundo
ACCENT2    = "#C084FC"       # lila brillante
GREEN      = "#4ADE80"       # verde play
TEXT_PRI   = "#F0EEF8"
TEXT_SEC   = "#8A849E"
TEXT_MUT   = "#4A4560"
BORDER     = "#1E1E2A"

# Fuentes
FONT_TITLE  = ("Helvetica", 24, "bold")
FONT_H2     = ("Helvetica", 16, "bold")
FONT_H3     = ("Helvetica", 12, "bold")
FONT_BODY   = ("Helvetica", 10)
FONT_SMALL  = ("Helvetica", 9)
FONT_TINY   = ("Helvetica", 8)

def lighten(hex_color):
    """Aclara ligeramente un color hex."""
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color