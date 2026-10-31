# M4.4 Gravitational Time Dilation from the Internal EMC Soliton Clock

> This is an Enhanced EWT extension, authored by Łukasz Smoliński, as registered in
> [`_CITATIONS.md`](../../theory/_CITATIONS.md) (The Geometric Identity of Gravity and
> Dimensional Unification, v4.5.6, DOI
> [10.5281/zenodo.22086668](https://doi.org/10.5281/zenodo.22086668)).

## Criterion
Gravity: local metric phenomena (gravitational time dilation component)

## What was computed
The solar-limb gravitational redshift of a static clock from the EMC
clock-speed encoding, checked against the exact Schwarzschild redshift
factor. This covers the gravitational time dilation component only; the
light-bending component is covered separately in M4.3, and the Shapiro
delay in M4.5.

## Mechanism
A clock is a standing-wave soliton. Its period is the time for an
internal longitudinal EMC lattice wave to travel from one side of
the soliton to the opposite side and back.

In natural lattice units (\(c=1\)), the internal wave speed is

\[
v_{\text{clock}}(r) = \sqrt{\eta(r)},
\]

where

\[
\eta(r) = \frac{N_\nu(r)}{N_{\text{stat}}} = 1 - \frac{r_s}{r}.
\]

The predicted fractional frequency shift is computed directly as

\[
\frac{\Delta f}{f} = \frac{v_{\text{clock}}(r)}{c} - 1,
\]

not as an externally inserted metric formula.

The script evaluates the formula in SI units for numerical
convenience. The natural-unit argument in the manuscript establishes
the dimensionless structure \(v_{\text{clock}}/c = \sqrt{\eta}\),
so the conversion factors \(c\) and \(G\) cancel consistently.

## Method
- Compute the EMC density ratio at the solar limb:
  \(\eta = 1 - r_s/R_\odot\).
- Compute the internal clock speed:
  \(v_{\text{clock}}/c = \sqrt{\eta}\).
- Predict the gravitational redshift:
  \(\Delta f/f = v_{\text{clock}}/c - 1\).
- Compare with the exact GR value for a static clock,
  \(\sqrt{1 - 2\Phi_N} - 1\), computed from \(GM/(c^2 R_\odot)\)
  directly (identity check).
- Print the first-order value \(-\Phi_N\) as a labelled sanity line.

## Result
- \(\eta = 0.999995753735\)
- \(v_{\text{clock}}/c = 0.999997876865\)
- Predicted \(\Delta f/f = -2.123135 \times 10^{-6}\)
- Exact GR \(\Delta f/f = -2.123135 \times 10^{-6}\); difference \(0\) (identity)
- First-order reference \(-\Phi_N = -2.123132 \times 10^{-6}\);
  relative difference \(0.000106\%\), equal to \(x/4\) with
  \(x = r_s/R_\odot\), i.e. the truncation error of the first-order
  reference, not a model discrepancy.

Once \(\eta = 1 - r_s/r\) is granted, \(v_{\text{clock}}/c - 1 =
\sqrt{1 - r_s/r} - 1\) is identically the exact Schwarzschild redshift
factor for a static clock, so the encoding reproduces the exact GR
result, not an approximation to it.

## Model assumptions (derived in the manuscript, not fitted here)

The following are not free parameters but structural consequences of
the Enhanced EWT lattice model, derived in the cited manuscript sections
(Reference) and not recomputed in-platform:

- The local EMC density ratio is
  \(\eta(r) = N_\nu(r)/N_{\text{stat}} = 1 - r_s/r\),
  the same weak-field profile used in the light-bending artifact.
- The internal clock speed is
  \(v_{\text{clock}}(r) = \sqrt{\eta(r)}\),
  following from the same lattice-strain mechanism that defines the
  external optical index.
- The redshift is computed directly from the clock-speed cycle as
  \(\Delta f/f = v_{\text{clock}}/c - 1\),
  without inserting the GR formula by hand.

No free numerical parameters are introduced. In-platform, this artifact
is a consistency test of the clock-speed encoding: the derivation of
\(\eta(r)\) and \(v_{\text{clock}} = \sqrt{\eta}\) from lattice
elasticity lives in the manuscript, not here.

## Reference

Full derivation in the Enhanced EWT manuscript, version 4.5.6:
[DOI: 10.5281/zenodo.22086668](https://doi.org/10.5281/zenodo.22086668) (version DOI; concept DOI 10.5281/zenodo.17654657)

Relevant section:

- “Mechanical Origin of Gravitational Redshift in the EMC Lattice”
