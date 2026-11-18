#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261117.

A broadsheet-style front page summing up the world news of Tuesday
17 November 2026, drawn entirely with PIL: crisp rendered text and
simple vector-style illustrations, no AI-generated imagery, so
nothing is garbled.

Design: "THE GLOBAL DISPATCH" — classic black-and-white broadsheet
with a crimson dateline, a full-width lead headline over a wide
Kerch Bridge illustration, a "BY THE NUMBERS" strip, and six
horizontal story cards (icon left, text right).

Every story was verified as first reported on 17 November 2026 (UTC)
before drawing; see SOURCES in README.md.

Run:  python3 draw.py            -> writes entry.png (1024x1024)
      python3 draw.py out.png    -> writes to the given path
"""

import math
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette -----------------------------------------------------------
PAPER = (250, 248, 240)    # page background
CARD = (255, 255, 255)     # story cards
INK = (18, 18, 18)         # main text
SOFT = (74, 72, 66)        # body text
GRAY = (120, 116, 106)     # footer
CRIMSON = (165, 28, 28)    # kickers, dateline, accents
DARK = (26, 26, 30)        # numbers strip
GOLD = (232, 184, 70)      # numbers
HAIR = (196, 188, 172)     # hairlines
EDGE = (216, 208, 190)     # card borders

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf"
SERIF_I = f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf"
SANS_B = f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap_capped(d, text, font, max_w, max_lines):
    """Wrap, then cap at max_lines, adding an ellipsis to the last line."""
    lines = wrap(d, text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and d.textlength(last + " …", font=font) > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = (last + " …").strip()
    return lines


def burst(d, cx, cy, r_out, r_in, n=9, rot=-90, fill=(255, 170, 0)):
    """Starburst polygon (explosion flash)."""
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def star(d, cx, cy, r, fill=(255, 255, 255)):
    burst(d, cx, cy, r, r * 0.42, n=5, fill=fill)


# ---- small flags -------------------------------------------------------
def flag_usa(d, x, y, w, h):
    step = h / 13
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * step, x + w, y + (i + 1) * step], fill=col)
    cw, ch = w * 0.42, step * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            sx = x + cw * (0.12 + 0.19 * c)
            sy = y + ch * (0.14 + 0.24 * r)
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))


def flag_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    r = h * 0.30
    d.ellipse([x + w / 2 - r, y + h / 2 - r, x + w / 2 + r, y + h / 2 + r],
              fill=(188, 0, 45))


def flag_india(d, x, y, w, h):
    third = h / 3
    d.rectangle([x, y, x + w, y + third], fill=(255, 153, 51))
    d.rectangle([x, y + third, x + w, y + 2 * third], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * third, x + w, y + h], fill=(19, 136, 8))
    cx, cy, r = x + w / 2, y + h / 2, h * 0.16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(6, 22, 110), width=1)
    for i in range(8):
        a = math.radians(i * 45)
        d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)],
               fill=(6, 22, 110), width=1)


def flag_australia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    cw, ch = w * 0.5, h * 0.5
    d.rectangle([x, y, x + cw, y + ch], fill=(1, 33, 105))
    d.line([x, y, x + cw, y + ch], fill=(255, 255, 255), width=3)
    d.line([x + cw, y, x, y + ch], fill=(255, 255, 255), width=3)
    d.line([x, y, x + cw, y + ch], fill=(204, 0, 0), width=1)
    d.line([x + cw, y, x, y + ch], fill=(204, 0, 0), width=1)
    d.rectangle([x + cw / 2 - 2, y, x + cw / 2 + 2, y + ch],
                fill=(255, 255, 255))
    d.rectangle([x, y + ch / 2 - 2, x + cw, y + ch / 2 + 2],
                fill=(255, 255, 255))
    d.rectangle([x + cw / 2 - 1, y, x + cw / 2 + 1, y + ch], fill=(204, 0, 0))
    d.rectangle([x, y + ch / 2 - 1, x + cw, y + ch / 2 + 1], fill=(204, 0, 0))
    star(d, x + cw / 2, y + ch + (h - ch) / 2, 5)
    for sx, sy in [(0.72, 0.30), (0.85, 0.48), (0.70, 0.66), (0.83, 0.80)]:
        star(d, x + w * sx, y + h * sy, 2.5)


def flag_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(1, 33, 105))
    dw = max(4, h // 7)
    d.line([x, y, x + w, y + h], fill=(255, 255, 255), width=dw)
    d.line([x + w, y, x, y + h], fill=(255, 255, 255), width=dw)
    d.line([x, y, x + w, y + h], fill=(204, 0, 0), width=max(2, dw // 2))
    d.line([x + w, y, x, y + h], fill=(204, 0, 0), width=max(2, dw // 2))
    t = h / 9
    d.rectangle([x + w / 2 - t, y, x + w / 2 + t, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h / 2 - t, x + w, y + h / 2 + t], fill=(255, 255, 255))
    t2 = h / 22
    d.rectangle([x + w / 2 - t2, y, x + w / 2 + t2, y + h], fill=(204, 0, 0))
    d.rectangle([x, y + h / 2 - t2, x + w, y + h / 2 + t2], fill=(204, 0, 0))


# ---- story icons (each draws inside x, y, w, h) ------------------------
def icon_quad(d, x, y, w, h):
    """Four Quad flags in a 2x2 grid over a sky-blue field."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    fw, fh, g = (w - 12) / 2, (h - 12) / 2, 4
    flag_usa(d, x + 4, y + 4, fw, fh)
    flag_japan(d, x + 8 + fw, y + 4, fw, fh)
    flag_india(d, x + 4, y + 8 + fh, fw, fh)
    flag_australia(d, x + 8 + fw, y + 8 + fh, fw, fh)
    for fx, fy in [(x + 4, y + 4), (x + 8 + fw, y + 4),
                   (x + 4, y + 8 + fh), (x + 8 + fw, y + 8 + fh)]:
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=(60, 60, 60), width=1)


