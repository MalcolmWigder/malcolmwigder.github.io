---
title: Fortnite!
summary: Try...
date: 2025-07-11
layout: default
status: open
published: true
---

<p> i) Circle of radius 1 (the map), populated randomly with N players. Each round a safe zone of radius 0.5 appears at a random position on the map; players outside it die. Players don't move. How many storms does it take to be 99% sure all N players are dead? </p>

Assuming you figured it out. Good job.

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim1" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">i) N=100 &middot; static &middot; auto-running</p>
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
    <p style="font-size:12px; color:#888; margin:6px 0 0;">ii) N=100 &middot; &delta;=0.1 &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot2" width="420" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">storms to 99% total death vs N &middot; 100 trials each</p>
  </div>
</div>

<script>
(function () {
  var DELTA = 0.1, STORM_R = 0.5, TRIALS = 100, MAX_N = 5000;

  function randDisk() {
    var u = Math.random(), a = Math.random() * 6.2832, r = Math.sqrt(u);
    return [r * Math.cos(a), r * Math.sin(a)];
  }
  function randInDisk(cx, cy, rad) {
    var u = Math.random(), a = Math.random() * 6.2832, r = rad * Math.sqrt(u);
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
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
    var N = 100, players, alive, storm, round, paused = false;
    function reset() {
      players = []; alive = [];
      for (var i = 0; i < N; i++) { players.push(randDisk()); alive.push(true); }
      storm = null; round = 0;
    }
    function step() {
      if (walk) for (var i = 0; i < N; i++) { if (alive[i]) players[i] = moveTowardCenter(players[i]); }
      storm = storm ? randInDisk(storm[0], storm[1], STORM_R) : randDisk();
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
    var ps = [], a = [], prev = null;
    for (var i = 0; i < n; i++) { ps.push(randDisk()); a.push(true); }
    var rounds = 0;
    while (true) {
      var done = true;
      for (var i = 0; i < n; i++) if (a[i]) { done = false; break; }
      if (done) return rounds;
      if (walk) for (var i = 0; i < n; i++) { if (a[i]) ps[i] = moveTowardCenter(ps[i]); }
      var c = prev ? randInDisk(prev[0], prev[1], STORM_R) : randDisk();
      prev = c;
      for (var i = 0; i < n; i++) { if (a[i] && dist(ps[i], c) >= STORM_R) a[i] = false; }
      rounds++;
    }
  }

  var N_STEP = 100, N_MIN = 100;

  function runMC(walk) {
    var medians = [], raw = [], maxY = 0;
    for (var n = N_MIN; n <= MAX_N; n += N_STEP) {
      var vals = [];
      for (var t = 0; t < TRIALS; t++) {
        var r = simulate(n, walk);
        vals.push(r);
        raw.push(n, r);
        if (r > maxY) maxY = r;
      }
      vals.sort(function(a,b){return a-b;});
      medians.push(n, vals[Math.floor(TRIALS / 2)]);
    }
    return { raw: raw, medians: medians, maxY: maxY };
  }

  /* ── shared scatter + median line plot ── */
  function drawPlot(canvasId, data) {
    var pc = document.getElementById(canvasId), ctx = pc.getContext('2d');
    var pw = pc.width, ph = pc.height;
    var pad = {l:50, r:16, t:16, b:40};
    var gw = pw - pad.l - pad.r, gh = ph - pad.t - pad.b;
    var maxY = Math.ceil(data.maxY * 1.1) || 1;

    function gx(n) { return pad.l + ((n - N_MIN) / (MAX_N - N_MIN)) * gw; }
    function gy(v) { return pad.t + gh - (v / maxY) * gh; }

    ctx.strokeStyle = '#bbb'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, pad.t+gh); ctx.lineTo(pad.l+gw, pad.t+gh); ctx.stroke();

    ctx.fillStyle = '#888'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
    var xStep = MAX_N <= 500 ? 100 : 1000;
    for (var n = N_MIN; n <= MAX_N; n += xStep) {
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

    // scatter (all trials)
    ctx.fillStyle = 'rgba(30,90,160,0.12)';
    var raw = data.raw;
    for (var i = 0; i < raw.length; i += 2) {
      ctx.beginPath(); ctx.arc(gx(raw[i]), gy(raw[i+1]), 2, 0, 6.2832); ctx.fill();
    }

    // median line
    var med = data.medians;
    ctx.strokeStyle = '#c33'; ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (var i = 0; i < med.length; i += 2) {
      var x = gx(med[i]), y = gy(med[i+1]);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // median dots
    ctx.fillStyle = '#c33';
    for (var i = 0; i < med.length; i += 2) {
      ctx.beginPath(); ctx.arc(gx(med[i]), gy(med[i+1]), 2.5, 0, 6.2832); ctx.fill();
    }
  }

  drawPlot('plot1', runMC(false));
  drawPlot('plot2', runMC(true));
})();
</script>
