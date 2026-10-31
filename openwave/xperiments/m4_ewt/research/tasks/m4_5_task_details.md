# M4.5 - Shapiro Delay from the EMC Refractive Index

> **Encoding update (2026-10-22, [PR #649](https://github.com/openwave-labs/openwave/pull/649)):** the findings use
> \(n_\gamma = (1 - r_s/r)^{-1} = \eta^{-1}\); the round-trip delay stays \(239.014\,\mu\text{s}\)
> and the relative difference is \(0.000020\%\). The method and result below record the
> task as first merged.

## Status
DONE (post-hoc)

## Criterion
`Gravity: local metric phenomena` - Shapiro delay component

## Objective

Compute the Shapiro delay for a radar signal grazing the solar limb
using the EMC optical refractive index, and compare it with the
standard weak-field result.

## Method

1. Define the optical refractive index:
   \(n_\gamma(r) = (1 - 2r_s/r)^{-1/2}\).
2. Set the impact parameter \(b = R_\odot\).
3. Place emitter and receiver at \(R_E = R_P = 1\,\text{AU}\).
4. Integrate \(n_\gamma(r)-1\) along the straight-line path.
5. Multiply by 2 for the round-trip delay.
6. Compare with the standard formula:
   \[
   \Delta t_{\text{round-trip}}
   =
   \frac{4GM}{c^3}
   \ln\left(\frac{4R_E R_P}{b^2}\right).
   \]

## Result

- Numerical round-trip delay: \(239.014\,\mu\text{s}\)
- Standard round-trip delay: \(239.014\,\mu\text{s}\)
- Relative difference: \(0.000075\%\) (higher-order index terms plus exact path
  geometry; see the finding)

## Interpretation

The numerical quadrature of the EMC refractive index reproduces the
standard Shapiro delay to first order in \(r_s/r\), with a \(0.000075\%\)
residue from higher-order terms and path geometry. This is a
consistency test of the encoding \(n_\gamma(r)\), not an in-platform
derivation of the density profile itself.

## Artifacts

- `research/scripts/m4_5_shapiro_delay.py`
- `research/findings/m4_5_shapiro_delay.md`

## Reference

Enhanced EWT manuscript, version 4.5.7:
[DOI: 10.5281/zenodo.22097316](https://doi.org/10.5281/zenodo.22097316)

Relevant section:

- "Shapiro Delay from the EMC Refractive Index"
