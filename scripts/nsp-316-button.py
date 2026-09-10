from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# SHOP 316 hover: ivory background with forest-green text.
s = s.replace(
    ".outline-button:hover{\n  background:var(--cream);\n  color:var(--burgundy);\n}",
    ".outline-button:hover{\n  background:var(--cream);\n  color:var(--forest);\n}"
)

# SHOP 316 button: open the 316 product page directly at the sizes section.
s = s.replace(
    'onclick="document.getElementById(\'shop\').scrollIntoView()"',
    'onclick="location.href=\'/product.html?product=8#sizes\'"'
)

p.write_text(s, encoding='utf-8')
