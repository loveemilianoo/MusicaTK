# Paleta de colores para toda la aplicación
BG_DARK    = "#2A2520"       # negro con tonos café
BG_CARD    = "#3D3A34"       # café oscuro
BG_SIDEBAR = "#342F2A"       # café muy oscuro
BG_HOVER   = "#4A4540"       # café claro (hover)
ACCENT     = "#D4A574"       # beige - color principal
ACCENT2    = "#E8C8A0"       # beige claro
GREEN      = "#8B9A6E"       # verde olivo
TEXT_PRI   = "#F5F0EA"       # cream/blanco cálido
TEXT_SEC   = "#A89485"       # gris café
TEXT_MUT   = "#5D5550"       # gris oscuro
BORDER     = "#4A4540"       # café

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