---
title: Lagrangian Fluids
summary: Smoothed-particle hydrodynamics from first principles
date: 2025-04-29
image: /assets/fluids.png
layout: default
status: closed
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
    <h1>Lagrangian Fluids</h1>
    <p>Smoothed-particle hydrodynamics from first principles. From my Computational Physics final project.</p>
    <p>Please Scroll</p>
    <p class="sub">move your cursor to stir the fluid</p>
  </div>
</section>

<section class="panel" data-mode="lagrangian">
  <div class="panel-inner">
    <h2>The Lagrangian View</h2>
    <p>The Navier&ndash;Stokes momentum equation, written at fixed points in space (the <em>Eulerian</em> frame):</p>
    <div class="formula">
      \[ \frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v}\cdot\nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p + \nu\nabla^2\mathbf{v} + \mathbf{g} \]
    </div>
    <p>The nonlinear advection term \((\mathbf{v}\cdot\nabla)\mathbf{v}\) is what makes fluids hard. The <em>Lagrangian</em> alternative: stop watching fixed points and ride along with parcels of fluid instead. The material derivative absorbs advection entirely:</p>
    <div class="formula">
      \[ \frac{D\mathbf{v}}{Dt} = -\frac{1}{\rho}\nabla p + \nu\nabla^2\mathbf{v} + \mathbf{g} \]
    </div>
    <p>Advection becomes free &mdash; it is just the particles moving. Mass conservation is automatic, because the particles <em>are</em> the mass. The faint grid behind the fluid is the Eulerian mesh we no longer need; each streak is one parcel's velocity.</p>
  </div>
</section>

<section class="panel" data-mode="kernel">
  <div class="panel-inner">
    <h2>Smoothed Particles</h2>
    <p>A particle is not a droplet &mdash; it is a moving sample point. Any continuous field is reconstructed by a kernel-weighted sum over neighbors:</p>
    <div class="formula">
      \[ A(\mathbf{r}) \;\approx\; \sum_j \frac{m_j}{\rho_j}\, A_j\, W(\lvert\mathbf{r}-\mathbf{r}_j\rvert,\, h) \]
    </div>
    <p>Setting \(A = \rho\) gives the density estimate, the first step of every timestep:</p>
    <div class="formula">
      \[ \rho_i = \sum_j m_j\, W(\lvert\mathbf{r}_i-\mathbf{r}_j\rvert,\, h), \qquad W_{\text{poly6}} = \frac{4}{\pi h^8}\,(h^2 - r^2)^3 \]
    </div>
    <p>\(h\) is the <em>smoothing length</em> &mdash; the rings show its size on a few tracked particles. Everything inside a ring contributes to that particle's density; everything outside is invisible to it. Color encodes density.</p>
  </div>
</section>

<section class="panel" data-mode="pressure">
  <div class="panel-inner">
    <h2>Pressure</h2>
    <p>True incompressibility means solving a Poisson equation every step. The weakly-compressible shortcut (M&uuml;ller et al., 2003) trades that for a stiff equation of state:</p>
    <div class="formula">
      \[ p = k\,(\rho - \rho_0), \qquad p \ge 0 \]
    </div>
    <p>Compressed regions push back; the clamp at zero avoids tensile instability. The force is symmetrized so Newton's third law holds pairwise:</p>
    <div class="formula">
      \[ \mathbf{f}_i^{\,\text{press}} = -\sum_j m_j\, \frac{p_i + p_j}{2\rho_j}\, \nabla W_{\text{spiky}} \]
    </div>
    <p>The <em>spiky</em> kernel is used here because the poly6 gradient vanishes as \(r \to 0\) &mdash; particles would clump without resistance. Spiky's gradient stays finite all the way in. Color encodes pressure: watch it spike where the fluid slams into the wall.</p>
  </div>
</section>

