from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- NSP WHOLE PAGE SIDE PANEL SHIFT -->'
if marker not in s:
    patch='''\n<style id="nsp-whole-page-side-shift">\n/* Push the complete site surface with the side panels. The panels themselves stay fixed. */\nbody.nsp-menu-open > :not(.nav-links):not(.modal-backdrop):not(script):not(style) {\n  transform:translateX(220px);\n  transition:transform .45s cubic-bezier(.22,1,.36,1);\n}\nbody.nsp-cart-open > :not(.nav-links):not(.modal-backdrop):not(script):not(style) {\n  transform:translateX(-220px);\n  transition:transform .45s cubic-bezier(.22,1,.36,1);\n}\n/* Keep the fixed header in sync with the page shift. */\nbody.nsp-menu-open .header, body.nsp-menu-open .navbar {\n  transform:translateX(220px);\n}\nbody.nsp-cart-open .header, body.nsp-cart-open .navbar {\n  transform:translateX(-220px);\n}\n@media(max-width:800px){\n  body.nsp-menu-open > :not(.nav-links):not(.modal-backdrop):not(script):not(style) { transform:translateX(220px); }\n  body.nsp-cart-open > :not(.nav-links):not(.modal-backdrop):not(script):not(style) { transform:translateX(-220px); }\n}\n</style>\n<!-- NSP WHOLE PAGE SIDE PANEL SHIFT -->\n'''
    s=s.replace('</head>',patch+'\n</head>',1)
    p.write_text(s,encoding='utf-8')
