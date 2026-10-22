#!/usr/bin/env python3
"""
M4/EWT - Shapiro delay from the EMC refractive index.

OpenWave criterion:
    Gravity: local metric phenomena
    Test: Shapiro delay / radar round-trip delay

Mechanism:
    The same EMC density deficit that curves light also slows the
    coordinate propagation of a photon. In natural lattice units the
    photon speed is

        v_gamma(r) = 1 / n_gamma(r),

    where n_gamma(r) is the optical refractive index derived in the
    Enhanced EWT manuscript v4.5.7.

    The excess coordinate time along a straight-line path is

        Delta_t = integral (n_gamma(r) - 1) ds.

    For a round-trip radar signal with impact parameter b, this gives
    the standard Shapiro delay.

This script computes the delay by numerical quadrature and compares it
with the standard weak-field logarithmic formula.
"""

import math

# ----------------------------------------------------------------------
# 1. Physical constants
# ----------------------------------------------------------------------
print("[1/4] Loading physical constants...")

G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 299792458.0  # m/s
M_sun = 1.989e30  # kg
R_sun = 6.957e8  # m

r_s = 2.0 * G * M_sun / (c * c)

# Heliocentric distances of emitter and receiver for a grazing radar
# signal. For a simple Earth-Sun-Earth test, both are set to 1 AU.
AU = 1.495978707e11  # m

b = R_sun  # impact parameter at the solar limb

print(f"    G          = {G:.6e} m^3 kg^-1 s^-2")
print(f"    c          = {c:.3f} m/s")
print(f"    M_sun      = {M_sun:.3e} kg")
print(f"    R_sun      = {R_sun:.3e} m")
print(f"    r_s        = {r_s:.3f} m")
print(f"    b          = {b:.3e} m")

# ----------------------------------------------------------------------
# 2. Refractive index and integration path
# ----------------------------------------------------------------------
print("[2/4] Building the EMC refractive index and integration path...")


def n_gamma(x, b):
    """
    Full EMC optical index along a straight line y = b.

    n_gamma(r) = 1 / (1 - r_s/r) = eta(r)^(-1)
    """
    r = math.sqrt(x * x + b * b)
    eta = 1.0 - r_s / r
    return 1.0 / eta


# Integration limits for the round-trip path.
# Emitter and receiver are placed symmetrically at distance AU.
L = math.sqrt(AU * AU - b * b)

print(f"    L = sqrt(AU^2 - b^2) = {L:.6e} m")

# ----------------------------------------------------------------------
# 3. Numerical Shapiro delay
# ----------------------------------------------------------------------
print("[3/4] Computing the Shapiro delay by numerical integration...")

try:
    from scipy.integrate import quad

    USE_SCIPY = True
except ImportError:
    USE_SCIPY = False
    print("    scipy not available; using simple trapezoidal fallback.")

if USE_SCIPY:

    def integrand(x):
        return n_gamma(x, b) - 1.0

    # Integrate separately over [-L, 0] and [0, L] to avoid numerical
    # roundoff warnings on a long symmetric interval.
    integral_left, err_left = quad(integrand, -L, 0, epsabs=1e-12, epsrel=1e-10, limit=200)
    integral_right, err_right = quad(integrand, 0, L, epsabs=1e-12, epsrel=1e-10, limit=200)
    integral_one_way = integral_left + integral_right
    delay_round_trip = 2.0 * integral_one_way / c
else:
    N = 20000
    dx = 2.0 * L / N
    total = 0.0
    for i in range(N):
        x = -L + (i + 0.5) * dx
        total += (n_gamma(x, b) - 1.0) * dx
    integral_one_way = total
    delay_round_trip = 2.0 * integral_one_way / c

print(f"    Integral one-way  = {integral_one_way:.6e} m")
print(f"    Delay round-trip  = {delay_round_trip:.6e} s")
print(f"    Delay round-trip  = {delay_round_trip * 1e6:.3f} us")

# ----------------------------------------------------------------------
# 4. Standard logarithmic formula and comparison
# ----------------------------------------------------------------------
print("[4/4] Comparing with the standard weak-field formula...")

# Standard Shapiro delay for round-trip radar signal:
#   Delta_t = (4GM/c^3) * ln(4 R_E R_P / b^2)
# with R_E = R_P = AU.
delay_standard = (4.0 * G * M_sun / (c**3)) * math.log(4.0 * AU * AU / (b * b))

rel_diff = abs(delay_round_trip - delay_standard) / delay_standard * 100.0

print(f"    Standard delay     = {delay_standard * 1e6:.3f} us")
print(f"    Relative difference = {rel_diff:.6f}%")

if rel_diff < 0.1:
    print("    RESULT: PASS (numerical quadrature matches standard formula)")
else:
    print("    RESULT: FAIL")

print("\nDone.")
