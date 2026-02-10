---
title: Non-Euclidean Worms
summary: Worms, but on curved surfaces
date: 2024-12-01
layout: default
status: closed
published: true
image: worms.png
---

<style>
  body > main { max-width: none !important; margin: 0 !important; padding: 0 !important; }
  header { position: relative; z-index: 10; }

  .gw { max-width: 900px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  h1.pt { font-size: 32px; font-weight: 700; margin: 0 0 6px; letter-spacing: -0.5px; color: #e8e8e8; }
  .ps { color: #888; font-size: 14px; margin: 0 0 24px; }

  .mode-row { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; align-items: center; }
  .mode-btn { padding: 8px 16px; border: 1.5px solid #333; border-radius: 8px; background: #1a1a1a; color: #999; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s; }
  .mode-btn:hover { border-color: #666; color: #ccc; }
  .mode-btn.active { background: #e8e8e8; color: #111; border-color: #e8e8e8; }
  .sc { margin-left: auto; font-size: 14px; font-weight: 600; color: #aaa; }

  .cw { position: relative; width: 100%; max-width: 600px; margin: 0 auto; }
  .cw canvas { width: 100%; display: block; border-radius: 4px; }
  .ov { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(0,0,0,0.75); z-index: 2; border-radius: 4px; }
  .ov.hidden { display: none; }
  .ov h2 { margin: 0 0 8px; font-size: 22px; color: #e8e8e8; }
  .ov p { margin: 0 0 16px; color: #888; font-size: 13px; }
  .pbtn { padding: 10px 28px; background: #e8e8e8; color: #111; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; font-weight: 500; }
  .pbtn:hover { background: #fff; }
  .inst { text-align: center; color: #666; font-size: 12px; margin-top: 10px; }
  .k-display { text-align: center; color: #888; font-size: 13px; margin-top: 6px; font-family: 'SF Mono', monospace; }

  .math-section { max-width: 700px; margin: 60px auto 0; padding: 0 20px 40px; line-height: 1.8; color: #bbb; font-size: 15px; }
  .math-section h2 { font-size: 20px; margin: 36px 0 12px; font-weight: 600; color: #e8e8e8; }
  .math-section h2:first-child { margin-top: 0; }
  .math-section p { margin: 0 0 14px; }
  .math-section ul { margin: 0 0 14px; padding-left: 20px; }
  .math-section li { margin-bottom: 6px; }
  .formula { background: #1a1a1a; padding: 12px 16px; border-radius: 6px; margin: 12px 0; overflow-x: auto; border: 1px solid #222; }

  @media (max-width: 600px) { .gw { padding: 12px; } }
</style>

<div class="gw">
  <h1 class="pt">Non-Euclidean Worms</h1>
  <p class="ps">The classic snake game on flat, spherical, hyperbolic, and dynamically curved surfaces.</p>

  <div class="mode-row">
    <button class="mode-btn active" data-mode="euclidean">Euclidean</button>
    <button class="mode-btn" data-mode="spherical">Spherical</button>
    <button class="mode-btn" data-mode="hyperbolic">Hyperbolic</button>
    <button class="mode-btn" data-mode="dynamic">Dynamic</button>
    <span class="sc">Score: <span id="score">0</span></span>
  </div>

  <div class="cw">
    <canvas id="game" width="600" height="600"></canvas>
    <div class="ov" id="overlay">
      <h2 id="ot">Non-Euclidean Worms</h2>
      <p id="om">Arrow keys to move</p>
      <button class="pbtn" id="pbtn">Play</button>
    </div>
  </div>
  <p class="inst" id="inst">Arrow keys to steer.</p>
  <p class="k-display hidden" id="kdisp"></p>
</div>

<div class="math-section">
  <h2>Euclidean Geometry (Flat)</h2>
  <p>The Euclidean board lives inside a disk. The worm moves at constant speed in a flat plane. Distances follow the familiar metric:</p>
  <div class="formula">\[ ds^2 = dx^2 + dy^2 \]</div>
  <p>Gaussian curvature is zero everywhere. Parallel lines stay parallel, triangle angles sum to exactly \(\pi\), and the circumference of a circle of radius \(r\) is \(2\pi r\). The boundary is a hard wall.</p>

  <h2>Spherical Geometry (Positive Curvature)</h2>
  <p>The spherical board maps the game onto \(S^2\), rendered via orthographic projection. The worm travels along lines of latitude and longitude. The metric on the sphere is:</p>
  <div class="formula">\[ ds^2 = d\theta^2 + \sin^2\!\theta \; d\phi^2 \]</div>
  <p>At the equator, cells have full width. Near the poles, the factor \(\sin\theta \to 0\) and longitude lines converge. The poles are singularities &mdash; reaching one kills the worm. The Gaussian curvature is constant: \(K = 1/R^2\).</p>
  <ul>
    <li>Triangles have angle sums exceeding \(\pi\); the excess equals \(\text{Area}/R^2\)</li>
    <li>The "top" and "bottom" are single points (poles), not edges</li>
    <li>Use WASD to rotate the camera, arrow keys to steer the worm</li>
  </ul>

  <h2>Hyperbolic Geometry (Negative Curvature)</h2>
  <p>The hyperbolic board uses the Poincar&eacute; disk model. The worm moves continuously forward; steer with left/right arrows. The metric is:</p>
  <div class="formula">\[ ds^2 = \frac{4(dx^2 + dy^2)}{(1 - x^2 - y^2)^2} \]</div>
  <p>The conformal factor \(\lambda = 2/(1 - r^2)\) diverges at the boundary, meaning the boundary is infinitely far away in hyperbolic distance. Curvature is constant: \(K = -1\).</p>
  <ul>
    <li>Exponentially more space near the edge &mdash; area of a hyperbolic disk of radius \(\rho\) is \(2\pi(\cosh\rho - 1) \sim \pi e^{\rho}\)</li>
    <li>Geodesics are arcs of circles orthogonal to the boundary</li>
    <li>Triangles have angle sums less than \(\pi\)</li>
  </ul>

  <h2>Dynamic Curvature</h2>
  <p>The dynamic mode starts flat (\(K=0\)) and changes curvature when the worm eats colored apples. Blue apples decrease \(K\) (more hyperbolic), yellow apples increase \(K\) (more spherical), and red apples just grow the worm.</p>
  <p>The movement metric interpolates continuously. For \(K < 0\) the worm slows near the boundary (hyperbolic drag); for \(K > 0\) it accelerates (spherical expansion). Concentric circles on the board show equal geodesic distances, which compress or expand as curvature shifts.</p>
  <div class="formula">\[ r_{\text{euclidean}} = \begin{cases} \tanh(\rho/2) / \sqrt{|K|} & K < 0 \\ \rho & K = 0 \\ \tan(\rho/2) / \sqrt{K} & K > 0 \end{cases} \]</div>

  <h2>Gauss-Bonnet Theorem</h2>
  <p>All three constant-curvature geometries are unified by the Gauss-Bonnet theorem. For a closed surface \(M\):</p>
  <div class="formula">\[ \int_M K \, dA = 2\pi \, \chi(M) \]</div>
  <p>where \(\chi\) is the Euler characteristic. For the sphere \(\chi = 2\), for the torus \(\chi = 0\), and for hyperbolic surfaces of genus \(g \geq 2\), \(\chi = 2 - 2g\). The total curvature is a topological invariant.</p>
</div>

<script>
(function(){
var canvas = document.getElementById('game');
var ctx = canvas.getContext('2d');
var overlay = document.getElementById('overlay');
var otEl = document.getElementById('ot');
var omEl = document.getElementById('om');
var pbtnEl = document.getElementById('pbtn');
var scoreEl = document.getElementById('score');
var instEl = document.getElementById('inst');
var kdispEl = document.getElementById('kdisp');

var W = 600, H = 600, CX = 300, CY = 300, CR = 270;

function resizeCanvas(){
  var wrap = canvas.parentElement;
  var w = wrap.clientWidth;
  canvas.style.width = w + 'px';
  canvas.style.height = w + 'px';
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// State
var mode = 'euclidean';
var snake, snakeDir, snakeSpeed, score, running, gameOver, food, K;
var phi0, lam0; // sphere camera
var SEG_R = 4, FOOD_R = 6;
var appleType, appleTypes = {normal:'#e74c3c', blue:'#3498db', yellow:'#f1c40f'};

// Mode buttons
document.querySelectorAll('.mode-btn').forEach(function(b){
  b.addEventListener('click', function(){
    document.querySelectorAll('.mode-btn').forEach(function(x){x.classList.remove('active');});
    b.classList.add('active');
    mode = b.dataset.mode;
    resetGame();
  });
});

function resetGame(){
  snake = [];
  score = 0; scoreEl.textContent = '0';
  gameOver = false; running = false;
  K = 0; appleType = 'normal';
  phi0 = -Math.PI/6; lam0 = 0;

  if(mode === 'euclidean'){
    snakeSpeed = 1.5; snakeDir = 0;
    for(var i=0;i<15;i++) snake.push([CX - i*snakeSpeed, CY]);
    instEl.textContent = 'Arrow keys to steer.';
    kdispEl.classList.add('hidden');
  } else if(mode === 'spherical'){
    snakeSpeed = 0.01; snakeDir = 0;
    // phi, lambda pairs; start on equator
    for(var i=0;i<20;i++) snake.push([0, i*0.08]);
    instEl.textContent = 'Arrows to steer worm. WASD to rotate camera.';
    kdispEl.classList.add('hidden');
  } else if(mode === 'hyperbolic'){
    snakeSpeed = 0.008; snakeDir = Math.PI/2;
    for(var i=0;i<15;i++) snake.push([0, -i*0.02]);
    instEl.textContent = 'Left/Right to steer. Auto-moves forward.';
    kdispEl.classList.add('hidden');
  } else {
    snakeSpeed = 0.008; snakeDir = Math.PI/2; K = 0;
    for(var i=0;i<15;i++) snake.push([0, -i*0.02]);
    instEl.textContent = 'Left/Right to steer. Eat colored apples to bend space.';
    kdispEl.classList.remove('hidden');
    kdispEl.textContent = 'K = 0.00 (flat)';
  }

  food = null;
  overlay.classList.remove('hidden');
  otEl.textContent = mode.charAt(0).toUpperCase()+mode.slice(1) + ' Worms';
  omEl.textContent = instEl.textContent;
  pbtnEl.textContent = 'Play';
  draw();
}

function spawnFood(){
  if(mode === 'euclidean'){
    var a = Math.random()*Math.PI*2, r = Math.random()*(CR-20);
    food = [CX + r*Math.cos(a), CY + r*Math.sin(a)];
    appleType = 'normal';
  } else if(mode === 'spherical'){
    food = [Math.random()*Math.PI - Math.PI/2, Math.random()*Math.PI*2];
    appleType = 'normal';
  } else if(mode === 'hyperbolic'){
    var r = Math.pow(Math.random(), 0.3) * 0.85;
    var a = Math.random()*Math.PI*2;
    food = [r*Math.cos(a), r*Math.sin(a)];
    appleType = 'normal';
  } else {
    var r = Math.pow(Math.random(), 0.3) * 0.85;
    var a = Math.random()*Math.PI*2;
    food = [r*Math.cos(a), r*Math.sin(a)];
    var rn = Math.random();
    appleType = rn < 0.4 ? 'normal' : rn < 0.7 ? 'blue' : 'yellow';
  }
}

function startGame(){
  if(gameOver) resetGame();
  running = true;
  overlay.classList.add('hidden');
  spawnFood();
  draw();
  requestAnimationFrame(loop);
}
pbtnEl.addEventListener('click', startGame);

// Input
var keys = {};
document.addEventListener('keydown', function(e){
  keys[e.key] = true;
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.key)>=0) e.preventDefault();
  if(!running && !gameOver) startGame();
});
document.addEventListener('keyup', function(e){ keys[e.key] = false; });

// Sphere helpers
var sphereAxis = 'lon', sphereConst = 0;
function projSphere(phi, lam){
  var x = CR * Math.cos(phi) * Math.sin(lam - lam0);
  var y = CR * (Math.cos(phi0)*Math.sin(phi) - Math.sin(phi0)*Math.cos(phi)*Math.cos(lam - lam0));
  var z = CR * Math.cos(phi) * Math.cos(lam - lam0);
  return [CX + x, CY - y, z];
}

function p2s(x, y){ return [CX + x*CR, CY - y*CR]; }

// Game loop
var lastTime = 0;
function loop(ts){
  if(!running) return;
  var dt = Math.min(ts - lastTime, 33);
  lastTime = ts;
  update();
  draw();
  requestAnimationFrame(loop);
}

function update(){
  if(mode === 'euclidean') updateEuc();
  else if(mode === 'spherical') updateSphere();
  else if(mode === 'hyperbolic') updateHyp();
  else updateDynamic();
}

function updateEuc(){
  if(keys['ArrowUp'] && snakeDir !== Math.PI/2) snakeDir = -Math.PI/2;
  if(keys['ArrowDown'] && snakeDir !== -Math.PI/2) snakeDir = Math.PI/2;
  if(keys['ArrowLeft'] && snakeDir !== 0) snakeDir = Math.PI;
  if(keys['ArrowRight'] && snakeDir !== Math.PI) snakeDir = 0;

  var hx = snake[0][0] + Math.cos(snakeDir)*snakeSpeed;
  var hy = snake[0][1] + Math.sin(snakeDir)*snakeSpeed;

  // boundary
  var dx = hx-CX, dy = hy-CY;
  if(dx*dx+dy*dy > CR*CR){ endGame(); return; }
  // self collision
  for(var i=10;i<snake.length;i++){
    var sx=snake[i][0]-hx, sy=snake[i][1]-hy;
    if(sx*sx+sy*sy < SEG_R*SEG_R*3){ endGame(); return; }
  }

  snake.unshift([hx, hy]);
  // food check
  if(food){
    var fx=food[0]-hx, fy=food[1]-hy;
    if(fx*fx+fy*fy < (FOOD_R+SEG_R)*(FOOD_R+SEG_R)){
      score++; scoreEl.textContent = score;
      spawnFood();
    } else {
      snake.pop();
    }
  } else snake.pop();
}

function updateSphere(){
  // camera
  if(keys['w']||keys['W']) phi0 = Math.max(-Math.PI/2, phi0 - 0.03);
  if(keys['s']||keys['S']) phi0 = Math.min(Math.PI/2, phi0 + 0.03);
  if(keys['a']||keys['A']) lam0 -= 0.03;
  if(keys['d']||keys['D']) lam0 += 0.03;

  // worm direction
  if(keys['ArrowUp']){ sphereAxis='lat'; snakeSpeed = Math.abs(snakeSpeed); sphereConst = snake[0][1]; }
  if(keys['ArrowDown']){ sphereAxis='lat'; snakeSpeed = -Math.abs(snakeSpeed); sphereConst = snake[0][1]; }
  if(keys['ArrowLeft']){ sphereAxis='lon'; snakeSpeed = Math.abs(snakeSpeed); sphereConst = snake[0][0]; }
  if(keys['ArrowRight']){ sphereAxis='lon'; snakeSpeed = -Math.abs(snakeSpeed); sphereConst = snake[0][0]; }

  var hp = snake[0][0], hl = snake[0][1];
  if(sphereAxis === 'lon'){
    hp = sphereConst;
    hl = (hl + snakeSpeed) % (Math.PI*2);
    if(hl<0) hl += Math.PI*2;
  } else {
    hp = hp + snakeSpeed;
    hl = sphereConst;
  }

  // pole death
  if(Math.abs(hp) >= Math.PI/2 - 0.03){ endGame(); return; }

  snake.unshift([hp, hl]);
  // food
  if(food){
    var dp = snake[0][0]-food[0], dl = snake[0][1]-food[1];
    if(dp*dp+dl*dl < 0.02){
      score++; scoreEl.textContent = score;
      spawnFood();
    } else snake.pop();
  } else snake.pop();
}

function updateHyp(){
  if(keys['ArrowLeft']) snakeDir += 0.06;
  if(keys['ArrowRight']) snakeDir -= 0.06;

  var hx = snake[0][0], hy = snake[0][1];
  var r2 = hx*hx + hy*hy;
  var norm = (1 - r2); norm = norm*norm;
  var dx = snakeSpeed * Math.cos(snakeDir) * norm;
  var dy = snakeSpeed * Math.sin(snakeDir) * norm;
  var nx = hx+dx, ny = hy+dy;

  if(nx*nx+ny*ny >= 0.98){
    var sc = 0.97 / Math.sqrt(nx*nx+ny*ny);
    nx *= sc; ny *= sc;
  }
  // self
  for(var i=8;i<snake.length;i++){
    var sx=snake[i][0]-nx, sy=snake[i][1]-ny;
    if(sx*sx+sy*sy < 0.0004){ endGame(); return; }
  }

  snake.unshift([nx, ny]);
  if(food){
    var fx=food[0]-nx, fy=food[1]-ny;
    if(fx*fx+fy*fy < 0.003){
      score++; scoreEl.textContent = score;
      spawnFood();
    } else snake.pop();
  } else snake.pop();
}

function updateDynamic(){
  if(keys['ArrowLeft']) snakeDir += 0.06;
  if(keys['ArrowRight']) snakeDir -= 0.06;

  var hx = snake[0][0], hy = snake[0][1];
  var r2 = hx*hx + hy*hy;
  var norm;
  if(K < 0) norm = (1 - r2) / Math.abs(K || 1);
  else if(K > 0) norm = (1 + r2) / (K || 1);
  else norm = 1;

  var dx = snakeSpeed * Math.cos(snakeDir) * norm;
  var dy = snakeSpeed * Math.sin(snakeDir) * norm;
  var nx = hx+dx, ny = hy+dy;

  if(nx*nx+ny*ny >= 0.98 && K <= 0){ endGame(); return; }
  // wrap for spherical-ish
  if(K > 0 && nx*nx+ny*ny >= 0.98){
    nx = -nx*0.9; ny = -ny*0.9;
  }

  for(var i=8;i<snake.length;i++){
    var sx=snake[i][0]-nx, sy=snake[i][1]-ny;
    if(sx*sx+sy*sy < 0.0004){ endGame(); return; }
  }

  snake.unshift([nx, ny]);
  if(food){
    var fx=food[0]-nx, fy=food[1]-ny;
    if(fx*fx+fy*fy < 0.003){
      if(appleType === 'normal') { /* just grow */ }
      else if(appleType === 'blue') K = Math.max(K - 0.5, -3);
      else if(appleType === 'yellow') K = Math.min(K + 0.5, 3);
      score++; scoreEl.textContent = score;
      var label = K < -0.1 ? 'hyperbolic' : K > 0.1 ? 'spherical' : 'flat';
      kdispEl.textContent = 'K = ' + K.toFixed(2) + ' (' + label + ')';
      spawnFood();
    } else snake.pop();
  } else snake.pop();
}

function endGame(){
  running = false; gameOver = true;
  overlay.classList.remove('hidden');
  otEl.textContent = 'Game Over';
  omEl.textContent = 'Score: ' + score;
  pbtnEl.textContent = 'Retry';
}

// Drawing
function draw(){
  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0,0,W,H);

  if(mode === 'euclidean') drawEuc();
  else if(mode === 'spherical') drawSphere();
  else if(mode === 'hyperbolic') drawHyp();
  else drawDynamic();
}

function drawEuc(){
  // grid
  ctx.strokeStyle = 'rgba(255,255,255,0.06)';
  ctx.lineWidth = 0.5;
  for(var i=0;i<=W;i+=40){
    ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(W,i); ctx.stroke();
  }
  // boundary
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.strokeStyle = 'rgba(80,80,255,0.4)'; ctx.lineWidth = 1.5; ctx.stroke();
  // food
  if(food){
    ctx.beginPath(); ctx.arc(food[0],food[1],FOOD_R,0,Math.PI*2);
    ctx.fillStyle = '#e74c3c'; ctx.fill();
  }
  // snake
  drawSnakeEuc();
}

function drawSnakeEuc(){
  for(var i=snake.length-1;i>=0;i--){
    var t = i/snake.length;
    var r = Math.round(30+t*30), g = Math.round(220-t*120), b = Math.round(60+t*30);
    ctx.beginPath(); ctx.arc(snake[i][0], snake[i][1], SEG_R, 0, Math.PI*2);
    ctx.fillStyle = 'rgb('+r+','+g+','+b+')';
    ctx.fill();
  }
}

function drawSphere(){
  // filled sphere bg
  var grad = ctx.createRadialGradient(CX-40, CY-40, 10, CX, CY, CR);
  grad.addColorStop(0, '#3a3a70');
  grad.addColorStop(1, '#1a1a40');
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.fillStyle = grad; ctx.fill();

  // lat lines
  for(var li=-5;li<=5;li++){
    var phi = li * Math.PI/12;
    ctx.beginPath();
    for(var j=0;j<=360;j++){
      var lam = j*Math.PI/180;
      var p = projSphere(phi, lam);
      if(j===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]);
    }
    var bright = 40;
    ctx.strokeStyle = 'rgba(60,60,180,0.25)'; ctx.lineWidth = 0.5; ctx.stroke();
  }
  // lon lines
  for(var li=0;li<12;li++){
    var lam = li * Math.PI/6;
    ctx.beginPath();
    for(var j=-90;j<=90;j++){
      var phi = j*Math.PI/180;
      var p = projSphere(phi, lam);
      if(j===-90) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]);
    }
    ctx.strokeStyle = 'rgba(60,60,180,0.25)'; ctx.lineWidth = 0.5; ctx.stroke();
  }

  // food
  if(food){
    var fp = projSphere(food[0], food[1]);
    ctx.beginPath(); ctx.arc(fp[0], fp[1], 5, 0, Math.PI*2);
    ctx.fillStyle = '#e74c3c'; ctx.fill();
  }

  // snake
  for(var i=snake.length-1;i>=0;i--){
    var p = projSphere(snake[i][0], snake[i][1]);
    var t = i/snake.length;
    var r = Math.round(30+t*30), g = Math.round(220-t*120), b = Math.round(60+t*30);
    ctx.beginPath(); ctx.arc(p[0], p[1], 3.5, 0, Math.PI*2);
    ctx.fillStyle = 'rgb('+r+','+g+','+b+')'; ctx.fill();
  }

  // boundary
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.strokeStyle = 'rgba(100,100,255,0.3)'; ctx.lineWidth = 1; ctx.stroke();
}

function drawHyp(){
  // disk bg
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.fillStyle = '#0d0d0d'; ctx.fill();

  // geodesic grid (radial lines + orthogonal arcs)
  ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 0.5;
  for(var a=0;a<360;a+=45){
    var rad = a*Math.PI/180;
    ctx.beginPath();
    ctx.moveTo(CX, CY);
    ctx.lineTo(CX + Math.cos(rad)*CR, CY - Math.sin(rad)*CR);
    ctx.stroke();
  }
  // concentric hyperbolic circles
  for(var ri=1;ri<=8;ri++){
    var rh = ri * 0.4;
    var re = Math.tanh(rh/2);
    if(re >= 1) break;
    ctx.beginPath(); ctx.arc(CX, CY, re*CR, 0, Math.PI*2);
    var alpha = 0.12 * (1 - re);
    ctx.strokeStyle = 'rgba(255,255,255,'+alpha+')'; ctx.stroke();
  }

  // boundary
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1.5; ctx.stroke();

  // food
  if(food){
    var fs = p2s(food[0], food[1]);
    ctx.beginPath(); ctx.arc(fs[0], fs[1], 5, 0, Math.PI*2);
    ctx.fillStyle = '#e74c3c'; ctx.fill();
  }

  // snake
  for(var i=snake.length-1;i>=0;i--){
    var s = p2s(snake[i][0], snake[i][1]);
    var t = i/snake.length;
    var r = Math.round(30+t*30), g = Math.round(220-t*120), b = Math.round(60+t*30);
    ctx.beginPath(); ctx.arc(s[0], s[1], 3, 0, Math.PI*2);
    ctx.fillStyle = 'rgb('+r+','+g+','+b+')'; ctx.fill();
  }
}

function drawDynamic(){
  // disk bg
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.fillStyle = '#0d0d0d'; ctx.fill();

  // concentric circles based on curvature
  ctx.lineWidth = 0.5;
  for(var ri=1;ri<=12;ri++){
    var rh = ri * 0.3;
    var re;
    if(K < -0.01) re = Math.tanh(rh/2) / Math.sqrt(Math.abs(K));
    else if(K > 0.01) re = Math.min(Math.tan(rh/2) / Math.sqrt(K), 2);
    else re = rh / 2;
    if(re >= 1) break;
    ctx.beginPath(); ctx.arc(CX, CY, re*CR, 0, Math.PI*2);
    var alpha = 0.1 * (1 - re);
    // color by curvature
    if(K < -0.1) ctx.strokeStyle = 'rgba(80,80,255,'+alpha+')';
    else if(K > 0.1) ctx.strokeStyle = 'rgba(255,200,50,'+alpha+')';
    else ctx.strokeStyle = 'rgba(255,255,255,'+alpha+')';
    ctx.stroke();
  }

  // radial lines
  ctx.strokeStyle = 'rgba(255,255,255,0.04)'; ctx.lineWidth = 0.5;
  for(var a=0;a<360;a+=45){
    var rad = a*Math.PI/180;
    ctx.beginPath(); ctx.moveTo(CX,CY);
    ctx.lineTo(CX+Math.cos(rad)*CR, CY-Math.sin(rad)*CR); ctx.stroke();
  }

  // boundary
  ctx.beginPath(); ctx.arc(CX,CY,CR,0,Math.PI*2);
  ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1.5; ctx.stroke();

  // food
  if(food){
    var fs = p2s(food[0], food[1]);
    ctx.beginPath(); ctx.arc(fs[0], fs[1], 5, 0, Math.PI*2);
    ctx.fillStyle = appleTypes[appleType]; ctx.fill();
  }

  // snake
  for(var i=snake.length-1;i>=0;i--){
    var s = p2s(snake[i][0], snake[i][1]);
    var t = i/snake.length;
    var r = Math.round(30+t*30), g = Math.round(220-t*120), b = Math.round(60+t*30);
    ctx.beginPath(); ctx.arc(s[0], s[1], 3, 0, Math.PI*2);
    ctx.fillStyle = 'rgb('+r+','+g+','+b+')'; ctx.fill();
  }
}

resetGame();
})();
</script>
