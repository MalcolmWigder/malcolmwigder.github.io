---
title: Gas me Up
summary: Starting off with a hard one
date: 2025-07-11
image: /assets/puzzle1/10.png
layout: default
status: open
published: false
---

My first project for Professor Gonnermann was to design experiments to determine how bubbles and liquid separate in a bubbly mixture. Using some imaging techniques, we extracted the average luminosity (brightness) of coffee at different \\( z \\) values (height in the column), at different times (one time shown below):

<p>
  <img src="/assets/puzzle1/11.png" width="100%">
</p>

But we are not interested in the brightness; we are interested in the *volume fraction of gas*, at every \\( z \\), at every \\( t \\).  Here, *volume fraction of gas* means the percentage of the total volume at height \\( z \\) that is occupied by gas (i.e., not liquid).

We know:

- The **total volume fraction of gas** at a given time, denoted \\( a_0 \\), is a known value between 0 and 1.
- The **luminosity profile** at each time \\( t \\) is given as a normalized function  
  \\[
  \text{luminosity}(z) = L(z): [0, h] \to [0, 1]
  \\]  
  where \\( h \\) is the total height of the fluid column.

Can we find a function  
\\[
u(L): [0, 1] \to [0, 1]
\\]  
such that  
\\[
u(L(z)) = a(z)
\\]  
(that is, it maps observed luminosity at a height \\( z \\) to the corresponding gas volume fraction)  
with the constraint  
\\[
\frac{1}{h} \int_0^h u(L(z))\, dz = a_0 \quad \text{for all } t?
\\]

Take for granted:

- At \\( t = 0 \\), both luminosity and volume fraction are flat lines.  
- At \\( t = \infty \\), they become step functions.

An analytical solution **or** an algorithmic technique is accepted.
