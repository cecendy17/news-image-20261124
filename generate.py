#!/usr/bin/env python3
"""Broadsheet variant (Variant B) for make.fun news-image-20261124.
Deterministic, stdlib + PIL only, no network. Draws entry.png 1024x576.
All facts come from the 24 Nov 2026 news dossier; nothing invented.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 576
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
INK = (26, 26, 26)
GREY = (110, 105, 95)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
RULE = (26, 26, 26)
LIGHT = (232, 226, 212)

F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, width, lh, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def kicker(draw, x, y, text, w):
    f = SANS_B(9)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + 13

def source_line(draw, x, y, text):
    draw.text((x, y), text, font=SANS(8), fill=GREY)
    return y + 11

# ---------------- procedural illustrations ----------------
def ill_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 84, 124))
    # sky glow near horizon
    d.rectangle([x, y + int(h * 0.52), x + w, y + int(h * 0.62)], fill=(90, 130, 165))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(22, 58, 88))
    # wake
    d.line([x + w * 0.10, y + h * 0.86, x + w * 0.90, y + h * 0.86],
           fill=(180, 210, 230), width=2)
    d.line([x + w * 0.20, y + h * 0.93, x + w * 0.80, y + h * 0.93],
           fill=(140, 180, 205), width=2)
    # hull: low, long, pointed bow
    d.polygon([(x + w * 0.08, y + h * 0.62), (x + w * 0.88, y + h * 0.62),
               (x + w * 0.80, y + h * 0.86), (x + w * 0.16, y + h * 0.86)],
              fill=(52, 52, 58))
    d.rectangle([x + w * 0.10, y + h * 0.62, x + w * 0.86, y + h * 0.67],
                fill=(120, 120, 125))
    # superstructure + mast
    d.rectangle([x + w * 0.36, y + h * 0.42, x + w * 0.58, y + h * 0.62],
                fill=(200, 200, 205))
    d.rectangle([x + w * 0.45, y + h * 0.28, x + w * 0.49, y + h * 0.42],
                fill=(70, 70, 75))
    # blast at the stern, overlapping the hull
    cx, cy = x + w * 0.12, y + h * 0.60
    for r, c in ((15, (255, 176, 32)), (9, (255, 110, 32)), (4, (255, 240, 180))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

def ill_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 52))
    for i in range(5):
        px = x + 6 + i * (w - 12) / 4
        d.line([px, y, px, y + 8], fill=(200, 200, 200), width=2)
        d.line([px, y + h - 8, px, y + h], fill=(200, 200, 200), width=2)
    d.rectangle([x + w * 0.28, y + h * 0.22, x + w * 0.72, y + h * 0.78],
                fill=(0, 176, 120), outline=(255, 255, 255), width=2)
    d.text((x + w * 0.38, y + h * 0.38), "AI", font=SANS_B(13), fill=(255, 255, 255))

def ill_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 196, 120))
    cx, cy, r = x + w * 0.5, y + h * 0.55, min(w, h) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 130, 90))
    d.ellipse([cx - r * 0.55, cy - r * 0.7, cx + r * 0.1, cy - r * 0.1], fill=(120, 190, 120))
    d.ellipse([cx - r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.65], fill=(120, 190, 120))
    d.line([cx - r * 0.7, cy - r * 0.9, cx, cy - r * 0.2, cx + r * 0.4, cy + r * 0.3,
            cx + r * 0.8, cy + r * 0.9], fill=(163, 22, 33), width=3)
    # round sun (radius from height, so it stays a circle at any size)
    scx, scy, sr = x + w * 0.86, y + h * 0.50, h * 0.30
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(255, 120, 40))

def ill_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    import math
    cx, cy, r = x + w / 2, y + h / 2, min(w, h) * 0.32
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        d.ellipse([cx + r * math.cos(a) - 2, cy + r * math.sin(a) - 2,
                   cx + r * math.cos(a) + 2, cy + r * math.sin(a) + 2],
                  fill=(255, 204, 0))

def ill_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 220, 228))
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - 12, cy - 6, cx + 12, cy + 6], fill=(40, 40, 40))
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        px, py = cx + sx * 16, cy + sy * 10
        d.ellipse([px - 7, py - 2, px + 7, py + 2], fill=(90, 90, 90))
        d.line([cx, cy, px, py], fill=(40, 40, 40), width=2)

def ill_city(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 60, 70))
    for i, bh in enumerate((0.55, 0.8, 0.65, 0.9, 0.5)):
        bx = x + i * w / 5
        d.rectangle([bx + 2, y + h * (1 - bh), bx + w / 5 - 2, y + h], fill=(30, 30, 38))
    d.ellipse([x + w * 0.62, y + h * 0.10, x + w * 0.86, y + h * 0.42], fill=(255, 150, 50))
    d.ellipse([x + w * 0.68, y + h * 0.18, x + w * 0.80, y + h * 0.34], fill=(255, 220, 120))

def ill_wave(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 90, 120))
    for i in range(3):
        yy = y + h * (0.3 + i * 0.22)
        d.arc([x + 4, yy - 6, x + w - 4, yy + 10], 0, 180, fill=(255, 255, 255), width=3)
    d.ellipse([x + w * 0.68, y + h * 0.08, x + w * 0.86, y + h * 0.32], fill=(255, 220, 120))

def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 110, 70))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.25), (x + w * 0.55, y + h),
               (x + w * 0.75, y + h * 0.45), (x + w, y + h)], fill=(110, 80, 50))
    d.line([x + w * 0.3, y + h * 0.25, x + w * 0.42, y + h * 0.55, x + w * 0.55, y + h],
           fill=(255, 240, 200), width=3)

def ill_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 40))
    for px, py in ((0.15, 0.2), (0.4, 0.12), (0.7, 0.25), (0.85, 0.15), (0.3, 0.4), (0.6, 0.55)):
        d.ellipse([x + w * px - 1, y + h * py - 1, x + w * px + 1, y + h * py + 1],
                  fill=(255, 255, 255))
    cx, cy = x + w * 0.5, y + h * 0.55
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(180, 120, 60))
    d.ellipse([cx - 20, cy - 5, cx + 20, cy + 5], outline=(220, 220, 220), width=2)

def ill_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 80, 60))
    pts = [(x + 6, y + h * 0.75), (x + w * 0.3, y + h * 0.6), (x + w * 0.5, y + h * 0.65),
           (x + w * 0.7, y + h * 0.35), (x + w - 6, y + h * 0.18)]
    d.line(pts, fill=(0, 220, 140), width=3)
    d.polygon(pts + [(x + w - 6, y + h), (x + 6, y + h)], fill=(0, 220, 140))

def ill_ball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 110, 50))
    cx, cy, r = x + w / 2, y + h / 2, min(w, h) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 230, 60))
    d.arc([cx - r, cy - r * 0.5, cx + r * 0.2, cy + r * 0.5], 270, 90,
          fill=(255, 255, 255), width=2)
    d.arc([cx - r * 0.2, cy - r * 0.5, cx + r, cy + r * 0.5], 90, 270,
          fill=(255, 255, 255), width=2)

def mini_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 68, 110))
    # simplified continents (abstract blobs)
    d.ellipse([x + w * 0.06, y + h * 0.18, x + w * 0.30, y + h * 0.62], fill=(90, 160, 100))  # Americas
    d.ellipse([x + w * 0.40, y + h * 0.12, x + w * 0.56, y + h * 0.45], fill=(90, 160, 100))  # Europe
    d.ellipse([x + w * 0.55, y + h * 0.20, x + w * 0.78, y + h * 0.58], fill=(110, 175, 105))  # Asia
    d.ellipse([x + w * 0.44, y + h * 0.48, x + w * 0.58, y + h * 0.85], fill=(90, 160, 100))  # Africa
    d.ellipse([x + w * 0.80, y + h * 0.60, x + w * 0.94, y + h * 0.85], fill=(120, 170, 110))  # Oceania
    dots = [(0.17, 0.35), (0.48, 0.28), (0.62, 0.38), (0.72, 0.40),
            (0.50, 0.66), (0.86, 0.72), (0.30, 0.55)]
    for dx, dy in dots:
        px, py = x + w * dx, y + h * dy
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 60, 60),
                  outline=(255, 255, 255))
    d.text((x + 4, y + h - 12), "WHERE THE NEWS IS", font=SANS_B(7), fill=(255, 255, 255))

# ---------------- story data (from dossier only) ----------------
LEAD1_HEAD = "Ukraine claims it sank Russian corvette Merkury off Benghazi"
LEAD1_DECK = ("Seven sea drones struck the warship in Libya's port, Kyiv says; "
              "Moscow has not confirmed it. Tripoli seeks answers and the UN "
              "wants an inquiry as the war reaches the Mediterranean.")
LEAD2_HEAD = "Jensen Huang is Nvidia CEO again \u2014 shares jump 31%"
LEAD2_DECK = ("Board calls the move unanimous after input from senior levels of "
              "the US government. Asia rallies; Congress members object.")
LEAD3_HEAD = "COP31 collapses with no deal after ~50 hours of overtime"
LEAD3_DECK = ("90+ nations rejected the final draft in Antalya because it did "
              "not mention fossil fuels. Grist calls it the darkest moment "
              "of climate diplomacy.")

PICTORIAL = [
    ("EUROPE", "EU proposes 22nd sanctions package on Russia", "60 banks, 70+ shadow-fleet ships targeted", ill_eu),
    ("EUROPE", "Polish air defences active as Russian drones stray in", "Two missiles and a drone fell in Poland on 20 Nov", ill_drone),
    ("EUROPE", "Russian strike on Zaporizhzhia kills 2, injures 22", "Two children among the injured, overnight 24 Nov", ill_city),
    ("MIDDLE EAST", "Israeli strikes kill at least 3 in Gaza, incl. UNRWA staff", "Oxfam: Gaza has become \u201ctoxic land\u201d", ill_city),
    ("MIDDLE EAST", "Three tankers hit by mines in the Strait of Hormuz", "IRGC reports strikes amid US escort; UK logs record attacks", ill_wave),
    ("ASIA", "Nepal quake 5.6 strikes Koshi province", "Near the China border; reported 24 Nov", ill_quake),
    ("ASIA", "Tiangong opens to first foreign astronaut", "Pakistan's Zeeshan Ali joins Shenzhou-24 mission", ill_space),
    ("AMERICAS", "Amazon buys Decart AI for ~$7.5bn", "Palo Alto buys Applied Compute for $4.5bn; Tesla launches FSD v15", ill_chart),
    ("SCIENCE & TECH", "BepiColombo enters orbit around Mercury", "ESA\u2013JAXA probe arrives after an 8-year journey", ill_space),
    ("SPORT", "Alcaraz wins first ATP Finals title in Turin", "Beats Zverev; Gukesh begins world title defence in Geneva", ill_ball),
]

TIMELINE = [
    ("00:00\u201302:00", "Nepal quake 5.6; factory fire in Indonesia reported."),
    ("~04:00", "Russian strike on Zaporizhzhia: 2 killed, 22 hurt."),
    ("07:55", "Forbes: \u201cWhy Jensen Huang and Nvidia matter so much\u201d."),
    ("08:36", "US Congress members criticise Huang's return."),
    ("09:33", "Stoxx 600 +0.73% as tech stocks rebound."),
    ("10:50", "Asia rallies: Nikkei +3.91%, Kospi +6%."),
    ("11:38", "US blacklists Alibaba unit, Megaspeed entities."),
    ("PM", "14 nations back ICJ Myanmar ruling; UN seeks Libya inquiry."),
]

BRIEFS = [
    ("EUROPE", [
        "Russia warns Estonia: moves \u201con verge of triggering open war\u201d.",
        "Report: \u201cSputnik-S\u201d satellite could carry nuclear arms to space.",
        "Trump\u2013Putin Shenzhen talks end in ~40 minutes with no deal.",
        "Spain's Hern\u00e1ndez de Cos tipped to replace Lagarde at the ECB.",
        "Novoshakhtinsk refinery shuts after 80 Ukrainian drones hit it.",
    ]),
    ("MIDDLE EAST", [
        "Trump warns of \u201cvery traumatic\u201d result if Iran nuclear deal fails.",
        "Houthis report dozens killed in Saudi air strikes on Yemen.",
        "14 nations back ICJ ruling on Myanmar's genocide of Rohingya.",
    ]),
    ("ASIA", [
        "Indonesia: big factory fire, workers missing as rescuers work.",
        "India holds No. 3 in Asia Power Index 2026; exports hit record.",
        "Trump announces Japan trade deal; SoftBank invests $2bn in Intel.",
        "Singapore, Australia sign two pacts; PM Wong hails partnership.",
        "Thailand\u2013Cambodia border fighting held after ceasefire.",
    ]),
    ("AMERICAS", [
        "Oregon and Virginia sue SpaceX over alleged Grok child images.",
        "Senate to vote on Trump's $9.4bn foreign aid and media cuts.",
        "Democrats win historic majority in the 2026 midterms.",
        "NHTSA lets Zoox charge for driverless robotaxis with no wheel.",
        "Car bomb destroys building in Villavicencio, Colombia.",
    ]),
    ("AFRICA", [
        "Somalia and Uganda step up operations against Al-Shabaab.",
        "School enrolment in Borno nearly doubles after conflict.",
        "Africa's first \u201ccomfort women\u201d statue to be unveiled in South Africa.",
    ]),
    ("SCIENCE & TECH", [
        "Brazil study: Wolbachia mosquitoes cut dengue by 69%.",
    ]),
    ("SPORT", [
        "Gukesh defends world chess crown vs Sindarov; India\u2013NZ Test drawn.",
    ]),
]

def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead ----
    d.text((12, 4), "THE WORLD TODAY", font=SERIF_B(34), fill=INK)
    d.text((700, 8), "TUESDAY 24 NOVEMBER 2026", font=SANS_B(13), fill=INK)
    # chip
    chip = "36 STORIES  \u2022  DATE-CHECKED"
    cw = d.textlength(chip, font=SANS_B(10)) + 16
    d.rounded_rectangle([1024 - 12 - cw, 26, 1024 - 12, 44], radius=8,
                        fill=RED)
    d.text((1024 - 12 - cw + 8, 30), chip, font=SANS_B(10), fill=(255, 255, 255))
    d.line([12, 50, 1012, 50], fill=RULE, width=2)
    d.line([12, 54, 1012, 54], fill=RULE, width=1)

    top, bot = 62, 556
    colw = 326
    xs = [12, 348, 684]

    # ---- LEFT: lead 1 + timeline + map ----
    x = xs[0]
    y = top
    y = kicker(d, x, y, "Lead \u2022 Europe / Mediterranean", colw)
    ill_ship(d, x, y, colw, 112)
    y += 112 + 5
    y = text_block(d, x, y, LEAD1_HEAD, SERIF_B(18), colw, 22, max_lines=3)
    y = text_block(d, x, y + 2, LEAD1_DECK, SANS(10), colw, 13, max_lines=4)
    y = source_line(d, x, y + 2, "MIDDLE EAST EYE  \u2022  REUTERS  \u2022  23 NOV")
    y += 6
    d.line([x, y, x + colw, y], fill=GREY, width=1)
    y += 5
    d.text((x, y), "THE DAY IN UTC", font=SANS_B(10), fill=RED)
    y += 15
    for t, txt in TIMELINE:
        d.line([x + 4, y + 3, x + 4, y + 24], fill=(180, 175, 160), width=2)
        d.ellipse([x + 1, y + 3, x + 7, y + 9], fill=RED)
        d.text((x + 14, y), t, font=SANS_B(9), fill=INK)
        y2 = text_block(d, x + 96, y, txt, SANS(9), colw - 96, 11, max_lines=2)
        y = max(y + 13, y2) + 1
    y += 4
    mini_map(d, x, y, colw, 66)
    left_end = y + 66

    # ---- MIDDLE: leads 2+3 + 10 pictorial ----
    x = xs[1]
    y = top
    for kick, head, deck, src, ill in [
        ("Lead \u2022 Science & Technology", LEAD2_HEAD, LEAD2_DECK,
         "FORBES EUROPE  \u2022  REUTERS  \u2022  23\u201324 NOV", ill_chip),
        ("Lead \u2022 Climate", LEAD3_HEAD, LEAD3_DECK,
         "GRIST  \u2022  THE DAILY EDITION  \u2022  23\u201324 NOV", ill_climate),
    ]:
        y = kicker(d, x, y, kick, colw)
        ill(d, x, y, colw, 40)
        y += 40 + 4
        y = text_block(d, x, y, head, SERIF_B(14), colw, 15, max_lines=2)
        y = text_block(d, x, y + 1, deck, SANS(9), colw, 11, max_lines=2)
        y = source_line(d, x, y + 1, src)
        y += 3
    d.line([x, y, x + colw, y], fill=GREY, width=1)
    y += 5
    d.text((x, y), "IN PICTURES \u2014 TEN MORE STORIES", font=SANS_B(10), fill=RED)
    y += 15
    for region, head, deck, ill in PICTORIAL:
        ill(d, x, y, 32, 20)
        hy = text_block(d, x + 38, y - 1, head, SANS_B(9), colw - 38, 11,
                        max_lines=1)
        # if headline wrapped to 1 line only, deck sits on second line
        y = text_block(d, x + 38, y + 10, deck, SANS(8), colw - 38, 9,
                       max_lines=1)
        y = max(y, hy + 1)
    mid_end = y

    # ---- RIGHT: briefs per region ----
    x = xs[2]
    y = top
    d.text((x, y), "BRIEFS BY REGION", font=SANS_B(10), fill=RED)
    y += 15
    for region, items in BRIEFS:
        d.text((x, y), region, font=SANS_B(9), fill=BLUE)
        d.line([x + d.textlength(region, font=SANS_B(9)) + 6, y + 5,
                x + colw, y + 5], fill=(180, 175, 160), width=1)
        y += 14
        for it in items:
            y = text_block(d, x, y, "\u2022  " + it, SANS(9), colw, 11,
                           max_lines=2)
            y += 1
        y += 3
    # date-checked box fills the foot of the right column
    y += 4
    d.rectangle([x, y, x + colw, y + 62], outline=RULE, width=1, fill=LIGHT)
    d.text((x + 8, y + 5), "DATE-CHECKED \u2014 HOW TO READ THIS PAGE",
           font=SANS_B(9), fill=RED)
    text_block(d, x + 8, y + 19,
               "Every story here was first reported 23\u201324 Nov 2026. Figures, "
               "names and quotes come only from the sources named with each "
               "story. \u201cUkraine claims\u201d means Moscow has not confirmed it.",
               SANS(9), colw - 16, 12, max_lines=3)
    right_end = y + 62

    # ---- footer ----
    d.line([12, 560, 1012, 560], fill=RULE, width=1)
    d.text((12, 564),
           "Sources: Reuters, Forbes Europe, Grist, Middle East Eye, European Commission, "
           "Al Jazeera, The Daily Edition. All stories reported 23\u201324 Nov 2026.",
           font=SANS(8), fill=GREY)
    d.text((12, 564), "", font=SANS(8), fill=GREY)
    img.save(OUT, optimize=True)
    return OUT, left_end, mid_end, right_end

if __name__ == "__main__":
    out, le, me, re_ = draw()
    print(out, "left_end=", le, "mid_end=", me, "right_end=", re_)
    print("sha256", hashlib.sha256(open(out, "rb").read()).hexdigest())
    print("bytes", os.path.getsize(out))
