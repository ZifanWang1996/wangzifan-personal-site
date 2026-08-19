(function(){
  'use strict';
  var reduced=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(pointer:fine)').matches;
  if(reduced||!fine)return;

  /* ---- cursor glow ---- */
  var dot=document.createElement('div');
  dot.className='glow-dot';
  dot.setAttribute('aria-hidden','true');
  document.body.appendChild(dot);
  document.documentElement.classList.add('fx-glow');
  var gx=innerWidth/2,gy=innerHeight/2,tx=gx,ty=gy;
  addEventListener('pointermove',function(e){tx=e.clientX;ty=e.clientY},{passive:true});
  (function glowLoop(){
    gx+=(tx-gx)*0.18;gy+=(ty-gy)*0.18;
    dot.style.transform='translate3d('+(gx-115)+'px,'+(gy-115)+'px,0)';
    requestAnimationFrame(glowLoop);
  })();

  /* ---- scramble-decode titles ---- */
  var GLYPHS='█▓▒░<>/\\|=+*#%&@01';
  function scramble(el){
    if(el.dataset.scrambled)return;
    el.dataset.scrambled='1';
    var original=el.textContent;
    var frame=0,total=Math.max(18,original.length*3);
    (function tick(){
      frame++;
      var resolved=Math.floor((frame/total)*original.length);
      var out='';
      for(var i=0;i<original.length;i++){
        var ch=original[i];
        if(ch===' '){out+=ch;continue}
        out+=i<resolved?ch:GLYPHS[Math.floor(Math.random()*GLYPHS.length)];
      }
      el.textContent=out;
      if(resolved<original.length)requestAnimationFrame(tick);
      else el.textContent=original;
    })();
  }
  var heroWord=document.querySelector('.gradient-word');
  if(heroWord)setTimeout(function(){scramble(heroWord)},380);
  if('IntersectionObserver' in window){
    var sio=new IntersectionObserver(function(entries){
      for(var i=0;i<entries.length;i++){
        if(entries[i].isIntersecting){scramble(entries[i].target);sio.unobserve(entries[i].target)}
      }
    },{threshold:.5});
    var st=document.querySelector('#timeline-title');
    if(st)sio.observe(st);
  }

  /* ---- magnetic primary CTAs ---- */
  var ctas=document.querySelectorAll('.btn-primary');
  for(var c=0;c<ctas.length;c++){
    (function(btn){
      btn.addEventListener('pointermove',function(e){
        var r=btn.getBoundingClientRect();
        var dx=e.clientX-(r.left+r.width/2);
        var dy=e.clientY-(r.top+r.height/2);
        var mx=Math.max(-7,Math.min(7,dx*0.18));
        var my=Math.max(-6,Math.min(6,dy*0.22));
        btn.style.transform='translate('+mx+'px,'+my+'px)';
      });
      btn.addEventListener('pointerleave',function(){btn.style.transform=''});
    })(ctas[c]);
  }

  /* ---- card thumbnail tilt ---- */
  var sitesBox=document.querySelector('.sites');
  if(sitesBox){
    sitesBox.addEventListener('pointermove',function(e){
      var shot=e.target&&e.target.closest?e.target.closest('.site-shot'):null;
      if(!shot)return;
      var r=shot.getBoundingClientRect();
      var px=(e.clientX-r.left)/r.width-0.5;
      var py=(e.clientY-r.top)/r.height-0.5;
      shot.style.transform='rotateX('+(-py*7).toFixed(2)+'deg) rotateY('+(px*9).toFixed(2)+'deg)';
    });
    sitesBox.addEventListener('pointerout',function(e){
      var shot=e.target&&e.target.closest?e.target.closest('.site-shot'):null;
      if(shot&&(!e.relatedTarget||!shot.contains(e.relatedTarget)))shot.style.transform='';
    });
  }
})();
