# mokhtarlahjaily.github.io

Personal portfolio of Mokhtar Lahjaily: software engineer, AI, Java and DevOps.

- `src/page.html`: the page (content, styles, English/French switch).
- `build.py`: wraps it into a complete `site/index.html` with metadata.
- `.github/workflows/pages.yml`: builds and deploys to GitHub Pages on every push to `main`.

Local preview:

```bash
python build.py
python -m http.server -d site 8000   # then open http://localhost:8000
```

Add `#fr` to the URL to open the French version directly.
