(function(){
  'use strict';
  var sites=document.querySelector('.sites');
  if(!sites||!sites.querySelector('.star-node'))return;
  var chips=document.querySelectorAll('.filter[data-filter]');
  var vc=document.getElementById('visibleCount');
  var CAT_LABEL={all:'ALL RELEASES',ai:'AI CLUSTER · 3',game:'GAME CLUSTER · 11',tool:'TOOL CLUSTER · 10',creative:'CREATIVE CLUSTER · 8'};

  /* filter chips -> focus a constellation cluster (nothing is hidden) */
  function focus(cat){
    sites.classList.remove('focus-ai','focus-game','focus-tool','focus-creative');
    if(cat!=='all')sites.classList.add('focus-'+cat);
    if(vc)vc.textContent=CAT_LABEL[cat]||'ALL RELEASES';
  }
  for(var i=0;i<chips.length;i++){(function(btn){
    btn.addEventListener('click',function(){
      for(var j=0;j<chips.length;j++){chips[j].classList.remove('active');chips[j].setAttribute('aria-pressed','false');}
      btn.classList.add('active');btn.setAttribute('aria-pressed','true');
      focus(btn.dataset.filter);
    });
  })(chips[i]);}

  /* hovering a node highlights its cluster's links */
  var nodes=sites.querySelectorAll('.star-node');
  function hl(cat,on){
    var ls=sites.querySelectorAll('.cl[data-cat="'+cat+'"]');
    for(var k=0;k<ls.length;k++){ls[k].style.strokeOpacity=on?'0.9':'';ls[k].style.strokeWidth=on?'0.22':'';}
  }
  for(var n=0;n<nodes.length;n++){(function(node){
    var cat=node.dataset.cat;
    node.addEventListener('pointerenter',function(){hl(cat,true)});
    node.addEventListener('pointerleave',function(){hl(cat,false)});
    node.addEventListener('focusin',function(){hl(cat,true)});
    node.addEventListener('focusout',function(){hl(cat,false)});
  })(nodes[n]);}
})();
