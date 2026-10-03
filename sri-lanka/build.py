#!/usr/bin/env python3
"""Build index.html from index.src.html + photo-credits.json.

Each <!--PHOTO:id--> marker becomes a real <img> when photo-credits.json has an
entry with that id, otherwise a solid colour block with the place name (never a
substitute photo). <!--CREDITS--> becomes the credit list.
"""
import html, json, pathlib

here = pathlib.Path(__file__).parent
src = (here / "index.src.html").read_text()
credits = json.loads((here / "photo-credits.json").read_text())
by_id = {c["id"]: c for c in credits}

FALLBACK = {  # id: (label, colour)
    "hero": ("Sri Lanka", "#3B4A54"), "ella": ("Ella", "#2F6B3A"),
    "train": ("Nanu Oya → Ella", "#0E7C86"), "kitulgala": ("Kitulgala", "#2F6B3A"),
    "arugam": ("Arugam Bay", "#0E7C86"), "hiriketiya": ("Hiriketiya", "#0E7C86"),
    "ahangama": ("Ahangama", "#B5452B"), "udawalawe": ("Udawalawe", "#E89B23"),
    "sigiriya": ("Sigiriya", "#B5452B"), "knuckles": ("Knuckles", "#3B4A54"),
    "adams": ("Adam's Peak", "#3B4A54"),
}

def credit_line(c, short=False):
    who = html.escape(c["photographer"])
    lic = html.escape(c["license"])
    link = f'<a href="{html.escape(c["source_url"])}">{"Photo" if short else html.escape(c["place"])}</a>'
    return f'{link}: {who}, {lic}' if not short else f'{link}: {who} ({lic})'

for pid, (label, colour) in FALLBACK.items():
    marker = f"<!--PHOTO:{pid}-->"
    c = by_id.get(pid)
    if c:
        load = 'fetchpriority="high"' if pid == "hero" else 'loading="lazy"'
        img = (f'<img src="images/{c["file"]}" alt="{html.escape(c["alt"])}" '
               f'width="{c["width"]}" height="{c["height"]}" '
               f'{load} decoding="async">')
        cls = "credit-inline" if pid == "hero" else "pcred"
        out = img + f'<span class="{cls}">{credit_line(c, short=True)}</span>'
    else:
        out = (f'<div class="ph-fallback" style="background:{colour}" role="img" '
               f'aria-label="{html.escape(label)} (no verified photo)">{html.escape(label)}</div>')
    src = src.replace(marker, out)

seen, items = set(), []
for c in credits:
    if c["file"] in seen:
        continue
    seen.add(c["file"])
    items.append(f"<li>{credit_line(c)}</li>")
src = src.replace("<!--CREDITS-->", "<ul>" + "".join(items) + "</ul>" if items
                  else "<p>No photos yet; colour blocks only.</p>")

hero = by_id.get("hero")
og = (f'<meta property="og:image" content="https://mark000.github.io/jordan-boys-trip/sri-lanka/images/{hero["file"]}">'
      if hero else "")
src = src.replace("<!--OG_IMAGE-->", og)

(here / "index.html").write_text(src)
print(f"built index.html with {len(by_id)} photos")