def icon_radar(d, x, y, w, h):
    """Desert radar dish under drone attack."""
    d.rectangle([x, y, x + w, y + h * 0.68], fill=(170, 203, 224))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(206, 178, 124))
    bx, by = x + w * 0.32, y + h * 0.86
    d.line([bx, by, bx, by - h * 0.44], fill=(70, 70, 70), width=4)
    d.pieslice([bx - 22, by - h * 0.44 - 26, bx + 22, by - h * 0.44 + 18],
               start=200, end=340, fill=(242, 242, 238))
    d.arc([bx - 22, by - h * 0.44 - 26, bx + 22, by - h * 0.44 + 18],
          start=200, end=340, fill=(70, 70, 70), width=2)
    d.polygon([(bx + 6, by - h * 0.44 - 6), (bx + 46, by - h * 0.62),
               (bx + 46, by - h * 0.34)], fill=(140, 225, 150))
    for dx, dy, s in [(0.68, 0.22, 1.0), (0.84, 0.42, 0.75)]:
        cx, cy = x + w * dx, y + h * dy
        d.ellipse([cx - 5 * s, cy - 3 * s, cx + 5 * s, cy + 3 * s],
                  fill=(35, 35, 35))
        d.line([cx - 10 * s, cy - 5 * s, cx + 10 * s, cy + 5 * s],
               fill=(35, 35, 35), width=2)
        d.line([cx - 10 * s, cy + 5 * s, cx + 10 * s, cy - 5 * s],
               fill=(35, 35, 35), width=2)
    burst(d, bx + 12, by - h * 0.44 - 4, 11, 4, n=8)


