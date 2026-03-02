---
title: Basic Creatures
summary: Hard one I reckon
date: 2026-03-02
layout: default
image: /assets/creature.png
status: open
published: true
---

<div style="text-align:center; margin: 1.5rem 0 2.5rem;">
  <img src="/assets/creature.png" style="max-width:340px; width:100%; border-radius:6px; opacity:0.88;">
</div>

You have **1000 creatures**, each with a value \\( x \in [0, 1] \\). The population starts uniformly distributed across this range.

Each **generation** runs three phases in order:

<svg viewBox="0 0 660 130" style="width:100%;max-width:660px;display:block;margin:2rem auto;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0.5 L6,3.5 L0,6.5" fill="none" stroke="#555" stroke-width="1.2"/>
    </marker>
  </defs>

  <!-- Box 1: Population -->
  <rect x="8" y="35" width="110" height="44" rx="5" fill="#1c1c1c" stroke="#3a3a3a" stroke-width="1.5"/>
  <text x="63" y="54" text-anchor="middle" fill="#ccc" font-size="12" font-family="-apple-system,sans-serif" font-weight="600">1000 creatures</text>
  <text x="63" y="70" text-anchor="middle" fill="#666" font-size="11" font-family="-apple-system,sans-serif">x ∈ [0, 1]</text>

  <!-- Arrow 1 -->
  <line x1="118" y1="57" x2="153" y2="57" stroke="#444" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Box 2: Purge -->
  <rect x="155" y="35" width="100" height="44" rx="5" fill="#1c1c1c" stroke="#3a3a3a" stroke-width="1.5"/>
  <text x="205" y="54" text-anchor="middle" fill="#ccc" font-size="12" font-family="-apple-system,sans-serif" font-weight="600">Purge</text>
  <text x="205" y="70" text-anchor="middle" fill="#888" font-size="11" font-family="-apple-system,sans-serif">die w.p. 1 − x</text>

  <!-- Arrow 2 -->
  <line x1="255" y1="57" x2="290" y2="57" stroke="#444" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Box 3: Starvation -->
  <rect x="292" y="35" width="110" height="44" rx="5" fill="#1c1c1c" stroke="#3a3a3a" stroke-width="1.5"/>
  <text x="347" y="54" text-anchor="middle" fill="#ccc" font-size="12" font-family="-apple-system,sans-serif" font-weight="600">Starvation</text>
  <text x="347" y="70" text-anchor="middle" fill="#888" font-size="11" font-family="-apple-system,sans-serif">die w.p. x</text>

  <!-- Arrow 3 -->
  <line x1="402" y1="57" x2="437" y2="57" stroke="#444" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Box 4: Reproduce -->
  <rect x="439" y="35" width="110" height="44" rx="5" fill="#1c1c1c" stroke="#3a3a3a" stroke-width="1.5"/>
  <text x="494" y="54" text-anchor="middle" fill="#ccc" font-size="12" font-family="-apple-system,sans-serif" font-weight="600">Reproduce</text>
  <text x="494" y="70" text-anchor="middle" fill="#888" font-size="11" font-family="-apple-system,sans-serif">back to 1000</text>

  <!-- Loop arrow back: from right edge of box4, arc under, back to left edge of box1 -->
  <path d="M549,79 Q549,112 330,112 Q110,112 63,79" fill="none" stroke="#333" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr)"/>
  <text x="330" y="126" text-anchor="middle" fill="#555" font-size="10" font-family="-apple-system,sans-serif">repeat</text>
</svg>

Reproduction is asexual — offspring inherit their parent's value \\( x \\). Generations repeat until **one creature remains**.

---

**1.** What creature \\( x \\) do you expect to win?

**2.** How many generations do you expect it to take?
