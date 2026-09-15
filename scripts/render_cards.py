#!/usr/bin/env python3
"""Render deterministic frosted text cards as RGBA PNG files."""

from __future__ import annotations

import argparse
import functools
import json
import math
import os
import random
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


W, H = 1080, 1350
PALETTES = {
    "P01": {"bg": (236, 231, 225, 236), "glass": (243, 237, 234, 168), "ink": (38, 42, 46, 242), "muted": (100, 106, 112, 215), "accent": (199, 123, 112, 230), "edge": (255, 255, 255, 180)},
    "P02": {"bg": (220, 231, 237, 236), "glass": (233, 241, 244, 168), "ink": (23, 36, 46, 242), "muted": (82, 99, 110, 215), "accent": (78, 120, 148, 230), "edge": (255, 255, 255, 180)},
    "P03": {"bg": (231, 229, 218, 236), "glass": (238, 240, 231, 168), "ink": (36, 48, 43, 242), "muted": (96, 106, 99, 215), "accent": (113, 135, 117, 230), "edge": (255, 255, 255, 180)},
    "P04": {"bg": (32, 27, 44, 236), "glass": (57, 49, 70, 168), "ink": (242, 238, 245, 242), "muted": (183, 171, 191, 210), "accent": (143, 115, 167, 230), "edge": (220, 210, 228, 170)},
    "P05": {"bg": (42, 33, 29, 236), "glass": (68, 53, 43, 168), "ink": (241, 232, 220, 242), "muted": (193, 174, 152, 210), "accent": (181, 123, 69, 230), "edge": (227, 212, 193, 170)},
    "P06": {"bg": (19, 40, 35, 236), "glass": (36, 64, 57, 168), "ink": (236, 243, 240, 242), "muted": (167, 187, 180, 210), "accent": (78, 139, 120, 230), "edge": (201, 219, 213, 170)},
    "P07": {"bg": (23, 23, 25, 236), "glass": (48, 48, 52, 168), "ink": (242, 242, 242, 242), "muted": (181, 181, 184, 210), "accent": (169, 78, 80, 230), "edge": (215, 215, 216, 170)},
    "P08": {"bg": (23, 33, 46, 236), "glass": (43, 56, 71, 168), "ink": (242, 238, 227, 242), "muted": (185, 179, 164, 210), "accent": (165, 138, 85, 230), "edge": (217, 209, 190, 170)},
    "P09": {"bg": (236, 237, 234, 236), "glass": (246, 246, 242, 168), "ink": (37, 40, 43, 242), "muted": (103, 108, 112, 215), "accent": (146, 153, 157, 230), "edge": (255, 255, 255, 180)},
    "P10": {"bg": (38, 41, 45, 236), "glass": (65, 69, 74, 168), "ink": (240, 241, 242, 242), "muted": (177, 180, 183, 210), "accent": (115, 122, 128, 230), "edge": (210, 213, 215, 170)},
    "P11": {"bg": (12, 13, 14, 236), "glass": (36, 38, 40, 168), "ink": (250, 250, 248, 246), "muted": (191, 194, 196, 215), "accent": (217, 221, 224, 235), "edge": (255, 255, 255, 185)},
    "P12": {"bg": (21, 26, 32, 236), "glass": (40, 49, 58, 168), "ink": (239, 242, 242, 242), "muted": (174, 183, 188, 205), "accent": (97, 116, 131, 230), "edge": (199, 210, 216, 165)},
}
PAL = PALETTES["P12"]

REPO_ROOT = Path(__file__).resolve().parents[1]
USER_FONT_DIR = Path.home() / "Library" / "Fonts"
WINDOWS_FONT_DIR = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
LOCAL_FONT_DIR = REPO_ROOT / "assets" / "fonts"

