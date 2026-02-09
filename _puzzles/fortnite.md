---
title: Fortnite!
summary: Try.
date: 2025-07-11
layout: default
status: open
published: true
---

<p> i) Circle of radius 1 (the map), populated randomly with N players. Each round a safe zone of radius 0.5 appears at a random position on the map &mdash; players outside it die. Players don't move. How many storms does it take to be 99% sure all N players are dead? </p>

Assuming you figured it out. Good job.

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim1" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">i) N=20 &middot; static &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot1" width="420" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">storms to 99% total death vs N &middot; 100 trials each</p>
  </div>
</div>

<p> ii) Same setup, but now before each storm every surviving player takes a step of at most &delta;=0.1 to maximize their survival probability. How does the answer change? </p>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim2" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">ii) N=20 &middot; &delta;=0.1 &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot2" width="420" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">storms to 99% total death vs N &middot; 100 trials each</p>
  </div>
</div>

<script>
(function () {
  var DELTA = 0.1, STORM_R = 0.5, TRIALS = 10, MAX_N = 5000;

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
    return [p[0] - p[0]*s, p[1] - p[1]*s];
  }

  /* ── shared drawing ── */
  function drawSim(ctx, w, h, players, alive, stormCenter, round, n) {
    var cx = w/2, cy = h/2, R = 130;
    ctx.clearRect(0, 0, w, h);
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.2832);
    ctx.strokeStyle = '#ccc'; ctx.lineWidth = 1.5; ctx.stroke();
    if (stormCenter) {
      ctx.beginPath();
      ctx.arc(cx + stormCenter[0]*R, cy + stormCenter[1]*R, STORM_R*R, 0, 6.2832);
      ctx.fillStyle = 'rgba(100,180,255,0.12)'; ctx.fill();
      ctx.strokeStyle = 'rgba(100,180,255,0.4)'; ctx.lineWidth = 1; ctx.stroke();
    }
    for (var i = 0; i < players.length; i++) {
      var px = cx + players[i][0]*R, py = cy + players[i][1]*R;
      ctx.beginPath(); ctx.arc(px, py, 3, 0, 6.2832);
      ctx.fillStyle = alive[i] ? '#2a2' : 'rgba(180,0,0,0.25)';
      ctx.fill();
    }
    ctx.fillStyle = '#888'; ctx.font = '12px sans-serif';
    ctx.fillText('round ' + round, 8, 18);
    var left = 0; for (var i = 0; i < alive.length; i++) if (alive[i]) left++;
    ctx.fillText('alive ' + left + '/' + n, 8, 34);
  }

  /* ── run an animated sim (walk = true/false) ── */
  function runAnimatedSim(canvasId, walk) {
    var sc = document.getElementById(canvasId), ctx = sc.getContext('2d');
    var N = 20, players, alive, storm, round, paused = false;
    function reset() {
      players = []; alive = [];
      for (var i = 0; i < N; i++) { players.push(randDisk()); alive.push(true); }
      storm = null; round = 0;
    }
    function step() {
      if (walk) for (var i = 0; i < N; i++) { if (alive[i]) players[i] = moveTowardCenter(players[i]); }
      storm = randDisk();
      for (var i = 0; i < N; i++) { if (alive[i] && dist(players[i], storm) >= STORM_R) alive[i] = false; }
      round++;
    }
    function allDead() { for (var i = 0; i < alive.length; i++) if (alive[i]) return false; return true; }
    reset(); drawSim(ctx, sc.width, sc.height, players, alive, storm, round, N);
    setInterval(function () {
      if (paused) return;
      if (allDead()) { paused = true; setTimeout(function () { reset(); drawSim(ctx, sc.width, sc.height, players, alive, storm, round, N); paused = false; }, 1500); return; }
      step(); drawSim(ctx, sc.width, sc.height, players, alive, storm, round, N);
    }, 600);
  }

  runAnimatedSim('sim1', false);
  runAnimatedSim('sim2', true);

  /* ── monte carlo (walk = true/false) ── */
  function simulate(n, walk) {
    var ps = [], a = [];
    for (var i = 0; i < n; i++) { ps.push(randDisk()); a.push(true); }
    var rounds = 0;
    while (true) {
      var done = true;
      for (var i = 0; i < n; i++) if (a[i]) { done = false; break; }
      if (done) return rounds;
      if (walk) for (var i = 0; i < n; i++) { if (a[i]) ps[i] = moveTowardCenter(ps[i]); }
      var c = randDisk();
      for (var i = 0; i < n; i++) { if (a[i] && dist(ps[i], c) >= STORM_R) a[i] = false; }
      rounds++;
    }
  }

  function runMC(walk) {
    var points = [], maxY = 0;
    for (var n = 1; n <= MAX_N; n++) {
      for (var t = 0; t < TRIALS; t++) {
        var r = simulate(n, walk);
        points.push(n, r);
        if (r > maxY) maxY = r;
      }
    }
    return { pts: points, maxY: maxY };
  }

  /* ── shared scatter plot ── */
  function drawPlot(canvasId, data) {
    var pc = document.getElementById(canvasId), ctx = pc.getContext('2d');
    var pw = pc.width, ph = pc.height;
    var pad = {l:50, r:16, t:16, b:40};
    var gw = pw - pad.l - pad.r, gh = ph - pad.t - pad.b;
    var maxY = Math.ceil(data.maxY * 1.1) || 1;
    var pts = data.pts;

    function gx(n) { return pad.l + ((n-1) / (MAX_N-1)) * gw; }
    function gy(v) { return pad.t + gh - (v / maxY) * gh; }

    ctx.strokeStyle = '#bbb'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, pad.t+gh); ctx.lineTo(pad.l+gw, pad.t+gh); ctx.stroke();

    ctx.fillStyle = '#888'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
    var xStep = MAX_N <= 100 ? 20 : 100;
    for (var n = xStep; n <= MAX_N; n += xStep) {
      var x = gx(n);
      ctx.beginPath(); ctx.moveTo(x, pad.t+gh); ctx.lineTo(x, pad.t+gh+4); ctx.stroke();
      ctx.fillText(n, x, pad.t+gh+16);
    }
    ctx.fillText('N', pad.l + gw/2, ph - 4);

    ctx.textAlign = 'right';
    var yStep = Math.max(1, Math.round(maxY / 5));
    for (var v = 0; v <= maxY; v += yStep) {
      var y = gy(v);
      ctx.beginPath(); ctx.moveTo(pad.l-4, y); ctx.lineTo(pad.l, y); ctx.stroke();
      ctx.fillText(v, pad.l-8, y+4);
    }
    ctx.save(); ctx.translate(14, pad.t + gh/2); ctx.rotate(-Math.PI/2);
    ctx.textAlign = 'center'; ctx.fillText('storms to total death', 0, 0);
    ctx.restore();

    // scatter
    ctx.fillStyle = 'rgba(30,90,160,0.04)';
    for (var i = 0; i < pts.length; i += 2) {
      ctx.fillRect(gx(pts[i]) - 0.5, gy(pts[i+1]) - 0.5, 1.5, 1.5);
    }
  }

  drawPlot('plot1', runMC(false));
  drawPlot('plot2', runMC(true));
})();
</script>
