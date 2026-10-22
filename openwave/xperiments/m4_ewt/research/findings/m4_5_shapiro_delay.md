# M4.5 Shapiro Delay from the EMC Refractive Index

> This is an Enhanced EWT extension, authored by Łukasz Smoliński, as registered in
> [`_CITATIONS.md`](../../theory/_CITATIONS.md) (The Geometric Identity of Gravity and
> Dimensional Unification, v4.5.7, DOI
> [10.5281/zenodo.22097316](https://doi.org/10.5281/zenodo.22097316)).

## Criterion
Gravity: local metric phenomena (Shapiro delay component)

## What was computed

A numerical quadrature of the EMC optical refractive index was used to
compute the round-trip radar delay for a signal grazing the solar limb.
The integration was performed along a straight-line path with impact
parameter \(b = R_\odot\), with emitter and receiver placed at 1 AU.

The result is compared with the standard weak-field Shapiro formula.

## Mechanism

In the Enhanced EWT framework, the same EMC density deficit that
curves light also reduces the coordinate propagation speed of a photon.

For a path with impact parameter \(b\), the photon speed is

\[
v_\gamma(r) = \frac{1}{n_\gamma(r)},
\]

where the optical refractive index is

\[
n_\gamma(r) = \left(1 - \frac{r_s}{r}\right)^{-1} = \eta(r)^{-1}.
\]

The excess coordinate time is therefore

\[
\Delta t
=
\int \bigl(n_\gamma(r)-1\bigr)\,ds .
\]

For a round-trip radar signal grazing the Sun, this reduces to the
standard logarithmic delay.

## Method

- Set \(r_s = 2GM/c^2\).
- Set the impact parameter \(b = R_\odot\).
- Place emitter and receiver at \(R_E = R_P = 1\,\text{AU}\).
- Integrate \(n_\gamma(r)-1\) numerically along the straight-line path.
- Multiply by 2 for the round-trip delay.
- Compare with the standard formula:
  \[
  \Delta t_{\text{round-trip}}
  =
  \frac{4GM}{c^3}
  \ln\left(\frac{4R_E R_P}{b^2}\right).
  \]

## Result

- Integral one-way: \(3.5827 \times 10^{4}\) m
- Numerical round-trip delay: \(239.014\,\mu\text{s}\)
- Standard round-trip delay: \(239.014\,\mu\text{s}\)
- Relative difference: \(0.000020\%\)

The residue is not quadrature error. To first order in \(r_s/r\) the
EMC index integrates exactly to the standard logarithmic formula; the
\(0.000020\%\) residue is the sum of the index's higher-order terms
and the exact straight-path geometry (\(\operatorname{asinh}(L/b)\)
against \(\ln(2\,\text{AU}/b)\)), both far below the \(0.1\%\) gate.

## Model assumptions (derived in the manuscript, not fitted here)

The following are not free parameters but structural consequences of
the Enhanced EWT lattice model:

- The normalised EMC density profile is
  \(\eta(r)=1-r_s/r\).
- The optical refractive index is
  \(n_\gamma(r)=\eta(r)^{-1}=(1-r_s/r)^{-1}\), which matches the
  exact Schwarzschild optical metric factor.
- The signal path is approximated as a straight line, which is
  valid in the weak-field regime.

No free numerical parameters are introduced.

## Reference

Full derivation in the Enhanced EWT manuscript, version 4.5.7:
[DOI: 10.5281/zenodo.22097316](https://doi.org/10.5281/zenodo.22097316)

Relevant section:

- "Shapiro Delay from the EMC Refractive Index"