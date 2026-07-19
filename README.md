# 🚀 Symmetry, Black Holes, and Python: Verifying Ramanujan's Mathematics on a Modern Computer

Can we use basic computer science to bridge the gap between high school algebra and the deepest theories of quantum physics?

I have spent the last few weeks working on an interdisciplinary project: computationally verifying several of the major mathematical discoveries of G. H. Hardy's legendary collaborator, Srinivasa Ramanujan (1887–1920). Using pure Python (with zero external dependencies), I built a computational engine to test and verify his formulas across seven key mathematical domains:

1. **Calculating π:** Simulating Ramanujan's 1914 infinite series, which converges so rapidly that every single term adds exactly 8 correct decimal places.

2. **Partition Congruences:** Verifying the divisibility rules of partition numbers modulo 5, 7, and 11.

3. **Rogers–Ramanujan Identities:** Equating two completely different partition counting methods using polynomial expansion.

4. **Rogers–Ramanujan Continued Fractions:** Exploring the convergence of nested fractions to the Golden Ratio.

5. **Divisor Functions & Highly Composite Numbers (HCNs):** Factoring numbers to find "highly divisible" integers, which are vital in modern Fast Fourier Transform (FFT) algorithms.

6. **Mock Theta Functions:** Generating coefficients for functions that physicists now use to calculate black hole entropy in string theory.

7. **The Ramanujan Tau Function:** Checking the multiplicative properties of coefficients that form a cornerstone of the Langlands Program (the "grand unified theory" of mathematics).

---

### 📚 Bridging the Gap: The Student Companion Guide

Abstract mathematics can often feel intimidating. To make these profound ideas accessible to the next generation, I created a Student's Companion Guide alongside the formal academic paper.

Written in LaTeX and designed for high school and undergraduate students, the guide explains the mathematics of Ramanujan's work using standard algebra, hands-on programming labs, and selected answers. By writing code, students can watch continued fractions converge and divisibility patterns emerge directly on their own screens.

### 🧪 Verification and Rigor

To ensure absolute reproducibility, the codebase is fully verified by a 15-test unit suite. The formal paper is formatted in standard AMS-LaTeX style (`amsart`), making it ready for preprint archiving on arXiv.

If you are a mathematics educator, software engineer, or student interested in the intersection of coding and number theory, I would love to hear your thoughts.

- How are you using programming to teach mathematical thinking?
- What is your favorite computational math problem to solve?

Let's connect!