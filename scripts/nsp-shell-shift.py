from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<!-- NSP WHOLE PAGE SIDE PANEL SHIFT -->'
patch = r'''
<style id="nsp-whole-page-side-shift">
.nav-links.nsp-reference-menu,
.nav-links.active {
  position:fixed !important;
  inset:0 auto 0 0 !important;
  width:25vw !important;
  min-width:280px !important;
  max-width:420px !important;
  height:100vh !important;
  padding:52px 44px !important;
  margin:0 !important;
  display:flex !important;
  flex-direction:column !important;
  align-items:flex-start !important;
  justify-content:flex-start !important;
  gap:0 !important;
  background:#fff !important;
  color:#0A0A0A !important;
  mix-blend-mode:normal !important;
  z-index:3000 !important;
  overflow:hidden !important;
  box-shadow:none !important;
  list-style:none !important;
}
.nav-links.nsp-reference-menu:not(.active) { display:none !important; }
.nav-links.nsp-reference-menu li { width:100%; margin:0 !important; padding:0 !important; }
.nav-links.nsp-reference-menu a {
  display:block !important;
  width:100% !important;
  padding:0 !important;
  margin:0 0 37px !important;
  color:#0A0A0A !important;
  font-family:Arial,Helvetica,sans-serif !important;
  font-size:21px !important;
  font-weight:400 !important;
  line-height:1.1 !important;
  letter-spacing:-.02em !important;
  text-transform:uppercase !important;
  opacity:1 !important;
}
.nav-links.nsp-reference-menu a:hover { opacity:.55 !important; }
body.nsp-menu-open > :not(.nav-links):not(.bag-panel):not(.modal-backdrop):not(script):not(style),
body.nsp-cart-open > :not(.nav-links):not(.bag-panel):not(.modal-backdrop):not(script):not(style) {
  transition:transform .45s cubic-bezier(.22,1,.36,1) !important;
}
body.nsp-menu-open > :not(.nav-links):not(.bag-panel):not(.modal-backdrop):not(script):not(style) {
  transform:translateX(25vw) !important;
}
body.nsp-cart-open > :not(.nav-links):not(.bag-panel):not(.modal-backdrop):not(script):not(style) {
  transform:translateX(-25vw) !important;
}
body.nsp-menu-open .navbar { transform:translateX(25vw) !important; }
body.nsp-cart-open .navbar { transform:translateX(-25vw) !important; }
body.nsp-menu-open { overflow:hidden !important; }

@media (max-width:800px){
  .nav-links.nsp-reference-menu,
  .nav-links.active {
    width:78vw !important;
    min-width:0 !important;
    max-width:none !important;
    padding:48px 32px !important;
  }
  .nav-links.nsp-reference-menu a { font-size:20px !important; margin-bottom:31px !important; }
  body.nsp-menu-open > :not(.nav-links):not(.bag-panel):not(.modal-backdrop):not(script):not(style),
  body.nsp-menu-open .navbar { transform:translateX(78vw) !important; }
  body.nsp-cart-open > :not(.nav-links):not(.bag-panel):not(.modal-backdrop):not(script):not(style),
  body.nsp-cart-open .navbar { transform:translateX(-78vw) !important; }
}
</style>
<script id="nsp-reference-menu-behavior">
(function(){
  function setup(){
    const menu = document.querySelector('.nav-links');
    const button = document.querySelector('.menu-btn');
    if(!menu || !button) return;
    if(menu.parentElement !== document.body) document.body.appendChild(menu);
    menu.classList.add('nsp-reference-menu');
    const sync = function(){
      const open = menu.classList.contains('active');
      document.body.classList.toggle('nsp-menu-open', open);
      if(open) document.body.classList.remove('nsp-cart-open');
    };
    button.addEventListener('click', function(){ setTimeout(sync, 0); });
    menu.addEventListener('click', function(e){
      if(e.target.closest('a')) setTimeout(sync, 0);
    });
    new MutationObserver(sync).observe(menu, {attributes:true, attributeFilter:['class']});
    sync();
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup);
  else setup();
})();
</script>
<!-- NSP WHOLE PAGE SIDE PANEL SHIFT -->
'''
if marker in s:
    s = re.sub(re.escape(marker) + r'.*?' + re.escape(marker), patch.strip(), s, count=1, flags=re.S)
else:
    s = s.replace('</head>', patch + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
