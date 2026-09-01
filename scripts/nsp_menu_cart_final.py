from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = '''\n<style id="nsp-menu-cart-final">\n/* Requested final menu/cart behavior */\n.nav-links{\n  background:#fff!important;\n  color:var(--black)!important;\n}\n.nav-links a{color:var(--black)!important;}\n.nsp-menu-close{\n  position:absolute;\n  top:24px;\n  right:24px;\n  width:36px;\n  height:36px;\n  border:1px solid rgba(10,10,10,.2);\n  background:transparent;\n  color:var(--black);\n  font:500 22px/1 Inter,Arial,sans-serif;\n  display:flex;\n  align-items:center;\n  justify-content:center;\n  cursor:pointer;\n}\n/* Only the three-line menu locks page scrolling. Cart must remain scrollable. */\nbody.nsp-menu-open{overflow:hidden!important;}\nbody.nsp-cart-open{overflow:auto!important;}\n</style>\n'''

if 'nsp-menu-cart-final' not in s:
    s = s.replace('</head>', css + '</head>', 1)

js = '''\n<script id="nsp-menu-cart-final-script">\n(function(){\n  function init(){\n    const nav=document.getElementById('navLinks');\n    const menu=document.getElementById('menuBtn');\n    const bag=document.getElementById('bagButton');\n    const bagPanel=document.getElementById('bagPanel');\n    if(!nav||!menu)return;\n\n    if(!nav.querySelector('.nsp-menu-close')){\n      const close=document.createElement('button');\n      close.type='button';\n      close.className='nsp-menu-close';\n      close.setAttribute('aria-label','Close menu');\n      close.innerHTML='×';\n      nav.prepend(close);\n      close.addEventListener('click',function(e){\n        e.preventDefault();\n        e.stopPropagation();\n        nav.classList.remove('active');\n        document.body.classList.remove('nsp-menu-open');\n        const header=document.querySelector('.navbar');\n        if(header) header.classList.remove('nsp-menu-open');\n      });\n    }\n\n    menu.addEventListener('click',function(){\n      requestAnimationFrame(function(){\n        const open=nav.classList.contains('active');\n        document.body.classList.toggle('nsp-menu-open',open);\n        if(open){\n          document.body.classList.remove('nsp-panel-open','nsp-cart-open');\n          if(bagPanel) bagPanel.classList.remove('open');\n        }\n      });\n    });\n\n    if(bag){\n      bag.addEventListener('click',function(){\n        requestAnimationFrame(function(){\n          nav.classList.remove('active');\n          document.body.classList.remove('nsp-menu-open');\n          /* Do not lock the page while cart is open. */\n          document.body.classList.remove('nsp-panel-open');\n          document.body.classList.add('nsp-cart-open');\n        });\n      });\n    }\n\n    const bagClose=document.getElementById('bagClose');\n    if(bagClose) bagClose.addEventListener('click',function(){\n      document.body.classList.remove('nsp-cart-open');\n      document.body.classList.remove('nsp-panel-open');\n    });\n  }\n  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);\n  else init();\n})();\n</script>\n'''

if 'nsp-menu-cart-final-script' not in s:
    s = s.replace('</body>', js + '</body>', 1)

p.write_text(s, encoding='utf-8')
