from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 316 collection: red hoodie front/back plus green hoodie front/back.
s = s.replace("const collection316Images=['/2.png','/3.png','/4.png','/5.png','/6.png','/7.png'];", "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];")
s = s.replace("const collection316Images=['/8.png','/9.png','/10.png','/11.png'];", "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];")

p.write_text(s, encoding='utf-8')
