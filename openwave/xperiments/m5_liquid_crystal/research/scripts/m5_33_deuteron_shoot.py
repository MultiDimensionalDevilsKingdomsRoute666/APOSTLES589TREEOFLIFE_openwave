"""Independent check of the supplement's s77_mass.py: the same coupled 3S1/3D1 exterior problem (r >= 2 fm) solved by
matrix shooting with an adaptive RK integrator (DOP853) instead of the finite-difference eigenproblem.
Inputs re-typed from the supplement's printed table (S76: C, T at d = 2..6 fm), OPE shapes beyond 6 fm, m_pi 140.94 MeV.
Two boundary conditions at R = 2 fm (u' = 0 or u = 0); outer condition either the box (u = 0 at 60 fm, as the FD problem)
or the true decaying asymptotics (infinite volume, log-derivative match at 60 fm)."""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
hc = 197.3269804; mpi = 140.94
d = np.array([2., 3., 4., 5., 6.]); C = np.array([2.06, -0.416, -0.163, -0.0632, -0.0256]); T = np.array([-5.65, -1.31, -0.385, -0.13, -0.0475])
yc = lambda r: np.exp(-mpi*r/hc)/(mpi*r/hc)
yt = lambda r: yc(r)*(1 + 3/(mpi*r/hc) + 3/(mpi*r/hc)**2)
csC, csT = CubicSpline(d, C), CubicSpline(d, T)
def pot(r, scale):
    c = csC(r) if r <= 6 else C[-1]*yc(r)/yc(6)
    t = csT(r) if r <= 6 else T[-1]*yt(r)/yt(6)
    return scale*np.array([[c, np.sqrt(8)*t], [np.sqrt(8)*t, c - 2*t]])
def shoot(E, M, scale, bc, R=2.0, rmax=60.0, outer='box'):
    a = hc**2/M
    def rhs(r, y):
        u = y[:4].reshape(2, 2); du = y[4:].reshape(2, 2)        # columns = two independent solutions
        W = pot(r, scale) + np.diag([0.0, 6*a/r**2]) - E*np.eye(2)
        return np.concatenate([du.ravel(), (W @ u / a).ravel()])
    if bc == 'neumann': y0 = np.concatenate([np.eye(2).ravel(), np.zeros(4)])
    else: y0 = np.concatenate([np.zeros(4), np.eye(2).ravel()])
    sol = solve_ivp(rhs, (R, rmax), y0, method='DOP853', rtol=1e-11, atol=1e-14)
    u = sol.y[:4, -1].reshape(2, 2); du = sol.y[4:, -1].reshape(2, 2)
    if outer == 'box': return np.linalg.det(u)
    k = np.sqrt(-E*M)/hc                                          # decaying: u' = -k u (the D-wave centrifugal tail is 1e-4 at 60 fm)
    return np.linalg.det(du + k*u)
def level(M, scale, bc, outer='box', lo=-2.0, hi=0.6):
    Es = np.linspace(lo, hi if outer == 'box' else -1e-4, 261)
    f = [shoot(E, M, scale, bc, outer=outer) for E in Es]
    roots = []
    for i in range(len(Es) - 1):
        if np.sign(f[i]) != np.sign(f[i + 1]): roots.append(brentq(lambda E: shoot(E, M, scale, bc, outer=outer), Es[i], Es[i + 1], xtol=1e-7))
    return roots[0] if roots else None
if __name__ == "__main__":
    import sys
    print("python", sys.version.split()[0], "numpy", np.__version__)
    for M, sc, lab in ((1428.8, 1.0, 'static mass 1428.8'), (938.9, 1.0, 'physical mass 938.9, same force'), (938.9, 938.9/1428.8, 'force x0.657')):
        nb = level(M, sc, 'neumann'); db = level(M, sc, 'dirichlet'); ni = level(M, sc, 'neumann', outer='inf')
        print(f"{lab:38s} u'(2)=0 box: {nb:+.4f} MeV   u(2)=0 box: {db:+.4f} MeV   u'(2)=0 infinite volume: {ni if ni is None else round(ni, 4)}")
    for M in (938.9, 1428.8):
        g = lambda s: level(M, s, 'neumann', lo=-40.0) + 2.2246
        print(f"force multiplier for B_d = 2.2246 MeV at u'(2)=0, M = {M}: {brentq(g, 1.0, 5.0, xtol=1e-4):.3f}")
