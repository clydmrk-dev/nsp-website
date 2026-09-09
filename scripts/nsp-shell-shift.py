from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 316 collection: red hoodie front/back plus green hoodie front/back.
s = s.replace("const collection316Images=['/2.png','/3.png','/4.png','/5.png','/6.png','/7.png'];", "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];")
s = s.replace("const collection316Images=['/8.png','/9.png','/10.png','/11.png'];", "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];")

# 316 collection: smooth crossfade with preloaded images so the browser does not
# reveal a loading gap while swapping the source.
s = s.replace(".collection-image img{\n  width:100%;\n  height:100%;\n  max-height:560px;\n  object-fit:contain;\n  object-position:center;\n}", ".collection-image img{\n  width:100%;\n  height:100%;\n  max-height:560px;\n  object-fit:contain;\n  object-position:center;\n  opacity:1;\n  transition:opacity 0.65s ease-in-out;\n  will-change:opacity;\n}")

old_js = "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];\nlet collection316Index=0;\nconst collection316Image=document.getElementById('collection316Image');\nif(collection316Image){setInterval(()=>{collection316Index=(collection316Index+1)%collection316Images.length;collection316Image.style.opacity='0';setTimeout(()=>{collection316Image.src=collection316Images[collection316Index];requestAnimationFrame(()=>{collection316Image.style.opacity='1';});},650);},4500);}"
new_js = "const collection316Images=['/8.png','/9.png','/10.png','/NSP DG back.png'];\nlet collection316Index=0;\nconst collection316Image=document.getElementById('collection316Image');\nif(collection316Image){\n  collection316Images.forEach(src=>{const preload=new Image();preload.src=src;});\n  setInterval(()=>{\n    collection316Index=(collection316Index+1)%collection316Images.length;\n    collection316Image.style.opacity='0';\n    setTimeout(()=>{\n      collection316Image.src=collection316Images[collection316Index];\n      requestAnimationFrame(()=>{collection316Image.style.opacity='1';});\n    },650);\n  },4500);\n}"
s = s.replace(old_js, new_js)

p.write_text(s, encoding='utf-8')
