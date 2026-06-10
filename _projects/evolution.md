---
title: Evolving Creatures
summary: A genetic algorithm that breeds scribbles into enclosed space
date: 2026-05-05
layout: default
status: open
published: true
image: /assets/evolution.png
---

<style>
  body > main { max-width: none !important; margin: 0 !important; padding: 0 !important; }
  header { position: relative; z-index: 10; }

  .ew { max-width: 940px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  h1.pt { font-size: 32px; font-weight: 700; margin: 0 0 6px; letter-spacing: -0.5px; color: #e8e8e8; }
  .ps { color: #888; font-size: 14px; margin: 0 0 24px; max-width: 640px; line-height: 1.6; }

  .ctrl { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; align-items: center; }
  .btn { padding: 8px 16px; border: 1.5px solid #333; border-radius: 8px; background: #1a1a1a; color: #ccc; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s; }
  .btn:hover { border-color: #4b8bff; color: #fff; }
  .btn.primary { background: #4b8bff; color: #08183a; border-color: #4b8bff; }
  .btn.primary:hover { background: #6fa3ff; }
  .toggle { display: inline-flex; align-items: center; gap: 6px; color: #999; font-size: 13px; cursor: pointer; user-select: none; }
  .toggle input { accent-color: #4b8bff; }
  .spacer { flex: 1; }
  .stat { font-size: 13px; color: #aaa; font-family: 'SF Mono', ui-monospace, monospace; }
  .stat b { color: #4b8bff; font-weight: 600; }

  .stage { display: grid; grid-template-columns: 1fr 320px; gap: 20px; align-items: start; }
  @media (max-width: 820px) { .stage { grid-template-columns: 1fr; } }
  .panel { background: #0c0c0c; border: 1px solid #222; border-radius: 10px; padding: 14px; }
  .panel h3 { margin: 0 0 10px; font-size: 12px; font-weight: 600; color: #777; text-transform: uppercase; letter-spacing: 1px; }
  #best { width: 100%; display: block; background: #000; border-radius: 6px; aspect-ratio: 1; }
  #pop { width: 100%; display: block; background: #000; border-radius: 6px; }
  #hist { width: 100%; display: block; background: #0c0c0c; border-radius: 6px; }
  .cap { color: #666; font-size: 11px; margin-top: 8px; line-height: 1.5; font-family: 'SF Mono', ui-monospace, monospace; }

  .math-section { max-width: 720px; margin: 56px auto 0; padding: 0 20px 60px; line-height: 1.8; color: #bbb; font-size: 15px; }
  .math-section h2 { font-size: 20px; margin: 36px 0 12px; font-weight: 600; color: #e8e8e8; }
  .math-section h2:first-child { margin-top: 0; }
  .math-section p { margin: 0 0 14px; }
  .math-section ul { margin: 0 0 14px; padding-left: 20px; }
  .math-section li { margin-bottom: 6px; }
  .math-section code { background: #1a1a1a; padding: 1px 6px; border-radius: 4px; font-size: 13px; color: #9fc0ff; }
  .formula { background: #1a1a1a; padding: 12px 16px; border-radius: 6px; margin: 12px 0; overflow-x: auto; border: 1px solid #222; }
</style>

<div class="ew">
  <h1 class="pt">Evolving Creatures</h1>
  <p class="ps">A "creature" is a walk. Starting at the center it takes 1000 unit steps, turning at each step by an angle read cyclically from its <em>genome</em>. I score a creature by how many enclosed regions &mdash; <em>holes</em> &mdash; its path traps, then let a genetic algorithm breed the best ones. Hit Run and the random scribbles fill in over a few generations.</p>

  <div class="ctrl">
    <button class="btn primary" id="run">Run</button>
    <button class="btn" id="step">Step</button>
    <button class="btn" id="reset">Reset</button>
    <label class="toggle"><input type="checkbox" id="mut" checked> mutation</label>
    <span class="spacer"></span>
    <span class="stat">gen <b id="s-gen">0</b> &nbsp; best holes <b id="s-holes">0</b> &nbsp; score <b id="s-score">0</b></span>
  </div>

  <div class="stage">
    <div class="panel">
      <h3>Best creature this generation</h3>
      <canvas id="best" width="600" height="600"></canvas>
      <div class="cap" id="best-cap">press Run to begin</div>
    </div>
    <div>
      <div class="panel" style="margin-bottom:20px;">
        <h3>Population (20)</h3>
        <canvas id="pop" width="320" height="384"></canvas>
      </div>
      <div class="panel">
        <h3>Score history</h3>
        <canvas id="hist" width="320" height="160"></canvas>
        <div class="cap">lower is better &middot; <span style="color:#4b8bff;">best</span> / <span style="color:#888;">mean</span></div>
      </div>
    </div>
  </div>
</div>

<div class="math-section">
  <h2>The genome</h2>
  <p>A genome is a fixed-length array of turn angles, here \(L = 128\) of them, each drawn uniformly from \(\left[-\tfrac{\pi}{4}, \tfrac{\pi}{4}\right]\). To grow the creature we keep a running heading \(\theta\) and a position \((x, y)\) starting at the center of a \(256 \times 256\) grid. At step \(s\) we read gene \(s \bmod L\), turn, and take one unit step:</p>
  <div class="formula">\[ \theta_{s} = \theta_{s-1} + g_{\,s \bmod L}, \qquad (x_s, y_s) = (x_{s-1} + \cos\theta_s,\; y_{s-1} + \sin\theta_s) \]</div>
  <p>Because the genome cycles, a creature with \(L=128\) genes repeats its turning pattern every 128 steps &mdash; the dense, roughly radial symmetry of the evolved tangles comes from this periodicity. The walk halts early if it leaves the grid.</p>

  <h2>Counting holes</h2>
  <p>Rasterize the path onto the grid (filled cells = 1). A <em>hole</em> is a connected component of empty cells that cannot reach the grid boundary. We find them with a flood fill: mark every empty cell 4-connected to the border as exterior, then count the connected components of the empty cells left over.</p>
  <p>This is the discrete version of a topological count. By <strong>Alexander duality</strong>, the number of bounded complementary regions of a closed curve in the plane equals the rank of its first homology &mdash; the number of independent loops. So the genetic algorithm is really maximizing \(b_1\) of a self-intersecting curve. One catch: the flood fill is 4-connected, so a region sealed only by a diagonal step still leaks, and some visually-closed loops don't get counted.</p>
  <div class="formula">\[ \text{score} = -\,(\text{number of holes}), \qquad \text{lower is better} \]</div>

  <h2>The genetic algorithm</h2>
  <p>Each generation, all 20 genomes are grown and scored. Then:</p>
  <ul>
    <li><strong>Select</strong> &mdash; keep the top \(k=2\) by score (the fittest survive unchanged).</li>
    <li><strong>Mutate</strong> (optional) &mdash; flip the sign of one random gene in each survivor before it breeds. A sign flip turns a left turn into a right turn, which changes the whole downstream path.</li>
    <li><strong>Reproduce</strong> &mdash; fill the rest of the population with children. Each child picks two parents and inherits each gene from one or the other by an independent coin flip (uniform crossover).</li>
  </ul>
  <p>There is no fitness-proportional sampling and no continuous mutation of magnitudes &mdash; selection just keeps the top two, and the only randomness in breeding is the crossover mask plus the optional sign flip. Even so it converges fast: within a handful of generations the whole population is descended from one or two champion scribbles.</p>

  <h2>Mutation matters</h2>
  <p>Toggle mutation off and the population converges fast but then stalls: crossover can only shuffle genes that already exist in the survivors, so once the parents agree on a gene, no child can ever change it. Sign-flip mutation adds variation along the one axis the score cares about (turn direction), which is what lets the search push past a local optimum and reach the dense tangles that trap a hundred-plus holes.</p>
</div>

<script>
(function(){
  var SIZE = 256, STEPS = 1000, GENOME_LEN = 128, POP_SIZE = 20, N_PARENTS = 2;
  var TWO_PI = Math.PI * 2;

  // ---- core mechanics (port of evolve_cont.py) ----
  function randGenome(){
    var g = new Float64Array(GENOME_LEN);
    for (var i=0;i<GENOME_LEN;i++) g[i] = (Math.random()*2-1) * Math.PI/4;
    return { angles:g, parents:null };
  }

  function grow(genome){
    var L = genome.angles.length;
    var grid = new Uint8Array(SIZE*SIZE);
    var x = SIZE/2, y = SIZE/2, heading = 0;
    grid[(y|0)*SIZE + (x|0)] = 1;
    var xs = [x], ys = [y];
    for (var s=0;s<STEPS;s++){
      heading += genome.angles[s % L];
      x += Math.cos(heading); y += Math.sin(heading);
      var ix = Math.round(x), iy = Math.round(y);
      if (ix<0 || ix>=SIZE || iy<0 || iy>=SIZE) break;
      xs.push(x); ys.push(y);
      grid[iy*SIZE + ix] = 1;
    }
    return { grid:grid, xs:xs, ys:ys };
  }

  function countHoles(grid){
    var ext = new Uint8Array(SIZE*SIZE);
    var qx = new Int32Array(SIZE*SIZE), qy = new Int32Array(SIZE*SIZE);
    var head=0, tail=0;
    function push(i,j){ if(grid[i*SIZE+j]===0 && !ext[i*SIZE+j]){ ext[i*SIZE+j]=1; qy[tail]=i; qx[tail]=j; tail++; } }
    for (var i=0;i<SIZE;i++){ push(i,0); push(i,SIZE-1); }
    for (var j=0;j<SIZE;j++){ push(0,j); push(SIZE-1,j); }
    while(head<tail){
      var ci=qy[head], cj=qx[head]; head++;
      if(ci>0) push(ci-1,cj);
      if(ci<SIZE-1) push(ci+1,cj);
      if(cj>0) push(ci,cj-1);
      if(cj<SIZE-1) push(ci,cj+1);
    }
    // connected components of interior empties
    var seen = new Uint8Array(SIZE*SIZE), comps=0;
    var sx = new Int32Array(SIZE*SIZE), sy = new Int32Array(SIZE*SIZE);
    for (var a=0;a<SIZE;a++){
      for (var b=0;b<SIZE;b++){
        var idx=a*SIZE+b;
        if(grid[idx]===0 && !ext[idx] && !seen[idx]){
          comps++; seen[idx]=1; var sp=0; sy[0]=a; sx[0]=b; sp=1;
          while(sp>0){
            sp--; var pi=sy[sp], pj=sx[sp];
            var nb=[[pi-1,pj],[pi+1,pj],[pi,pj-1],[pi,pj+1]];
            for(var n=0;n<4;n++){
              var ni=nb[n][0], nj=nb[n][1];
              if(ni>=0&&ni<SIZE&&nj>=0&&nj<SIZE){
                var nidx=ni*SIZE+nj;
                if(grid[nidx]===0 && !ext[nidx] && !seen[nidx]){ seen[nidx]=1; sy[sp]=ni; sx[sp]=nj; sp++; }
              }
            }
          }
        }
      }
    }
    return comps;
  }

  function evaluate(genome){
    var r = grow(genome);
    var holes = countHoles(r.grid);
    return { xs:r.xs, ys:r.ys, holes:holes, score:-holes };
  }

  function select(pop, results){
    var order = results.map(function(r,i){return i;}).sort(function(a,b){return results[a].score - results[b].score;});
    return order.slice(0, N_PARENTS).map(function(i){return pop[i];});
  }

  function mutate(genome){
    var g = genome.angles.slice();
    var k = (Math.random()*g.length)|0;
    g[k] = -g[k];
    return { angles:g, parents:genome.parents };
  }

  function reproduce(parents, n){
    var kids = [];
    for (var c=0;c<n;c++){
      var ia = (Math.random()*parents.length)|0, ib;
      do { ib = (Math.random()*parents.length)|0; } while(ib===ia && parents.length>1);
      var pa = parents[ia].angles, pb = parents[ib].angles;
      var g = new Float64Array(pa.length);
      for (var i=0;i<pa.length;i++) g[i] = Math.random()<0.5 ? pa[i] : pb[i];
      kids.push({ angles:g, parents:null });
    }
    return kids;
  }

  // ---- state ----
  var bestC = document.getElementById('best'), bctx = bestC.getContext('2d');
  var popC = document.getElementById('pop'), pctx = popC.getContext('2d');
  var histC = document.getElementById('hist'), hctx = histC.getContext('2d');
  var sGen = document.getElementById('s-gen'), sHoles = document.getElementById('s-holes'), sScore = document.getElementById('s-score');
  var bestCap = document.getElementById('best-cap');

  var population, gen, history, running=false, timer=null;

  function reset(){
    population = [];
    for (var i=0;i<POP_SIZE;i++) population.push(randGenome());
    gen = 0; history = [];
    bctx.fillStyle='#000'; bctx.fillRect(0,0,bestC.width,bestC.height);
    pctx.fillStyle='#000'; pctx.fillRect(0,0,popC.width,popC.height);
    hctx.fillStyle='#0c0c0c'; hctx.fillRect(0,0,histC.width,histC.height);
    sGen.textContent='0'; sHoles.textContent='0'; sScore.textContent='0';
    bestCap.textContent='press Run to begin';
  }

  function drawPath(ctx, res, w, h, color, lw){
    var xs=res.xs, ys=res.ys;
    var pad=0.08*Math.min(w,h);
    var minx=Infinity,maxx=-Infinity,miny=Infinity,maxy=-Infinity;
    for(var i=0;i<xs.length;i++){ if(xs[i]<minx)minx=xs[i]; if(xs[i]>maxx)maxx=xs[i]; if(ys[i]<miny)miny=ys[i]; if(ys[i]>maxy)maxy=ys[i]; }
    var span=Math.max(maxx-minx, maxy-miny) || 1;
    var sc=(Math.min(w,h)-2*pad)/span;
    var ox=(w-(maxx-minx)*sc)/2 - minx*sc, oy=(h-(maxy-miny)*sc)/2 - miny*sc;
    ctx.lineWidth=lw; ctx.strokeStyle=color; ctx.lineJoin='round'; ctx.lineCap='round';
    ctx.beginPath();
    for(var k=0;k<xs.length;k++){ var px=xs[k]*sc+ox, py=ys[k]*sc+oy; if(k===0)ctx.moveTo(px,py); else ctx.lineTo(px,py); }
    ctx.stroke();
  }

  function renderGeneration(results){
    var bestIdx=0;
    for (var i=1;i<results.length;i++) if(results[i].score<results[bestIdx].score) bestIdx=i;
    var best=results[bestIdx];

    bctx.fillStyle='#000'; bctx.fillRect(0,0,bestC.width,bestC.height);
    drawPath(bctx, best, bestC.width, bestC.height, '#4b8bff', 2.2);

    // population grid 5x4
    var cols=5, rows=4, cw=popC.width/cols, ch=popC.height/rows;
    pctx.fillStyle='#000'; pctx.fillRect(0,0,popC.width,popC.height);
    for (var p=0;p<results.length;p++){
      var cx=(p%cols)*cw, cy=((p/cols)|0)*ch;
      pctx.save(); pctx.translate(cx,cy); pctx.beginPath(); pctx.rect(0,0,cw,ch); pctx.clip();
      var col = p===bestIdx ? '#4b8bff' : '#2f6fd0';
      drawPath(pctx, results[p], cw, ch, col, 0.7);
      pctx.restore();
    }

    sGen.textContent=String(gen);
    sHoles.textContent=String(best.holes);
    sScore.textContent=best.score.toFixed(0);
    bestCap.textContent='gen '+gen+' · holes='+best.holes+' · steps='+(best.xs.length-1)+' · '+results.length+' creatures evaluated';
    drawHistory();
  }

  function drawHistory(){
    var w=histC.width, h=histC.height, pad=18;
    hctx.fillStyle='#0c0c0c'; hctx.fillRect(0,0,w,h);
    if(history.length<1) return;
    var allmin=Infinity, allmax=-Infinity;
    history.forEach(function(d){ allmin=Math.min(allmin,d.best,d.mean); allmax=Math.max(allmax,d.best,d.mean); });
    if(allmin===allmax) allmax=allmin+1;
    var n=history.length;
    function X(i){ return pad + (w-2*pad)*(n===1?0.5:i/(n-1)); }
    function Y(v){ return h-pad - (h-2*pad)*(v-allmin)/(allmax-allmin); }
    // zero line
    if(allmin<=0 && allmax>=0){ hctx.strokeStyle='#222'; hctx.beginPath(); hctx.moveTo(pad,Y(0)); hctx.lineTo(w-pad,Y(0)); hctx.stroke(); }
    function line(key,color){
      hctx.strokeStyle=color; hctx.lineWidth=1.6; hctx.beginPath();
      history.forEach(function(d,i){ var px=X(i),py=Y(d[key]); if(i===0)hctx.moveTo(px,py); else hctx.lineTo(px,py); });
      hctx.stroke();
      hctx.fillStyle=color;
      history.forEach(function(d,i){ hctx.beginPath(); hctx.arc(X(i),Y(d[key]),2,0,TWO_PI); hctx.fill(); });
    }
    line('mean','#888');
    line('best','#4b8bff');
  }

  function stepGen(){
    var results = population.map(evaluate);
    var scores = results.map(function(r){return r.score;});
    history.push({ best: Math.min.apply(null,scores), mean: scores.reduce(function(a,b){return a+b;},0)/scores.length });
    if(history.length>40) history.shift();
    renderGeneration(results);

    // breed next generation
    var parents = select(population, results);
    if (document.getElementById('mut').checked) parents = parents.map(mutate);
    var children = reproduce(parents, POP_SIZE - parents.length);
    population = parents.concat(children);
    gen++;
  }

  function loop(){
    if(!running) return;
    stepGen();
    timer = setTimeout(function(){ requestAnimationFrame(loop); }, 120);
  }

  document.getElementById('step').onclick=function(){ if(running)return; stepGen(); };
  document.getElementById('reset').onclick=function(){ running=false; clearTimeout(timer); document.getElementById('run').textContent='Run'; document.getElementById('run').classList.add('primary'); reset(); };
  document.getElementById('run').onclick=function(){
    running=!running;
    this.textContent = running ? 'Pause' : 'Run';
    this.classList.toggle('primary', !running);
    if(running) loop(); else clearTimeout(timer);
  };

  reset();
})();
</script>
