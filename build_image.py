#!/usr/bin/env python3
"""Render a 1024x1024 editorial front page summing up Thursday 19 November 2026.

Pure Pillow shapes and text -- no photos, no network, no randomness, no
timestamps. Running this script always produces the same bytes.
"""

import textwrap
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# Palette: deep teal + amber + cream.
TEAL_DARK = (9, 58, 62)
TEAL = (14, 92, 96)
TEAL_LIGHT = (31, 128, 133)
AMBER = (233, 163, 44)
AMBER_SOFT = (246, 201, 107)
CREAM = (250, 244, 228)
CREAM_DIM = (238, 229, 206)
INK = (24, 34, 33)
WHITE = (255, 255, 255)
TEAL_PALE = (206, 230, 228)

WIDTH = 1024
HEIGHT = 1024


@dataclass(frozen=True)
class Story:
    kicker: str
    headline: str
    body: str
    accent: tuple


STORIES = [
    Story(
        kicker="DIPLOMACY  /  ASIA",
        headline="Trump, Xi and Putin hold first trilateral summit in Shenzhen",
        body="The three leaders meet on the APEC sidelines, with nuclear arms, "
        "Ukraine and Iran on the table; no deal is expected.",
        accent=AMBER,
    ),
    Story(
        kicker="GULF  /  WAR",
        headline="Iran widens attacks on US bases in Kuwait and Bahrain",
        body="Tehran targets a US air base in Kuwait and sites in Bahrain "
        "after US strikes on Qeshm Island.",
        accent=AMBER,
    ),
    Story(
        kicker="CULTURE  /  GAMING",
        headline="GTA VI begins global rollout after 13-year wait",
        body="Rockstar's game unlocks at midnight around the world, starting "
        "in New Zealand; pre-orders top $1.5 billion.",
        accent=TEAL_LIGHT,
    ),
    Story(
        kicker="USA  /  POLITICS",
        headline="Democrats nominate Jeffries for Speaker",
        body="House Democrats pick Hakeem Jeffries 251-11; a January floor "
        "vote would make him the first Black Speaker.",
        accent=TEAL_LIGHT,
    ),
    Story(
        kicker="SPACE  /  SCIENCE",
        headline="Voyager 1 is one light-day from Earth",
        body="NASA confirms the 1977 probe has reached 16 billion miles; a "
        "radio signal now takes a full day to reach it.",
        accent=AMBER,
    ),
    Story(
        kicker="WEATHER  /  INDIA",
        headline="Cyclone Akvan bears down on India's east coast",
        body="The storm strengthens toward very severe as it nears Andhra "
        "Pradesh and Odisha.",
        accent=AMBER_SOFT,
    ),
]


def load(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap using the real rendered width of each candidate line."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, font, fill, max_width, leading):
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_kicker(draw, x, y, story, font):
    draw.text((x, y), story.kicker, font=font, fill=story.accent)
    draw.rectangle([x, y + 22, x + 44, y + 26], fill=story.accent)


def draw_lead(canvas, story, box):
    """Full-width lead panel: big headline, amber rule, two-column body."""
    x0, y0, x1, y1 = box
    canvas.rectangle(box, fill=TEAL)
    canvas.rectangle([x0, y0, x1, y0 + 4], fill=AMBER)
    draw_kicker(canvas, x0 + 28, y0 + 24, story, load(19, bold=True))
    y = draw_wrapped(
        canvas, x0 + 28, y0 + 62, story.headline,
        load(44, bold=True), WHITE, x1 - x0 - 56, 52,
    )
    canvas.rectangle([x0 + 28, y + 8, x0 + 72, y + 12], fill=AMBER)
    draw_wrapped(
        canvas, x0 + 28, y + 22, story.body,
        load(21), CREAM, x1 - x0 - 56, 26,
    )
    canvas.text(
        (x1 - 28, y0 + 24), "01", font=load(26, bold=True),
        fill=AMBER_SOFT, anchor="ra",
    )


def draw_cell(canvas, story, box, number):
    """One of the four middle grid cells on a cream card."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=CREAM, outline=TEAL_PALE, width=2)
    canvas.rectangle([x0, y0, x0 + 6, y1], fill=story.accent)
    draw_kicker(canvas, x0 + 24, y0 + 18, story, load(15, bold=True))
    y = draw_wrapped(
        canvas, x0 + 24, y0 + 50, story.headline,
        load(25, bold=True), INK, x1 - x0 - 48, 31,
    )
    draw_wrapped(
        canvas, x0 + 24, y + 6, story.body,
        load(17), (58, 74, 72), x1 - x0 - 48, 23,
    )
    canvas.text(
        (x1 - 44, y1 - 36), number, font=load(20, bold=True), fill=TEAL_LIGHT,
    )


def draw_strip(canvas, story, box):
    """Full-width bottom strip: amber band with the final story."""
    x0, y0, x1, y1 = box
    canvas.rectangle(box, fill=AMBER)
    canvas.rectangle([x0, y0, x1, y0 + 4], fill=TEAL_DARK)
    canvas.text(
        (x0 + 28, y0 + 16), story.kicker, font=load(16, bold=True), fill=TEAL_DARK,
    )
    canvas.text(
        (x0 + 28, y0 + 42), story.headline, font=load(27, bold=True), fill=INK,
    )
    draw_wrapped(
        canvas, x0 + 28, y0 + 84, story.body,
        load(17), (58, 44, 8), x1 - x0 - 150, 22,
    )
    canvas.ellipse([x1 - 100, y0 + 26, x1 - 36, y0 + 90], outline=TEAL_DARK, width=3)
    canvas.text((x1 - 78, y0 + 42), "06", font=load(24, bold=True), fill=TEAL_DARK)


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, WIDTH, 118], fill=TEAL_DARK)
    draw.rectangle([0, 118, WIDTH, 122], fill=AMBER)
    draw.text((36, 18), "THE WORLD IN ONE PAGE", font=load(46, bold=True), fill=WHITE)
    draw.text(
        (36, 76), "THURSDAY 19 NOVEMBER 2026  |  SIX STORIES, ONE DAY",
        font=load(18, bold=True), fill=AMBER_SOFT,
    )
    draw.text((WIDTH - 36, 76), "No. 323", font=load(18), fill=CREAM_DIM, anchor="ra")

    # Lead story, full width.
    draw_lead(draw, STORIES[0], (24, 140, WIDTH - 24, 392))

    # Stories 2-5 in a two-column grid.
    grid_top = 410
    cell_w = (WIDTH - 24 * 2 - 16) // 2
    cell_h = 218
    for idx, story in enumerate(STORIES[1:5]):
        col = idx % 2
        row = idx // 2
        x0 = 24 + col * (cell_w + 16)
        y0 = grid_top + row * (cell_h + 16)
        draw_cell(draw, story, (x0, y0, x0 + cell_w, y0 + cell_h), "0%d" % (idx + 2))

    # Story 6 as a full-width bottom strip.
    draw_strip(draw, STORIES[5], (24, 878, WIDTH - 24, 1000))

    # Footer.
    draw.text(
        (36, 1006 - 4), "Compiled from verified reports  |  One image, six stories",
        font=load(13), fill=(110, 122, 120),
    )
    return img


def main():
    image = render()
    image.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
