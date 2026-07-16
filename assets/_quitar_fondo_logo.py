"""Saca una version con fondo transparente del lockup OFICIAL de Centrum.

NO redibuja nada: parte de `centrum-logo-navy.png` (el archivo oficial de
Mariano M.M/CENTRUM, wordmark crema + capitel verde sobre navy) y solo elimina
el fondo. El arte se conserva pixel a pixel.

El fondo navy del render tiene algo de ruido, asi que no vale un color-key
exacto: se mide la distancia de cada pixel al navy del fondo y se convierte en
alpha, lo que ademas conserva el antialiasing de los bordes.
"""
from PIL import Image

SRC = "centrum-logo-navy.png"
DST = "centrum-logo-trans.png"

BG = (28, 52, 100)   # navy del fondo, muestreado en las esquinas
NEAR, FAR = 26, 74   # <NEAR = fondo puro; >FAR = tinta pura; en medio, antialiasing

im = Image.open(SRC).convert("RGB")
out = Image.new("RGBA", im.size)
px_in, px_out = im.load(), out.load()

for y in range(im.size[1]):
    for x in range(im.size[0]):
        r, g, b = px_in[x, y]
        d = ((r - BG[0]) ** 2 + (g - BG[1]) ** 2 + (b - BG[2]) ** 2) ** 0.5

        if d <= NEAR:
            px_out[x, y] = (0, 0, 0, 0)
        elif d >= FAR:
            px_out[x, y] = (r, g, b, 255)
        else:
            a = (d - NEAR) / (FAR - NEAR)
            # Deshacer la mezcla con el fondo para que el borde no arrastre navy
            un = tuple(max(0, min(255, int(round((c - BG[i] * (1 - a)) / a)))) for i, c in enumerate((r, g, b)))
            px_out[x, y] = (*un, int(round(a * 255)))

bbox = out.getchannel("A").getbbox()   # recorta el aire sobrante del render
if bbox:
    out = out.crop(bbox)

out.save(DST)
print(f"{DST}  {out.size}")
