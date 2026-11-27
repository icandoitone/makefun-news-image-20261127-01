#!/usr/bin/env python3
"""News-poster entry for make.fun news-image-20261127.

Draws a one-page newspaper poster summing up the world news of
Friday 27 November 2026 and writes it to /output/entry.png.

Pure standard library (os, struct, zlib): the grader runs Python 3.13
with no network and nothing installed. The drawing is fully
deterministic, so two runs write byte-identical output.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 231)
NAVY = (20, 33, 61)
NAVY2 = (28, 45, 84)
RED = (176, 32, 32)
GOLD = (212, 160, 23)
INK = (26, 26, 26)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (200, 192, 176)

# ------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, top to bottom. Uppercase only.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
}


def text_width(text, scale):
    """Pixel width of text at the given scale (6 units per char)."""
    return len(text) * 6 * scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            self.fill_rect(x, y, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.set(xx, yy, color)
                elif not fill and r * r - 2 * r <= d <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        minx, maxx = min(x0, x1, x2), max(x0, x1, x2)
        miny, maxy = min(y0, y1, y2), max(y0, y1, y2)
        denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if denom == 0:
            return
        for yy in range(miny, maxy + 1):
            for xx in range(minx, maxx + 1):
                a = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / denom
                b = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / denom
                c = 1 - a - b
                if a >= 0 and b >= 0 and c >= 0:
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        s = s.upper()
        for ci, ch in enumerate(s):
            glyph = FONT.get(ch, FONT["?"])
            ox = x + ci * 6 * scale
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill_rect(ox + col * scale, y + row * scale,
                                       scale, scale, color)

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)


# ------------------------------------------------------------------ icons
# Each draws a small pictogram inside a 96x96 box at (ox, oy).
def icon_strike(c, ox, oy):
    # Explosion starburst over a skyline.
    c.fill_rect(ox + 6, oy + 66, 84, 6, (120, 120, 120))
    c.fill_rect(ox + 12, oy + 44, 16, 22, (90, 90, 90))
    c.fill_rect(ox + 34, oy + 34, 16, 32, (70, 70, 70))
    c.fill_rect(ox + 56, oy + 50, 16, 16, (90, 90, 90))
    cx, cy = ox + 48, oy + 26
    for ang in range(0, 360, 30):
        import math
        r = 24
        x1 = cx + int(r * math.cos(math.radians(ang)))
        y1 = cy + int(r * math.sin(math.radians(ang)))
        c.line(cx, cy, x1, y1, (230, 120, 20), 3)
    c.circle(cx, cy, 9, (255, 200, 40))
    c.circle(cx, cy, 4, (176, 32, 32))


def icon_eu(c, ox, oy):
    # Circle of gold stars on blue.
    import math
    c.circle(ox + 48, oy + 48, 40, (31, 78, 121))
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = ox + 48 + int(26 * math.cos(a))
        sy = oy + 48 + int(26 * math.sin(a))
        c.circle(sx, sy, 3, GOLD)
    c.circle(ox + 48, oy + 48, 12, (212, 160, 23))
    c.text(ox + 41, oy + 41, "EU", 2, NAVY)


def icon_gaza(c, ox, oy):
    # Damaged buildings and rubble.
    c.fill_rect(ox + 10, oy + 30, 22, 52, (120, 110, 100))
    c.fill_rect(ox + 38, oy + 14, 22, 68, (100, 92, 84))
    c.fill_rect(ox + 66, oy + 40, 20, 42, (120, 110, 100))
    c.triangle(ox + 38, oy + 14, ox + 48, oy + 4, ox + 60, oy + 14, (70, 64, 58))
    for bx, by in ((ox + 15, oy + 38), (ox + 44, oy + 26), (ox + 71, oy + 48)):
        c.fill_rect(bx, by, 5, 5, (40, 40, 40))
    c.triangle(ox + 6, oy + 82, ox + 22, oy + 66, ox + 38, oy + 82, (150, 140, 128))
    c.triangle(ox + 52, oy + 82, ox + 68, oy + 68, ox + 88, oy + 82, (150, 140, 128))


def icon_storm(c, ox, oy):
    # Storm cloud, rain and a parade balloon.
    c.circle(ox + 34, oy + 30, 16, (90, 100, 115))
    c.circle(ox + 54, oy + 24, 20, (110, 120, 135))
    c.circle(ox + 70, oy + 34, 13, (90, 100, 115))
    c.fill_rect(ox + 20, oy + 30, 62, 14, (100, 110, 125))
    for rx in (26, 42, 58, 74):
        c.line(ox + rx, oy + 50, ox + rx - 6, oy + 62, (40, 110, 180), 3)
    c.circle(ox + 48, oy + 78, 11, RED)
    c.line(ox + 48, oy + 89, ox + 48, oy + 94, INK, 2)


def icon_missile(c, ox, oy):
    # Rocket rising diagonally with flame.
    c.line(ox + 30, oy + 66, ox + 66, oy + 30, (120, 120, 120), 8)
    c.triangle(ox + 66, oy + 30, ox + 78, oy + 18, ox + 58, oy + 22, RED)
    c.triangle(ox + 30, oy + 66, ox + 22, oy + 78, ox + 38, oy + 58, RED)
    c.triangle(ox + 30, oy + 66, ox + 18, oy + 66, ox + 26, oy + 80, (255, 140, 0))
    c.circle(ox + 48, oy + 48, 5, GOLD)
    c.circle(ox + 82, oy + 14, 3, GOLD)
    c.circle(ox + 88, oy + 24, 2, GOLD)


def icon_football(c, ox, oy):
    # Football with a black pentagon.
    c.circle(ox + 48, oy + 48, 38, WHITE)
    c.circle(ox + 48, oy + 48, 38, INK, fill=False)
    import math
    pts = []
    for k in range(5):
        a = math.radians(k * 72 - 90)
        pts.append((ox + 48 + int(13 * math.cos(a)),
                    oy + 48 + int(13 * math.sin(a))))
    for i in range(5):
        c.line(pts[i][0], pts[i][1], pts[(i + 1) % 5][0],
               pts[(i + 1) % 5][1], INK, 2)
    cx = (sum(p[0] for p in pts) // 5, sum(p[1] for p in pts) // 5)
    for (px, py) in pts:
        c.line(cx[0], cx[1], px, py, INK, 2)
    for k in range(5):
        a = math.radians(k * 72 - 90)
        ex = ox + 48 + int(38 * math.cos(a))
        ey = oy + 48 + int(38 * math.sin(a))
        px, py = pts[k]
        c.line(px, py, ex, ey, INK, 2)


# --------------------------------------------------------------- stories
# (kicker, kicker colour, icon fn, icon tint, headline, caption)
STORIES = [
    ("MIDDLE EAST", (176, 32, 32), icon_strike, (252, 235, 225),
     "IRAN STRIKES HIT KUWAIT",
     "Drone attack on a Kuwait steel plant kills two Italians. "
     "Iran denies it; a Saudi refinery is hit too."),
    ("EUROPE", (31, 78, 121), icon_eu, (226, 236, 245),
     "EU SUMMIT ON 1.7TN BUDGET",
     "Brussels summit haggles over Ukraine aid. "
     "Trump tells Putin to pull back his aggression."),
    ("GAZA", (85, 74, 64), icon_gaza, (238, 232, 224),
     "ISRAELI STRIKES HIT GAZA",
     "Israeli strikes kill Palestinians, including a deputy "
     "education minister. Hamas weighs its response."),
    ("AMERICA", (14, 116, 144), icon_storm, (224, 240, 244),
     "STORM HALTS MACY'S PARADE",
     "Thanksgiving storm postpones the 100th parade, a first. "
     "500,000 homes lose power."),
    ("ASIA", (107, 33, 168), icon_missile, (240, 230, 248),
     "KIM VOWS BIGGER ARSENAL",
     "North Korea's leader orders more nuclear weapons "
     "and rejects Trump's offer of talks."),
    ("SPORT", (22, 101, 52), icon_football, (228, 242, 232),
     "LILLE STUN BAYERN MUNICH",
     "Bayern suffer their first defeat of the season "
     "in France."),
]

TICKER = ("ALSO TODAY: BLACK FRIDAY SALES, UK MIGRATION LOWEST "
          "SINCE 1997, NEW ECB CHIEF, SERBIA VOTE 27 DEC, "
          "EGYPT FIRE KILLS 30+")


def draw_panel(c, x, y, w, h, story):
    kicker, kcolor, icon, tint, headline, caption = story
    c.fill_rect(x, y, w, h, CARD)
    c.rect(x, y, w, h, LINE, 2)
    # Kicker bar.
    c.fill_rect(x, y, w, 30, kcolor)
    c.text(x + 14, y + 8, kicker, 2, WHITE)
    # Headline, up to two lines, full panel width.
    lines = wrap_text(headline, w - 28, 3)
    hy = y + 40
    for ln in lines[:2]:
        c.text(x + 14, hy, ln, 3, INK)
        hy += 22
    # Icon box + caption below the headline, centred in the space left.
    cap_lines = wrap_text(caption, w - 110 - 14 - 28, 2)[:5]
    block_h = max(110, len(cap_lines) * 15)
    iy = y + 40 + len(lines[:2]) * 22 + 10
    iy += max(0, (y + h - 14 - iy - block_h) // 2)
    box = 110
    c.fill_rect(x + 14, iy, box, box, tint)
    c.rect(x + 14, iy, box, box, LINE, 1)
    icon(c, x + 14 + (box - 96) // 2, iy + (box - 96) // 2)
    cy = iy + (block_h - len(cap_lines) * 15) // 2 + 2
    for ln in cap_lines:
        c.text(x + 14 + box + 14, cy, ln, 2, (48, 48, 48))
        cy += 15


def build_png():
    c = Canvas(W, H, PAPER)
    # Masthead.
    c.fill_rect(24, 24, 976, 144, NAVY)
    c.fill_rect(24, 24, 976, 6, RED)
    c.fill_rect(24, 162, 976, 6, RED)
    c.text_center(512, 40, "THE WORLD IN ONE DAY", 3, GOLD)
    c.text_center(512, 66, "27 NOVEMBER 2026", 7, WHITE)
    c.text_center(512, 128, "FRIDAY - THE DAY'S NEWS IN SIX STORIES", 2,
                  (200, 205, 220))
    # Story panels: 2 columns x 3 rows.
    pw, ph, gap = 480, 237, 16
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = 24 + col * (pw + gap)
        y = 184 + row * (ph + gap)
        draw_panel(c, x, y, pw, ph, story)
    # Footer ticker.
    c.fill_rect(24, 943, 976, 57, NAVY)
    tlines = wrap_text(TICKER, 976 - 28, 2)
    ty = 953
    for ln in tlines[:2]:
        c.text(38, ty, ln, 2, WHITE)
        ty += 15
    return encode_png(c)


def encode_png(c):
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    raw = bytearray()
    for yy in range(c.h):
        raw.append(0)  # filter: none
        raw += c.px[yy * c.w * 3:(yy + 1) * c.w * 3]
    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build_png()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