<section class="panel" data-mode="viscosity">
  <div class="panel-inner">
    <h2>Viscosity</h2>
    <p>Internal friction diffuses momentum between neighboring parcels:</p>
    <div class="formula">
      \[ \mathbf{f}_i^{\,\text{visc}} = \mu \sum_j m_j\, \frac{\mathbf{v}_j - \mathbf{v}_i}{\rho_j}\, \nabla^2 W_{\text{visc}}, \qquad \nabla^2 W = \frac{40}{\pi h^5}(h - r) \]
    </div>
    <p>This kernel's Laplacian is positive everywhere, so the force always damps <em>relative</em> motion and never injects energy &mdash; it is unconditionally stabilizing, which is why it doubles as the simulation's safety net.</p>
    <p>Here \(\mu\) is raised four-fold: the same dam break, but the water is now honey. Vorticity dies before it forms, and the collapse becomes a slow ooze.</p>
  </div>
</section>

<section class="panel" data-mode="grid">
  <div class="panel-inner">
    <h2>Finding Neighbors</h2>
    <p>Every SPH sum runs only over neighbors within \(h\) &mdash; the kernels have compact support. Testing all pairs is \(\mathcal{O}(N^2)\); the fix is a uniform grid with cell size exactly \(h\):</p>
    <div class="formula">
      \[ \text{bin all particles} \;\rightarrow\; \text{scan } 3\times3 \text{ cells} \;\Rightarrow\; \mathcal{O}(N) \]
    </div>
    <p>Particles are bucketed with a counting sort each substep (no allocation, cache-friendly). The outlined cells are the occupied bins; one particle's kernel radius and its \(3\times3\) neighborhood are highlighted.</p>
    <p>The same loop ported to the GPU (Taichi, one thread per particle) ran 10,000+ particles at 60&thinsp;fps &mdash; the structure parallelizes for free because each particle only reads its neighborhood. The stability rule of thumb: \(\Delta t \cdot v_{\max} < h\), so nothing skips past its own neighbor cell.</p>
  </div>
</section>

<section class="panel" data-mode="zerog">
  <div class="panel-inner">
    <h2>Zero Gravity</h2>
    <p>Switch gravity off, add a weak cohesive attraction between neighbors, and give the fluid a spin. Pressure pushes out, cohesion pulls in, and the competition settles into a rotating drop &mdash; a poor man's surface tension.</p>
    <p>The full project went further: spinning-drop experiments in 2D and 3D measuring spin-down against viscosity, drop oscillation under a tension force, and radial collisions of free-floating blobs &mdash; all on the GPU via Taichi.</p>
    <p>What you are watching on this page is the same algorithm in plain JavaScript: a couple thousand particles, four substeps per frame, density &rarr; pressure &rarr; forces &rarr; integrate, sixty times a second in your browser.</p>
  </div>
</section>

<section class="panel intro-panel" data-mode="zerog" style="min-height:40vh;"></section>

