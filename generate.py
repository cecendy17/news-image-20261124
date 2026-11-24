#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261124 (Variant A).

Front-page newspaper, three layers: masthead, 3 big illustrated leads,
UTC timeline strip, 10 illustrated stories, 23 briefs grouped by 7 regions,
mini world map + markets box. Pure stdlib + PIL, fully deterministic,
no network. All facts come from news-dossier-24-nov.md only.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 576
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FDIR = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

F_TITLE  = F("DejaVuSerif-Bold.ttf", 27)
F_DATE   = F("DejaVuSans-Bold.ttf", 11)
F_CHIP   = F("DejaVuSans-Bold.ttf", 10)
F_KICK   = F("DejaVuSans-Bold.ttf", 9)
F_LEAD   = F("DejaVuSerif-Bold.ttf", 15)
F_BODY   = F("DejaVuSans.ttf", 10)
F_SRC    = F("DejaVuSans.ttf", 8)
F_SECT   = F("DejaVuSans-Bold.ttf", 10)
F_ILL    = F("DejaVuSans-Bold.ttf", 10)
F_ILLB   = F("DejaVuSans.ttf", 9)
F_BRIEF  = F("DejaVuSans-Bold.ttf", 10)
F_TL_T   = F("DejaVuSans-Bold.ttf", 9)
F_TL     = F("DejaVuSans.ttf", 9)
F_MAPT   = F("DejaVuSans-Bold.ttf", 9)
F_MKT    = F("DejaVuSans.ttf", 9)
F_MKTB   = F("DejaVuSans-Bold.ttf", 9)
F_FOOT   = F("DejaVuSans.ttf", 8)

PAPER   = (247, 243, 232)
INK     = (20, 20, 20)
RED     = (178, 34, 34)
GRAY    = (110, 105, 95)
LGRAY   = (200, 194, 182)
BLUE    = (31, 78, 121)
SKY     = (168, 205, 225)
SEA     = (46, 111, 148)
GREEN   = (46, 125, 50)

# ---------------------------------------------------------------- data ----
LEADS = [
    dict(kicker="EUROPE  \u2022  MEDITERRANEAN",
         head="Ukraine claims it sank a Russian corvette in Libya",
         body=("Seven sea drones hit the Merkury at Benghazi, Kyiv says. "
               "Moscow has not confirmed; the UN wants an inquiry."),
         src="Middle East Eye  \u2022  Reuters  \u2022  23 Nov", art="ship"),
    dict(kicker="TECHNOLOGY  \u2022  MARKETS",
         head="Jensen Huang is Nvidia CEO again \u2014 markets roar",
         body=("Shares jumped about 31% to $164.34 after the board\u2019s unanimous "
               "vote. Asia rallied, led by the Nikkei and the Kospi."),
         src="Forbes Europe  \u2022  Reuters  \u2022  23\u201324 Nov", art="chip"),
    dict(kicker="CLIMATE  \u2022  ANTALYA",
         head="COP31 collapses with no deal",
         body=("Talks ran about 50 hours over, then fell apart as 90+ nations "
               "rejected a draft that never named fossil fuels."),
         src="Grist  \u2022  The Daily Edition  \u2022  23\u201324 Nov", art="climate"),
]

ILLUSTRATED = [
    ("EU unveils 22nd sanctions package on Russia",
     "60 banks, 70+ ships targeted.",
     "European Commission  \u2022  23 Nov", "eu"),
    ("Russia strikes Zaporizhzhia overnight",
     "2 killed, 22 hurt, incl. 2 children.",
     "Reuters  \u2022  24 Nov", "blast"),
    ("Israeli strikes in Gaza kill at least 3",
     "Dead include an UNRWA staffer.",
     "Al Jazeera  \u2022  24 Nov", "rubble"),
    ("Three tankers hit by mines in Strait of Hormuz",
     "Blasts reported amid a US escort.",
     "IQMIA  \u2022  24 Nov", "tanker"),
    ("Magnitude 5.6 quake shakes Nepal\u2019s Koshi",
     "Near the border with China.",
     "Horizon  \u2022  24 Nov", "quake"),
    ("Tiangong opens to its first foreign astronaut",
     "Zeeshan Ali of Pakistan aboard.",
     "Straits Times  \u2022  24 Nov", "rocket"),
    ("Alcaraz wins his first ATP Finals title",
     "Beats Zverev in Turin.",
     "CareerIndia  \u2022  24 Nov", "tennis"),
    ("BepiColombo enters orbit around Mercury",
     "An 8-year journey ends.",
     "govjobs digest", "planet"),
    ("Trump\u2013Putin talks end after 40 minutes",
     "No deal; guarantees discussed.",
     "Washington Post via Meduza", "talks"),
    ("Novoshakhtinsk refinery shuts after drone attack",
     "14 refineries hit in November.",
     "Bloomberg", "refinery"),
]

