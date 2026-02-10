---
title: Fortnite!
summary: Give this a try.
date: 2024-12-11
layout: default
image: /assets/fortnite.png
status: open
published: true
---

<p> i) Circle of radius 1 (the map), populated randomly with N players. Each round a new safe zone appears: its radius is half the previous one, and it must be entirely contained within the previous circle. Players outside the new zone die. Players don't move. The first safe zone has radius 0.5. On average, how many rounds until total death for N starting players? </p>

Assuming you figured it out. Good job.

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim1" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">i) N=100 &middot; static &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot1" width="420" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">mean rounds to total death vs N &middot; 100 trials each</p>
  </div>
</div>

<p> ii) Same setup, but this time, the players may move up to 0.1 times the current radius toward the center. How does the answer change?  </p>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim2" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">ii) N=100 &middot; &delta;=0.1 &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot2" width="420" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">mean rounds to total death vs N &middot; 100 trials each</p>
  </div>
</div>

<script>
(function () {
  var DELTA = 0.1, R0 = 0.5, TRIALS = 100, MAX_N = 5000;

  function randInDisk(cx, cy, rad) {
    var u = Math.random(), a = Math.random() * 6.2832, r = rad * Math.sqrt(u);
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  }
  function randDisk() { return randInDisk(0, 0, 1); }
  function dist(a, b) { var dx = a[0]-b[0], dy = a[1]-b[1]; return Math.sqrt(dx*dx+dy*dy); }

  function moveToward(p, tx, ty, maxStep) {
    var dx = tx - p[0], dy = ty - p[1];
    var d = Math.sqrt(dx*dx + dy*dy);
    if (d <= maxStep) return [tx, ty];
    return [p[0] + dx/d*maxStep, p[1] + dy/d*maxStep];
  }

  /* ── drawing ── */
  function drawSim(ctx, w, h, players, alive, sc, sr, round, n) {
    var cx = w/2, cy = h/2, R = 130;
    ctx.clearRect(0, 0, w, h);
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.2832);
    ctx.strokeStyle = '#ccc'; ctx.lineWidth = 1.5; ctx.stroke();
    if (sc) {
      ctx.beginPath();
      ctx.arc(cx + sc[0]*R, cy + sc[1]*R, sr*R, 0, 6.2832);
      ctx.fillStyle = 'rgba(100,180,255,0.12)'; ctx.fill();
      ctx.strokeStyle = 'rgba(100,180,255,0.4)'; ctx.lineWidth = 1; ctx.stroke();
    }
    for (var i = 0; i < players.length; i++) {
      var px = cx + players[i][0]*R, py = cy + players[i][1]*R;
      ctx.beginPath(); ctx.arc(px, py, 2, 0, 6.2832);
      ctx.fillStyle = alive[i] ? '#2a2' : 'rgba(180,0,0,0.2)';
      ctx.fill();
    }
    ctx.fillStyle = '#888'; ctx.font = '12px sans-serif';
    ctx.fillText('round ' + round, 8, 18);
    var left = 0; for (var i = 0; i < alive.length; i++) if (alive[i]) left++;
    ctx.fillText('alive ' + left + '/' + n, 8, 34);
    if (sr > 0) ctx.fillText('r = ' + sr.toFixed(4), 8, 50);
  }

  /* ── animated sim ── */
  function runAnimatedSim(canvasId, walk) {
    var cv = document.getElementById(canvasId), ctx = cv.getContext('2d');
    var N = 100, players, alive, storm, stormR, round, paused = false;
    function reset() {
      players = []; alive = [];
      for (var i = 0; i < N; i++) { players.push(randDisk()); alive.push(true); }
      storm = null; stormR = 0; round = 0;
    }
    function step() {
      // walk toward current safe zone center
      if (walk && storm) {
        var step = DELTA * stormR;
        for (var i = 0; i < N; i++) {
          if (alive[i]) players[i] = moveToward(players[i], storm[0], storm[1], step);
        }
      }
      // new storm: contained within previous, radius halves
      var newR, nc;
      if (!storm) {
        newR = R0;
        nc = randInDisk(0, 0, 1 - newR); // fully inside map
      } else {
        newR = stormR / 2;
        nc = randInDisk(storm[0], storm[1], stormR - newR); // fully inside prev
      }
      storm = nc; stormR = newR;
      // kill
      for (var i = 0; i < N; i++) {
        if (alive[i] && dist(players[i], storm) >= stormR) alive[i] = false;
      }
      round++;
    }
    function allDead() { for (var i = 0; i < alive.length; i++) if (alive[i]) return false; return true; }
    reset(); drawSim(ctx, cv.width, cv.height, players, alive, storm, stormR, round, N);
    setInterval(function () {
      if (paused) return;
      if (allDead()) {
        paused = true;
        setTimeout(function () { reset(); drawSim(ctx, cv.width, cv.height, players, alive, storm, stormR, round, N); paused = false; }, 1500);
        return;
      }
      step(); drawSim(ctx, cv.width, cv.height, players, alive, storm, stormR, round, N);
    }, 600);
  }

  runAnimatedSim('sim1', false);
  runAnimatedSim('sim2', true);

  /* ── monte carlo ── */
  function simulate(n, walk) {
    var ps = [], a = [], sc = null, sr = 0;
    for (var i = 0; i < n; i++) { ps.push(randDisk()); a.push(true); }
    var rounds = 0;
    while (true) {
      var done = true;
      for (var i = 0; i < n; i++) if (a[i]) { done = false; break; }
      if (done) return rounds;
      // walk
      if (walk && sc) {
        var step = DELTA * sr;
        for (var i = 0; i < n; i++) { if (a[i]) ps[i] = moveToward(ps[i], sc[0], sc[1], step); }
      }
      // new storm
      var newR, nc;
      if (!sc) {
        newR = R0;
        nc = randInDisk(0, 0, 1 - newR);
      } else {
        newR = sr / 2;
        nc = randInDisk(sc[0], sc[1], sr - newR);
      }
      sc = nc; sr = newR;
      // kill
      for (var i = 0; i < n; i++) { if (a[i] && dist(ps[i], sc) >= sr) a[i] = false; }
      rounds++;
    }
  }

  var N_STEP = 100, N_MIN = 100;

  function runMC(walk) {
    var means = [], maxY = 0;
    for (var n = N_MIN; n <= MAX_N; n += N_STEP) {
      var sum = 0;
      for (var t = 0; t < TRIALS; t++) sum += simulate(n, walk);
      var avg = sum / TRIALS;
      means.push(n, avg);
      if (avg > maxY) maxY = avg;
    }
    return { means: means, maxY: maxY };
  }

  /* ── mean line plot ── */
  function drawPlot(canvasId, data) {
    var pc = document.getElementById(canvasId), ctx = pc.getContext('2d');
    var pw = pc.width, ph = pc.height;
    var pad = {l:50, r:16, t:16, b:40};
    var gw = pw - pad.l - pad.r, gh = ph - pad.t - pad.b;
    var maxY = Math.ceil(data.maxY * 1.15) || 1;
    var pts = data.means;

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
    ctx.textAlign = 'center'; ctx.fillText('mean rounds to total death', 0, 0);
    ctx.restore();

    // line
    ctx.strokeStyle = '#444'; ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (var i = 0; i < pts.length; i += 2) {
      var x = gx(pts[i]), y = gy(pts[i+1]);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // dots
    ctx.fillStyle = '#444';
    for (var i = 0; i < pts.length; i += 2) {
      ctx.beginPath(); ctx.arc(gx(pts[i]), gy(pts[i+1]), 2.5, 0, 6.2832); ctx.fill();
    }
  }

  drawPlot('plot1', runMC(false));
  drawPlot('plot2', runMC(true));
})();
</script>
