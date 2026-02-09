---
title: Fortnite!
summary: Try.
date: 2025-07-11
image: /assets/puzzle1/10.png
layout: default
status: open
published: false
---

<p> i) Ok. Circle of radius 1 (fortnite map), populated randomly with N players. But now there's a storm of radius 0.5 randomly on the map, and the players not in the storm die. How many storms does it take for us to be 99% sure that all N players have died? "P(total_death(N)) > 0.99"? </p>

Assuming you figured it out. Good job.

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:32px 0;">
  <div>
    <canvas id="sim" width="300" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">N=20 &middot; auto-running</p>
  </div>
  <div>
    <canvas id="plot" width="400" height="300" style="border:1px solid #eee; border-radius:8px;"></canvas>
    <p style="font-size:12px; color:#888; margin:6px 0 0;">storms to 99% total death vs N &middot; 100 trials each</p>
  </div>
</div>

<script>
(function () {
  /* ── helpers ── */
  function randDisk() {
    var u = Math.random(), a = Math.random() * 6.2832;
    var r = Math.sqrt(u);
    return [r * Math.cos(a), r * Math.sin(a)];
  }
  function dist(a, b) { var dx = a[0]-b[0], dy = a[1]-b[1]; return Math.sqrt(dx*dx+dy*dy); }

  /* ── simulation graphic ── */
  var sc = document.getElementById('sim'), sctx = sc.getContext('2d');
  var N_SIM = 20, players, alive, stormCenter, round;

  function resetSim() {
    players = []; alive = [];
    for (var i = 0; i < N_SIM; i++) { players.push(randDisk()); alive.push(true); }
    stormCenter = null; round = 0;
  }

  function stepSim() {
    stormCenter = randDisk();
    for (var i = 0; i < players.length; i++) {
      if (alive[i] && dist(players[i], stormCenter) >= 0.5) alive[i] = false;
    }
    round++;
  }

  function allDead() { for (var i = 0; i < alive.length; i++) if (alive[i]) return false; return true; }

  function drawSim() {
    var w = sc.width, h = sc.height, cx = w/2, cy = h/2, R = 130;
    sctx.clearRect(0, 0, w, h);
    // map
    sctx.beginPath(); sctx.arc(cx, cy, R, 0, 6.2832);
    sctx.strokeStyle = '#ccc'; sctx.lineWidth = 1.5; sctx.stroke();
    // storm safe zone
    if (stormCenter) {
      sctx.beginPath();
      sctx.arc(cx + stormCenter[0]*R, cy + stormCenter[1]*R, 0.5*R, 0, 6.2832);
      sctx.fillStyle = 'rgba(100,180,255,0.12)';
      sctx.fill();
      sctx.strokeStyle = 'rgba(100,180,255,0.4)';
      sctx.lineWidth = 1;
      sctx.stroke();
    }
    // players
    for (var i = 0; i < players.length; i++) {
      var px = cx + players[i][0]*R, py = cy + players[i][1]*R;
      sctx.beginPath(); sctx.arc(px, py, 3, 0, 6.2832);
      if (alive[i]) { sctx.fillStyle = '#2a2'; }
      else { sctx.fillStyle = 'rgba(180,0,0,0.25)'; }
      sctx.fill();
    }
    // round counter
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

  /* ── monte carlo plot ── */
  var pc = document.getElementById('plot'), pctx = pc.getContext('2d');
  var Ns = [1,2,3,5,8,10,15,20,30,50,75,100];
  var TRIALS = 100;

  function simulate(n) {
    var ps = []; for (var i = 0; i < n; i++) ps.push(randDisk());
    var a = []; for (var i = 0; i < n; i++) a.push(true);
    var rounds = 0;
    while (true) {
      var allGone = true;
      for (var i = 0; i < n; i++) if (a[i]) { allGone = false; break; }
      if (allGone) return rounds;
      var c = randDisk();
      for (var i = 0; i < n; i++) {
        if (a[i] && dist(ps[i], c) >= 0.5) a[i] = false;
      }
      rounds++;
    }
  }

  // run trials and get 99th percentile
  var results = [];
  for (var ni = 0; ni < Ns.length; ni++) {
    var vals = [];
    for (var t = 0; t < TRIALS; t++) vals.push(simulate(Ns[ni]));
    vals.sort(function(a,b){return a-b;});
    results.push(vals[Math.floor(TRIALS * 0.99)]);
  }

  // draw plot
  var pw = pc.width, ph = pc.height;
  var pad = {l:50, r:20, t:20, b:40};
  var gw = pw - pad.l - pad.r, gh = ph - pad.t - pad.b;
  var maxN = 100, maxY = 0;
  for (var i = 0; i < results.length; i++) if (results[i] > maxY) maxY = results[i];
  maxY = Math.ceil(maxY * 1.15);

  function px(n) { return pad.l + (n / maxN) * gw; }
  function py(v) { return pad.t + gh - (v / maxY) * gh; }

  // axes
  pctx.strokeStyle = '#bbb'; pctx.lineWidth = 1;
  pctx.beginPath(); pctx.moveTo(pad.l, pad.t); pctx.lineTo(pad.l, pad.t+gh); pctx.lineTo(pad.l+gw, pad.t+gh); pctx.stroke();

  // ticks & labels
  pctx.fillStyle = '#888'; pctx.font = '11px sans-serif'; pctx.textAlign = 'center';
  for (var n = 0; n <= 100; n += 20) {
    var x = px(n);
    pctx.beginPath(); pctx.moveTo(x, pad.t+gh); pctx.lineTo(x, pad.t+gh+4); pctx.stroke();
    pctx.fillText(n, x, pad.t+gh+16);
  }
  pctx.fillText('N players', pad.l + gw/2, ph - 4);

  pctx.textAlign = 'right';
  var yStep = Math.max(1, Math.round(maxY / 5));
  for (var v = 0; v <= maxY; v += yStep) {
    var y = py(v);
    pctx.beginPath(); pctx.moveTo(pad.l-4, y); pctx.lineTo(pad.l, y); pctx.stroke();
    pctx.fillText(v, pad.l-8, y+4);
  }
  pctx.save(); pctx.translate(14, pad.t + gh/2); pctx.rotate(-Math.PI/2);
  pctx.textAlign = 'center'; pctx.fillText('storms (99th pct)', 0, 0);
  pctx.restore();

  // line
  pctx.strokeStyle = '#444'; pctx.lineWidth = 1.5;
  pctx.beginPath();
  for (var i = 0; i < Ns.length; i++) {
    var x = px(Ns[i]), y = py(results[i]);
    if (i === 0) pctx.moveTo(x, y); else pctx.lineTo(x, y);
  }
  pctx.stroke();

  // dots
  for (var i = 0; i < Ns.length; i++) {
    pctx.beginPath(); pctx.arc(px(Ns[i]), py(results[i]), 3, 0, 6.2832);
    pctx.fillStyle = '#444'; pctx.fill();
  }
})();
</script>

ii) Now, solve it for when the size of the next storm is some random number between 0 and the size of the current storm circle.