def icon_jets(d, x, y, w, h):
    """Two fighter jets against a rising-sun disc over the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 236))
    d.rectangle([x, y + h * 0.74, x + w, y + h], fill=(44, 84, 122))
    sx, sy, sr = x + w * 0.76, y + h * 0.28, 13
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(188, 0, 45))
    for jx, jy, s in [(0.28, 0.32, 1.15), (0.48, 0.55, 0.9)]:
        cx, cy = x + w * jx, y + h * jy
        d.polygon([(cx - 18 * s, cy), (cx + 18 * s, cy - 3 * s),
                   (cx + 10 * s, cy + 2 * s), (cx + 14 * s, cy + 8 * s),
                   (cx + 2 * s, cy + 5 * s), (cx - 6 * s, cy + 10 * s),
                   (cx - 8 * s, cy + 3 * s)],
                  fill=(40, 44, 52))
        d.line([cx - 30 * s, cy + 4 * s, cx - 18 * s, cy + 1 * s],
               fill=(255, 255, 255), width=2)


def icon_sanctions(d, x, y, w, h):
    """Union Jack beside a building under a prohibition ring."""
    flag_uk(d, x, y, w * 0.46, h)
    d.rectangle([x + w * 0.46, y, x + w, y + h], fill=(238, 234, 222))
    bx, by = x + w * 0.75, y + h * 0.66
    d.rectangle([bx - 14, by - 19, bx + 14, by + 12], fill=(122, 118, 108))
    d.polygon([(bx - 18, by - 19), (bx, by - 30), (bx + 18, by - 19)],
              fill=(92, 88, 80))
    for wy in (by - 11, by + 1):
        for wx in (bx - 9, bx + 2):
            d.rectangle([wx, wy, wx + 7, wy + 7], fill=(255, 240, 180))
    d.ellipse([bx - 22, by - 32, bx + 22, by + 14], outline=(200, 30, 30),
              width=5)
    d.line([bx - 15, by + 10, bx + 15, by - 28], fill=(200, 30, 30), width=5)


def icon_crash(d, x, y, w, h):
    """Plane falling over snowy Siberian ground, smoke and fire."""
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(168, 190, 208))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(232, 236, 240))
    d.polygon([(x, y + h * 0.62), (x + w * 0.30, y + h * 0.40),
               (x + w * 0.55, y + h * 0.62)], fill=(120, 138, 158))
    d.polygon([(x + w * 0.45, y + h * 0.62), (x + w * 0.72, y + h * 0.34),
               (x + w, y + h * 0.62)], fill=(100, 120, 142))
    d.polygon([(x + w * 0.66, y + h * 0.38), (x + w * 0.72, y + h * 0.34),
               (x + w * 0.78, y + h * 0.38), (x + w * 0.72, y + h * 0.44)],
              fill=(255, 255, 255))
    # falling plane, nose down-right: a jet silhouette rotated 60 degrees
    cx, cy = x + w * 0.42, y + h * 0.30
    shape = [(-18, 0), (18, -3), (10, 2), (14, 8), (2, 5), (-6, 10), (-8, 3)]
    ang = math.radians(60)
    ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(cx + px * ca - py * sa, cy + px * sa + py * ca)
               for px, py in shape], fill=(50, 54, 60))
    # smoke trail behind it, up to the left
    for sx, sy, r in [(0.28, 0.12, 5), (0.32, 0.17, 7), (0.36, 0.22, 8)]:
        d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r,
                   y + h * sy + r], fill=(150, 150, 150))
    # impact fire
    burst(d, x + w * 0.60, y + h * 0.66, 14, 6, n=8)
    burst(d, x + w * 0.60, y + h * 0.66, 8, 3, n=8, fill=(255, 230, 120))


def icon_virus(d, x, y, w, h):
    """Spiky measles virus on a pale clinical field."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 232))
    cx, cy, r = x + w * 0.5, y + h * 0.52, 22
    for i in range(12):
        a = math.radians(i * 30)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(165, 28, 28), width=3)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(165, 28, 28))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 60, 60))
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx - r * 0.1, cy - r * 0.1],
              fill=(235, 130, 130))
    for px, py, pr in [(0.16, 0.18, 4), (0.84, 0.22, 3), (0.82, 0.80, 4),
                       (0.15, 0.82, 3)]:
        d.ellipse([x + w * px - pr, y + h * py - pr, x + w * px + pr,
                   y + h * py + pr], fill=(200, 60, 60))