# (region, headline, source) — 23 briefs
BRIEFS = [
    ("EUROPE", "Russia warns Estonia it is \u201con verge of triggering open war\u201d",
     "Russian media"),
    ("EUROPE", "Report: \u201cSputnik-S\u201d satellite could carry nukes to space",
     "The Daily Feeder / NATO"),
    ("EUROPE", "Polish air defences active as Russian drones cross border",
     "The Conversation"),
    ("EUROPE", "Ukraine, Germany agree first batch of extra interceptor missiles",
     "en.h.ua  \u2022  24 Nov"),
    ("MIDDLE EAST", "Trump warns of \u201cvery traumatic\u201d result if Iran nuclear deal fails",
     "Access24"),
    ("MIDDLE EAST", "Houthis report dozens killed in Saudi air strikes on Yemen",
     "Horizon"),
    ("MIDDLE EAST", "14 nations back ICJ ruling on Myanmar\u2019s Rohingya genocide",
     "Horizon  \u2022  23\u201324 Nov"),
    ("ASIA", "Huge fire at Indonesian industrial plant; workers missing",
     "CareerIndia  \u2022  24 Nov"),
    ("ASIA", "India holds No. 3 in Asia Power Index; exports hit record $89.99bn",
     "govjobs digest"),
    ("ASIA", "Indian astronomers find rare fossil star HE 1153\u22120518",
     "PIB via govjobs"),
    ("ASIA", "Trump announces Japan trade deal; SoftBank invests $2bn in Intel",
     "Access24"),
    ("ASIA", "Thailand\u2013Cambodia border fighting halted after ceasefire",
     "Access24"),
    ("AMERICAS", "Oregon and Virginia sue SpaceX over alleged Grok abuse images",
     "IQMIA"),
    ("AMERICAS", "Senate to vote on Trump\u2019s $9.4bn foreign aid and media cuts",
     "Access24"),
    ("AMERICAS", "Democrats win historic majority in 2026 midterms",
     "News Media House"),
    ("AMERICAS", "NHTSA lets Zoox charge for driverless robotaxis",
     "presentofai  \u2022  24 Nov"),
    ("AMERICAS", "Amazon buys Decart AI for about $7.5bn; Tesla launches FSD v15",
     "presentofai"),
    ("AFRICA", "Somalia and Uganda step up operations against Al-Shabaab",
     "IQMIA"),
    ("AFRICA", "School enrolment in Borno nearly doubles after conflict",
     "Al Jazeera"),
    ("SCIENCE & TECH", "Wolbachia mosquitoes cut dengue and chikungunya 69% in Brazil study",
     "govjobs digest"),
    ("SCIENCE & TECH", "UN chief Guterres wants AI risk framework within a year",
     "Horizon  \u2022  24 Nov"),
    ("SPORT", "Gukesh begins defence of world chess title vs Sindarov in Geneva",
     "govjobs digest"),
    ("SPORT", "India\u2013New Zealand Test in Wellington ends in a draw",
     "CareerIndia"),
]

TIMELINE = [
    ("00:00", "Nepal quake 5.6; Indonesia factory fire reported"),
    ("04:00", "Russia strikes Zaporizhzhia: 2 killed, 22 hurt"),
    ("07:55", "Forbes: why Jensen Huang and Nvidia matter"),
    ("09:33", "Stoxx 600 +0.73% as tech rebounds"),
    ("10:50", "Asia rallies: Nikkei +3.91%, Kospi +6%"),
    ("11:38", "US blacklists Alibaba unit and Megaspeed"),
]

MARKETS = [
    ("NVIDIA", "+31%", "$164.34"),
    ("SK HYNIX ADR", "+20%", "$124.28"),
    ("KOSPI", "+6%+", ""),
    ("NIKKEI", "+3.91%", ""),
    ("STOXX 600", "+0.73%", ""),
]

REGIONS = ["EUROPE", "MIDDLE EAST", "ASIA", "AMERICAS", "AFRICA",
           "SCIENCE & TECH", "SPORT"]

