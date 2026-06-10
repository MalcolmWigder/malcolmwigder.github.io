---
title: Holes
summary: How much can one angle enclose?
date: 2026-05-05
layout: default
image: /assets/evolution.png
status: open
published: true
---

This one comes from the [Evolving Creatures]({{ site.baseurl }}/projects/) project, where a genetic algorithm breeds walks that trap as many enclosed regions &mdash; **holes** &mdash; as possible.

A **creature** is a walk. It starts facing along heading \\( \theta = 0 \\) and takes unit steps. Before each step it turns by an angle read cyclically from its **genome** \\( (g_0, g_1, \dots, g_{L-1}) \\):

\\[ \theta_s = \theta_{s-1} + g_{\,s \bmod L}, \qquad p_s = p_{s-1} + (\cos\theta_s,\ \sin\theta_s). \\]

Treat the finished path as an ideal curve in the plane. A **hole** is a bounded region of the plane that the curve encloses (a connected piece of the complement that you can't escape to infinity from).

The evolved champions are dense scribbles with a hundred-plus holes and genomes of length 128. This puzzle asks the opposite question: **how much can you enclose with the dumbest possible genome &mdash; a single angle repeated forever?**

So fix \\( g_i = \theta \\) for every gene. Every step turns by the same \\( \theta \\).

---

**1.** For which \\( \theta \\) does the creature eventually close up into a simple regular polygon, and how many holes does it trap when it does?

**2.** You can do better than one hole with a constant genome. Pick \\( \theta = \tfrac{2\pi k}{n} \\) with \\( \gcd(n, k) = 1 \\) and \\( 2 \le k < \tfrac{n}{2} \\), and the path closes into a regular **star** polygon \\( \{n/k\} \\) &mdash; like the pentagram \\( \{5/2\} \\) below, which traps **6** holes. Find a formula for the number of holes \\( \{n/k\} \\) traps.

<svg viewBox="0 0 200 210" style="width:100%;max-width:240px;display:block;margin:2rem auto;" xmlns="http://www.w3.org/2000/svg">
  <path d="M100,20 L147,164.7 L23.9,75.3 L176.1,75.3 L53,164.7 Z"
        fill="none" stroke="#4b8bff" stroke-width="2" stroke-linejoin="round"/>
  <text x="100" y="200" text-anchor="middle" fill="#666" font-size="11" font-family="-apple-system,sans-serif">{5/2} — one angle, six holes</text>
</svg>

*Hint: think of the closed path as a graph whose vertices are its self-crossings. Euler's formula \\( V - E + F = 2 \\) does the rest.*

**3.** The creature only takes so many steps. If the path must close within \\( N \\) steps, what \\( \theta \\) traps the most holes, and how does that maximum grow with \\( N \\)?

---

Solutions, partial or complete, to <a href="mailto:mbw7@rice.edu" style="color:#4b8bff;">mbw7@rice.edu</a>.
