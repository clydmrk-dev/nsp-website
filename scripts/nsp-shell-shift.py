from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 316 collection: red hoodie front/back plus green hoodie front/back.
s = s.replace("const collection316Images=['/2.png','/3.png','/4.png','/5.png','/6.png','/7.png'];", "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];")
s = s.replace("const collection316Images=['/8.png','/9.png','/10.png','/11.png'];", "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];")

# Instagram CTA: ivory text normally, forest-green text on hover/active.
s = s.replace(".social .outline-button{\n  display:inline-block;\n}", ".social .outline-button{\n  display:inline-block;\n  color:var(--cream);\n}\n.social .outline-button:hover,\n.social .outline-button:active{\n  color:var(--forest);\n}")
s = s.replace(".social .outline-button{\n  display:inline-block;\n  color:var(--forest);\n}\n.social .outline-button:hover,\n.social .outline-button:active{\n  color:var(--cream);\n}", ".social .outline-button{\n  display:inline-block;\n  color:var(--cream);\n}\n.social .outline-button:hover,\n.social .outline-button:active{\n  color:var(--forest);\n}")

# Marquee: use two identical sequences with no trailing gap at the loop boundary.
old_marquee = '<div class="marquee"><div class="marquee-track"><span>Faith Over Fear</span><span>None Shall Perish</span><span>John 3:16</span><span>Made For The Called</span><span>Faith Over Fear</span><span>None Shall Perish</span><span>John 3:16</span><span>Made For The Called</span></div></div>'
new_marquee = '<div class="marquee"><div class="marquee-track"><span>Faith Over Fear</span><span>None Shall Perish</span><span>John 3:16</span><span>Made For The Called</span><span>Faith Over Fear</span><span>None Shall Perish</span><span>John 3:16</span><span>Made For The Called</span><span>Faith Over Fear</span><span>None Shall Perish</span><span>John 3:16</span><span>Made For The Called</span><span>Faith Over Fear</span><span>None Shall Perish</span><span>John 3:16</span><span>Made For The Called</span></div></div>'
s = s.replace(old_marquee, new_marquee)

# Ensure the repeated marquee sequence loops exactly at the boundary without an extra 50px gap.
s = s.replace(".marquee span{\n  margin-right:50px;", ".marquee span{\n  margin-right:50px;")
marker = ".marquee span{\n  margin-right:50px;\n  font-size:10px;\n  font-weight:800;\n  letter-spacing:3px;\n  text-transform:uppercase;\n}"
replacement = marker + "\n.marquee span:nth-child(8n){margin-right:0;}"
s = s.replace(marker, replacement)

p.write_text(s, encoding='utf-8')
