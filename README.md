# From Theta Lifts to the Critical Line

Independent paper reconstruction and audit of the Alpöge–Claude argument for Dirichlet $`L`$-functions. Revised 22 November 2026, 329 pages.

[Read the paper (PDF)](./Arithmetic-reconstruction-after-review.pdf) | [Download this fork (ZIP)](https://github.com/leecrossley/alpoge-claude-rh-reconstruction/archive/refs/heads/main.zip) | [LaTeX source](./main.tex) | [Proof status by theorem and page](./audit/paper-proof-status.tsv) | [Upstream reconstruction](https://github.com/Sidler4Hare/alpoge-claude-rh-reconstruction/tree/7d17bb991581172cebd554c33a205b1b0f3a2fb3)

Theorem 1.3 proves a **conditional critical-line theorem**. Either of two uniform arithmetic estimates on arbitrarily late windows implies the critical-line assertions for the Riemann zeta function and every Dirichlet $`L`$-function. Establishing one of the estimates on the whole arithmetic family remains open in this reconstruction, including for $`\psi=1`$. Equations (15.1) and (15.2) appear on p. 270.

The paper reconstructs the mathematical argument of the 20 November 2026 Lean 4 formalization announced by L. Alpöge with Claude. The upstream project used Lean 4.33.1 and contains 175,187 compiled modules, with approximately 1.48 million declarations in each root's dependency closure. The paper checks signs, normalizations, shared arithmetic data and the order of quantifiers. Section 14 distinguishes the published machine checks from the paper deductions. [Pinned upstream source](https://github.com/leanprover-community/riemann-hypothesis/tree/40e56bab026552e089d7afcfeff08d2defb9c005)

## The two arithmetic estimates

### Pointwise translate estimate (15.1)

Fix a primitive Dirichlet character $`\psi`$ and a sufficiently small positive $`\varepsilon`$. For every $`Y_0`$ there must be a $`Y\ge\max(1,Y_0)`$ such that at **every** $`x\in[Y,Y^{3/2}]`$ one can choose common host, frame and weight data $`\mathcal D_x`$. These must satisfy the scale, coset-share, rank and discarded-character hypotheses in Sections 10 and 15. With that choice fixed, (15.1) requires the following for **every** $`u\in A_0(\mathcal D_x)`$.

```math
\begin{aligned}
D_u(\mathcal D_x)
  &=\sum_{t\in T}\sum_{j=1}^{m}
       \bigl(\mathrm{ASK}_{u,t,j}-\mathrm{MAIN}_{u,t,j}\bigr)\\[2pt]
  &\le E_x(\mathcal D_x).
\end{aligned}
```

The common error budget is

```math
\begin{aligned}
E_x(\mathcal D_x)
 &= x^{5\varepsilon}\Bigl(n_T a_E+\frac{n_T a_E m^2}{k}\\[2pt]
 &\qquad {}+2n m^2 b x^\varepsilon
              +\frac{m b n_2 k x^{2\varepsilon}}{n^2}\Bigr).
\end{aligned}
```

### Signed translate mean (15.2)

The same choice of window and common data suffices if the uniform **signed mean** over the translate subgroup satisfies

```math
\frac{1}{\lvert A_0(\mathcal D_x)\rvert}
\sum_{u\in A_0(\mathcal D_x)}D_u(\mathcal D_x)
\le E_x(\mathcal D_x).
```

**Four primitive twists.** Proposition 10.4 computes $`2\bar D/(B\delta)`$ with an explicit remainder. Each power of $`\psi`$ contributes the primitive inducers of $`\psi^a,\ \psi^aJ_q,\ \psi^aJ_d,\ \psi^aJ_qJ_d`$ with signs $`+,+,-,-`$. Corollary 10.5 bounds the three discarded twists using Theorem 6.4. For $`\psi=1`$, the main term is $`G[1]+G[J_q]-G[J_d]-G[J_qJ_d]`$. Corollary 10.6 shows that supplying the common arithmetic hypotheses and (15.2) at the **integer squares** in each window suffices for the critical-line implication. [Section 10](./sections/arithmetic.tex)

For a quadratic $`\psi`$ and a prime $`p`$ outside the conductors, the $`a=1`$ bracket has character factor $`\psi(p)(1+J_q(p))(1-J_d(p))`$. With the fixed references $`q=3`$ and $`d=7`$, it equals $`4\psi(p)`$ for $`p\equiv10,13,19\pmod{21}`$ and zero on the other reduced residue classes. Proposition 10.4 gives this bracket weight $`1/7`$. Theorem 6.4 requires $`d\equiv-1\pmod q`$, which the fixed pair fails since $`7\equiv1\pmod3`$. The signed mean in (15.2) still requires centred prime-power sums on the selected host. [Prime selection in Section 6](./sections/prime-expansion.tex)

**One slope comparison.** Section 8.6 forms a direct sum over translates before composing the first operator. Each path keeps its translate label. Lemma 8.11 measures the finite denominator and archimedean norm costs, whose mean is $`\mathcal J`$. Theorem 8.12 and Corollary 8.13 compare slopes in a single normalized trace even when ranks and frame defects vary with $`u`$. The low target-slope tail contributes $`T_{\mathrm{out}}`$. [Section 8.6, pp. 124–127](./sections/translate-slopes.tex)

**How much error the window permits.** Proposition 11.3 and Corollaries 11.4–11.5 apply the mean division bound (11.1) and the frame, variation and size hypotheses on one host. At $`e_{\mathrm{div}}\le2`$, $`e_{\mathrm{loss}}=0`$, put $`y=x^\varepsilon`$ and define

```math
\begin{aligned}
P &= n_T a_E(1+m^2/k)+m(B_0+N_c),\\[2pt]
\Delta &= \mathbb{E}_{u\in A_0}(\mathcal A_u-G_u+\kappa I_u)
                -(1+\kappa)L_P.
\end{aligned}
```

Under those hypotheses the following single inequality, numbered (11.4) in the paper, suffices for (15.2).

```math
\Delta+\frac{4\mathcal J}{1-\delta_*}+T_{\mathrm{out}}
\le (y^5-y^3)P.
```

This gives the window exponent $`1/2+9\varepsilon`$. If $`\mathcal J=T_{\mathrm{out}}=0`$ and $`\Delta\le0`$, the same argument gives $`G_{\mathcal F_\psi}(x)\le x^{1/2+7\varepsilon}`$. The arithmetic bounds must hold uniformly on the required windows. [Section 11.1, pp. 260–263](./sections/mean-assembly.tex)

Corollary 15.34 reduces both estimates, under the stated host, overlap and local comparison hypotheses, to an upper bound on one signed relative determinant at one translate and one positive-rank word. For any fixed integer $`r\ge1`$, the bound must hold at all but an $`O(X^{-c})`$ fraction of the integer $`r`$th powers in arbitrarily late fixed-ratio intervals, for some fixed $`c>0`$. This arithmetic bound remains open. For primitive conductors up to 400,000, Corollary 15.35 gives a subinterval of length $`2t^{1-\nu}`$ for every fixed $`0<\nu<1`$ in each sufficiently late such interval contained in a supplied window. Both estimates hold throughout that subinterval. [Section 15, pp. 323–325](./sections/sparse-window-mean.tex)

## Paper coverage and remaining inputs

The entries give printed page numbers in the 329-page edition. The 96-entry register lists individual results, hypotheses and outstanding inputs. [Proof-status table](./audit/paper-proof-status.tsv)

**Critical-line deduction and Fourier extraction (§§1, 10, 12–13, pp. 2–3, 252–258, 263–267).** Lemma 10.1 proves the inertia and centring identity. Propositions 10.3–10.4 and Corollaries 10.5–10.6 give the four losses, signed mean, discarded-twist bound and square test. Given the arithmetic hypotheses, Proposition 12.1, Lemmas 12.2–12.4 and Theorem 12.5 isolate a pole and exclude it from the half-plane. Section 13 passes to arbitrary conductors and reflects across the critical line.

**Auxiliary primes and the common field (§§4.1–4.2, 6–7, pp. 23–26, 107–115).** Lemma 4.1 proves the $`O(Q^{1/4})`$ auxiliary-box bound. Theorem 6.4 selects the primes $`q,d`$ while allowing an exceptional real zero. The results in §7 construct the cyclotomic CM host and half-different lattice (7.1–7.2), fit the rank, choose the orbit-avoiding and biased sets (7.3–7.5), and control the thin coordinates and CM scalar (7.6, 7.8). Simultaneous automorphic realization across the translates enters in §11.

**Galois representations and crystalline lattices (§§2–3, pp. 3–23).** The paper proves trace interpolation and semisimple realization (2.1–2.2), lacunary rank extraction (3.2), crystalline closure using T. Liu (3.5), rectangular period comparisons (3.6–3.7), and principal-level and adjoint Selmer consequences for the stated classical systems (3.8–3.11). Results 3.12–3.15 give exact periods on the odd-rank spherical subfamily under its stated seed and congruence hypotheses, classical attachment on the standard definite unitary group, and cuspidal congruences at fixed weights. Realizing the singular-weight towers with the required genericity and linked bounded-height integral period frames remains open. [Sections 3.8–3.10](./sections/galois-supplement.tex)

**Integral cohomology, deformation rings and Selmer groups (§§4.3–4.5, 5, pp. 26–107).** The paper obtains cyclotomic descent and a moving two-rank (5.3), the low-layer $`H^2`$ bound $`C_K=32`$ (5.4), a multigraded Koszul intersection bound (5.20), and rank-three and rank-four trace products (5.22, 5.27). Results 5.30–5.39 treat specified endoscopic, odd-orthogonal and imprimitive quartic branches. Results 5.45 and 5.47–5.53 give the auxiliary two-power Bernoulli unit, all-depth vanishings, the empty Case III for two-power-order targets including $`\psi=1`$, and a summed Selmer estimate on $`16fe\le x^{\varepsilon/204}`$. Results 4.2–4.4 construct integral twisted-norm cycles and compute the valuation loss, including at two. Results 5.63–5.70 bound the dyadic field contribution through all twists $`1\le e<\lfloor v^{401}\rfloor`$ on a jointly selected window and the entire odd-prime opposite-parity sum. Corollary 5.70 isolates the remaining matching-parity contributions in Cases I, II, III and V outside the proved ranges. The strongly irreducible branches, the even two-dimensional block, characteristic-$`\ell`$ test curves, component propagation and one-sided exclusions still require arithmetic input. [Twisted-norm cycles](./sections/twisted-norm-cycles.tex) · [Selmer reduction](./sections/odd-field-supplement.tex)

**Theta chains and family assembly (§§8, 11, pp. 115–127, 258–263).** Results 8.1–8.7 cover chain composition, integral shifts, determinant costs, descended heights, frame coercivity and the finite-layer Harder–Narasimhan estimate. Results 8.11–8.13 and 11.3–11.5 give the single translate-mean comparison above. Applying it throughout the family still needs actual local chain valuations, recorded gains for the descended columns, the archimedean frame bounds and the simultaneous data in Formal input 11.2.

**Theta periods (§§9.1–9.5, pp. 127–177).** The paper treats split, inert and real local matching quotients. Theorem 9.38 gives global proportionality $`I(\Phi)=cI'(\Phi')`$ and both rank recursions for matched periods at the stated signatures.

**Theta denominators and arithmetic Hilbert–Samuel (§§9.6–9.11, pp. 177–252).** The paper treats semiabelian denominators $`D_M^2`$ (9.54), short harmonic generators (9.61), the doubled graph and spanning on marked charts (9.69–9.70, 9.76–9.80), cusp, half-maximum and flag-volume estimates giving the Bergman bound $`\beta_*`$ (9.72–9.75), and the integral Moret–Bailly key (9.82). Results 9.85, 9.87 and 9.88 compare product CM degrees and vertical orders and produce bounded final-weight sections on a good indefinite cover. Results 9.40–9.45 and 9.89–9.90 give the normed-filtration degree estimates. Applying them throughout the family requires compatible good deep covers (`Y.Good(e,o)` and `Y.Match`), integral flag and toroidal subcanonical sheaf comparisons, and uniform restriction, Chow-height and `MeanAll` bounds.

### The zeta specialization and the deep covers

For the trivial target, Proposition 5.58 identifies every layer at $`(\ell,\xi)=(3,J_d)`$ with equivariant homomorphisms from a finite real abelian class group. Two consecutive layers of equal order give the full length. At $`q=43,\ d=325079,\ e=3`$ the normalized length is one. Results 5.60–5.62 identify the odd-prime field summands, bound the whole opposite-parity sum, and give a common integer for Case I under the ternary trace-product hypothesis. The specialized Case II deformation level is $`\lceil\log_2(192N)\rceil`$. For this target, Case III is empty and the dyadic field term satisfies the window budget. The remaining matching-parity entries lie in Cases I, II and V. [Sections 5.21–5.23](./sections/selmer-uniform-continuation.tex) · [Exact class-number calculation](./verification/check_zeta_jd_example.py)

Proposition 9.91 constructs a ray class coefficient field within the deep-level budget. Lemma 9.92 computes both finite-index and archimedean costs of changing the flag lattice. Proposition 9.93 reduces the mixed component mean height to the norms of finitely many parameter sections per weight and component. Results 9.94–9.96 construct a rational CM point on each principal marked component, compare the split half-level maps and their metrics, and identify the unmodified central-weight-zero flag lattice at good primes. The modified flag, the indices at bad primes and the final signed component height still require estimates. [Section 9.10](./sections/theta-expansion.tex) · [Section 9.11](./sections/geometry-supplement.tex)

## Building and verifying the paper

From the repository root, build the manuscript with Tectonic. The output is `main.pdf`.

```sh
tectonic main.tex
```

Section 14 describes the external checks on the upstream export and the independent local checks on a prefix. The upstream record reports kernel replay of 175,187 compiled modules and checks with Nanoda, ConLeche and Lean4Lean. The classical root uses `Classical.choice`, `propext` and `Quot.sound`. [Upstream verification record](https://math.mit.edu/~drew/grh/)

| Local evidence | What it checks |
| --- | --- |
| [Prefix digest and size](./verification/prefix-receipt.json) · [arithmetic declaration indices](./verification/arithmetic-prefix-receipt.json) | An unmodified prefix of 1,539,032,259 bytes and 140,192 raw declaration records, including `rh_of_every`, `poleData`, `landau_window`, `ch_core`, `ch_top` and `core_gm`. |
| [Nanoda log](./verification/nanoda-prefix.log) · [ConLeche log](./verification/con-leche-prefix.log) | Nanoda 0.4.17 checked 145,327 internal declarations. ConLeche accepted 140,188 declarations and completed 137,728 deferred checks. |
| [WindowBridge.lean](./verification/WindowBridge.lean) | The logarithmic exceptional-set window lemma, with $`J=4(2C/\eta)^R`$. |
| [CriticalLineBridge.lean](./verification/CriticalLineBridge.lean) | The choice of exponents and the passage from arbitrarily late arithmetic windows to zero exclusion to the right of $`\operatorname{Re}s=1/2`$, under the stated analytic input. |
| [Case I and II proof-value paths](./verification/zeta-count-trace.zip) | Original serialized expressions and direct references in 24 pinned compiled modules for the two generic deformation counts. |
| [TranslateMean.lean](./verification/TranslateMean.lean) | Finite-group character projection and uniform error averaging used in Proposition 10.4. |

The three Mathlib bridge files use Lean 4.36.0 and Mathlib v4.36.0. The [supplementary arithmetic modules](./lean-15-1) and the [local pairing test](./verification/LargePrimePrecision.lean) use the pinned original Lean 4.33.1 project. The verification guide gives the commands, pinned versions and scope of each check. [Verification guide](./verification/README.md) · [Manuscript build checks](./verification/manuscript-check.log)

## Compute and development log

The initial end-to-end breakdown and paper reconstruction used **GPT-6.2 Astra** and approximately **70% of a single Pro 100 weekly quota**, according to the project author's estimate. Current work focuses on the uniform arithmetic inputs for (15.1) and (15.2).

## Primary references

- L. Alpöge, *Announcement of a proof of the Riemann hypothesis*, 20 November 2026. [Author's release note](https://alpo.ge/remark.pdf)
- L. Alpöge with Claude, *Lean formalization of RH and Dirichlet GRH*, Lean 4.33.1. [Pinned community mirror](https://github.com/leanprover-community/riemann-hypothesis/tree/40e56bab026552e089d7afcfeff08d2defb9c005)
- A. V. Sutherland, *Verification files for the Lean proof of the Riemann Hypothesis*. [Verification archive](https://math.mit.edu/~drew/grh/)

The paper's 79 bibliography entries appear on pp. 325–329. [Manuscript PDF](./Arithmetic-reconstruction-after-review.pdf)