FONT_CANDIDATES = {
    "cn_bold": [
        os.environ.get("FROSTED_FONT_CN_BOLD"),
        LOCAL_FONT_DIR / "FrostedCNDisplay.ttf",
        USER_FONT_DIR / "Alimama_ShuHeiTi_Bold.ttf",
        USER_FONT_DIR / "AlibabaPuHuiTi-3-105-Heavy.ttf",
        USER_FONT_DIR / "AlibabaPuHuiTi-3-95-ExtraBold.ttf",
        USER_FONT_DIR / "SourceHanSansCN-Bold.otf",
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        WINDOWS_FONT_DIR / "msyhbd.ttc",
        WINDOWS_FONT_DIR / "simhei.ttf",
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"),
        Path("/usr/share/fonts/opentype/source-han-sans/SourceHanSansCN-Bold.otf"),
    ],
    "cn_regular": [
        os.environ.get("FROSTED_FONT_CN_BODY"),
        LOCAL_FONT_DIR / "FrostedCNBody.ttf",
        USER_FONT_DIR / "AlibabaPuHuiTi-3-75-SemiBold.ttf",
        USER_FONT_DIR / "AlibabaPuHuiTi-3-65-Medium.ttf",
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        WINDOWS_FONT_DIR / "msyh.ttc",
        WINDOWS_FONT_DIR / "simhei.ttf",
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    ],
    "latin": [
        os.environ.get("FROSTED_FONT_LATIN"),
        LOCAL_FONT_DIR / "FrostedLatin.ttf",
        USER_FONT_DIR / "Rajdhani-SemiBold.ttf",
        USER_FONT_DIR / "BarlowCondensed-SemiBold.ttf",
        Path("/System/Library/Fonts/HelveticaNeue.ttc"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        WINDOWS_FONT_DIR / "arialbd.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ],
    "latin_display": [
        os.environ.get("FROSTED_FONT_LATIN_DISPLAY"),
        LOCAL_FONT_DIR / "FrostedLatinDisplay.ttf",
        USER_FONT_DIR / "BarlowCondensed-ExtraBold.ttf",
        USER_FONT_DIR / "BarlowCondensed-Black.ttf",
        USER_FONT_DIR / "Rajdhani-Bold.ttf",
        Path("/System/Library/Fonts/HelveticaNeue.ttc"),
        WINDOWS_FONT_DIR / "arialbd.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"),
    ],
    "serif": [
        os.environ.get("FROSTED_FONT_SERIF"),
        LOCAL_FONT_DIR / "FrostedSerif.ttf",
        USER_FONT_DIR / "Lora.ttf",
        Path("/System/Library/Fonts/Supplemental/Georgia.ttf"),
        Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
        WINDOWS_FONT_DIR / "georgia.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
    ],
}


@functools.lru_cache(maxsize=None)
def font(kind: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES[kind]:
        if not candidate:
            continue
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    env_name = {
        "cn_bold": "FROSTED_FONT_CN_BOLD",
        "cn_regular": "FROSTED_FONT_CN_BODY",
        "latin": "FROSTED_FONT_LATIN",
        "latin_display": "FROSTED_FONT_LATIN_DISPLAY",
        "serif": "FROSTED_FONT_SERIF",
    }[kind]
    raise RuntimeError(f"No usable font found for {kind}. Set {env_name} to a licensed font file.")


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def fit_font(draw: ImageDraw.ImageDraw, text: str, kind: str, start: int, max_width: int, minimum: int = 34):
    size = start
    while size > minimum:
        candidate = font(kind, size)
        if text_width(draw, text, candidate) <= max_width:
            return candidate
        size -= 2
    return font(kind, minimum)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int, max_lines: int = 2):
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if current and text_width(draw, trial, fnt) > max_width:
            lines.append(current.rstrip())
            current = char.lstrip()
            if len(lines) == max_lines - 1:
                break
        else:
            current = trial
    consumed = sum(len(line) for line in lines)
    remaining = text[consumed:].strip() if lines else current
    if len(lines) < max_lines and remaining:
        while text_width(draw, remaining, fnt) > max_width and len(remaining) > 1:
            remaining = remaining[:-1]
        if consumed + len(remaining) < len(text):
            remaining = remaining.rstrip("，。；、 ") + "…"
        lines.append(remaining)
    return lines[:max_lines]


def clipped_alpha(layer: Image.Image, mask: Image.Image) -> Image.Image:
    layer = layer.copy()
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
    return layer


def rounded_mask(box: tuple[int, int, int, int], radius: int) -> Image.Image:
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    return mask


def polygon_mask(points: list[tuple[int, int]]) -> Image.Image:
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


def add_blob(img: Image.Image, box, color, blur: int = 90, mask: Image.Image | None = None):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(box, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    if mask is not None:
        layer = clipped_alpha(layer, mask)
    img.alpha_composite(layer)


def add_grain(img: Image.Image, mask: Image.Image, seed: int, amount: int = 5200):
    rng = random.Random(seed)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for _ in range(amount):
        x = rng.randrange(W)
        y = rng.randrange(H)
        alpha = rng.randrange(3, 13)
        shade = 235 if rng.random() > 0.42 else 35
        draw.point((x, y), fill=(shade, shade, shade, alpha))
    img.alpha_composite(clipped_alpha(layer, mask))


def base_canvas(seed: int) -> tuple[Image.Image, Image.Image]:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    outer = rounded_mask((30, 30, W - 30, H - 30), 54)
    base = Image.new("RGBA", (W, H), PAL["bg"])
    base.putalpha(ImageChops.multiply(base.getchannel("A"), outer))
    img.alpha_composite(base)
    add_blob(img, (560, 720, 1250, 1450), PAL["accent"][:3] + (92,), 130, outer)
    add_blob(img, (-260, 820, 420, 1480), PAL["ink"][:3] + (26,), 120, outer)
    add_grain(img, outer, seed)
    return img, outer


def glass_from_mask(img: Image.Image, mask: Image.Image, seed: int, edge_drawer):
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_mask = mask.filter(ImageFilter.GaussianBlur(28))
    shadow.putalpha(shadow_mask.point(lambda p: int(p * 0.34)))
    shadow.paste((5, 8, 11, 115), (0, 0, W, H), shadow.getchannel("A"))
    img.alpha_composite(shadow)

    blurred = img.filter(ImageFilter.GaussianBlur(22))
    img.paste(blurred, (0, 0), mask)

    panel = Image.new("RGBA", (W, H), PAL["glass"])
    panel.putalpha(ImageChops.multiply(panel.getchannel("A"), mask))
    img.alpha_composite(panel)

    rng = random.Random(seed)
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grain_draw = ImageDraw.Draw(grain)
    for _ in range(1800):
        x = rng.randrange(W)
        y = rng.randrange(H)
        a = rng.randrange(4, 18)
        grain_draw.point((x, y), fill=(235, 240, 242, a))
    img.alpha_composite(clipped_alpha(grain, mask))

    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    edge_drawer(ImageDraw.Draw(edge))
    img.alpha_composite(edge)


def glass_rect(img: Image.Image, box, radius: int, seed: int):
    mask = rounded_mask(box, radius)

    def edge(draw):
        draw.rounded_rectangle(box, radius=radius, outline=PAL["edge"], width=2)
        x1, y1, x2, _ = box
        draw.line((x1 + radius, y1 + 2, x2 - radius, y1 + 2), fill=(255, 255, 255, 90), width=2)

    glass_from_mask(img, mask, seed, edge)


def glass_polygon(img: Image.Image, points: list[tuple[int, int]], seed: int):
    mask = polygon_mask(points)

    def edge(draw):
        draw.line(points + [points[0]], fill=PAL["edge"], width=2, joint="curve")

    glass_from_mask(img, mask, seed, edge)


def large_text(img: Image.Image, xy, text: str, size: int, color, kind: str = "latin_display", spacing: int = 0):
    draw = ImageDraw.Draw(img)
    draw.text(xy, text, font=font(kind, size), fill=color, spacing=spacing)


def draw_support(draw: ImageDraw.ImageDraw, text: str, xy, max_width: int, size: int = 47, max_lines: int = 2):
    fnt = font("cn_regular", size)
    lines = wrap_text(draw, text, fnt, max_width, max_lines)
    draw.multiline_text(xy, "\n".join(lines), font=fnt, fill=PAL["muted"], spacing=18)


def guide(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int, dot_at_end: bool = True):
    draw.line((x1, y, x2, y), fill=(174, 183, 188, 125), width=2)
    for x in range(x1, x2 + 1, 52):
        draw.line((x, y - 6, x, y + 6), fill=(174, 183, 188, 110), width=1)
    if dot_at_end:
        draw.ellipse((x2 - 7, y - 7, x2 + 7, y + 7), fill=PAL["accent"])


def layout_l01(card, seed: int):
    img, outer = base_canvas(seed)
    large_text(img, (-55, -35), "SAME", 285, PAL["ink"][:3] + (110,))
    large_text(img, (500, 1065), "B", 310, PAL["accent"][:3] + (210,))
    glass_rect(img, (125, 110, 955, 1240), 42, seed + 1)
    draw = ImageDraw.Draw(img)
    draw.text((185, 220), card["eyebrow"], font=font("cn_regular", 40), fill=PAL["muted"])
    title_font = fit_font(draw, card["headline"], "cn_bold", 116, 670)
    draw.text((185, 385), card["headline"], font=title_font, fill=PAL["ink"])
    draw.rounded_rectangle((185, 535, 320, 545), radius=5, fill=PAL["accent"])
    draw_support(draw, card["support"], (185, 620), 670, 48, 2)
    guide(draw, 185, 820, 925)
    draw.text((185, 1125), "OPAL FROST / 40% DIFFUSE", font=font("latin", 29), fill=PAL["muted"])
    draw.text((750, 1125), card["metadata"], font=font("latin", 31), fill=PAL["muted"])
    return img, outer


def layout_l03(card, seed: int):
    img, outer = base_canvas(seed)
    large_text(img, (-40, 35), card["english_anchor"].split()[0], 250, PAL["ink"][:3] + (96,))
    large_text(img, (250, 1080), "MUSIC", 225, PAL["accent"][:3] + (175,))
    glass_rect(img, (68, 430, 1012, 875), 34, seed + 2)
    draw = ImageDraw.Draw(img)
    draw.text((130, 495), card["eyebrow"], font=font("cn_regular", 40), fill=PAL["muted"])
    title_font = fit_font(draw, card["headline"], "cn_bold", 136, 810)
    draw.text((130, 585), card["headline"], font=title_font, fill=PAL["ink"])
    draw_support(draw, card["support"], (130, 750), 810, 46, 1)
    draw.text((70, 1260), card["metadata"], font=font("latin", 30), fill=PAL["muted"])
    return img, outer


def layout_l04(card, seed: int):
    img, outer = base_canvas(seed)
    large_text(img, (-30, 5), "A / B", 245, PAL["accent"][:3] + (185,))
    glass_rect(img, (255, 205, 970, 1025), 44, seed + 3)
    draw = ImageDraw.Draw(img)
    draw.text((585, 775), "异调 / 突兀", font=font("cn_regular", 44), fill=PAL["muted"])
    glass_rect(img, (95, 385, 835, 1250), 44, seed + 4)
    draw = ImageDraw.Draw(img)
    draw.text((155, 475), card["eyebrow"], font=font("cn_regular", 40), fill=PAL["muted"])
    title_font = fit_font(draw, card["headline"], "cn_bold", 102, 610)
    draw.text((155, 625), card["headline"], font=title_font, fill=PAL["ink"])
    draw.rounded_rectangle((155, 770, 300, 780), radius=5, fill=PAL["accent"])
    draw_support(draw, card["support"], (155, 850), 610, 46, 2)
    draw.text((155, 1140), "同调 / 连贯", font=font("cn_regular", 42), fill=PAL["ink"])
    return img, outer


def layout_l07(card, seed: int):
    img, outer = base_canvas(seed)
    draw = ImageDraw.Draw(img)
    head = fit_font(draw, "KEY DESIGN", "latin_display", 138, 860)
    draw.text((W // 2, 150), "KEY DESIGN", anchor="mm", font=head, fill=PAL["ink"][:3] + (150,))
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((320, 400, 800, 880), outline=PAL["accent"][:3] + (220,), width=110)
    img.alpha_composite(ring)
    folder = [(110, 670), (390, 670), (455, 610), (670, 610), (735, 670), (970, 670), (970, 1230), (110, 1230)]
    glass_polygon(img, folder, seed + 5)
    draw = ImageDraw.Draw(img)
    draw.text((170, 750), card["eyebrow"], font=font("cn_regular", 39), fill=PAL["muted"])
    draw.text((830, 735), "↗", font=font("cn_regular", 62), fill=PAL["muted"])
    title_font = fit_font(draw, card["headline"], "cn_bold", 112, 690)
    draw.text((170, 900), card["headline"], font=title_font, fill=PAL["ink"])
    draw_support(draw, card["support"], (170, 1055), 690, 44, 2)
    draw.text((170, 1175), card["metadata"], font=font("latin", 29), fill=PAL["muted"])
    return img, outer


def layout_l08(card, seed: int):
    img, outer = base_canvas(seed)
    add_blob(img, (280, 1040, 800, 1430), PAL["ink"][:3] + (135,), 80, outer)
    silhouette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(silhouette)
    sd.ellipse((440, 260, 640, 460), fill=PAL["accent"][:3] + (120,))
    sd.rounded_rectangle((335, 425, 745, 890), radius=130, fill=PAL["accent"][:3] + (100,))
    silhouette = silhouette.filter(ImageFilter.GaussianBlur(34))
    img.alpha_composite(clipped_alpha(silhouette, outer))
    glass_rect(img, (250, 65, 830, 1285), 10, seed + 6)
    draw = ImageDraw.Draw(img)
    draw.line((330, 665, 485, 665), fill=PAL["muted"], width=2)
    draw.line((330, 665, 330, 830), fill=PAL["muted"], width=2)
    draw.line((595, 665, 750, 665), fill=PAL["muted"], width=2)
    draw.line((750, 665, 750, 830), fill=PAL["muted"], width=2)
    draw.text((330, 700), card["eyebrow"], font=font("cn_regular", 36), fill=PAL["muted"])
    title_font = fit_font(draw, card["headline"], "cn_bold", 102, 430)
    draw.text((330, 790), card["headline"], font=title_font, fill=PAL["ink"])
    draw_support(draw, card["support"], (330, 925), 420, 40, 2)
    guide(draw, 330, 750, 1090, False)
    draw.text((330, 1130), card["metadata"], font=font("latin", 29), fill=PAL["muted"])
    return img, outer


def layout_l09(card, seed: int):
    img, outer = base_canvas(seed)
    texture = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(texture)
    for i in range(35):
        pad = i * 22 - 130
        color = (174, 183, 188, max(12, 78 - i))
        td.ellipse((pad - 210, pad - 70, 780 - pad // 4, 970 - pad // 5), outline=color, width=3)
        td.ellipse((410 + pad // 5, 350 + pad // 5, 1260 - pad, 1320 - pad), outline=PAL["accent"][:3] + (max(10, 70 - i),), width=3)
    texture = texture.filter(ImageFilter.GaussianBlur(1.2))
    img.alpha_composite(clipped_alpha(texture, outer))
    glass_rect(img, (520, 300, 1000, 530), 8, seed + 7)
    glass_rect(img, (80, 690, 650, 930), 8, seed + 8)
    draw = ImageDraw.Draw(img)
    draw.rectangle((80, 360, 400, 430), fill=PAL["bg"][:3] + (232,))
    draw.text((105, 360), card["headline"], font=font("cn_bold", 52), fill=PAL["ink"])
    draw.rectangle((710, 120, 1000, 185), fill=PAL["ink"][:3] + (230,))
    draw.text((735, 130), "SAME KEY", font=font("latin", 34), fill=PAL["bg"][:3] + (245,))
    nodes = card.get("keywords", [])[:3]
    for index, node in enumerate(nodes):
        x = 130 + index * 295
        y = 1035
        draw.text((x, y), f"0{index + 1}", font=font("latin", 31), fill=PAL["accent"])
        draw.text((x, y + 48), node, font=font("cn_bold", 47), fill=PAL["ink"])
        if index < len(nodes) - 1:
            draw.line((x + 150, y + 77, x + 255, y + 77), fill=PAL["muted"], width=2)
    draw.text((80, 1230), card["metadata"], font=font("latin", 29), fill=PAL["muted"])
    return img, outer


def layout_l10(card, seed: int):
    img, outer = base_canvas(seed)
    large_text(img, (-45, 20), "KEY", 265, PAL["ink"][:3] + (115,), "serif")
    large_text(img, (-70, 520), "SAME", 245, PAL["accent"][:3] + (200,), "serif")
    large_text(img, (-35, 1110), "FLOW", 220, PAL["ink"][:3] + (90,), "serif")
    blur_word = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(blur_word)
    word_font = fit_font(bdraw, card["headline"], "cn_bold", 122, 570)
    bdraw.text((W // 2, 650), card["headline"], anchor="mm", font=word_font, fill=PAL["accent"][:3] + (235,))
    img.alpha_composite(blur_word.filter(ImageFilter.GaussianBlur(13)))
    glass_rect(img, (235, 105, 845, 1245), 16, seed + 9)
    drops = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(drops)
    rng = random.Random(seed + 10)
    for _ in range(150):
        x = rng.randint(255, 825)
        y = rng.randint(125, 1225)
        r = rng.randint(2, 7)
        dd.ellipse((x - r, y - r, x + r, y + r), fill=PAL["ink"][:3] + (rng.randint(35, 100),))
    img.alpha_composite(drops)
    draw = ImageDraw.Draw(img)
    draw.text((W // 2, 685), card["headline"], anchor="mm", font=fit_font(draw, card["headline"], "cn_bold", 76, 470), fill=PAL["ink"][:3] + (205,))
    draw_support(draw, card["support"], (315, 805), 450, 41, 2)
    draw.text((W // 2, 1130), card["metadata"], anchor="mm", font=font("latin", 29), fill=PAL["muted"])
    return img, outer


LAYOUTS = {
    "L01": layout_l01,
    "L03": layout_l03,
    "L04": layout_l04,
    "L07": layout_l07,
    "L08": layout_l08,
    "L09": layout_l09,
    "L10": layout_l10,
}


def finalize(img: Image.Image, outer: Image.Image) -> Image.Image:
    img.putalpha(ImageChops.multiply(img.getchannel("A"), outer))
    return img


def safe_slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    return cleaned or "card"


def make_contact_sheet(files: list[Path], output: Path, palette_id: str):
    thumb_w, thumb_h = 324, 405
    gap, top = 34, 70
    cols = 2
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGBA", (cols * thumb_w + (cols + 1) * gap, rows * (thumb_h + 55) + top), PAL["bg"][:3] + (255,))
    draw = ImageDraw.Draw(sheet)
    draw.text((gap, 22), f"{palette_id} / FROSTED TEXT CARDS", font=font("latin", 24), fill=PAL["ink"])
    for i, path in enumerate(files):
        card = Image.open(path).convert("RGBA")
        card.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = gap + (i % cols) * (thumb_w + gap)
        y = top + (i // cols) * (thumb_h + 55)
        checker = Image.new("RGBA", (thumb_w, thumb_h), (45, 51, 57, 255))
        cd = ImageDraw.Draw(checker)
        for yy in range(0, thumb_h, 24):
            for xx in range(0, thumb_w, 24):
                if (xx // 24 + yy // 24) % 2 == 0:
                    cd.rectangle((xx, yy, xx + 23, yy + 23), fill=(58, 65, 72, 255))
        checker.alpha_composite(card, ((thumb_w - card.width) // 2, 0))
        sheet.alpha_composite(checker, (x, y))
        draw.text((x, y + thumb_h + 12), path.stem.upper(), font=font("latin", 19), fill=PAL["muted"])
    sheet.save(output, "PNG", optimize=True)


def alpha_stats(path: Path):
    alpha = Image.open(path).convert("RGBA").getchannel("A")
    lo, hi = alpha.getextrema()
    histogram = alpha.histogram()
    mid = sum(histogram[1:255])
    return lo, hi, mid


def main():
    global PAL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--palette", choices=sorted(PALETTES), help="Override the series palette id")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    if not cards:
        raise SystemExit("No cards found in input JSON.")
    palette_id = args.palette or data.get("series", {}).get("palette", "P12")
    if palette_id not in PALETTES:
        raise SystemExit(f"Unsupported palette: {palette_id}")
    PAL = PALETTES[palette_id]
    args.output.mkdir(parents=True, exist_ok=True)

    rendered: list[Path] = []
    for index, card in enumerate(cards, start=1):
        layout = card.get("layout", "L01")
        if layout not in LAYOUTS:
            raise SystemExit(f"Unsupported layout: {layout}")
        image, outer = LAYOUTS[layout](card, 1200 + index * 37)
        image = finalize(image, outer)
        filename = f"{card.get('id', f'{index:02d}')}-{layout.lower()}-{safe_slug(card.get('slug', 'card'))}.png"
        target = args.output / filename
        image.save(target, "PNG", optimize=True)
        rendered.append(target)
        lo, hi, mid = alpha_stats(target)
        print(f"{target.name}: RGBA alpha={lo}..{hi}, translucent_pixels={mid}")

    make_contact_sheet(rendered, args.output / "contact-sheet.png", palette_id)
    print(f"Rendered {len(rendered)} cards with {palette_id} to {args.output}")


if __name__ == "__main__":
    main()
