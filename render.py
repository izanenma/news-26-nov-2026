"""Draw the front page for Thursday, 26 November 2026.

A single 1024x1024 newspaper front page, "THE WORLD", drawn with PIL from
the verified headlines of the day. Deterministic: no clock, no randomness,
no network. Run: python3 render.py  ->  writes entry.png beside this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 17, 17)
MUTED = (90, 84, 72)
SEA = (38, 84, 124)
SKY = (214, 226, 235)
STEEL = (120, 128, 138)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, width, leading, color=INK):
    """Draw wrapped paragraph, return y just below it."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, text, x, y, size=17):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=MUTED)
    return y + size + 8


def rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)


def draw_tanker_panel(draw, x0, y0, x1, y1):
    """A tanker on a mined strait: hull, bridge, smoke, waves, mines."""
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 58], fill=SKY)
    # sun
    draw.ellipse([x1 - 58, y0 + 12, x1 - 28, y0 + 42], fill=(232, 196, 96))
    # smoke from funnel
    for i, r in enumerate((8, 11, 14)):
        cx = x0 + 148 + i * 24
        cy = y0 + 26 - i * 5
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 148))
    # hull
    hx0, hx1, hy = x0 + 40, x1 - 40, y0 + 76
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 24, hy + 28), (hx0 + 24, hy + 28)],
                 fill=STEEL, outline=INK)
    draw.rectangle([hx0, hy - 20, hx0 + 112, hy], fill=(90, 98, 108), outline=INK)
    # funnel
    draw.rectangle([hx0 + 142, hy - 44, hx0 + 168, hy - 20],
                   fill=(176, 58, 44), outline=INK)
    # bridge windows
    for i in range(4):
        wx = hx0 + 10 + i * 24
        draw.rectangle([wx, hy - 14, wx + 14, hy - 5], fill=(220, 228, 235))
    # sea
    sea_top = hy + 28
    cap_top = y1 - 26
    draw.rectangle([x0 + 2, sea_top, x1 - 2, cap_top], fill=SEA)
    wy = sea_top + 16
    while wy < cap_top - 8:
        for wx in range(x0 + 12, x1 - 18, 40):
            draw.arc([wx, wy - 6, wx + 24, wy + 6], 180, 360,
                     fill=(255, 255, 255), width=2)
        wy += 18
    # mines: spiked circles in the water
    for mx, my in ((x0 + 64, sea_top + 22), (x1 - 84, sea_top + 40),
                   (x0 + 190, sea_top + 52)):
        draw.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=INK)
        for dx, dy in ((-9, 0), (9, 0), (0, -9), (0, 9),
                       (-6, -6), (6, -6), (-6, 6), (6, 6)):
            draw.line([(mx + dx, my + dy), (mx + dx * 1.5, my + dy * 1.5)],
                      fill=INK, width=2)
    # caption bar
    draw.rectangle([x0 + 2, cap_top, x1 - 2, y1 - 2], fill=(22, 58, 92))
    cap = font(SANS, 14)
    draw.text((x0 + 8, cap_top + 5),
              "A tanker threads the mined Strait of Hormuz.",
              font=cap, fill=(240, 240, 238))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # margin
    rx = W - mx

    # ---- masthead ----
    mast = font(SERIF_B, 96)
    title = "THE WORLD"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 18), title, font=mast, fill=INK)
    rule(d, mx, rx, 128, 3)
    sub = font(SANS_B, 19)
    d.text((mx, 140), "THURSDAY, 26 NOVEMBER 2026", font=sub, fill=INK)
    right = "ONE PAGE  •  SIX STORIES"
    d.text((rx - d.textlength(right, font=sub), 140), right, font=sub, fill=INK)
    rule(d, mx, rx, 172, 2)

    # ---- lead story ----
    y = kicker(d, "THE GULF WAR WIDENS", mx, 190, 18)
    y = para(d, "TANKERS HIT BY MINES AS THREAT SPREADS TO THE RED SEA",
             font(SERIF_B, 36), mx, y, rx - mx, 44)
    # body row: text left, tanker panel right
    body_y = 314
    col_w = 520
    panel_x0 = mx + col_w + 24
    yy = para(d, "Iran's Revolutionary Guard says two or three oil tankers "
                 "were hit by naval mines in the Strait of Hormuz, and "
                 "Tehran has ordered the waterway shut again. The war is "
                 "widening: Yemen's Houthis struck Saudi Arabia's Ras "
                 "Tanura refinery and threatened Jeddah.",
              font(SANS, 18), mx, body_y, col_w, 25)
    yy = para(d, "Shipping through the strait is down more than 40 percent "
                 "and Brent crude has passed $91 a barrel. Qatar is "
                 "mediating; Tehran offers to reopen the strait in "
                 "48 hours.",
              font(SANS, 18), mx, yy + 8, col_w, 25)
    draw_tanker_panel(d, panel_x0, body_y, rx, 530)

    # ---- middle row: two stories ----
    rule(d, mx, rx, 548, 2)
    mid = W // 2
    y1 = kicker(d, "UKRAINE  •  RUSSIA", mx, 564, 17)
    y1 = para(d, "PUTIN VOWS RETALIATION AS WAR SPILLS INTO LIBYA",
              font(SERIF_B, 26), mx, y1, mid - mx - 18, 31)
    para(d, "Putin called Ukraine's strikes on Russian refineries a blow "
            "that demands an \"inevitable\" reply. Kyiv's sea drones sank "
            "the Russian corvette Merkury at Benghazi; Tripoli called it a "
            "declaration of war and sought an emergency UN Security Council "
            "session.",
         font(SANS, 17), mx, y1 + 4, mid - mx - 18, 24)
    y2 = kicker(d, "UNITED STATES", mid + 18, 564, 17)
    y2 = para(d, "THANKSGIVING STORM THREATENS 250 MILLION",
              font(SERIF_B, 26), mid + 18, y2, rx - mid - 18, 31)
    para(d, "A dual-coast storm is battering holiday travel, with 81.5 "
            "million Americans on the move. Gusts above 70 mph threaten the "
            "100th Macy's parade in New York, where the giant balloons may "
            "be grounded for the first time since 1971.",
         font(SANS, 17), mid + 18, y2 + 4, rx - mid - 18, 24)

    # ---- bottom row: three stories ----
    rule(d, mx, rx, 782, 2)
    third = (rx - mx) // 3
    stories = [
        ("MARKETS", "SHARES SLIDE, DOW TOPS 50,000",
         "Nasdaq futures fell nearly 3% and Nvidia slid toward $147, while "
         "the Dow crossed 50,000 and US growth came in at 4.3%."),
        ("KYIV'S NEW FRIENDS", "HUNGARY'S PM MEETS ZELENSKY",
         "Péter Magyar met Volodymyr Zelensky, the first Hungarian prime "
         "minister to visit Ukraine since 2015. Norway pledged $7bn aid "
         "for 2027."),
        ("GAZA", "TRUCE FRAYS AS ISRAEL PUSHES IN",
         "Israel made its first ground push since the ceasefire; three were "
         "killed in airstrikes, including a UN worker. The Duma raised "
         "defence spending 27%."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        x0 = mx + i * third + (12 if i else 0)
        x1 = mx + (i + 1) * third - (12 if i < 2 else 0)
        yy = kicker(d, kick, x0, 798, 16)
        yy = para(d, head, font(SERIF_B, 21), x0, yy, x1 - x0, 26)
        para(d, body, font(SANS, 15), x0, yy + 4, x1 - x0, 21)

    # ---- footer ----
    rule(d, mx, rx, 972, 2)
    foot = font(SANS_B, 16)
    ft = "THE WORLD  —  THURSDAY 26 NOVEMBER 2026  •  SUMMED UP IN ONE PAGE"
    d.text(((W - d.textlength(ft, font=foot)) / 2, 984), ft, font=foot, fill=MUTED)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
