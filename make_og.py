"""Draw the 1200x630 link-preview image (Open Graph) used when the site is shared."""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).parent
PHOTO = ROOT / "src" / "assets" / "pdp.jpg"
OUT = ROOT / "src" / "assets" / "og.png"
FONTS = Path(r"C:\Windows\Fonts")

W, H = 1200, 630
BG = (7, 10, 18)
INK = (233, 237, 245)
MUTED = (142, 153, 174)
ACCENT = (111, 139, 255)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)

    # soft blue glow behind the portrait
    glow = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(glow).ellipse((620, 40, 1120, 590), fill=(34, 50, 120))
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(120)), 0.9)

    # dotted sphere around the portrait
    cx, cy, R = 870, 315, 250
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(dots)
    rnd = random.Random(11)
    n = 900
    for k in range(n):
        y = 1 - (k + 0.5) / n * 2
        r = math.sqrt(1 - y * y)
        th = k * 2.399963 + 0.6
        x, z = math.cos(th) * r, math.sin(th) * r
        # tilt towards the viewer a little
        y2 = y * math.cos(0.3) - z * math.sin(0.3)
        z2 = y * math.sin(0.3) + z * math.cos(0.3)
        px, py = cx + x * R, cy - y2 * R
        depth = (z2 + 1) / 2
        size = 1.2 + depth * 1.8
        alpha = int(70 + depth * 170)
        colour = (240, 243, 255) if k % 17 == 0 else ((120, 145, 255) if k % 3 == 0 else (150, 170, 255))
        d.ellipse((px - size, py - size, px + size, py + size), fill=colour + (alpha,))
    for _ in range(140):
        px, py = rnd.uniform(560, 1200), rnd.uniform(0, 630)
        s = rnd.uniform(0.6, 1.4)
        d.ellipse((px - s, py - s, px + s, py + s), fill=(80, 95, 150, 120))
    img = Image.alpha_composite(img.convert("RGBA"), dots)

    # round portrait with a thin ring
    size = 300
    photo = Image.open(PHOTO).convert("RGB").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    ring = ImageDraw.Draw(img)
    ring.ellipse((cx - size / 2 - 10, cy - size / 2 - 10, cx + size / 2 + 10, cy + size / 2 + 10), outline=(60, 78, 150), width=2)
    img.paste(photo, (cx - size // 2, cy - size // 2), mask)

    t = ImageDraw.Draw(img)
    t.text((72, 150), "SOFTWARE ENGINEER · CASABLANCA", font=font("consola.ttf", 22), fill=MUTED)
    t.text((68, 196), "Mokhtar", font=font("seguibl.ttf", 92), fill=INK)
    t.text((68, 300), "Lahjaily", font=font("seguibl.ttf", 92), fill=INK)
    t.text((72, 432), "Back end · Full stack · DevOps · AI", font=font("segoeui.ttf", 28), fill=ACCENT)
    t.text((72, 520), "mokhtarlahjaily.github.io", font=font("consola.ttf", 22), fill=MUTED)

    img.convert("RGB").save(OUT, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