# ---- lead illustration: the Kerch Bridge, broken -----------------------
def lead_bridge(d, x, y, w, h):
    # dusk sky
    for i in range(h):
        t = i / h
        rr = int(150 + (226 - 150) * t)
        gg = int(168 + (214 - 168) * t)
        bb = int(186 + (200 - 186) * t)
        d.line([x, y + i, x + w, y + i], fill=(rr, gg, bb))
    # water
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(38, 62, 86))
    for i in range(14):
        wx = x + 12 + i * (w - 24) / 13
        d.line([wx, y + h * 0.75, wx + 26, y + h * 0.75],
               fill=(110, 150, 180), width=2)
        d.line([wx + 14, y + h * 0.80, wx + 34, y + h * 0.80],
               fill=(90, 130, 165), width=2)
    deck = y + h * 0.58
    # towers
    for tx in (x + w * 0.22, x + w * 0.78):
        d.rectangle([tx - 6, y + h * 0.06, tx + 6, deck], fill=(24, 28, 34))
    # tied arch springing from the deck at the towers, apex near the top
    d.arc([x + w * 0.22, y + h * 0.08, x + w * 0.78, y + h * 1.08],
          start=180, end=360, fill=(24, 28, 34), width=5)

    def arch_y(f):
        # height of the arch above the deck at width-fraction f
        dx = (f - 0.5) / 0.28
        return deck - 0.50 * h * math.sqrt(max(0.0, 1 - dx * dx))

    # suspension cables from the arch down to the deck
    for f in (0.28, 0.34, 0.40, 0.60, 0.66, 0.72):
        cx = x + w * f
        d.line([cx, arch_y(f), cx, deck], fill=(24, 28, 34), width=2)
    # cables severed at the break, dangling from the arch
    for f in (0.45, 0.55):
        cx = x + w * f
        d.line([cx, arch_y(f), cx, arch_y(f) + 0.16 * h],
               fill=(24, 28, 34), width=2)
    # stay cables on the approach spans
    d.line([x + 6, y + h * 0.30, x + w * 0.22, y + h * 0.06],
           fill=(24, 28, 34), width=3)
    d.line([x + w * 0.78, y + h * 0.06, x + w - 6, y + h * 0.30],
           fill=(24, 28, 34), width=3)
    # deck, broken in the middle
    ex = x + w * 0.5
    d.line([x + 6, deck, ex - 40, deck], fill=(24, 28, 34), width=9)
    d.line([ex + 40, deck, x + w - 6, deck], fill=(24, 28, 34), width=9)
    # jagged broken ends
    d.line([ex - 40, deck, ex - 26, deck + 20], fill=(24, 28, 34), width=4)
    d.line([ex + 40, deck, ex + 26, deck + 20], fill=(24, 28, 34), width=4)
    # fallen span in the water, tilted (above the caption ribbon)
    d.polygon([(ex - 40, y + h * 0.79), (ex + 34, y + h * 0.72),
               (ex + 44, y + h * 0.79), (ex - 30, y + h * 0.85)],
              fill=(20, 24, 30))
    d.line([ex - 36, y + h * 0.77, ex + 30, y + h * 0.71],
           fill=(90, 100, 110), width=2)
    # explosion at the break
    burst(d, ex, deck - 10, 42, 16, n=10)
    burst(d, ex, deck - 10, 26, 10, n=10, rot=-70, fill=(255, 230, 120))
    d.ellipse([ex - 8, deck - 18, ex + 8, deck - 2], fill=(255, 255, 240))
    # smoke
    for sx, sy, r in [(-52, -44, 10), (-32, -56, 13), (34, -52, 12),
                      (54, -38, 9), (0, -62, 11)]:
        d.ellipse([ex + sx - r, deck - 10 + sy - r, ex + sx + r,
                   deck - 10 + sy + r], fill=(110, 110, 110))
    # caption ribbon
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(18, 18, 18))
    d.text((x + 14, y + h - 21), "KERCH STRAIT — THE ROAD ARCH FELL INTO "
           "THE SEA; THE RAILWAY STANDS, DAMAGED", font=F(SANS_B, 14),
           fill=(232, 184, 70))