# ------------------------------------------------------------- helpers ----
def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, max_w, max_lines, lh, fill=INK):
    lines = wrap(draw, text, font, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "\u2026", font=font) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh

def fit1(draw, text, font, max_w):
    """Truncate text to a single line that fits max_w."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "\u2026", font=font) > max_w:
        text = text[:-1]
    return text + "\u2026"

def rule(draw, x0, x1, y, w=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)

# ------------------------------------------------- procedural art ---------
def art_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(28, 74, 102))
    # sun, top right
    d.ellipse([x + w - 48, y + 3, x + w - 28, y + 23], fill=(255, 190, 60))
    d.ellipse([x + w - 42, y + 9, x + w - 34, y + 17], fill=(255, 120, 40))
    # sea drones: three white dots
    for dx, dy in ((150, 10), (205, 7), (250, 14)):
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=(240, 240, 230))
    # corvette hull + mast, all inside the box
    d.polygon([(x + 16, y + h - 10), (x + 50, y + h - 10), (x + 58, y + h - 22),
               (x + 24, y + h - 22)], fill=(60, 60, 64))
    d.rectangle([x + 28, y + 8, x + 32, y + h - 22], fill=(60, 60, 64))
    d.rectangle([x + 32, y + 12, x + 48, y + 16], fill=(60, 60, 64))
    # explosion flash above the hull
    d.polygon([(x + 92, y + h - 22), (x + 98, y + h - 30), (x + 104, y + h - 22)],
              fill=(255, 120, 40))

def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 44))
    for i in range(4):
        d.line([(x + 8, y + 10 + i * 8), (x + 40, y + 10 + i * 8)], fill=(90, 160, 90), width=2)
        d.line([(x + w - 40, y + 10 + i * 8), (x + w - 8, y + 10 + i * 8)], fill=(90, 160, 90), width=2)
    d.rectangle([x + 44, y + 7, x + w - 44, y + h - 7], fill=(34, 120, 70), outline=(120, 220, 140), width=2)
    d.rectangle([x + 58, y + 14, x + w - 58, y + h - 14], outline=(180, 240, 190), width=1)
    d.text((x + w // 2 - 30, y + h - 16), "NVIDIA", font=F_CHIP, fill=(255, 255, 255))
    pts = [(x + 8, y + h - 9), (x + 60, y + h - 22), (x + 110, y + h - 15),
           (x + 170, y + h - 28), (x + 230, y + h - 24), (x + w - 10, y + 9)]
    d.line(pts, fill=(255, 200, 60), width=3)
    d.ellipse([x + w - 15, y + 3, x + w - 4, y + 14], fill=(255, 200, 60))
    d.text((x + 8, y + 3), "+31%", font=F_CHIP, fill=(255, 200, 60))

def art_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    # globe, left, sized to the box height
    gd = int(h * 0.76)
    gx, gy = x + 18, y + (h - gd) // 2
    d.ellipse([gx, gy, gx + gd, gy + gd], fill=(90, 140, 180))
    d.ellipse([gx + 5, gy + 6, gx + 16, gy + 14], fill=(120, 170, 110))
    d.ellipse([gx + 12, gy + 15, gx + 22, gy + 22], fill=(120, 170, 110))
    # summit buildings, right, bases on the box bottom
    base = y + h - 5
    bx = x + 110
    for i, bh in enumerate((14, 18, 12, 16)):
        b0 = bx + i * 44
        d.rectangle([b0, base - bh, b0 + 34, base], fill=(150, 120, 80))
        d.rectangle([b0 + 6, base - bh + 4, b0 + 12, base - bh + 10], fill=(232, 214, 170))
        d.rectangle([b0 + 20, base - bh + 4, b0 + 26, base - bh + 10], fill=(232, 214, 170))
    d.rectangle([bx - 6, base, x + w - 16, base + 3], fill=(120, 90, 60))
    d.text((x + w - 96, y + 3), "NO DEAL", font=F_CHIP, fill=RED)
    d.line([(x + w - 96, y + 16), (x + w - 16, y + 16)], fill=RED, width=2)

def art_box(d, x, y, w, h, kind):
    """Small ~38x38 procedural illustration."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216), outline=LGRAY)
    c = (x + w // 2, y + h // 2)
    if kind == "eu":
        d.ellipse([x + 6, y + 6, x + w - 6, y + h - 6], fill=BLUE)
        for i in range(8):
            a = math.pi * i / 4
            sx, sy = c[0] + int(10 * math.cos(a)), c[1] + int(10 * math.sin(a))
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 215, 0))
    elif kind == "blast":
        d.polygon([(c[0], y + 4), (c[0] + 5, c[1] - 6), (c[0] + 13, c[1] - 7),
                   (c[0] + 7, c[1]), (c[0] + 13, c[1] + 7), (c[0] + 4, c[1] + 6),
                   (c[0], y + h - 4), (c[0] - 4, c[1] + 6), (c[0] - 13, c[1] + 7),
                   (c[0] - 7, c[1]), (c[0] - 13, c[1] - 7), (c[0] - 5, c[1] - 6)],
                  fill=(255, 150, 40))
        d.ellipse([c[0] - 5, c[1] - 5, c[0] + 5, c[1] + 5], fill=RED)
    elif kind == "rubble":
        d.rectangle([x + 6, y + 20, x + w - 6, y + h - 4], fill=(140, 130, 115))
        d.polygon([(x + 6, y + 20), (x + 18, y + 7), (x + 30, y + 20)], fill=(170, 160, 140))
        d.line([(x + 10, y + 24), (x + 24, y + 13)], fill=RED, width=2)
        d.line([(x + 24, y + 13), (x + 32, y + 24)], fill=RED, width=2)
    elif kind == "tanker":
        d.rectangle([x, y + 22, x + w, y + h - 4], fill=SEA)
        d.polygon([(x + 5, y + 15), (x + 14, y + 15), (x + 33, y + 15), (x + 29, y + 22),
                   (x + 8, y + 22)], fill=(60, 60, 64))
        d.rectangle([x + 21, y + 7, x + 27, y + 15], fill=(60, 60, 64))
        d.ellipse([x + 27, y + 24, x + 35, y + 32], fill=(255, 150, 40))
    elif kind == "quake":
        d.polygon([(x + 4, y + h - 6), (x + 12, y + 11), (x + 20, y + h - 6)], fill=(120, 110, 95))
        d.polygon([(x + 16, y + h - 6), (x + 26, y + 5), (x + 36, y + h - 6)], fill=(150, 140, 120))
        d.line([(x + 4, y + 7), (x + 14, y + 13), (x + 22, y + 7), (x + 32, y + 13)],
               fill=RED, width=2)
    elif kind == "rocket":
        d.polygon([(c[0], y + 4), (c[0] + 5, y + 15), (c[0] + 5, y + 24),
                   (c[0], y + 28), (c[0] - 5, y + 24), (c[0] - 5, y + 15)], fill=(220, 220, 225))
        d.polygon([(c[0] - 5, y + 20), (c[0] - 10, y + 28), (c[0] - 5, y + 26)], fill=RED)
        d.polygon([(c[0] + 5, y + 20), (c[0] + 10, y + 28), (c[0] + 5, y + 26)], fill=RED)
        d.polygon([(c[0] - 3, y + 28), (c[0], y + h - 4), (c[0] + 3, y + 28)], fill=(255, 150, 40))
        d.ellipse([x + 4, y + 4, x + 12, y + 12], fill=(255, 215, 0))
    elif kind == "tennis":
        d.ellipse([x + 6, y + 6, x + w - 6, y + h - 6], fill=(180, 210, 60))
        d.arc([x + 6, y + 6, x + w - 6, y + h - 6], 200, 340, fill=(255, 255, 255), width=2)
        d.arc([x + 6, y + 6, x + w - 6, y + h - 6], 20, 160, fill=(255, 255, 255), width=2)
    elif kind == "planet":
        d.ellipse([x + 6, y + 7, x + w - 6, y + h - 7], fill=(170, 120, 80))
        for dx, dy, r in ((12, 11, 3), (23, 20, 2), (15, 24, 2)):
            d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(120, 80, 55))
        d.ellipse([x + 27, y + 4, x + 33, y + 10], fill=(255, 220, 120))
    elif kind == "talks":
        d.ellipse([x + 8, y + 9, x + 18, y + 19], fill=(60, 60, 64))
        d.ellipse([x + 21, y + 9, x + 31, y + 19], fill=(60, 60, 64))
        d.arc([x + 6, y + 17, x + 20, y + 31], 180, 360, fill=(60, 60, 64), width=2)
        d.arc([x + 19, y + 17, x + 33, y + 31], 180, 360, fill=(60, 60, 64), width=2)
        d.line([(x + 12, y + 25), (x + 27, y + 25)], fill=RED, width=2)
    elif kind == "refinery":
        d.rectangle([x + 6, y + 19, x + w - 6, y + h - 4], fill=(140, 130, 115))
        d.rectangle([x + 10, y + 7, x + 14, y + 19], fill=(100, 95, 85))
        d.rectangle([x + 20, y + 11, x + 24, y + 19], fill=(100, 95, 85))
        d.polygon([(x + 10, y + 7), (x + 12, y + 2), (x + 14, y + 7)], fill=(255, 150, 40))
        d.polygon([(x + 20, y + 11), (x + 22, y + 5), (x + 24, y + 11)], fill=(255, 120, 40))