<script>
(function () {
  var canvas = document.getElementById('sim');
  var ctx = canvas.getContext('2d');
  var statsEl = document.getElementById('stats');

  function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
  window.addEventListener('resize', resize);
  resize();

  /* ── SPH constants (2D, Müller 2003 normalizations) ── */
  var WORLD_H = 1.0;
  var WORLD_W = Math.min(Math.max(canvas.width / canvas.height, 1.0), 2.2) * WORLD_H;
  var H = 0.03, H2 = H * H;
  var SP = 0.55 * H;                    // rest particle spacing
  var RHO0 = 1000, M = RHO0 * SP * SP;  // particle mass
  var POLY6 = 4 / (Math.PI * Math.pow(H, 8));
  var SPIKY = -30 / (Math.PI * Math.pow(H, 5));
  var VLAP = 40 / (Math.PI * Math.pow(H, 5));
  var SELF_RHO = M * POLY6 * H2 * H2 * H2;
  var DT = 2.5e-3, VCLAMP = 8, PAD = 0.5 * H, WALL_REST = 0.3;

  /* ── particle state ── */
  var MAXN = 2600, n = 0;
  var px = new Float32Array(MAXN), py = new Float32Array(MAXN);
  var vx = new Float32Array(MAXN), vy = new Float32Array(MAXN);
  var fx = new Float32Array(MAXN), fy = new Float32Array(MAXN);
  var rho = new Float32Array(MAXN), pre = new Float32Array(MAXN);

  /* ── spatial hash (counting sort each substep) ── */
  var GX = Math.floor(WORLD_W / H) + 1, GY = Math.floor(WORLD_H / H) + 1;
  var NC = GX * GY;
  var cellStart = new Int32Array(NC + 1), fillPtr = new Int32Array(NC);
  var sorted = new Int32Array(MAXN), cellIdx = new Int32Array(MAXN);

  function cellX(x) { var c = (x / H) | 0; return c < 0 ? 0 : (c >= GX ? GX - 1 : c); }
  function cellY(y) { var c = (y / H) | 0; return c < 0 ? 0 : (c >= GY ? GY - 1 : c); }

  function buildGrid() {
    var i, c;
    for (c = 0; c <= NC; c++) cellStart[c] = 0;
    for (i = 0; i < n; i++) {
      c = cellY(py[i]) * GX + cellX(px[i]);
      cellIdx[i] = c;
      cellStart[c + 1]++;
    }
    for (c = 0; c < NC; c++) cellStart[c + 1] += cellStart[c];
    for (c = 0; c < NC; c++) fillPtr[c] = cellStart[c];
    for (i = 0; i < n; i++) sorted[fillPtr[cellIdx[i]]++] = i;
  }

  /* ── mode config ── */
  var cfg = null, mode = '', modeT = 0, stepMs = 0, substeps = 4;
  var ringIdx = [];

  function densityPressure() {
    var k = cfg.k;
    for (var i = 0; i < n; i++) {
      var xi = px[i], yi = py[i], r = SELF_RHO;
      var cx = cellX(xi), cy = cellY(yi);
      for (var gy = cy - 1; gy <= cy + 1; gy++) {
        if (gy < 0 || gy >= GY) continue;
        for (var gx = cx - 1; gx <= cx + 1; gx++) {
          if (gx < 0 || gx >= GX) continue;
          var c = gy * GX + gx, e = cellStart[c + 1];
          for (var s = cellStart[c]; s < e; s++) {
            var j = sorted[s];
            if (j === i) continue;
            var dx = xi - px[j], dy = yi - py[j];
            var r2 = dx * dx + dy * dy;
            if (r2 < H2) { var a = H2 - r2; r += M * POLY6 * a * a * a; }
          }
        }
      }
      rho[i] = r;
      var p = k * (r - RHO0);
      pre[i] = p > 0 ? p : 0;
    }
  }

  function forces() {
    var mu = cfg.mu, coh = cfg.coh || 0;
    for (var i = 0; i < n; i++) {
      var xi = px[i], yi = py[i], vxi = vx[i], vyi = vy[i];
      var pi = pre[i], fxi = 0, fyi = 0, cxa = 0, cya = 0;
      var cx = cellX(xi), cy = cellY(yi);
      for (var gy = cy - 1; gy <= cy + 1; gy++) {
        if (gy < 0 || gy >= GY) continue;
        for (var gx = cx - 1; gx <= cx + 1; gx++) {
          if (gx < 0 || gx >= GX) continue;
          var c = gy * GX + gx, e = cellStart[c + 1];
          for (var s = cellStart[c]; s < e; s++) {
            var j = sorted[s];
            if (j === i) continue;
            var dx = xi - px[j], dy = yi - py[j];
            var r2 = dx * dx + dy * dy;
            if (r2 >= H2) continue;
            var d = Math.sqrt(r2) + 1e-9;
            var rj = rho[j] > 1e-6 ? rho[j] : 1e-6;
            var hd = H - d;
            // pressure (symmetric, spiky gradient — repels when compressed)
            var pc = -M * (pi + pre[j]) / (2 * rj) * SPIKY * hd * hd / d;
            fxi += pc * dx; fyi += pc * dy;
            // viscosity (laplacian kernel — damps relative motion)
            var vc = mu * M * VLAP * hd / rj;
            fxi += vc * (vx[j] - vxi); fyi += vc * (vy[j] - vyi);
            // cohesion (zero-g mode): triangle profile peaking at h/2
            if (coh > 0) {
              var t = coh * 4 * (d / H) * (1 - d / H) / d;
              cxa -= t * dx; cya -= t * dy;
            }
          }
        }
      }
      var ri = rho[i] > 1e-6 ? rho[i] : 1e-6;
      fx[i] = fxi / ri + cxa;
      fy[i] = fyi / ri + cya + cfg.g;
    }
  }

  function integrate() {
    var damp = cfg.damp || 1;
    var loX = PAD, hiX = WORLD_W - PAD, loY = PAD, hiY = WORLD_H - PAD;
    for (var i = 0; i < n; i++) {
      vx[i] = (vx[i] + fx[i] * DT) * damp;
      vy[i] = (vy[i] + fy[i] * DT) * damp;
      var s2 = vx[i] * vx[i] + vy[i] * vy[i];
      if (s2 > VCLAMP * VCLAMP) { var sc = VCLAMP / Math.sqrt(s2); vx[i] *= sc; vy[i] *= sc; }
      px[i] += vx[i] * DT;
      py[i] += vy[i] * DT;
      if (px[i] < loX) { px[i] = loX; if (vx[i] < 0) vx[i] = -vx[i] * WALL_REST; }
      if (px[i] > hiX) { px[i] = hiX; if (vx[i] > 0) vx[i] = -vx[i] * WALL_REST; }
      if (py[i] < loY) { py[i] = loY; if (vy[i] < 0) vy[i] = -vy[i] * WALL_REST; }
      if (py[i] > hiY) { py[i] = hiY; if (vy[i] > 0) vy[i] = -vy[i] * WALL_REST; }
    }
  }

  /* ── seeding ── */
  function seedBlock(x0, y0, x1, y1) {
    for (var y = y0; y < y1 && n < MAXN - 1; y += SP)
      for (var x = x0; x < x1 && n < MAXN - 1; x += SP) {
        px[n] = x + (Math.random() - 0.5) * SP * 0.1;
        py[n] = y + (Math.random() - 0.5) * SP * 0.1;
        vx[n] = 0; vy[n] = 0;
        n++;
      }
  }
  function initDam() {
    n = 0;
    seedBlock(PAD + 0.005, PAD + 0.005, 0.37 * WORLD_W, 0.85);
  }
  function initPool() {
    n = 0;
    seedBlock(PAD + 0.005, PAD + 0.005, WORLD_W - PAD, 0.24);
    ringIdx = [(n * 0.3) | 0, (n * 0.55) | 0, (n * 0.82) | 0];
    // a blob dropped into the pool for some action
    var bx = WORLD_W * 0.55, by = 0.68, R = 0.09;
    for (var y = -R; y <= R; y += SP)
      for (var x = -R; x <= R; x += SP)
        if (x * x + y * y <= R * R && n < MAXN - 1) {
          px[n] = bx + x; py[n] = by + y;
          vx[n] = 0; vy[n] = -0.8;
          n++;
        }
  }
  function initDisc() {
    n = 0;
    var cx = WORLD_W / 2, cy = WORLD_H / 2, R = 0.22, om = 1.0;
    for (var y = -R; y <= R; y += SP)
      for (var x = -R; x <= R; x += SP)
        if (x * x + y * y <= R * R && n < MAXN - 1) {
          px[n] = cx + x + (Math.random() - 0.5) * SP * 0.1;
          py[n] = cy + y + (Math.random() - 0.5) * SP * 0.1;
          vx[n] = -om * y; vy[n] = om * x;   // solid-body spin
          n++;
        }
  }

  /* ── color ramps (quantized to prebuilt strings) ── */
  function ramp(stops) {
    var out = [];
    for (var q = 0; q < 48; q++) {
      var t = q / 47 * (stops.length - 1);
      var i = Math.min(t | 0, stops.length - 2), f = t - i;
      var a = stops[i], b = stops[i + 1];
      out.push('rgb(' + (a[0] + (b[0] - a[0]) * f | 0) + ',' +
                        (a[1] + (b[1] - a[1]) * f | 0) + ',' +
                        (a[2] + (b[2] - a[2]) * f | 0) + ')');
    }
    return out;
  }
  var RAMPS = {
    speed:    ramp([[41, 79, 199], [142, 168, 230], [230, 240, 255]]),
    honey:    ramp([[97, 56, 14], [222, 147, 41], [255, 235, 160]]),
    density:  ramp([[13, 8, 51], [38, 77, 166], [26, 179, 128], [250, 230, 38]]),
    pressure: ramp([[20, 16, 60], [120, 40, 120], [230, 80, 60], [255, 230, 80]])
  };
  function colorT(i) {
    if (cfg.color === 'density')  return (rho[i] - 600) / 700;
    if (cfg.color === 'pressure') return pre[i] / 25000;
    var s = Math.sqrt(vx[i] * vx[i] + vy[i] * vy[i]);
    return cfg.color === 'honey' ? s / 1.5 : s / 3;
  }

  /* ── modes ── */
  var MODES = {
    intro:      { init: initDam,  g: -6, k: 50, mu: 0.2, color: 'speed',    reset: 14, label: 'WCSPH (Müller 2003)' },
    lagrangian: { init: initDam,  g: -6, k: 50, mu: 0.2, color: 'speed',    reset: 14, streaks: true, eulerGrid: true, label: 'Lagrangian frame' },
    kernel:     { init: initPool, g: -6, k: 50, mu: 0.25, color: 'density', reset: 20, rings: true, label: 'poly6 density' },
    pressure:   { init: initDam,  g: -6, k: 50, mu: 0.2, color: 'pressure', reset: 14, label: 'p = k(ρ − ρ₀)' },
    viscosity:  { init: initDam,  g: -6, k: 50, mu: 0.8, color: 'honey',    reset: 18, label: 'μ × 4' },
    grid:       { init: initDam,  g: -6, k: 50, mu: 0.2, color: 'speed',    reset: 14, hashGrid: true, label: 'spatial hash O(N)' },
    zerog:      { init: initDisc, g: 0,  k: 50, mu: 0.3, color: 'speed',    coh: 0.6, damp: 0.999, label: 'g = 0, cohesion on' }
  };

  function setMode(m) {
    if (m === mode) return;
    mode = m;
    cfg = MODES[m];
    cfg.init();
    modeT = 0;
  }

  /* ── mouse stir ── */
  var mWX = 0, mWY = 0, mVX = 0, mVY = 0, mLast = -1e9, mHave = false;
  function pointerMove(cx2, cy2) {
    var wx = (cx2 - offX) / scale;
    var wy = WORLD_H - (cy2 - offY) / scale;
    var now = performance.now();
    if (mHave) {
      var dt = Math.max((now - mLast) / 1000, 1 / 240);
      mVX = (wx - mWX) / dt; mVY = (wy - mWY) / dt;
      var s = Math.sqrt(mVX * mVX + mVY * mVY);
      if (s > 6) { mVX *= 6 / s; mVY *= 6 / s; }
    }
    mWX = wx; mWY = wy; mLast = now; mHave = true;
  }
  window.addEventListener('mousemove', function (e) { pointerMove(e.clientX, e.clientY); });
  window.addEventListener('touchmove', function (e) {
    if (e.touches.length) pointerMove(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: true });

  function applyStir() {
    if (performance.now() - mLast > 120) return;
    var R = 0.12, R2 = R * R;
    for (var i = 0; i < n; i++) {
      var dx = px[i] - mWX, dy = py[i] - mWY;
      var d2 = dx * dx + dy * dy;
      if (d2 < R2) {
        var w = (1 - d2 / R2) * 0.25;
        vx[i] += (mVX - vx[i]) * w;
        vy[i] += (mVY - vy[i]) * w;
      }
    }
  }

  /* ── world → screen mapping ── */
  var scale = 1, offX = 0, offY = 0;
  function remap() {
    scale = Math.min(canvas.width / WORLD_W, canvas.height / WORLD_H) * 0.96;
    offX = (canvas.width - WORLD_W * scale) / 2;
    offY = (canvas.height - WORLD_H * scale) / 2;
  }
  function sx(x) { return offX + x * scale; }
  function sy(y) { return offY + (WORLD_H - y) * scale; }

  /* ── render ── */
  function render() {
    remap();
    ctx.fillStyle = 'rgb(8,10,18)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // container
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 1;
    ctx.strokeRect(sx(0), sy(WORLD_H), WORLD_W * scale, WORLD_H * scale);

    // the Eulerian grid we don't need (lagrangian panel)
    if (cfg.eulerGrid) {
      ctx.strokeStyle = 'rgba(120,140,220,0.07)';
      ctx.beginPath();
      for (var gx2 = 0.125; gx2 < WORLD_W; gx2 += 0.125) {
        ctx.moveTo(sx(gx2), sy(0)); ctx.lineTo(sx(gx2), sy(WORLD_H));
      }
      for (var gy2 = 0.125; gy2 < WORLD_H; gy2 += 0.125) {
        ctx.moveTo(sx(0), sy(gy2)); ctx.lineTo(sx(WORLD_W), sy(gy2));
      }
      ctx.stroke();
    }

    // occupied spatial-hash cells (grid panel)
    if (cfg.hashGrid) {
      ctx.strokeStyle = 'rgba(40,100,220,0.13)';
      var cs = H * scale;
      for (var c = 0; c < NC; c++) {
        if (cellStart[c + 1] > cellStart[c]) {
          var cy3 = (c / GX) | 0, cx3 = c - cy3 * GX;
          ctx.strokeRect(sx(cx3 * H), sy((cy3 + 1) * H), cs, cs);
        }
      }
      // one particle's 3×3 neighborhood + kernel radius
      if (n > 0) {
        var f = (n * 0.4) | 0;
        var fcx = cellX(px[f]), fcy = cellY(py[f]);
        ctx.strokeStyle = 'rgba(255,200,80,0.45)';
        ctx.strokeRect(sx((fcx - 1) * H), sy((fcy + 2) * H), 3 * cs, 3 * cs);
        ctx.beginPath();
        ctx.arc(sx(px[f]), sy(py[f]), H * scale, 0, 6.2832);
        ctx.stroke();
      }
    }

    var ramp2 = RAMPS[cfg.color];
    var pr = Math.max(1.5, SP * scale * 0.42);

    if (cfg.streaks) {
      ctx.lineWidth = Math.max(1, pr * 0.8);
      for (var i = 0; i < n; i++) {
        var t = colorT(i);
        var q = (t < 0 ? 0 : (t > 1 ? 1 : t)) * 47 | 0;
        ctx.strokeStyle = ramp2[q];
        ctx.beginPath();
        ctx.moveTo(sx(px[i]), sy(py[i]));
        ctx.lineTo(sx(px[i] - vx[i] * 0.035), sy(py[i] - vy[i] * 0.035));
        ctx.stroke();
        ctx.fillStyle = ramp2[q];
        ctx.fillRect(sx(px[i]) - 1, sy(py[i]) - 1, 2, 2);
      }
    } else {
      for (var i = 0; i < n; i++) {
        var t = colorT(i);
        var q = (t < 0 ? 0 : (t > 1 ? 1 : t)) * 47 | 0;
        ctx.fillStyle = ramp2[q];
        ctx.beginPath();
        ctx.arc(sx(px[i]), sy(py[i]), pr, 0, 6.2832);
        ctx.fill();
      }
    }

    // smoothing-length rings (kernel panel)
    if (cfg.rings) {
      ctx.strokeStyle = 'rgba(255,255,255,0.4)';
      ctx.lineWidth = 1;
      for (var r2 = 0; r2 < ringIdx.length; r2++) {
        var k2 = ringIdx[r2];
        if (k2 >= n) continue;
        ctx.beginPath();
        ctx.arc(sx(px[k2]), sy(py[k2]), H * scale, 0, 6.2832);
        ctx.stroke();
        ctx.fillStyle = '#fff';
        ctx.fillRect(sx(px[k2]) - 1.5, sy(py[k2]) - 1.5, 3, 3);
      }
    }

    statsEl.textContent = 'n = ' + n + '\n' + cfg.label + '\nstep  ' + stepMs.toFixed(2) + ' ms';
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

  var slowFrames = 0, lastT = performance.now();
  function animate() {
    var now = performance.now();
    modeT += Math.min((now - lastT) / 1000, 0.1);
    lastT = now;
    if (cfg.reset && modeT > cfg.reset) { cfg.init(); modeT = 0; }

    var t0 = performance.now();
    for (var s = 0; s < substeps; s++) {
      buildGrid();
      densityPressure();
      forces();
      integrate();
    }
    applyStir();
    stepMs = performance.now() - t0;

    // back off if this machine can't keep up
    if (stepMs > 24) { if (++slowFrames > 90 && substeps > 2) { substeps--; slowFrames = 0; } }
    else slowFrames = 0;

    render();
    requestAnimationFrame(animate);
  }
  animate();
})();
</script>
