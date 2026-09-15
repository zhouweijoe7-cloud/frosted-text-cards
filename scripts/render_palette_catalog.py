#!/usr/bin/env python3
"""Render one representative card for every built-in palette."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw

import render_cards as cards


SAMPLE_CARD = {
    "id": "04",
    "slug": "same-key",
    "eyebrow": "04 / 剪辑技巧",
    "headline": "同调衔接",
    "support": "拼接多首 BGM，优先选择相同调性的音乐",
    "keywords": ["BGM", "同调"],
    "english_anchor": "SAME KEY",
    "metadata": "KEY / B",
    "layout": "L01",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    cols = 4
    thumb_w, thumb_h = 270, 338
    gap_x, gap_y = 28, 58
    top = 100
    palette_ids = sorted(cards.PALETTES)
    rows = math.ceil(len(palette_ids) / cols)
    sheet_w = cols * thumb_w + (cols + 1) * gap_x
    sheet_h = top + rows * (thumb_h + gap_y) + 24
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (20, 23, 27, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((gap_x, 30), "FROSTED TEXT CARDS / PALETTE CATALOG", font=cards.font("latin", 30), fill=(239, 242, 242, 240))

    for index, palette_id in enumerate(palette_ids):
        cards.PAL = cards.PALETTES[palette_id]
        image, outer = cards.layout_l01(SAMPLE_CARD, 2400 + index * 53)
        image = cards.finalize(image, outer)
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = gap_x + (index % cols) * (thumb_w + gap_x)
        y = top + (index // cols) * (thumb_h + gap_y)
        sheet.alpha_composite(image, (x, y))
        label_color = (239, 242, 242, 230)
        draw.text((x, y + thumb_h + 12), palette_id, font=cards.font("latin", 24), fill=label_color)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, "PNG", optimize=True)
    print(args.output)


if __name__ == "__main__":
    main()