# ------------------------------------------------------------- world map ---
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
           (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-80, 32), (-85, 25),
           (-95, 20), (-105, 22), (-115, 30), (-125, 40), (-125, 48), (-140, 60), (-165, 60)],
    "SA": [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-50, -30),
           (-60, -40), (-70, -50), (-75, -40), (-80, -20), (-80, -5)],
    "EU": [(-10, 36), (0, 40), (10, 44), (20, 45), (30, 45), (40, 47),
           (30, 55), (20, 58), (10, 58), (5, 55), (0, 50), (-5, 48), (-10, 43)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
           (35, 28), (40, 15), (48, 10), (51, 0), (40, -10), (35, -20),
           (30, -30), (20, -35), (15, -25), (12, -15), (9, -5), (9, 5), (-5, 5), (-15, 10)],
    "AS": [(40, 47), (50, 50), (60, 55), (70, 60), (80, 70), (90, 75),
           (110, 75), (130, 72), (150, 70), (170, 67), (180, 65), (160, 60),
           (150, 55), (140, 45), (130, 40), (120, 35), (110, 25), (105, 15),
           (100, 10), (95, 15), (90, 20), (80, 15), (75, 10), (70, 20),
           (60, 25), (50, 30), (45, 40)],
    "OC": [(113, -22), (125, -15), (135, -12), (142, -15), (150, -22),
           (150, -30), (140, -38), (130, -32), (120, -35), (113, -30)],
}
# (lon, lat) of story places
MAP_DOTS = [(20, 32), (30, 37), (35, 32), (56, 26), (85, 28), (8, 46),
            (175, -41), (103, 1), (139, 35)]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238), outline=LGRAY)
    def px(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (90 - lat) / 150 * h)
    for pts in CONTINENTS.values():
        d.polygon([px(lon, lat) for lon, lat in pts], fill=(96, 128, 110))
    for lon, lat in MAP_DOTS:
        dx, dy = px(lon, lat)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=RED, outline=(255, 255, 255))
    d.text((x + 5, y + 4), "WORLD AT A GLANCE", font=F_MAPT, fill=INK)
    d.text((x + 5, y + h - 12), "Red dots mark today\u2019s datelines.", font=F_FOOT, fill=GRAY)

