import segno
from pathlib import Path

# ==========================
# SETTINGS
# ==========================

DATA = "https://example.com"
OUTPUT = Path("qr.svg")

SVG_SIZE = 500

TEXT_TOP = "HELLO"
TEXT_BOTTOM = "WORLD"

CIRCLE_RADIUS_RATIO = 0.18
CIRCLE_COLOR = "black"
CIRCLE_STROKE = "red"
INNER_SCALE = 0.82

# ==========================
# QR
# ==========================

qr = segno.make(DATA, error="h", version=4, micro=False)
matrix = list(qr.matrix)
size = len(matrix)

# ==========================
# FIT FONT
# ==========================

def fit_font_size(text, radius, svg_size):
    max_width = radius * 1.6
    base = svg_size * 0.075
    if len(text) == 0:
        return base
    scale = min(1, max_width / (len(text) * base * 0.6))
    return base * scale

# ==========================
# FINDER
# ==========================

def finder(x, y, rotate=None):
    rotate_start = f'<g transform="rotate({rotate})">' if rotate else ''
    rotate_end = '</g>' if rotate else ''
    return f'''
<g transform="translate({x},{y})">
{rotate_start}
<path d="M-3.5 -3.5L3.5 -3.5L3.5 3.5L-3.5 3.5ZM-2.5 -2.5L-2.5 2.5L2.5 2.5L2.5 -2.5Z"
style="fill-rule:evenodd;fill:#000"/>
<path d="M-1.5 -1.5L1.5 -1.5L1.5 1.5L-1.5 1.5Z"
style="fill-rule:evenodd;fill:#000"/>
{rotate_end}
</g>
'''

# ==========================
# DATA PATH
# ==========================

path_data = []
for y in range(size):
    for x in range(size):
        if matrix[y][x]:
            path_data.append(f"M{x} {y}h1v1h-1z")

path_string = "".join(path_data)

# ==========================
# CENTER CIRCLE + TEXT
# ==========================

center = SVG_SIZE / 2
radius = SVG_SIZE * CIRCLE_RADIUS_RATIO
stroke = SVG_SIZE * 0.01

top_size = fit_font_size(TEXT_TOP, radius, SVG_SIZE) * INNER_SCALE
bottom_size = fit_font_size(TEXT_BOTTOM, radius, SVG_SIZE) * 0.9 * INNER_SCALE

circle_block = f"""
<circle cx="{center}" cy="{center}" r="{radius}"
fill="{CIRCLE_COLOR}"
stroke="{CIRCLE_STROKE}"
stroke-width="{stroke}"/>

<text x="{center}" y="{center-radius*0.25*INNER_SCALE}"
fill="white"
font-size="{top_size}"
font-family="Arial Black"
font-weight="900"
text-anchor="middle"
dominant-baseline="middle">{TEXT_TOP}</text>

<text x="{center}" y="{center+radius*0.25*INNER_SCALE}"
fill="white"
font-size="{bottom_size}"
font-family="Arial Black"
font-weight="900"
text-anchor="middle"
dominant-baseline="middle">{TEXT_BOTTOM}</text>
"""

# ==========================
# SVG
# ==========================

SCALE = SVG_SIZE / (size + 2)

svg = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
width="{SVG_SIZE}"
height="{SVG_SIZE}"
viewBox="0 0 {SVG_SIZE} {SVG_SIZE}">

<rect width="{SVG_SIZE}" height="{SVG_SIZE}" fill="#ffffff"/>

<g transform="scale({SCALE})">
<g transform="translate(1,1)">

{finder(3.5,3.5)}
{finder(size-3.5,3.5,90)}
{finder(3.5,size-3.5,-90)}

<path d="{path_string}" fill="#000"/>

</g>
</g>

{circle_block}

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")
print("✅ QR saved:", OUTPUT)