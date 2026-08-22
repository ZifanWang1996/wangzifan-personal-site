(function(){
  'use strict';
  var reduced=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(pointer:fine)').matches;
  var host=document.querySelector('[data-launch]');
  if(!host)return;
  var SHIPS=/*__SHIPS__*/;

  /* ---- canvas: starfield + orbital ships, mouse parallax + attraction ---- */
  var cv=host.querySelector('.orbit-canvas'),ctx=cv.getContext('2d');
  var W=0,H=0,DPR=Math.min(2,window.devicePixelRatio||1);
  var mx=.5,my=.4,tmx=.5,tmy=.4,stars=[],ships=[];
  function size(){
    W=host.clientWidth;H=host.clientHeight;
    cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);
    stars=[];var n=Math.round(W*H/6500);
    for(var i=0;i<n;i++)stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.1+.2,a:Math.random()*.5+.12,p:Math.random()*6.28});
    ships=[];for(var j=0;j<SHIPS.length;j++){var t=j/(SHIPS.length-1||1);
      ships.push({a:t*6.283-1.57,rx:W*.20+t*W*.16,ry:H*.13+t*H*.10,sp:.00006+t*.00009,s:1.1+t*1.3,t:t});}
  }
  function frame(ts){
    ctx.clearRect(0,0,W,H);
    var cx=W/2,cy=H*.52;
    mx+=(tmx-mx)*.06;my+=(tmy-my)*.06;
    var ox=(mx-.5)*18,oy=(my-.5)*14;
    for(var i=0;i<stars.length;i++){var s=stars[i];
      var tw=s.a*(reduced?1:(.6+.4*Math.sin(ts*.001+s.p)));
      ctx.fillStyle='rgba(198,255,63,'+tw+')';
      ctx.fillRect(s.x+ox*(s.r*.4),s.y+oy*(s.r*.4),s.r,s.r);}
    if(!reduced){
      var mxx=mx*W,myy=my*H;
      for(var j=0;j<ships.length;j++){var p=ships[j];
        p.a+=p.sp*16.6;
        var x=cx+Math.cos(p.a)*p.rx+ox*(.5+p.t);
        var y=cy+Math.sin(p.a)*p.ry+oy*(.5+p.t);
        var dx=mxx-x,dy=myy-y,d2=dx*dx+dy*dy;
        if(d2<90000){var f=(1-d2/90000)*26;x+=dx/Math.sqrt(d2+1)*f;y+=dy/Math.sqrt(d2+1)*f;}
        var g=ctx.createRadialGradient(x,y,0,x,y,p.s*7);
        g.addColorStop(0,'rgba(198,255,63,.85)');g.addColorStop(.4,'rgba(198,255,63,.28)');g.addColorStop(1,'rgba(198,255,63,0)');
        ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,p.s*7,0,6.283);ctx.fill();
        ctx.fillStyle='rgba(234,255,176,.95)';ctx.beginPath();ctx.arc(x,y,p.s*.8,0,6.283);ctx.fill();
      }
    }
    requestAnimationFrame(frame);
  }
  size();requestAnimationFrame(frame);
  window.addEventListener('resize',size,{passive:true});
  if(fine&&!reduced){host.addEventListener('pointermove',function(e){
    var r=host.getBoundingClientRect();tmx=(e.clientX-r.left)/r.width;tmy=(e.clientY-r.top)/r.height;
  },{passive:true});}

  /* ---- telemetry cascade ---- */
  var lines=host.querySelectorAll('.tele-line');
  for(var l=0;l<lines.length;l++){(function(el,i){setTimeout(function(){el.classList.add('on')},500+i*260);})(lines[l],l);}

  /* ---- T-minus countdown (cadence-derived) ---- */
  var tm=document.getElementById('tminus');
  if(tm){
    var newest=new Date(SHIPS[SHIPS.length-1].d+'T00:00:00');
    var eta=new Date(newest.getTime()+1.3*86400000);
    var pad=function(n){return String(n).padStart(2,'0')};
    var tick=function(){
      var d=eta-Date.now();
      if(d<=0){tm.textContent='SHIP TODAY';return}
      var hh=Math.floor(d/3600000),mm=Math.floor(d%3600000/60000),ss=Math.floor(d%60000/1000);
      tm.textContent=pad(hh)+':'+pad(mm)+':'+pad(ss);
    };
    tick();if(!reduced)setInterval(tick,1000);
  }

  /* ---- matrix: click scrolls to card ---- */
  var px=host.querySelectorAll('.px');
  var cards=document.querySelectorAll('article.site');
  for(var p=0;p<px.length;p++){(function(btn){
    btn.addEventListener('click',function(){
      var idx=parseInt(btn.dataset.i,10);
      var card=cards[cards.length-1-idx];
      if(card){card.scrollIntoView({behavior:reduced?'auto':'smooth',block:'center'});
        card.style.transition='box-shadow .4s';card.style.boxShadow='0 0 0 3px rgba(198,255,63,.8)';
        setTimeout(function(){card.style.boxShadow=''},1400);}
    });
  })(px[p]);}
})();
