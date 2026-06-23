#!/usr/bin/env python3
"""Gera o ícone do plugin (512x512 PNG) com Pillow: um cristal de aether facetado
nas cores do Brasil (verde→amarelo→azul, núcleo ciano) sobre tile escuro arredondado.
Remete ao BR e à gema/cristal de FFXIV, alinhado à marca 'Eorzea PT-BR'."""
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
SS = 4                      # supersampling p/ antialiasing
R = SIZE * SS
OUT = r"E:\ffxiv-ptbr-localizer-repo\images\icon.png"

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ── paleta (BR vívido p/ tela + aether) ─────────────────────────────
BG_TOP   = (18, 23, 34)
BG_BOT   = (6, 8, 13)
GREEN    = (22, 163, 74)
GREEN_L  = (52, 211, 110)
GREEN_D  = (10, 102, 48)
YELLOW   = (250, 204, 21)
YELLOW_L = (253, 230, 138)
YELLOW_D = (193, 134, 6)
BLUE     = (30, 64, 175)
BLUE_D   = (15, 33, 110)
CYAN     = (150, 220, 255)
WHITE    = (255, 255, 255)

# ── base: gradiente vertical recortado em quadrado arredondado ──────
base = Image.new("RGBA", (R, R), (0, 0, 0, 0))
grad = Image.new("RGB", (R, R), BG_TOP)
gd = ImageDraw.Draw(grad)
for y in range(R):
    gd.line([(0, y), (R, y)], fill=lerp(BG_TOP, BG_BOT, y / R))
mask = Image.new("L", (R, R), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, R - 1, R - 1], radius=int(R * 0.22), fill=255)
base.paste(grad, (0, 0), mask)

cx, cy = R // 2, int(R * 0.50)
hw, hh = int(R * 0.295), int(R * 0.345)   # meia-largura / meia-altura do losango (cristal)

def diamond(c, w, h):
    x, y = c
    return [(x, y - h), (x + w, y), (x, y + h), (x - w, y)]  # T, R, B, L

def facets(draw, c, w, h, top_l, top_r, bot_l, bot_r):
    """4 triângulos (luz vinda de cima-esquerda) p/ aparência de gema."""
    x, y = c
    T, Rv, B, L = (x, y - h), (x + w, y), (x, y + h), (x - w, y)
    C = (x, y)
    draw.polygon([T, L, C], fill=top_l)
    draw.polygon([T, Rv, C], fill=top_r)
    draw.polygon([B, L, C], fill=bot_l)
    draw.polygon([B, Rv, C], fill=bot_r)

# ── glow externo (aura verde-ciano) ─────────────────────────────────
glow = Image.new("RGBA", (R, R), (0, 0, 0, 0))
gdr = ImageDraw.Draw(glow)
gdr.polygon(diamond((cx, cy), int(hw * 1.18), int(hh * 1.18)), fill=(40, 200, 120, 160))
glow = glow.filter(ImageFilter.GaussianBlur(R * 0.045))
base = Image.alpha_composite(base, glow)

d = ImageDraw.Draw(base)

# ── cristal verde (facetado) ────────────────────────────────────────
facets(d, (cx, cy), hw, hh, GREEN_L, GREEN, GREEN, GREEN_D)
# aresta de contorno sutil
d.line(diamond((cx, cy), hw, hh) + [diamond((cx, cy), hw, hh)[0]], fill=(8, 80, 40), width=max(2, SS))

# ── losango amarelo interno (facetado) ──────────────────────────────
yw, yh = int(hw * 0.56), int(hh * 0.56)
facets(d, (cx, cy), yw, yh, YELLOW_L, YELLOW, YELLOW, YELLOW_D)

# ── núcleo azul + brilho de aether ──────────────────────────────────
br = int(R * 0.092)
# esfera azul com leve gradiente (mais clara em cima-esq)
d.ellipse([cx - br, cy - br, cx + br, cy + br], fill=BLUE)
sphere = Image.new("RGBA", (R, R), (0, 0, 0, 0))
ImageDraw.Draw(sphere).ellipse(
    [cx - int(br * 0.72), cy - int(br * 0.78), cx + int(br * 0.30), cy + int(br * 0.10)],
    fill=(90, 130, 230, 150))
sphere = sphere.filter(ImageFilter.GaussianBlur(R * 0.010))
base = Image.alpha_composite(base, sphere)

# brilho de aether (glow ciano radial)
glow2 = Image.new("RGBA", (R, R), (0, 0, 0, 0))
ImageDraw.Draw(glow2).ellipse(
    [cx - int(br * 0.62), cy - int(br * 0.62), cx + int(br * 0.62), cy + int(br * 0.62)],
    fill=(150, 220, 255, 235))
glow2 = glow2.filter(ImageFilter.GaussianBlur(R * 0.016))
base = Image.alpha_composite(base, glow2)
d = ImageDraw.Draw(base)

# estrela de 4 pontas afilada (sparkle de aether)
def star4(c, long_r, short_r, color):
    x, y = c
    return [(x, y - long_r), (x + short_r, y - short_r), (x + long_r, y),
            (x + short_r, y + short_r), (x, y + long_r), (x - short_r, y + short_r),
            (x - long_r, y), (x - short_r, y - short_r)]
d.polygon(star4((cx, cy), int(R * 0.085), int(R * 0.012), (220, 240, 255)),
          fill=(225, 242, 255))
d.polygon(star4((cx, cy), int(R * 0.045), int(R * 0.010), WHITE), fill=WHITE)

# realce especular no topo do cristal (vidro)
hl = Image.new("RGBA", (R, R), (0, 0, 0, 0))
ImageDraw.Draw(hl).polygon([(cx, cy - hh), (cx - int(hw * 0.34), cy - int(hh * 0.34)),
                            (cx, cy - int(hh * 0.30))], fill=(255, 255, 255, 70))
base = Image.alpha_composite(base, hl)

# ── recorta de novo no arredondado (limpa overflow do glow) ─────────
out = Image.new("RGBA", (R, R), (0, 0, 0, 0))
out.paste(base, (0, 0), mask)

out = out.resize((SIZE, SIZE), Image.LANCZOS)
out.save(OUT)
print(f"OK {OUT} ({SIZE}x{SIZE})")
