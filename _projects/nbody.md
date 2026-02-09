---
title: N-Body
summary: Gravitational dynamics from first principles
date: 2025-07-20
layout: default
status: open
---

<style>
  body > main {
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  header {
    background: rgba(0,0,0,0.6) !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    position: relative;
    z-index: 3;
  }
  header .nav-link, header a { color: rgba(255,255,255,0.6) !important; }
  header .nav-link:hover, header .nav-link.active { color: #fff !important; }

  #sim {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
  }

  .panel {
    position: relative;
    z-index: 1;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 60px 5%;
    box-sizing: border-box;
  }

  .panel-inner {
    background: rgba(5, 5, 8, 0.84);
    border-left: 2px solid rgba(255,255,255,0.06);
    padding: 32px 36px;
    max-width: 460px;
    color: #aaa;
    font-size: 14.5px;
    line-height: 1.8;
    border-radius: 3px;
  }
  .panel-inner h2 {
    color: #e8e8e8;
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 14px 0;
    letter-spacing: -0.3px;
  }
  .panel-inner p { margin: 0 0 12px 0; }
  .panel-inner p:last-child { margin-bottom: 0; }
  .panel-inner em { color: #ccc; font-style: italic; }

  .intro-panel {
    justify-content: center;
    text-align: center;
    padding-top: 0;
  }
  .intro-inner {
    background: none;
    border-left: none;
    max-width: 600px;
    text-align: center;
  }
  .intro-inner h1 {
    color: #fff;
    font-size: 44px;
    font-weight: 700;
    margin: 0 0 10px 0;
    letter-spacing: -1.5px;
  }
  .intro-inner .sub {
    color: rgba(255,255,255,0.25);
    font-size: 13px;
    margin-top: 20px;
  }

  .formula {
    background: rgba(255,255,255,0.03);
    padding: 10px 14px;
    border-radius: 3px;
    margin: 10px 0;
    overflow-x: auto;
    color: #ccc;
  }

  .stats {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 2;
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    text-align: right;
    line-height: 1.6;
    white-space: pre;
  }

  @media (max-width: 640px) {
    .panel-inner { max-width: 100%; padding: 24px; font-size: 13.5px; }
    .intro-inner h1 { font-size: 32px; }
  }
</style>

<canvas id="sim"></canvas>

<div class="stats" id="stats"></div>

<section class="panel intro-panel" data-mode="intro">
  <div class="panel-inner intro-inner">
    <h1>N-Body</h1>
    <p>Gravitational dynamics from first principles. from my Cosmology Final Project</p>
    <p class="sub">Scroll</p>
  </div>
</section>

<section class="panel" data-mode="two">
  <div class="panel-inner">
    <h2>Two-Body Problem</h2>
    <p>Two masses under Newtonian gravity. The force on body \(i\):</p>
    <div class="formula">
      \[ \mathbf{F}_{ij} = -\frac{Gm_i m_j}{\lvert\mathbf{r}_{ij}\rvert^3}\,\mathbf{r}_{ij} \]
    </div>
    <p>Define the reduced mass \(\mu = m_1 m_2 / (m_1 + m_2)\) and relative coordinate \(\mathbf{r} = \mathbf{r}_1 - \mathbf{r}_2\). The problem reduces to an equivalent one-body Kepler problem:</p>
    <div class="formula">
      \[ \mu\,\ddot{\mathbf{r}} = -\frac{Gm_1 m_2}{\lvert\mathbf{r}\rvert^3}\,\mathbf{r} \]
    </div>
    <p>Closed-form solutions: conic sections. Bound orbits are ellipses. Energy and angular momentum are both conserved.</p>
  </div>
</section>

<section class="panel" data-mode="three">
  <div class="panel-inner">
    <h2>Three-Body Problem</h2>
    <p>Add a third comparable mass and the system becomes <em>non-integrable</em>. Poincar&eacute; proved in 1890 that no general closed-form solution exists.</p>
    <p>Trajectories are sensitive to initial conditions&mdash;deterministic chaos. Small perturbations grow exponentially:</p>
    <div class="formula">
      \[ \lvert\delta\mathbf{r}(t)\rvert \;\sim\; \lvert\delta\mathbf{r}(0)\rvert\, e^{\lambda t} \]
    </div>
    <p>where \(\lambda > 0\) is the largest Lyapunov exponent. Apart from special periodic orbits (Lagrange, figure-eight), long-term prediction requires numerical integration.</p>
  </div>
</section>

<section class="panel" data-mode="nbody">
  <div class="panel-inner">
    <h2>N-Body: Direct Summation</h2>
    <p>Compute all pairwise gravitational accelerations. A softening length \(\epsilon\) regularizes close encounters:</p>
    <div class="formula">
      \[ \ddot{\mathbf{r}}_i = G\sum_{j \neq i} \frac{m_j\,(\mathbf{r}_j - \mathbf{r}_i)}{(\lvert\mathbf{r}_j - \mathbf{r}_i\rvert^2 + \epsilon^2)^{3/2}} \]
    </div>
    <p>Integrated with the leapfrog (St&ouml;rmer&ndash;Verlet) scheme&mdash;symplectic and time-reversible:</p>
    <div class="formula">
      \[ \mathbf{v}_{n+\frac{1}{2}} = \mathbf{v}_n + \mathbf{a}_n\,\frac{\Delta t}{2} \]
      \[ \mathbf{r}_{n+1} = \mathbf{r}_n + \mathbf{v}_{n+\frac{1}{2}}\,\Delta t \]
      \[ \mathbf{v}_{n+1} = \mathbf{v}_{n+\frac{1}{2}} + \mathbf{a}_{n+1}\,\frac{\Delta t}{2} \]
    </div>
    <p>Cost per step: \(\mathcal{O}(N^2)\). Color encodes velocity magnitude.</p>
  </div>
</section>

<section class="panel" data-mode="barneshut">
  <div class="panel-inner">
    <h2>Barnes&ndash;Hut</h2>
    <p>Hierarchical spatial decomposition via quadtree. Each internal node stores the total mass and center of mass of its subtree.</p>
    <p>When computing the force on a body, walk the tree. If a cell subtends a small angle, treat it as a point mass. The multipole acceptance criterion:</p>
    <div class="formula">
      \[ \frac{s}{d} < \theta \]
    </div>
    <p>where \(s\) is the cell width, \(d\) the distance to the cell's center of mass, and \(\theta \approx 0.5\).</p>
    <p>Cost per step: \(\mathcal{O}(N \log N)\). The quadtree cells are drawn behind the particles.</p>
  </div>
</section>

<section class="panel" data-mode="collision">
  <div class="panel-inner">
    <h2>Galactic Collision</h2>
    <p>Two self-gravitating disks on a bound trajectory. Each galaxy is a central mass surrounded by an orbiting population, initialized with circular Keplerian velocities.</p>
    <p>As the galaxies approach, tidal forces distort both disks. The near side of each galaxy feels a stronger pull than the far side, stretching material into <em>tidal tails</em> and <em>bridges</em>:</p>
    <div class="formula">
      \[ \Delta\mathbf{a} \;\approx\; -\frac{2GM}{d^3}\,\delta\mathbf{r} \]
    </div>
    <p>where \(d\) is the inter-galactic separation and \(\delta\mathbf{r}\) the offset from a galaxy's center. The \(1/d^3\) scaling is the tidal term from a Taylor expansion of the gravitational field.</p>
    <p>Energy is redistributed through <em>violent relaxation</em> (Lynden-Bell, 1967): the time-varying potential scrambles individual orbits on a crossing timescale, driving the merged remnant toward a quasi-equilibrium.</p>
  </div>
</section>

<section class="panel intro-panel" data-mode="collision" style="min-height:40vh;"></section>

<script>
(function () {
  var canvas = document.getElementById('sim');
  var ctx = canvas.getContext('2d');
  var statsEl = document.getElementById('stats');

  function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
  window.addEventListener('resize', resize);
  resize();

  /* ── colormap (plasma-like) ── */
  var CMAP = [
    [13,8,135],[70,3,159],[114,1,168],[156,23,158],
    [189,55,134],[216,87,107],[237,121,83],[249,160,52],[240,249,33]
  ];
  function heat(t) {
    t = Math.max(0, Math.min(1, t)) * (CMAP.length - 1);
    var i = Math.min(Math.floor(t), CMAP.length - 2), f = t - i;
    var a = CMAP[i], b = CMAP[i + 1];
    return 'rgb(' + (a[0]+(b[0]-a[0])*f|0) + ',' + (a[1]+(b[1]-a[1])*f|0) + ',' + (a[2]+(b[2]-a[2])*f|0) + ')';
  }
  /* ── state ── */
  var G = 1, EPS = 4, bodies = [];
  var mode = '', dt = 0.1, substeps = 4, trail = 0.12, view = 700, drawTree = false;
  var treeRoot = null, stepMs = 0;

  function B(x, y, vx, vy, m) { return {x:x, y:y, vx:vx, vy:vy, m:m, ax:0, ay:0}; }

  /* ── init helpers ── */
  function initTwo() {
    var M = 800, d = 80, v = Math.sqrt(G * M / (4 * d));
    bodies = [B(d, 0, 0, v, M), B(-d, 0, 0, -v, M)];
    dt = 0.4; substeps = 6; trail = 0.015; view = 400; drawTree = false;
  }
  function initThree() {
    bodies = [];
    var M = 500, R = 80;
    for (var i = 0; i < 3; i++) {
      var a = 2 * Math.PI * i / 3;
      var v = Math.sqrt(G * M * 0.55 / R);
      bodies.push(B(
        R * Math.cos(a), R * Math.sin(a),
        -v * Math.sin(a) + (Math.random() - 0.5) * 0.4,
         v * Math.cos(a) + (Math.random() - 0.5) * 0.4, M));
    }
    dt = 0.18; substeps = 6; trail = 0.025; view = 500; drawTree = false;
  }
  function diskBodies(n) {
    bodies = [];
    var Mc = 8000;
    bodies.push(B(0, 0, 0, 0, Mc));
    for (var i = 0; i < n; i++) {
      var r = 35 + Math.random() * 260;
      var a = Math.random() * 2 * Math.PI;
      var vc = Math.sqrt(G * Mc / r);
      bodies.push(B(
        r * Math.cos(a), r * Math.sin(a),
        -vc * Math.sin(a) + (Math.random() - 0.5) * 0.7,
         vc * Math.cos(a) + (Math.random() - 0.5) * 0.7,
        0.8 + Math.random() * 2.5));
    }
  }
  function initN() {
    diskBodies(200);
    dt = 0.08; substeps = 5; trail = 0.1; view = 700; drawTree = false;
  }
  function initBH() {
    diskBodies(800);
    dt = 0.08; substeps = 5; trail = 0.13; view = 700; drawTree = true;
  }
  function galaxy(cx, cy, cvx, cvy, Mc, n) {
    bodies.push(B(cx, cy, cvx, cvy, Mc));
    for (var i = 0; i < n; i++) {
      var r = 15 + Math.random() * 110;
      var a = Math.random() * 2 * Math.PI;
      var vc = Math.sqrt(G * Mc / r);
      bodies.push(B(
        cx + r * Math.cos(a), cy + r * Math.sin(a),
        cvx - vc * Math.sin(a) + (Math.random() - 0.5) * 0.4,
        cvy + vc * Math.cos(a) + (Math.random() - 0.5) * 0.4,
        0.6 + Math.random() * 2));
    }
  }
  function initCollision() {
    bodies = [];
    galaxy(-200, -50, 0.9, 0.25, 5000, 200);
    galaxy( 200,  50, -0.9, -0.25, 5000, 200);
    dt = 0.1; substeps = 5; trail = 0.04; view = 800; drawTree = false;
  }

  /* ── direct O(n²) forces ── */
  function forcesDirect() {
    var n = bodies.length, eps2 = EPS * EPS;
    for (var i = 0; i < n; i++) { bodies[i].ax = 0; bodies[i].ay = 0; }
    for (var i = 0; i < n; i++) {
      var bi = bodies[i];
      for (var j = i + 1; j < n; j++) {
        var bj = bodies[j];
        var dx = bj.x - bi.x, dy = bj.y - bi.y;
        var r2 = dx * dx + dy * dy + eps2;
        var inv = G / (r2 * Math.sqrt(r2));
        bi.ax += inv * bj.m * dx; bi.ay += inv * bj.m * dy;
        bj.ax -= inv * bi.m * dx; bj.ay -= inv * bi.m * dy;
      }
    }
  }

  /* ── quadtree ── */
  function QN(cx, cy, s) { return {cx:cx, cy:cy, s:s, m:0, mx:0, my:0, b:null, ch:null, n:0}; }

  function qtIns(nd, b, d) {
    if (d > 28) return;
    if (nd.n === 0) { nd.b = b; nd.m = b.m; nd.mx = b.x; nd.my = b.y; nd.n = 1; return; }
    if (!nd.ch) {
      var hs = nd.s / 2, qs = nd.s / 4;
      nd.ch = [
        QN(nd.cx - qs, nd.cy - qs, hs), QN(nd.cx + qs, nd.cy - qs, hs),
        QN(nd.cx - qs, nd.cy + qs, hs), QN(nd.cx + qs, nd.cy + qs, hs)
      ];
      qtPut(nd, nd.b, d); nd.b = null;
    }
    qtPut(nd, b, d);
    var tm = nd.m + b.m;
    nd.mx = (nd.mx * nd.m + b.x * b.m) / tm;
    nd.my = (nd.my * nd.m + b.y * b.m) / tm;
    nd.m = tm; nd.n++;
  }
  function qtPut(nd, b, d) {
    var i = (b.x >= nd.cx ? 1 : 0) + (b.y >= nd.cy ? 2 : 0);
    qtIns(nd.ch[i], b, d + 1);
  }
  function qtForce(nd, b, th) {
    if (nd.n === 0) return;
    var dx = nd.mx - b.x, dy = nd.my - b.y;
    var r2 = dx * dx + dy * dy;
    if (nd.n === 1 && nd.b === b) return;
    if (nd.n === 1 || nd.s * nd.s / r2 < th * th) {
      var d2 = r2 + EPS * EPS, inv = G * nd.m / (d2 * Math.sqrt(d2));
      b.ax += inv * dx; b.ay += inv * dy;
      return;
    }
    for (var c = 0; c < 4; c++) qtForce(nd.ch[c], b, th);
  }
  function forcesBH() {
    var minX = 1e9, maxX = -1e9, minY = 1e9, maxY = -1e9;
    for (var i = 0; i < bodies.length; i++) {
      var b = bodies[i];
      if (b.x < minX) minX = b.x; if (b.x > maxX) maxX = b.x;
      if (b.y < minY) minY = b.y; if (b.y > maxY) maxY = b.y;
    }
    var cx = (minX + maxX) / 2, cy = (minY + maxY) / 2;
    var sz = Math.max(maxX - minX, maxY - minY) + 2;
    treeRoot = QN(cx, cy, sz);
    for (var i = 0; i < bodies.length; i++) qtIns(treeRoot, bodies[i], 0);
    for (var i = 0; i < bodies.length; i++) { bodies[i].ax = 0; bodies[i].ay = 0; }
    for (var i = 0; i < bodies.length; i++) qtForce(treeRoot, bodies[i], 0.5);
  }

  /* ── leapfrog integrator ── */
  function forces() { if (mode === 'barneshut' || mode === 'collision') forcesBH(); else forcesDirect(); }
  function step() {
    var i, b, hdt = dt * 0.5;
    for (i = 0; i < bodies.length; i++) { b = bodies[i]; b.vx += b.ax * hdt; b.vy += b.ay * hdt; }
    for (i = 0; i < bodies.length; i++) { b = bodies[i]; b.x += b.vx * dt; b.y += b.vy * dt; }
    forces();
    for (i = 0; i < bodies.length; i++) { b = bodies[i]; b.vx += b.ax * hdt; b.vy += b.ay * hdt; }
  }

  /* ── coordinate mapping ── */
  function sc() { return Math.min(canvas.width, canvas.height) / view; }
  function sx(x) { return canvas.width / 2 + x * sc(); }
  function sy(y) { return canvas.height / 2 + y * sc(); }
  function ss(r) { return r * sc(); }

  /* ── render quadtree cells ── */
  function renderTree(nd) {
    if (!nd || nd.n === 0) return;
    var hs = nd.s / 2;
    ctx.strokeRect(sx(nd.cx - hs), sy(nd.cy - hs), ss(nd.s), ss(nd.s));
    if (nd.ch) for (var c = 0; c < 4; c++) renderTree(nd.ch[c]);
  }

  /* ── escape check for few-body modes ── */
  function checkEscape() {
    if (bodies.length > 10) return;
    var lim = view * 1.8;
    for (var i = 0; i < bodies.length; i++) {
      if (bodies[i].x * bodies[i].x + bodies[i].y * bodies[i].y > lim * lim) {
        var m = mode; mode = ''; setMode(m); return;
      }
    }
  }

  /* ── render frame ── */
  function render() {
    ctx.fillStyle = 'rgba(0,0,0,' + trail + ')';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // quadtree overlay
    if (drawTree && treeRoot) {
      ctx.strokeStyle = 'rgba(40,100,220,0.1)';
      ctx.lineWidth = 0.5;
      renderTree(treeRoot);
    }

    var many = bodies.length > 10;

    if (many) {
      // compute vmax from light bodies
      var vmax = 0;
      for (var i = 0; i < bodies.length; i++) {
        if (bodies[i].m > 100) continue;
        var v2 = bodies[i].vx * bodies[i].vx + bodies[i].vy * bodies[i].vy;
        if (v2 > vmax) vmax = v2;
      }
      vmax = Math.sqrt(vmax) || 1;
      for (var i = 0; i < bodies.length; i++) {
        var b = bodies[i];
        if (b.m > 100) {
          ctx.fillStyle = 'rgba(255,255,255,0.8)';
          ctx.beginPath();
          ctx.arc(sx(b.x), sy(b.y), 2.5, 0, 6.2832);
          ctx.fill();
        } else {
          var v = Math.sqrt(b.vx * b.vx + b.vy * b.vy);
          ctx.fillStyle = heat(v / vmax);
          ctx.beginPath();
          ctx.arc(sx(b.x), sy(b.y), 1.4, 0, 6.2832);
          ctx.fill();
        }
      }
    } else {
      // few bodies: white with glow
      for (var i = 0; i < bodies.length; i++) {
        var b = bodies[i], px = sx(b.x), py = sy(b.y);
        var grad = ctx.createRadialGradient(px, py, 0, px, py, 18);
        grad.addColorStop(0, 'rgba(255,255,255,0.9)');
        grad.addColorStop(0.3, 'rgba(255,255,255,0.3)');
        grad.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(px, py, 18, 0, 6.2832);
        ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(px, py, 4, 0, 6.2832);
        ctx.fill();
      }
    }

    // stats
    var label = (mode === 'barneshut' || mode === 'collision') ? 'Barnes-Hut  O(N log N)' : 'direct  O(N\u00B2)';
    if (mode === 'two' || mode === 'three' || mode === 'intro') label = 'direct';
    statsEl.textContent = 'n = ' + bodies.length + '\n' + label + '\nstep  ' + stepMs.toFixed(2) + ' ms';
  }

  /* ── mode switching ── */
  function setMode(m) {
    if (m === mode) return;
    mode = m;
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (m === 'intro') initN();
    else if (m === 'two') initTwo();
    else if (m === 'three') initThree();
    else if (m === 'nbody') initN();
    else if (m === 'barneshut') initBH();
    else if (m === 'collision') initCollision();
    forces();
  }

  /* ── scroll observer ── */
  var panels = document.querySelectorAll('.panel[data-mode]');
  var obs = new IntersectionObserver(function (entries) {
    for (var i = 0; i < entries.length; i++) {
      if (entries[i].isIntersecting) setMode(entries[i].target.getAttribute('data-mode'));
    }
  }, { threshold: 0.45 });
  for (var i = 0; i < panels.length; i++) obs.observe(panels[i]);

  /* ── boot ── */
  setMode('intro');

  /* ── loop ── */
  function animate() {
    var t0 = performance.now();
    for (var i = 0; i < substeps; i++) step();
    stepMs = performance.now() - t0;
    checkEscape();
    render();
    requestAnimationFrame(animate);
  }
  animate();
})();
</script>