# ---- page assembly ------------------------------------------------------
def build_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24                      # side margin
    CW = W - 2 * M              # content width

    # ===== masthead =====
    d.line([M, 12, W - M, 12], fill=INK, width=3)
    d.line([M, 18, W - M, 18], fill=INK, width=1)
    d.text((W / 2, 26), "THE GLOBAL DISPATCH", font=F(SERIF_B, 62),
           fill=INK, anchor="ma")
    # dateline row
    d.text((M, 102), "TUESDAY, 17 NOVEMBER 2026", font=F(SANS_B, 19),
           fill=CRIMSON, anchor="la")
    d.text((W / 2, 103), "WORLD EDITION", font=F(SANS_B, 16), fill=SOFT,
           anchor="ma")
    d.text((W - M, 103), "ONE DAY  •  SEVEN STORIES", font=F(SANS_B, 16),
           fill=SOFT, anchor="ra")
    d.line([M, 130, W - M, 130], fill=INK, width=4)
    d.line([M, 136, W - M, 136], fill=INK, width=1)

    # ===== lead story =====
    ly = 148
    d.text((M, ly), "LEAD STORY  •  WAR IN UKRAINE", font=F(SANS_B, 18),
           fill=CRIMSON, anchor="la")
    head = wrap(d, "Ukraine drops a span of the Kerch Bridge into the "
                "strait", F(SERIF_B, 44), CW)
    yy = ly + 28
    for line in head:
        d.text((M, yy), line, font=F(SERIF_B, 44), fill=INK, anchor="la")
        yy += 52
    lead_bridge(d, M, yy + 6, CW, 140)
    d.rectangle([M, yy + 6, M + CW, yy + 146], outline=INK, width=2)
    sy = yy + 156
    stand = wrap(d, "Missiles and drones strike the road link to Crimea "
                 "overnight in what Zelensky calls an “unprecedented” "
                 "operation. Two people were killed, Crimea’s governor says.",
                 F(SERIF_I, 20), CW)
    for line in stand:
        d.text((M, sy), line, font=F(SERIF_I, 20), fill=SOFT, anchor="la")
        sy += 26

    # ===== by the numbers =====
    ny = sy + 12
    d.rectangle([M, ny, W - M, ny + 72], fill=DARK)
    stats = [
        ("1,441", "drones Russia says it shot down in one night — a record"),
        ("19", "killed as an An-12 crashes in Siberia"),
        ("5,412", "measles cases in the US in 2026"),
        ("8", "Israeli firms hit by UK sanctions"),
    ]
    col_w = CW / 4
    for i, (num, label) in enumerate(stats):
        cx = M + col_w * i
        if i:
            d.line([cx, ny + 12, cx, ny + 62], fill=(90, 90, 96), width=1)
        d.text((cx + 14, ny + 8), num, font=F(SANS_B, 30), fill=GOLD,
               anchor="la")
        for j, ln in enumerate(wrap(d, label, F(SANS, 13), col_w - 28)):
            d.text((cx + 14, ny + 42 + j * 15), ln, font=F(SANS, 13),
                   fill=(226, 226, 226), anchor="la")

    # ===== six stories, horizontal cards =====
    stories = [
        ("DIPLOMACY  •  ASIA-PACIFIC",
         "Quad meets in Manila, first summit in two years",
         "Trump, Modi, Albanese and Takaichi agree joint maritime "
         "patrols, undersea-cable protection and a business forum "
         "for 2027.", icon_quad),
        ("WAR  •  MIDDLE EAST",
         "Iran drones target US radar in Bahrain",
         "Tehran’s third strike on US targets there in five days; "
         "Bahrain says its defences intercepted the drones. No US "
         "casualties.", icon_radar),
        ("SECURITY  •  EAST ASIA",
         "Japan scrambles jets as Russian planes enter its airspace",
         "Two suspected Russian aircraft cross in near Fukuoka for "
         "about three minutes each; Tokyo lodges a “very stern "
         "protest”.", icon_jets),
        ("DIPLOMACY  •  MIDDLE EAST",
         "Britain sanctions eight settlement firms",
         "Asset freezes hit Israeli construction companies and "
         "Tzav 9, the group accused of blocking aid convoys into "
         "Gaza.", icon_sanctions),
        ("DISASTER  •  RUSSIA",
         "Military plane crashes in Siberia; 19 killed",
         "An An-12 transport goes down near Yagunovo in the "
         "Kemerovo region; a technical fault is the suspected "
         "cause.", icon_crash),
        ("HEALTH  •  AMERICAS",
         "US loses measles-free status after 26 years",
         "PAHO declares endemic transmission is back: 5,412 US "
         "cases in 2026, the most in 35 years. Mexico and Bolivia "
         "too.", icon_virus),
    ]
    gx = [M, M + 322, M + 644]
    gy = [ny + 86, ny + 86 + 192]
    cw, chh = 310, 180
    for i, (kicker, headline, detail, icon_fn) in enumerate(stories):
        cx, cy = gx[i % 3], gy[i // 3]
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD,
                    outline=EDGE, width=2)
        d.rectangle([cx, cy, cx + 5, cy + chh], fill=CRIMSON)
        d.text((cx + 16, cy + 10), kicker, font=F(SANS_B, 13),
               fill=CRIMSON, anchor="la")
        icon_fn(d, cx + 16, cy + 32, 74, 74)
        d.rectangle([cx + 16, cy + 32, cx + 90, cy + 106],
                    outline=EDGE, width=1)
        hlines = wrap_capped(d, headline, F(SANS_B, 18), cw - 118, 3)
        hy = cy + 32
        for line in hlines:
            d.text((cx + 100, hy), line, font=F(SANS_B, 18), fill=INK,
                   anchor="la")
            hy += 23
        dlines = wrap_capped(d, detail, F(SANS, 14), cw - 32, 3)
        dy = cy + 114
        for line in dlines:
            d.text((cx + 16, dy), line, font=F(SANS, 14), fill=SOFT,
                   anchor="la")
            dy += 18

    # ===== footer =====
    fy = gy[1] + chh + 12
    d.line([M, fy, W - M, fy], fill=HAIR, width=2)
    d.text((W / 2, fy + 6), "A drawn summary of the world’s news  •  "
           "Tuesday, 17 November 2026  •  Every story first reported "
           "on that day", font=F(SANS, 14), fill=GRAY, anchor="ma")
    d.text((W / 2, fy + 22), "Sources include AP, Reuters, BBC, GOV.UK "
           "and PAHO", font=F(SANS, 12), fill=GRAY, anchor="ma")
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build_page()
    img.save(out, optimize=True)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
