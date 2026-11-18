#!/usr/bin/env python3
"""Render entry.png for make.fun competition news-image-20261118.

The single image that sums up the world news of Wednesday 18 November 2026.
Written as a plain-text source so the picture is reproducible:
    python3 tools/make_entry_image.py entry.png

The program that the grader runs is main.ts, which copies the PNG this script
produces to /output/entry.png.  Standard library plus Pillow for the offline
render only; nothing is needed at grading time.
"""

from __future__ import annotations

import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas ----

W = H = 1024
MARGIN = 36
GUTTER = 18

BG = (11, 18, 32)
CARD = (19, 30, 51)
CARD_EDGE = (36, 51, 77)
RED = (200, 16, 46)
WHITE = (255, 255, 255)
MUTED = (154, 167, 191)
AMBER = (245, 166, 35)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REGULAR = f"{FONT_DIR}/DejaVuSans.ttf"

# ------------------------------------------------------------- the news -----
# Each item: (place tag, headline, one line of detail, accent colour).
# Stories are the events of, or first reported on, 18 November 2026.

STORIES = [
    (
        "MANILA · ASIA-PACIFIC",
        "Quad leaders meet as ASEAN summit closes",
        "Trump and Marcos meet ahead of the APEC summit",
        (245, 166, 35),
    ),
    (
        "SHENZHEN · ASIA",
        "Putin arrives for APEC as Trump heads in",
        "A three-way Trump\u2013Xi\u2013Putin meeting is set for Thursday",
        (79, 163, 247),
    ),
    (
        "STRAIT OF HORMUZ · MIDDLE EAST",
        "US and Iran trade fresh strikes",
        "IRGC hits a US radar in Bahrain; US hits Qeshm Island",
        (228, 87, 46),
    ),
    (
        "KYIV · EUROPE",
        "Ukraine strikes the Kerch Bridge again",
        "Allies meet at NATO as Kyiv presses for air defence",
        (160, 108, 240),
    ),
    (
        "WALL STREET · ECONOMY",
        "Tech selloff deepens as Nvidia reels",
        "Stocks slide; traders bet on a December Fed rate rise",
        (63, 178, 127),
    ),
    (
        "WASHINGTON · HEALTH",
        "US loses measles elimination status",
        "First loss in 26 years after 5,400 cases this year",
        (232, 99, 143),
    ),
    (
        "ANTALYA · CLIMATE",
        "COP31 concedes 1.5C will be overshot",
        "Draft deal urges an accelerated exit from fossil fuels",
        (46, 196, 182),
    ),
    (
        "MAPUTO · AFRICA",
        "Opposition leader Mondlane goes on trial",
        "Court refuses to void five charges; hearing continues",
        (217, 180, 74),
    ),
]

ALSO_TODAY = [
    "GTA VI mania grips gamers, 13 years on",
    "Brazil's Senate votes on budget repair",
    "Ghana weighs El Ni\u00f1o risk to cocoa",
    "Ecuador crew sue the US over a strike at sea",
]


# ------------------------------------------------------------- helpers ------

def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_ls(draw: ImageDraw.ImageDraw, xy, s, f, fill, ls: float = 0.0) -> float:
    """Draw s with letter spacing ls; return the x after the last glyph."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + ls
    return x - ls


def ls_width(draw: ImageDraw.ImageDraw, s, f, ls: float = 0.0) -> float:
    if not s:
        return 0.0
    return sum(draw.textlength(ch, font=f) for ch in s) + ls * (len(s) - 1)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if draw.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, s, path, size, max_w, max_lines, floor=16):
    """Largest size <= size, >= floor, whose wrapped text fits max_lines."""
    while size >= floor:
        f = font(path, size)
        lines = wrap(draw, s, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font(path, floor)
    return f, wrap(draw, s, f, max_w)[:max_lines]


def block(draw, xy, lines, f, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


# --------------------------------------------------------------- render -----

def render() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead: a red rule, a kicker, then the date as the biggest thing here.
    d.rectangle([0, 0, W, 7], fill=RED)
    kick = font(BOLD, 25)
    text_ls(d, (MARGIN, 26), "WORLD NEWS IN ONE PICTURE  ·  WEDNESDAY", kick, AMBER, 2.0)

    date = font(BOLD, 72)
    d.text((MARGIN, 62), "18 NOVEMBER 2026", font=date, fill=WHITE)

    sub = font(REGULAR, 21)
    d.text((MARGIN, 148), "The day's news from every region, in a single image",
           font=sub, fill=MUTED)
    d.rectangle([0, 158, W, 161], fill=RED)

    # Eight story cards, two across and four down, with the footer pinned to
    # a fixed budget so nothing runs off the bottom of the canvas.
    top, rows, gap = 172, 4, 14
    foot = 134                      # separator, "ALSO TODAY", two item rows
    card_h = (H - top - foot - (rows - 1) * gap) // rows
    card_w = (W - 2 * MARGIN - GUTTER) // 2
    lowest = 0                      # nothing may be drawn past the canvas
    for i, (tag, head, detail, accent) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = MARGIN + col * (card_w + GUTTER)
        y = top + row * (card_h + gap)
        d.rounded_rectangle([x, y, x + card_w, y + card_h], 12, fill=CARD,
                            outline=CARD_EDGE, width=1)
        d.rounded_rectangle([x + 12, y + 14, x + 17, y + card_h - 14], 3, fill=accent)

        tx = x + 30
        tw = card_w - 50
        tagf = font(BOLD, 18)
        text_ls(d, (tx, y + 14), tag, tagf, accent, 2.0)

        hf, hlines = fit(d, head, BOLD, 28, tw, 2)
        block(d, (tx, y + 44), hlines, hf, WHITE, hf.size + 4)
        assert (len(hlines) - 1) * (hf.size + 4) + y + 44 + hf.size <= y + 110, \
            f"{tag}: headline overflows the card"

        df, dlines = fit(d, detail, REGULAR, 20, tw, 2)
        block(d, (tx, y + 112), dlines, df, MUTED, df.size + 4)
        detail_bottom = (len(dlines) - 1) * (df.size + 4) + y + 112 + df.size
        assert detail_bottom <= y + card_h - 4, f"{tag}: detail overflows the card"
        lowest = max(lowest, y + card_h)

    # Footer: the day has more than eight stories; list the tail.
    grid_bottom = top + rows * card_h + (rows - 1) * gap
    fy = grid_bottom + 14
    d.rectangle([MARGIN, fy, W - MARGIN, fy + 1], fill=CARD_EDGE)
    tagf = font(BOLD, 18)
    text_ls(d, (MARGIN, fy + 14), "ALSO TODAY", tagf, AMBER, 2.5)
    itemf = font(REGULAR, 20)
    col_w = (W - 2 * MARGIN) // 2
    for i, item in enumerate(ALSO_TODAY):
        col, row = i % 2, i // 2
        x = MARGIN + col * col_w
        yy = fy + 46 + row * 30
        assert d.textlength(item, font=itemf) <= col_w - 24, \
            f"footer item too wide: {item}"
        d.ellipse([x, yy + 8, x + 6, yy + 14], fill=MUTED)
        d.text((x + 16, yy), item, font=itemf, fill=MUTED)
        lowest = max(lowest, yy + itemf.size + 8)

    assert lowest <= H, f"the layout runs {lowest - H}px past the canvas"
    return img


def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = render()
    img.save(out, format="PNG", optimize=True)
    import os

    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {os.path.getsize(out)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
