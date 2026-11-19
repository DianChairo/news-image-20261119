#!/usr/bin/env python3
"""Draw the 19 November 2026 front page: one image, six stories.

Pure Pillow shapes and text, no photos, no network. Renders entry.png
at 1024x1024 in the same directory as this script.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

CREAM = (251, 243, 220)
CARD = (255, 249, 232)
TEAL = (12, 79, 74)
TEAL_DARK = (9, 62, 58)
AMBER = (242, 160, 7)
INK = (26, 26, 24)
BODY = (74, 74, 66)
MUTED = (120, 110, 92)
WHITE = (255, 255, 255)
TEAL_LINE = (12, 79, 74)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, fnt, color, max_width, leading):
    lines = wrap(draw, text, fnt, max_width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=TEAL)
    title = font(SANS_BOLD, 52)
    d.text((34, 26), "THE WORLD IN ONE PAGE", font=title, fill=WHITE)
    sub = font(SANS_BOLD, 22)
    d.text((34, 84), "THURSDAY 19 NOVEMBER 2026  |  SIX STORIES, ONE DAY",
           font=sub, fill=AMBER)
    issue = font(SANS, 22)
    d.text((W - 34 - d.textlength("No. 323", font=issue), 84),
           "No. 323", font=issue, fill=WHITE)
    d.rectangle([0, 118, W, 124], fill=AMBER)

    # ---- Lead story -----------------------------------------------------
    d.rectangle([24, 138, 1000, 404], fill=TEAL)
    d.rectangle([24, 138, 1000, 144], fill=AMBER)
    kick = font(SANS_BOLD, 24)
    d.text((52, 156), "DIPLOMACY  /  ASIA", font=kick, fill=AMBER)
    num = font(SANS_BOLD, 34)
    d.text((1000 - 52 - d.textlength("01", font=num), 150), "01",
           font=num, fill=AMBER)
    d.rectangle([52, 190, 98, 195], fill=AMBER)
    head = font(SANS_BOLD, 46)
    y = draw_wrapped(d, 52, 206,
                     "Trump, Xi and Putin hold first trilateral summit in Shenzhen",
                     head, WHITE, 920, 52)
    d.rectangle([52, y + 8, 98, y + 13], fill=AMBER)
    deck = font(SANS, 25)
    draw_wrapped(d, 52, y + 24,
                 "The three leaders meet on the APEC sidelines, with nuclear "
                 "arms, Ukraine and Iran on the table; no deal is expected.",
                 deck, WHITE, 920, 31)

    # ---- Story grid -----------------------------------------------------
    stories = [
        ("GULF  /  WAR", AMBER,
         "Iran widens attacks on US bases in Kuwait, Bahrain",
         "Tehran hits US bases in Kuwait and Bahrain after US strikes "
         "on Qeshm Island; Gulf defences intercept them.",
         "02"),
        ("CULTURE  /  GAMING", TEAL,
         "GTA VI begins global rollout after 13-year wait",
         "The game unlocks at midnight worldwide from New Zealand; "
         "pre-orders top $1.5 billion.",
         "03"),
        ("USA  /  POLITICS", TEAL,
         "Democrats nominate Jeffries for Speaker",
         "House Democrats pick Jeffries 251-11; a January vote would "
         "make him the first Black Speaker.",
         "04"),
        ("SPACE  /  SCIENCE", AMBER,
         "Voyager 1 is one light-day from Earth",
         "NASA confirms the 1977 probe is 16 billion miles out; its "
         "signal now takes a full day.",
         "05"),
    ]
    card_w, card_h = 476, 216
    xs = [24, 524]
    ys = [418, 648]
    kick_f = font(SANS_BOLD, 21)
    head_f = font(SANS_BOLD, 27)
    body_f = font(SANS, 19)
    num_f = font(SANS_BOLD, 28)
    for i, (kicker, accent, headline, body, number) in enumerate(stories):
        x, y = xs[i % 2], ys[i // 2]
        d.rectangle([x, y, x + card_w, y + card_h], fill=CARD,
                    outline=TEAL_LINE, width=2)
        d.rectangle([x, y, x + 8, y + card_h], fill=accent)
        tx = x + 26
        d.text((tx, y + 14), kicker, font=kick_f, fill=accent)
        d.rectangle([tx, y + 42, tx + 46, y + 47], fill=accent)
        hy = draw_wrapped(d, tx, y + 54, headline, head_f, INK, 424, 35)
        # Narrow body column so the corner number never collides with text.
        draw_wrapped(d, tx, hy + 8, body, body_f, BODY, 360, 24)
        d.text((x + card_w - 26 - d.textlength(number, font=num_f),
                y + card_h - 38), number, font=num_f, fill=TEAL)

    # ---- Bottom strip: cyclone ------------------------------------------
    d.rectangle([24, 878, 1000, 984], fill=AMBER)
    d.text((52, 890), "WEATHER  /  INDIA", font=kick_f, fill=TEAL_DARK)
    storm = font(SANS_BOLD, 28)
    d.text((52, 914), "Cyclone Akvan bears down on India's east coast",
           font=storm, fill=INK)
    storm_body = font(SANS, 21)
    d.text((52, 950),
           "Extremely heavy rain is forecast for Andhra Pradesh and Odisha on 19-20 Nov.",
           font=storm_body, fill=(58, 44, 8))
    d.ellipse([892, 896, 968, 972], outline=TEAL_DARK, width=4)
    circ = font(SANS_BOLD, 34)
    label = "06"
    d.text((930 - d.textlength(label, font=circ) / 2, 914), label,
           font=circ, fill=TEAL_DARK)

    # ---- Footer ---------------------------------------------------------
    foot = font(SANS, 19)
    d.text((24, 994), "Compiled from verified reports  |  One image, six stories",
           font=foot, fill=MUTED)

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
