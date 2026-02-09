---
title: Fortnite!
summary: Try.
date: 2025-07-11
image: /assets/puzzle1/10.png
layout: default
status: open
published: true
---

<p> i) Circle of radius 1 (the map), populated randomly with N players. Each round a safe zone of radius 0.5 appears at a random position on the map &mdash; players outside it die. Before each storm, every surviving player takes a step of at most &delta;=0.1 to maximize their survival probability. How many storms does it take to be 99% sure all N players are dead? </p>

Assuming you figured it out. Good job.

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">N=20 &middot; &delta;=0.1 &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot" width="420" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">storms to 99% total death vs N &middot; 100 trials each</p>
  </div>
</div>

<script>
(function () {
  var DELTA = 0.1, STORM_R = 0.5;

  function randDisk() {
    var u = Math.random(), a = Math.random() * 6.2832, r = Math.sqrt(u);
    return [r * Math.cos(a), r * Math.sin(a)];
  }
  function dist(a, b) { var dx = a[0]-b[0], dy = a[1]-b[1]; return Math.sqrt(dx*dx+dy*dy); }
  function norm(p) { return Math.sqrt(p[0]*p[0]+p[1]*p[1]); }

  function moveTowardCenter(p) {
    var d = norm(p);
    if (d <= DELTA) return [0, 0];
    var s = DELTA / d;
    return [p[0] - p[0] * s, p[1] - p[1] * s];
  }

  /* ── simulation graphic ── */
  var sc = document.getElementById('sim'), sctx = sc.getContext('2d');
  var N_SIM = 20, players, alive, stormCenter, round;

  function resetSim() {
    players = []; alive = [];
    for (var i = 0; i < N_SIM; i++) { players.push(randDisk()); alive.push(true); }
    stormCenter = null; round = 0;
  }

  function stepSim() {
    // move
    for (var i = 0; i < players.length; i++) {
      if (alive[i]) players[i] = moveTowardCenter(players[i]);
    }
    // storm
    stormCenter = randDisk();
    for (var i = 0; i < players.length; i++) {
      if (alive[i] && dist(players[i], stormCenter) >= STORM_R) alive[i] = false;
    }
    round++;
  }

  function allDead() { for (var i = 0; i < alive.length; i++) if (alive[i]) return false; return true; }

  function drawSim() {
    var w = sc.width, h = sc.height, cx = w/2, cy = h/2, R = 130;
    sctx.clearRect(0, 0, w, h);
    sctx.beginPath(); sctx.arc(cx, cy, R, 0, 6.2832);
    sctx.strokeStyle = '#ccc'; sctx.lineWidth = 1.5; sctx.stroke();
    if (stormCenter) {
      sctx.beginPath();
      sctx.arc(cx + stormCenter[0]*R, cy + stormCenter[1]*R, STORM_R*R, 0, 6.2832);
      sctx.fillStyle = 'rgba(100,180,255,0.12)'; sctx.fill();
      sctx.strokeStyle = 'rgba(100,180,255,0.4)'; sctx.lineWidth = 1; sctx.stroke();
    }
    for (var i = 0; i < players.length; i++) {
      var px = cx + players[i][0]*R, py = cy + players[i][1]*R;
      sctx.beginPath(); sctx.arc(px, py, 3, 0, 6.2832);
      sctx.fillStyle = alive[i] ? '#2a2' : 'rgba(180,0,0,0.25)';
      sctx.fill();
    }
    sctx.fillStyle = '#888'; sctx.font = '12px sans-serif';
    sctx.fillText('round ' + round, 8, 18);
    var left = 0; for (var i = 0; i < alive.length; i++) if (alive[i]) left++;
    sctx.fillText('alive ' + left + '/' + N_SIM, 8, 34);
  }

  resetSim(); drawSim();
  var paused = false;
  setInterval(function () {
    if (paused) return;
    if (allDead()) { paused = true; setTimeout(function () { resetSim(); drawSim(); paused = false; }, 1500); return; }
    stepSim(); drawSim();
  }, 600);

  /* ── monte carlo plot: N = 1..100 ── */
  var pc = document.getElementById('plot'), pctx = pc.getContext('2d');
  var TRIALS = 100, MAX_N = 100;

  function simulate(n) {
    var ps = [], a = [];
    for (var i = 0; i < n; i++) { ps.push(randDisk()); a.push(true); }
    var rounds = 0;
    while (true) {
      var done = true;
      for (var i = 0; i < n; i++) if (a[i]) { done = false; break; }
      if (done) return rounds;
      for (var i = 0; i < n; i++) { if (a[i]) ps[i] = moveTowardCenter(ps[i]); }
      var c = randDisk();
      for (var i = 0; i < n; i++) {
        if (a[i] && dist(ps[i], c) >= STORM_R) a[i] = false;
      }
      rounds++;
    }
  }

  var results = [];
  for (var n = 1; n <= MAX_N; n++) {
    var vals = [];
    for (var t = 0; t < TRIALS; t++) vals.push(simulate(n));
    vals.sort(function(a,b){return a-b;});
    results.push(vals[Math.floor(TRIALS * 0.99)]);
  }

  var pw = pc.width, ph = pc.height;
  var pad = {l:50, r:16, t:16, b:40};
  var gw = pw - pad.l - pad.r, gh = ph - pad.t - pad.b;
  var maxY = 0;
  for (var i = 0; i < results.length; i++) if (results[i] > maxY) maxY = results[i];
  maxY = Math.ceil(maxY * 1.12);

  function gx(n) { return pad.l + ((n - 1) / (MAX_N - 1)) * gw; }
  function gy(v) { return pad.t + gh - (v / maxY) * gh; }

  // axes
  pctx.strokeStyle = '#bbb'; pctx.lineWidth = 1;
  pctx.beginPath(); pctx.moveTo(pad.l, pad.t); pctx.lineTo(pad.l, pad.t+gh); pctx.lineTo(pad.l+gw, pad.t+gh); pctx.stroke();

  // x ticks
  pctx.fillStyle = '#888'; pctx.font = '11px sans-serif'; pctx.textAlign = 'center';
  for (var n = 1; n <= 100; n += 20) {
    if (n === 1) n = 1;
    var x = gx(n === 1 ? 1 : n);
    pctx.beginPath(); pctx.moveTo(x, pad.t+gh); pctx.lineTo(x, pad.t+gh+4); pctx.stroke();
    pctx.fillText(n, x, pad.t+gh+16);
  }
  pctx.fillText('N', pad.l + gw/2, ph - 4);

  // y ticks
  pctx.textAlign = 'right';
  var yStep = Math.max(1, Math.round(maxY / 5));
  for (var v = 0; v <= maxY; v += yStep) {
    var y = gy(v);
    pctx.beginPath(); pctx.moveTo(pad.l-4, y); pctx.lineTo(pad.l, y); pctx.stroke();
    pctx.fillText(v, pad.l-8, y+4);
  }
  pctx.save(); pctx.translate(14, pad.t + gh/2); pctx.rotate(-Math.PI/2);
  pctx.textAlign = 'center'; pctx.fillText('storms (99th pct)', 0, 0);
  pctx.restore();

  // line
  pctx.strokeStyle = '#555'; pctx.lineWidth = 1.2;
  pctx.beginPath();
  for (var i = 0; i < results.length; i++) {
    var x = gx(i + 1), y = gy(results[i]);
    if (i === 0) pctx.moveTo(x, y); else pctx.lineTo(x, y);
  }
  pctx.stroke();
})();
</script>

ii) Now, solve it for when the size of the next storm is some random number between 0 and the size of the current storm circle.
