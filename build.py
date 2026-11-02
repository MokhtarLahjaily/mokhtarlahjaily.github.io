"""Wrap src/page.html into a complete site/index.html for GitHub Pages.

src/page.html is written without <html>/<head>/<body> so it can also be previewed
as a claude.ai artifact. This script moves its <title>, font links and <style>
into a real <head>, adds the page metadata, copies src/assets/ next to it, and
writes the deployable file.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "page.html"
ASSETS = ROOT / "src" / "assets"
SITE = ROOT / "site"
OUT = SITE / "index.html"

TITLE = "Mokhtar Lahjaily · Software Engineer (Back end, Full stack, DevOps, AI)"
DESCRIPTION = (
    "Software engineer: Java and Spring back ends, full-stack apps, Docker and CI/CD pipelines, "
    "and LLM systems that run on-premise. Open to back-end, full-stack, DevOps and AI roles."
)
URL = "https://mokhtarlahjaily.github.io/"
OG_IMAGE = URL + "assets/og.png"

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='14' fill='%232743B0'/%3E"
    "%3Ctext x='32' y='42' font-family='Arial,sans-serif' font-size='28' "
    "font-weight='700' text-anchor='middle' fill='white'%3EML%3C/text%3E%3C/svg%3E"
)

# Same base rules the artifact viewer's skeleton provides.
RESET = """<style>
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>"""


def main() -> None:
    page = SRC.read_text(encoding="utf-8")

    page = re.sub(r"<title>.*?</title>\s*", "", page, count=1, flags=re.S)
    head_links = re.findall(r"<link [^>]*>\s*", page)
    for link in head_links:
        page = page.replace(link, "", 1)
    style = re.search(r"<style>.*?</style>\s*", page, flags=re.S)
    assert style, "page.html must start with its <style> block"
    page = page.replace(style.group(0), "", 1)

    head = "\n".join([
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"<title>{TITLE}</title>",
        f'<meta name="description" content="{DESCRIPTION}">',
        '<meta name="theme-color" content="#070A12">',
        f'<link rel="canonical" href="{URL}">',
        f'<link rel="icon" href="{FAVICON}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{TITLE}">',
        f'<meta property="og:description" content="{DESCRIPTION}">',
        f'<meta property="og:url" content="{URL}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        *[link.strip() for link in head_links],
        RESET,
        style.group(0).strip(),
    ])

    html = f'<!doctype html>\n<html lang="en">\n<head>\n{head}\n</head>\n<body>\n{page.strip()}\n</body>\n</html>\n'
    SITE.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    if ASSETS.exists():
        shutil.copytree(ASSETS, SITE / "assets", dirs_exist_ok=True)
    print(f"wrote {OUT} ({len(html):,} bytes) and copied assets/")


if __name__ == "__main__":
    main()
