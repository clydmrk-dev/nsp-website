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
marker = ".marquee span{\n  margin-right:50px;\n  font-size:10px;\n  font-weight:800;\n  letter-spacing:3px;\n  text-transform:uppercase;\n}"
replacement = marker + "\n.marquee span:nth-child(8n){margin-right:0;}"
s = s.replace(marker, replacement)

p.write_text(s, encoding='utf-8')

# Product detail: Collection 01 uses one product with Forest Green and Black color variants.
product_path = Path('product.html')
q = product_path.read_text(encoding='utf-8')
q = q.replace(".size.active{border:1px solid var(--black);background:var(--cream)}", ".size.active{border:1px solid var(--forest);background:var(--forest);color:var(--cream)}")
q = q.replace(".sizes{display:flex;gap:12px}.size{width:48px;height:42px;background:#fff;border:1px solid #aaa;font-size:11px}", ".sizes{display:flex;gap:12px}.size{width:48px;height:42px;background:#fff;border:1px solid #aaa;font-size:11px}.colors{display:flex;gap:10px;flex-wrap:wrap}.color{min-width:130px;height:42px;padding:0 16px;background:#fff;border:1px solid #aaa;font-size:10px;font-weight:800;letter-spacing:1px;text-transform:uppercase}.color.active{border:1px solid var(--forest);background:var(--forest);color:var(--cream)}.color-gallery{display:flex;gap:10px;margin-top:22px;justify-content:center}.color-thumb{width:78px;height:78px;border:1px solid var(--line);background:#fff;padding:5px;cursor:pointer}.color-thumb.active{border:1px solid var(--forest)}.color-thumb img{width:100%;height:100%;object-fit:contain}")
q = q.replace('<section class="visual"><img id="photo" src="/1.png" alt="NSP Collection 01"></section>', '<section class="visual"><div><img id="photo" src="/2.png" alt="NSP Collection 01"><div class="color-gallery" id="colorGallery"></div></div></section>')
q = q.replace('<div class="price" id="price">₱490.00</div><div class="label">Size</div>', '<div class="price" id="price">₱490.00</div><div class="label" id="colorLabel">Color</div><div class="colors" id="colors"><button class="color active" data-color="Forest Green">Forest Green</button><button class="color" data-color="Black">Black</button></div><div class="label">Size</div>')
old_products = "const products={1:{name:'NSP Collection 01',price:490,image:'/1.png'},2:{name:'NSP Collection 02',price:490,image:'/2.png'},3:{name:'NSP Collection 03',price:490,image:'/3.png'},4:{name:'NSP Collection 04',price:490,image:'/4.png'},5:{name:'NSP Collection 05',price:490,image:'/5.png'},6:{name:'NSP Collection 06',price:490,image:'/6.png'},7:{name:'NSP Collection 07',price:490,image:'/7.png'}};"
new_products = "const products={1:{name:'NSP Collection 01',price:490,image:'/1.png'},2:{name:'NSP Collection 01',price:490,image:'/2.png',gallery:{'Forest Green':['/2.png','/3.png'],'Black':['/4.png','/5.png']}},3:{name:'NSP Collection 03',price:490,image:'/3.png'},4:{name:'NSP Collection 02',price:490,image:'/4.png'},5:{name:'NSP Collection 05',price:490,image:'/5.png'},6:{name:'NSP Collection 03',price:490,image:'/6.png'},7:{name:'NSP Collection 07',price:490,image:'/7.png'}};"
q = q.replace(old_products, new_products)
old_init = "const id=Number(new URLSearchParams(location.search).get('product'))||1;const p=products[id]||products[1];document.getElementById('photo').src=p.image;document.getElementById('photo').alt=p.name;document.getElementById('name').textContent=p.name;document.getElementById('price').textContent='₱'+p.price.toFixed(2);document.title='NSP — '+p.name;"
new_init = "const id=Number(new URLSearchParams(location.search).get('product'))||1;const p=products[id]||products[1];document.getElementById('photo').src=p.image;document.getElementById('photo').alt=p.name;document.getElementById('name').textContent=p.name;document.getElementById('price').textContent='₱'+p.price.toFixed(2);document.title='NSP — '+p.name;const colors=document.getElementById('colors');const colorGallery=document.getElementById('colorGallery');let selectedColor='Forest Green';function renderColor(color){selectedColor=color;const gallery=p.gallery?.[color]||[p.image];document.getElementById('photo').src=gallery[0];colorGallery.innerHTML=gallery.map((src,i)=>`<button class=\"color-thumb${i===0?' active':''}\" data-src=\"${src}\"><img src=\"${src}\" alt=\"${p.name} ${color} ${i===0?'front':'back'}\"></button>`).join('');colorGallery.querySelectorAll('.color-thumb').forEach(b=>b.onclick=()=>{colorGallery.querySelectorAll('.color-thumb').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById('photo').src=b.dataset.src;});}if(colors&&p.gallery){colors.querySelectorAll('.color').forEach(b=>b.onclick=()=>{colors.querySelectorAll('.color').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderColor(b.dataset.color);});renderColor('Forest Green');}"
q = q.replace(old_init, new_init)
q = q.replace("bag.push({name:p.name,price:p.price,image:p.image,size});", "bag.push({name:p.name,price:p.price,image:document.getElementById('photo').src,size,color:selectedColor});")
product_path.write_text(q, encoding='utf-8')
