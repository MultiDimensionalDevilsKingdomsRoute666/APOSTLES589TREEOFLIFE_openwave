# M4 Light Bending from EMC Density Gradient

> This is an Enhanced EWT extension, authored by Łukasz Smoliński, as registered in
> [`_CITATIONS.md`](../../theory/_CITATIONS.md) (The Geometric Identity of Gravity and
> Dimensional Unification, v5.1.7, DOI
> [10.5281/zenodo.23559858](https://doi.org/10.5281/zenodo.23559858)).

## Criterion
Gravity: local metric phenomena (light bending component; gravitational
time dilation is computed separately in M4.4, Shapiro delay is computed
separately in M4.5)

## Status
⚠️ partial validation candidate

## Mechanism

In the Enhanced EWT framework, the speed of light is the structural
conversion factor between the spatial and temporal steps of the BCC
lattice:

\[
c \equiv \frac{\lambda_l}{t_p}.
\]

In the natural units of the lattice, \(c = 1\) and therefore
\([m] = [s]\). Consequently, a single EMC-density deformation
manifests simultaneously as:

- **light bending** — the ray follows the deformed lattice geometry
  produced by the EMC displacement field
  \(\vec{u}(r) = -\chi \nabla N_\nu(r)\),
- **gravitational time dilation** — a clock ticks more slowly
  because the geometric path required for each internal signal
  changes in the same density gradient.

Thus, within this model, a test of light bending is also a test of
the geometric mechanism underlying gravitational time dilation.
They are not independent phenomena.

## Method

- Assumed EMC density profile:
  \[
  N_\nu(r) = N_{\text{stat}} \left(1 - \frac{r_s}{r}\right),
  \]
  where \(r_s = 2GM_{\odot}/c^2\).

- The displacement field is encoded by the scalar
  \[
  n(r) = 1 / \left(1 - \frac{r_s}{r}\right) = \eta(r)^{-1},
  \]
  which is not an independent optical assumption but a convenient
  representation of the deformed EMC geometry. It combines the spatial
  stretching of the cell spacing (\(\eta^{-1/2}\)) and the temporal
  dilation of the propagation period (\(\eta^{-1/2}\)) of the strained
  lattice.

- The bending angle is obtained from the standard ray integral in
  the variable \(u = R_{\odot}/r\):

  \[
  \Delta\theta
  = \frac{2r_s}{R_{\odot}}
    \int_0^1
    \frac{
      u\left(1 - \frac{r_s u}{R_{\odot}}\right)^{-2}
    }{
      \sqrt{1-u^2}
    }
    \,du .
  \]

## Result

- Solar-limb bending angle:
  \(\Delta\theta = 1.751722\) arcsec
- Reference value (general-relativistic prediction): \(1.7517\) arcsec
- Relative difference: \(0.0012\%\)

## Model assumptions (derived in the manuscript, not fitted here)

The following are not free parameters but structural consequences of
the Enhanced EWT lattice model, derived in the cited manuscript sections
(Reference) and not recomputed in-platform:

- The normalised EMC density profile
  \(N_\nu(r)/N_{\text{stat}} = 1 - r_s/r\)
  follows from the weak-field spherical deficit around a matter
  soliton.
- The radial displacement
  \(u_r(r) = \int_r^\infty |\nabla(N_\nu/N_{\text{stat}})| dr'\)
  is the cumulative structural response to that deficit.
- At first order in the weak-field expansion, the scalar index is
  \(n_\gamma(r) \approx 1 + u_r(r) = 1 + r_s/r\).
- The full non-linear expression is
  \(n_\gamma(r) = \eta(r)^{-1} = (1 - r_s/r)^{-1}\), combining the
  spatial stretching \(\eta^{-1/2}\) and the temporal dilation
  \(\eta^{-1/2}\) of the strained lattice. It equals the radial
  Schwarzschild optical factor \(\sqrt{|g_{rr}/g_{00}|}\) exactly.

No free numerical parameters are introduced.

## Interpretation

The numerical result shows that once the EMC density deficit is
encoded as \(n(r) = \eta(r)^{-1} = (1 - r_s/r)^{-1}\),
the standard ray integral reproduces the observed solar-limb bending.
The encoding, not the bending, is the model-specific step: the
derivation of \(n(r)\) from lattice elasticity is given in the
manuscript (Reference); it is not recomputed in-platform, so
in-platform this artifact remains a consistency test of the encoding.
The same density ratio \(\eta\) is argued, via \(c \equiv \lambda_l/t_p\), to control clock rates; gravitational
time dilation is not separately computed here.

Formally, the ray bends because of the gradient of the phase
velocity. In EWT, the physical carrier of this gradient is the
lattice deformation field \(\vec{u}(r)\), not an abstract optical
property.

## Reference

Full derivation in the Enhanced EWT manuscript, version 5.1.7:
[DOI: 10.5281/zenodo.23559858](https://doi.org/10.5281/zenodo.23559858) (version DOI; concept DOI 10.5281/zenodo.17654657)

Relevant sections:

- "The Two Faces of EMC Displacement: Speed and Trajectory"
- "Bridging the Vector Displacement to the Scalar Refractive Index"
- "Asymptotic Continuous Limit and Schwarzschild Equivalence"