# --------------------------------------------------------------- build -----
# Vertical budget (576 total):
#   masthead 0-50 | leads 52-169 | timeline 171-215
#   illustrated 217-315 | briefs 317-572
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 8

    # ---- masthead (0-50) ----
    d.text((W // 2, 3), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=INK, anchor="ma")
    rule(d, MX, W - MX, 36, 2)
    d.text((MX, 40), "TUESDAY, 24 NOVEMBER 2026", font=F_DATE, fill=INK)
    d.text((W // 2, 40), "WORLD EDITION", font=F_DATE, fill=GRAY, anchor="ma")
    chip = "36 STORIES  \u2022  DATE-CHECKED"
    cw = d.textlength(chip, font=F_CHIP) + 16
    d.rounded_rectangle([W - MX - cw, 38, W - MX, 56], radius=3, fill=RED)
    d.text((W - MX - cw + 8, 41), chip, font=F_CHIP, fill=(255, 255, 255))
    rule(d, MX, W - MX, 60, 2)

    # ---- 3 leads (62-169) ----
    ly, colw, gap = 64, 328, 12
    art = {"ship": art_ship, "chip": art_chip, "climate": art_climate}
    lead_bottom = ly
    for i, lead in enumerate(LEADS):
        x0 = MX + i * (colw + gap)
        d.text((x0, ly), lead["kicker"], font=F_KICK, fill=RED)
        y = para(d, x0, ly + 12, lead["head"], F_LEAD, colw, 2, 17)
        ay = y + 3
        art[lead["art"]](d, x0, ay, colw, 34)
        by = ay + 34 + 4
        para(d, x0, by, lead["body"], F_BODY, colw, 2, 11)
        d.text((x0, by + 23), lead["src"], font=F_SRC, fill=GRAY)
        lead_bottom = max(lead_bottom, by + 32)
        if i < 2:
            d.line([(x0 + colw + 6, ly), (x0 + colw + 6, by + 32)], fill=LGRAY)
    rule(d, MX, W - MX, lead_bottom + 4, 1)

    # ---- timeline strip (171-215) ----
    ty = lead_bottom + 8
    d.text((MX, ty), "TUESDAY IN UTC", font=F_SECT, fill=RED)
    tx = MX + 128
    seg = (W - MX - tx) / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = tx + i * seg
        d.text((cx, ty), t, font=F_TL_T, fill=INK)
        d.ellipse([cx + 2, ty + 14, cx + 8, ty + 20], fill=RED)
        if i:
            d.line([(cx - seg + 8, ty + 17), (cx + 2, ty + 17)], fill=LGRAY, width=2)
        para(d, cx, ty + 23, txt, F_TL, seg - 8, 2, 10)
    tl_bottom = ty + 44
    rule(d, MX, W - MX, tl_bottom, 1)

    # ---- illustrated stories: 2 rows x 5 (217-315) ----
    iy = tl_bottom + 4
    d.text((MX, iy), "MORE TOP STORIES", font=F_SECT, fill=INK)
    rule(d, MX + 130, W - MX, iy + 6, 1, fill=LGRAY)
    iw = (W - 2 * MX - 4 * 8) / 5
    row_h, row_gap = 38, 2
    for idx, (head, sub, src, kind) in enumerate(ILLUSTRATED):
        r, c = divmod(idx, 5)
        x0 = MX + c * (iw + 8)
        y0 = iy + 12 + r * (row_h + row_gap)
        art_box(d, x0, y0, 36, 36, kind)
        tx0 = x0 + 42
        tw = iw - 42
        para(d, tx0, y0, head, F_ILL, tw, 2, 10.5)
        d.text((tx0, y0 + 22), fit1(d, sub, F_ILLB, tw), font=F_ILLB, fill=GRAY)
        d.text((tx0, y0 + 31), fit1(d, src, F_SRC, tw), font=F_SRC, fill=GRAY)
    ill_bottom = iy + 12 + 2 * row_h + row_gap
    rule(d, MX, W - MX, ill_bottom + 2, 1)

    # ---- briefs grid (317-572) ----
    by = ill_bottom + 6
    d.text((MX, by), "THE DAY IN BRIEF", font=F_SECT, fill=INK)
    rule(d, MX + 118, W - MX, by + 6, 1, fill=LGRAY)
    cols = [
        (8,   248, ["EUROPE", "MIDDLE EAST"]),
        (264, 248, ["ASIA", "AFRICA"]),
        (520, 248, ["AMERICAS", "SCIENCE & TECH"]),
        (776, 240, ["SPORT"]),
    ]
    briefs_by_region = {r: [b for b in BRIEFS if b[0] == r] for r in REGIONS}
    y = by + 12
    col_bottom = {}
    for (x0, cw, regs) in cols:
        cy = y
        for reg in regs:
            d.text((x0, cy), reg, font=F_KICK, fill=RED)
            cy += 11
            for (_, head, src) in briefs_by_region[reg]:
                cy = para(d, x0, cy, head, F_BRIEF, cw, 2, 9.5)
                d.text((x0, cy), fit1(d, src, F_SRC, cw), font=F_SRC, fill=GRAY)
                cy += 8.5
            cy += 2
        col_bottom[x0] = cy
        if x0 != 776:
            d.line([(x0 + cw + 4, y), (x0 + cw + 4, 568)], fill=LGRAY)

    # ---- right rail (col 4): world map + markets ----
    map_y = col_bottom[776] + 4
    draw_map(d, 776, map_y, 240, 78)
    my = map_y + 78 + 6
    d.text((776, my), "MARKETS  \u2022  MONDAY 23 NOV", font=F_KICK, fill=RED)
    my += 12
    for name, chg, px in MARKETS:
        d.text((776, my), name, font=F_MKTB, fill=INK)
        d.text((1016, my), chg + (("  " + px) if px else ""), font=F_MKT, fill=GREEN, anchor="ra")
        my += 10
    rule(d, MX, W - MX, 572, 1)

    img.save(OUT, optimize=True)
    return OUT

if __name__ == "__main__":
    print(build())
