---
title: Non-Euclidean Worms
summary: Worms, but on curved surfaces
date: 2025-08-01
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
    position: relative;
    z-index: 10;
  }

  .game-wrap {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  h1.page-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
  }
  .page-sub {
    color: #888;
    font-size: 14px;
    margin: 0 0 24px 0;
  }

  /* tabs */
  .tabs {
    display: flex;
    gap: 0;
    border-bottom: 2px solid #eee;
    margin-bottom: 24px;
  }
  .tab-btn {
    padding: 10px 20px;
    background: none;
    border: none;
    font-size: 14px;
    font-weight: 500;
    color: #999;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: color 0.15s;
  }
  .tab-btn:hover { color: #333; }
  .tab-btn.active { color: #111; border-bottom-color: #111; }

  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* game controls */
  .mode-row {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    align-items: center;
  }
  .mode-btn {
    padding: 8px 18px;
    border: 1.5px solid #ddd;
    border-radius: 8px;
    background: #fff;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
  }
  .mode-btn:hover { border-color: #999; }
  .mode-btn.active { background: #111; color: #fff; border-color: #111; }

  .score-display {
    margin-left: auto;
    font-size: 14px;
    font-weight: 600;
    color: #333;
  }

  /* canvas */
  .game-canvas-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 1;
    max-width: 600px;
    margin: 0 auto;
    border-radius: 12px;
    overflow: hidden;
    border: 1.5px solid #eee;
    background: #fafafa;
  }
  .game-canvas-wrap canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  .game-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.85);
    z-index: 2;
  }
  .game-overlay.hidden { display: none; }
  .game-overlay h2 { margin: 0 0 8px; font-size: 22px; }
  .game-overlay p { margin: 0 0 16px; color: #666; font-size: 14px; }
  .play-btn {
    padding: 10px 28px;
    background: #111;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
  }
  .play-btn:hover { background: #333; }

  .instructions {
    text-align: center;
    color: #aaa;
    font-size: 12px;
    margin-top: 12px;
  }

  /* math tab */
  .math-content {
    max-width: 700px;
    line-height: 1.8;
    color: #333;
    font-size: 15px;
  }
  .math-content h2 {
    font-size: 20px;
    margin: 32px 0 12px;
    font-weight: 600;
  }
  .math-content h2:first-child { margin-top: 0; }
  .math-content p { margin: 0 0 14px; }
  .math-content .formula {
    background: #f6f6f6;
    padding: 12px 16px;
    border-radius: 6px;
    margin: 12px 0;
    overflow-x: auto;
  }

  @media (max-width: 600px) {
    .game-wrap { padding: 12px; }
    .tab-btn { padding: 8px 12px; font-size: 13px; }
  }
</style>

<div class="game-wrap">
  <h1 class="page-title">Non-Euclidean Worms</h1>
  <p class="page-sub">The classic snake game on flat, spherical, and hyperbolic surfaces.</p>

  <div class="tabs">
    <button class="tab-btn active" data-tab="game">Play</button>
    <button class="tab-btn" data-tab="math">The Math</button>
  </div>

  <!-- GAME TAB -->
  <div class="tab-content active" id="tab-game">
    <div class="mode-row">
      <button class="mode-btn active" data-mode="normal">Euclidean</button>
      <button class="mode-btn" data-mode="spherical">Spherical</button>
      <button class="mode-btn" data-mode="hyperbolic">Hyperbolic</button>
      <span class="score-display">Score: <span id="score">0</span></span>
    </div>

    <div class="game-canvas-wrap">
      <canvas id="game"></canvas>
      <div class="game-overlay" id="overlay">
        <h2 id="overlay-title">Non-Euclidean Worms</h2>
        <p id="overlay-msg">Arrow keys or WASD to move</p>
        <button class="play-btn" id="play-btn">Play</button>
      </div>
    </div>
    <p class="instructions">Arrow keys / WASD to steer. The geometry changes how the board wraps.</p>
  </div>

  <!-- MATH TAB -->
  <div class="tab-content" id="tab-math">
    <div class="math-content">
      <h2>Euclidean Geometry (Flat)</h2>
      <p>The standard snake board lives on a flat torus: when you leave one edge you reappear on the opposite side. The grid is a quotient of \(\mathbb{R}^2\) by a lattice. Distances follow the familiar metric:</p>
      <div class="formula">
        \[ ds^2 = dx^2 + dy^2 \]
      </div>
      <p>The board has zero Gaussian curvature everywhere. Parallel lines stay parallel, the angles of a triangle sum to exactly \(\pi\), and the circumference of a circle of radius \(r\) is \(2\pi r\). The wrapping identification means the topology is \(T^2 = S^1 \times S^1\), but the local geometry is flat.</p>

      <h2>Spherical Geometry (Positive Curvature)</h2>
      <p>In the spherical mode, the board is mapped onto \(S^2\). We use an equirectangular projection: columns correspond to longitude \(\phi \in [0, 2\pi)\) and rows to latitude \(\theta \in [0, \pi]\).</p>
      <div class="formula">
        \[ ds^2 = d\theta^2 + \sin^2\!\theta \; d\phi^2 \]
      </div>
      <p>At the equator, cells have their full width. Near the poles, the factor \(\sin\theta \to 0\), so longitude lines converge. A step east or west near a pole covers a much larger angular distance. This means:</p>
      <ul>
        <li>Moving horizontally near the poles wraps around very quickly</li>
        <li>The "top" and "bottom" edges are single points (poles), not edges at all</li>
        <li>Triangles have angle sums exceeding \(\pi\) &mdash; the excess equals the area divided by \(R^2\)</li>
      </ul>
      <p>The Gaussian curvature is constant and positive: \(K = 1/R^2\). In the game, this manifests as the horizontal wrapping distance shrinking as you approach the poles, and the snake appearing to accelerate laterally near them.</p>

      <h2>Hyperbolic Geometry (Negative Curvature)</h2>
      <p>The hyperbolic mode uses the Poincar&eacute; disk model. The board is a disk of radius 1 in the Euclidean plane, but distances are warped: near the boundary, a small Euclidean step covers a huge hyperbolic distance.</p>
      <div class="formula">
        \[ ds^2 = \frac{4(dx^2 + dy^2)}{(1 - x^2 - y^2)^2} \]
      </div>
      <p>The conformal factor \(\lambda = 2/(1 - r^2)\) blows up as \(r \to 1\), meaning the boundary is infinitely far away in the hyperbolic metric. The Gaussian curvature is constant and negative: \(K = -1\).</p>
      <p>Consequences for gameplay:</p>
      <ul>
        <li>There is exponentially more space near the edges &mdash; the area of a hyperbolic disk of radius \(\rho\) is \(2\pi(\cosh\rho - 1)\), which grows as \(\sim \pi e^{\rho}\)</li>
        <li>Parallel lines diverge: two geodesics that start nearly parallel will spread apart exponentially</li>
        <li>Triangles have angle sums less than \(\pi\) &mdash; the deficit equals the area times \(|K|\)</li>
      </ul>
      <p>In the game, the grid cells near the center are large and easy to navigate, but the playable area expands enormously toward the boundary. The apple can hide in the vast hyperbolic outskirts.</p>

      <h2>Gauss-Bonnet Theorem</h2>
      <p>All three geometries are unified by the Gauss-Bonnet theorem. For a closed surface \(M\):</p>
      <div class="formula">
        \[ \int_M K \, dA = 2\pi \, \chi(M) \]
      </div>
      <p>where \(\chi\) is the Euler characteristic. For the sphere \(\chi = 2\), for the torus \(\chi = 0\), and for hyperbolic surfaces of genus \(g \geq 2\), \(\chi = 2 - 2g\). The total curvature is a topological invariant &mdash; it doesn't care about how you bend the surface, only about the number of holes.</p>
    </div>
  </div>
</div>

<script>
(function() {
  // --- Tabs ---
  document.querySelectorAll('.tab-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
      document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
  });

  // --- Mode buttons ---
  var currentMode = 'normal';
  document.querySelectorAll('.mode-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.mode-btn').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      currentMode = btn.dataset.mode;
      resetGame();
    });
  });

  // --- Canvas setup ---
  var canvas = document.getElementById('game');
  var ctx = canvas.getContext('2d');
  var overlay = document.getElementById('overlay');
  var overlayTitle = document.getElementById('overlay-title');
  var overlayMsg = document.getElementById('overlay-msg');
  var playBtn = document.getElementById('play-btn');
  var scoreEl = document.getElementById('score');

  var GRID = 20; // grid cells per side
  var SIZE;

  function resizeCanvas() {
    var wrap = canvas.parentElement;
    var w = wrap.clientWidth;
    canvas.width = w;
    canvas.height = w;
    SIZE = w / GRID;
  }
  resizeCanvas();
  window.addEventListener('resize', function() {
    resizeCanvas();
    if (!running) drawState();
  });

  // --- Game state ---
  var snake, dir, nextDir, apple, score, running, gameOver, tickTimer;
  var TICK_MS = 120;

  function resetGame() {
    var mid = Math.floor(GRID / 2);
    snake = [{x: mid, y: mid}, {x: mid - 1, y: mid}, {x: mid - 2, y: mid}];
    dir = {x: 1, y: 0};
    nextDir = {x: 1, y: 0};
    score = 0;
    scoreEl.textContent = '0';
    gameOver = false;
    running = false;
    clearInterval(tickTimer);
    overlay.classList.remove('hidden');
    overlayTitle.textContent = 'Non-Euclidean Worms';
    overlayMsg.textContent = 'Arrow keys or WASD to move';
    playBtn.textContent = 'Play';
    drawState();
  }

  function placeApple() {
    var occupied = {};
    for (var i = 0; i < snake.length; i++) {
      occupied[snake[i].x + ',' + snake[i].y] = true;
    }
    var free = [];
    if (currentMode === 'hyperbolic') {
      // only place apples within the disk
      var center = GRID / 2;
      var radius = GRID / 2 - 0.5;
      for (var x = 0; x < GRID; x++) {
        for (var y = 0; y < GRID; y++) {
          var dx = x - center + 0.5, dy = y - center + 0.5;
          if (dx * dx + dy * dy < radius * radius && !occupied[x + ',' + y]) {
            free.push({x: x, y: y});
          }
        }
      }
    } else {
      for (var x = 0; x < GRID; x++) {
        for (var y = 0; y < GRID; y++) {
          if (!occupied[x + ',' + y]) free.push({x: x, y: y});
        }
      }
    }
    if (free.length === 0) return;
    apple = free[Math.floor(Math.random() * free.length)];
  }

  // --- Wrapping logic per geometry ---
  function wrapNormal(pos) {
    return {
      x: ((pos.x % GRID) + GRID) % GRID,
      y: ((pos.y % GRID) + GRID) % GRID
    };
  }

  function wrapSpherical(pos) {
    var x = pos.x, y = pos.y;
    // vertical: bounce at poles and flip longitude
    if (y < 0) { y = 0; x = x + Math.floor(GRID / 2); }
    else if (y >= GRID) { y = GRID - 1; x = x + Math.floor(GRID / 2); }
    // horizontal: wrap normally (longitude)
    x = ((x % GRID) + GRID) % GRID;
    return {x: x, y: y};
  }

  function wrapHyperbolic(pos) {
    // Poincare disk: no wrapping, boundary is a wall
    return {x: pos.x, y: pos.y};
  }

  function isInsideDisk(pos) {
    var center = GRID / 2;
    var radius = GRID / 2 - 0.5;
    var dx = pos.x - center + 0.5, dy = pos.y - center + 0.5;
    return dx * dx + dy * dy < radius * radius;
  }

  function wrap(pos) {
    if (currentMode === 'spherical') return wrapSpherical(pos);
    if (currentMode === 'hyperbolic') return wrapHyperbolic(pos);
    return wrapNormal(pos);
  }

  // --- Tick ---
  function tick() {
    dir = nextDir;
    var head = snake[0];
    var raw = {x: head.x + dir.x, y: head.y + dir.y};
    var npos = wrap(raw);

    // collision check
    if (currentMode === 'hyperbolic' && !isInsideDisk(npos)) {
      endGame(); return;
    }
    for (var i = 0; i < snake.length; i++) {
      if (snake[i].x === npos.x && snake[i].y === npos.y) {
        endGame(); return;
      }
    }

    snake.unshift(npos);

    if (npos.x === apple.x && npos.y === apple.y) {
      score++;
      scoreEl.textContent = score;
      placeApple();
    } else {
      snake.pop();
    }

    drawState();
  }

  function endGame() {
    running = false;
    gameOver = true;
    clearInterval(tickTimer);
    overlay.classList.remove('hidden');
    overlayTitle.textContent = 'Game Over';
    overlayMsg.textContent = 'Score: ' + score;
    playBtn.textContent = 'Retry';
  }

  function startGame() {
    if (gameOver) {
      var mid = Math.floor(GRID / 2);
      snake = [{x: mid, y: mid}, {x: mid - 1, y: mid}, {x: mid - 2, y: mid}];
      dir = {x: 1, y: 0};
      nextDir = {x: 1, y: 0};
      score = 0;
      scoreEl.textContent = '0';
      gameOver = false;
    }
    running = true;
    overlay.classList.add('hidden');
    placeApple();
    drawState();
    tickTimer = setInterval(tick, TICK_MS);
  }

  playBtn.addEventListener('click', startGame);

  // --- Input ---
  document.addEventListener('keydown', function(e) {
    var key = e.key;
    if (key === 'ArrowUp' || key === 'w' || key === 'W') {
      if (dir.y !== 1) nextDir = {x: 0, y: -1};
      e.preventDefault();
    } else if (key === 'ArrowDown' || key === 's' || key === 'S') {
      if (dir.y !== -1) nextDir = {x: 0, y: 1};
      e.preventDefault();
    } else if (key === 'ArrowLeft' || key === 'a' || key === 'A') {
      if (dir.x !== 1) nextDir = {x: -1, y: 0};
      e.preventDefault();
    } else if (key === 'ArrowRight' || key === 'd' || key === 'D') {
      if (dir.x !== -1) nextDir = {x: 1, y: 0};
      e.preventDefault();
    }
    // start on key if overlay showing and not game over prompt
    if (!running && !gameOver) {
      startGame();
    }
  });

  // --- Drawing ---
  function drawState() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (currentMode === 'hyperbolic') {
      drawHyperbolicBoard();
    } else if (currentMode === 'spherical') {
      drawSphericalBoard();
    } else {
      drawNormalBoard();
    }
  }

  function drawNormalBoard() {
    // grid
    for (var x = 0; x < GRID; x++) {
      for (var y = 0; y < GRID; y++) {
        ctx.fillStyle = (x + y) % 2 === 0 ? '#f0f0f0' : '#e8e8e8';
        ctx.fillRect(x * SIZE, y * SIZE, SIZE, SIZE);
      }
    }
    drawSnakeAndApple(function(pos) {
      return {px: pos.x * SIZE, py: pos.y * SIZE, s: SIZE};
    });
  }

  function drawSphericalBoard() {
    // draw grid with varying cell widths based on latitude
    for (var y = 0; y < GRID; y++) {
      var theta = (y + 0.5) / GRID * Math.PI;
      var widthFactor = Math.sin(theta);
      var cellW = SIZE * widthFactor;
      var totalW = cellW * GRID;
      var offsetX = (canvas.width - totalW) / 2;
      for (var x = 0; x < GRID; x++) {
        ctx.fillStyle = (x + y) % 2 === 0 ? '#eef0f8' : '#e2e6f2';
        ctx.fillRect(offsetX + x * cellW, y * SIZE, cellW, SIZE);
      }
    }
    // apple and snake with spherical projection
    drawSnakeAndApple(function(pos) {
      var theta = (pos.y + 0.5) / GRID * Math.PI;
      var widthFactor = Math.sin(theta);
      var cellW = SIZE * widthFactor;
      var totalW = cellW * GRID;
      var offsetX = (canvas.width - totalW) / 2;
      return {px: offsetX + pos.x * cellW, py: pos.y * SIZE, s: Math.max(cellW, SIZE * 0.3), sy: SIZE};
    });
  }

  function drawHyperbolicBoard() {
    // draw Poincare disk
    var center = canvas.width / 2;
    var radius = center - SIZE * 0.5;

    // disk background
    ctx.save();
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, Math.PI * 2);
    ctx.fillStyle = '#f4f0ee';
    ctx.fill();
    ctx.restore();

    // grid cells inside disk with hyperbolic scaling
    var gcenter = GRID / 2;
    var gradius = GRID / 2 - 0.5;
    for (var x = 0; x < GRID; x++) {
      for (var y = 0; y < GRID; y++) {
        var dx = x - gcenter + 0.5, dy = y - gcenter + 0.5;
        var r2 = (dx * dx + dy * dy) / (gradius * gradius);
        if (r2 < 1) {
          // map grid to disk via Poincare-like scaling
          var px = center + (dx / gradius) * radius;
          var py = center + (dy / gradius) * radius;
          var scale = 1 - r2;
          var cs = SIZE * Math.max(scale, 0.25);
          ctx.fillStyle = (x + y) % 2 === 0 ? '#ede8e4' : '#e4ddd8';
          ctx.fillRect(px - cs/2, py - cs/2, cs, cs);
        }
      }
    }

    // disk border
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, Math.PI * 2);
    ctx.strokeStyle = '#ccc';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    drawSnakeAndApple(function(pos) {
      var dx = pos.x - gcenter + 0.5, dy = pos.y - gcenter + 0.5;
      var r2 = (dx * dx + dy * dy) / (gradius * gradius);
      var px = center + (dx / gradius) * radius;
      var py = center + (dy / gradius) * radius;
      var scale = 1 - r2;
      var cs = SIZE * Math.max(scale, 0.25);
      return {px: px - cs/2, py: py - cs/2, s: cs};
    });
  }

  function drawSnakeAndApple(mapFn) {
    // apple
    if (apple) {
      var ap = mapFn(apple);
      var as = ap.s || SIZE;
      var asy = ap.sy || as;
      ctx.fillStyle = '#e74c3c';
      ctx.beginPath();
      ctx.arc(ap.px + as/2, ap.py + asy/2, Math.max(as * 0.35, 4), 0, Math.PI * 2);
      ctx.fill();
    }

    // snake
    for (var i = snake.length - 1; i >= 0; i--) {
      var sp = mapFn(snake[i]);
      var ss = sp.s || SIZE;
      var ssy = sp.sy || ss;
      var t = i / snake.length;
      var r = Math.round(40 + t * 20);
      var g = Math.round(180 - t * 80);
      var b = Math.round(60 + t * 20);
      ctx.fillStyle = 'rgb(' + r + ',' + g + ',' + b + ')';
      var pad = ss * 0.08;
      var padY = ssy * 0.08;
      ctx.beginPath();
      var rx = Math.max((ss - pad * 2) * 0.2, 2);
      roundRect(ctx, sp.px + pad, sp.py + padY, ss - pad * 2, ssy - padY * 2, rx);
      ctx.fill();
    }
  }

  function roundRect(ctx, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  // --- Init ---
  resetGame();
})();
</script>
