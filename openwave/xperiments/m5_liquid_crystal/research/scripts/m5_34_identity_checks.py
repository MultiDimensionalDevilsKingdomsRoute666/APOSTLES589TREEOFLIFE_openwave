"""M5.34 R1v: our own verification of the identities the author's v1.1 package states about the
certified record action L_cert = -4 I1 - V4 (package scripts V1, V2, V3, V10, V6, V14, V49).

Every check here uses THIS repo's functions (m5_32_lagrangian.F_of_A, v4_traces_np, c4_of;
m5_32_r7_a_kt_form.kt_density_np) or a self-contained formula; nothing is imported from the package.
Each check states the input that would make it fail.

Run from this directory:  python3 m5_34_identity_checks.py  -> ../data/m5_34_identity_checks.json
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
from scipy.linalg import expm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m5_32_lagrangian as LAG                      # noqa: E402
import m5_32_r7_a_kt_form as KT                     # noqa: E402

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
P_TOY = dict(s=-1.0, g=32.0, delta=0.3, w=7.24023879e-4)
rng = np.random.default_rng(2026_10_26)
out: dict = {"versions": {"python": sys.version.split()[0], "numpy": np.__version__}}
t_start = time.time()


def sym(X):
    return X + X.swapaxes(-1, -2)


def I1_of_A(A):
    """sum_{mu<nu} eta^mu eta^nu tr(eta F eta F^T) with F from OUR F_of_A; A shape (4, 4, 4)."""
    F = LAG.F_of_A(A[:, None, None, None, :, :])[0, 0, 0]       # (4, 4, 4, 4)
    e = np.diag(ETA)
    tot = 0.0
    for mu in range(4):
        for nu in range(mu + 1, 4):
            Fm = F[mu, nu]
            tot += e[mu] * e[nu] * np.einsum("a,b,ab,ab->", e, e, Fm, Fm)
    return float(tot)


def V4_of_M(M, p=P_TOY):
    t = LAG.v4_traces_np(M)
    cp = LAG.c4_of(p)
    return float(p["w"] * sum((t[k] - cp[k]) ** 2 for k in range(4)))


def L_cert(M, A, p=P_TOY):
    return -4.0 * I1_of_A(A) - V4_of_M(M, p)


def random_jet():
    return sym(rng.normal(size=(4, 4, 4)))


def M_vac(p=P_TOY):
    return np.diag([-p["s"] * p["g"], 1.0, p["delta"], 0.0])


def sym_basis():
    out = []
    for a in range(4):
        X = np.zeros((4, 4)); X[a, a] = 1.0; out.append((f"diag{a}", X))
    for j in range(1, 4):
        X = np.zeros((4, 4)); X[0, j] = X[j, 0] = 1.0; out.append((f"boost0{j}", X))
    for i, j in [(1, 2), (1, 3), (2, 3)]:
        X = np.zeros((4, 4)); X[i, j] = X[j, i] = 1.0; out.append((f"rot{i}{j}", X))
    return out


# ---------------- V1: F is blind to the trace direction eta; eta is the only such constant direction ----------
res = []
for _ in range(50):
    A = random_jet(); s = rng.normal(size=4)
    A2 = A + s[:, None, None] * ETA[None]
    F1 = LAG.F_of_A(A[:, None, None, None])[0, 0, 0]; F2 = LAG.F_of_A(A2[:, None, None, None])[0, 0, 0]
    res.append(float(np.max(np.abs(F2 - F1))) / max(1.0, float(np.max(np.abs(F1)))))
# uniqueness: for which symmetric constant N does A -> A + s N leave F unchanged for all A? null space of the linear map
basis = sym_basis()
trials = [(random_jet(), rng.normal(size=4)) for _ in range(4)]      # ONE trial set for every column (the map is linear in N on a fixed set)
cols = []
for _, N in basis:
    col = []
    for A, s in trials:
        dF = LAG.F_of_A((A + s[:, None, None] * N[None])[:, None, None, None])[0, 0, 0] - LAG.F_of_A(A[:, None, None, None])[0, 0, 0]
        col.append(dF.ravel())
    cols.append(np.concatenate(col))
Mmat = np.array(cols).T
svals = np.linalg.svd(Mmat, compute_uv=False)
null = np.linalg.svd(Mmat)[2][-1]
Nnull = sum(c * X for c, (_, X) in zip(null, basis))
Nnull = Nnull / Nnull[1, 1]
out["V1_eta_shift"] = {
    "max_rel_residual_F(A+s.eta)-F(A)": max(res),
    "null_space_dim_(singular_values_below_1e-10)": int(np.sum(svals < 1e-10 * svals[0])),
    "null_direction_normalized": np.round(Nnull, 10).tolist(),
    "null_direction_is_eta": bool(np.allclose(Nnull, ETA, atol=1e-8)),
    "fails_if": "a residual above 1e-12, or a null space of dimension other than 1, or a null direction other than eta",
}

# ---------------- V2: homogeneous fields have F = 0; V4(M_vac) = 0; V4 >= 0 ----------
worst = 0.0
for _ in range(200):
    A = np.zeros((4, 4, 4)); A[0] = sym(rng.normal(size=(4, 4)))
    worst = max(worst, float(np.max(np.abs(LAG.F_of_A(A[:, None, None, None])))))
v4vac = V4_of_M(M_vac())
# V4 is w * sum of squares with w > 0: non-negative by construction; sample anyway
v4min = min(V4_of_M(sym(rng.normal(size=(4, 4))) * 10) for _ in range(500))
# the vacuum manifold: L M_vac L^T for internal O(1,3) L keeps V4 = 0 (the traces of (M eta)^p are invariants)
orb = []
for _ in range(50):
    K = np.zeros((4, 4)); th = rng.normal(size=3); K[0, 1:] = th; K[1:, 0] = th
    R = np.zeros((4, 4)); w = rng.normal(size=3)
    R[1, 2], R[2, 1], R[1, 3], R[3, 1], R[2, 3], R[3, 2] = w[0], -w[0], w[1], -w[1], w[2], -w[2]
    Lm = expm(K) @ expm(R)
    orb.append(V4_of_M(Lm @ M_vac() @ Lm.T))
out["V2_homogeneous_and_vacuum"] = {
    "max|F|_on_200_time-only_jets": worst,
    "V4(M_vac)": v4vac,
    "min_V4_over_500_random_M_(nonnegative_by_construction)": v4min,
    "max_V4_on_the_internal_O(1,3)_orbit_of_M_vac": max(orb),
    "reading": "a uniform M(t) has L = -V4, so the certified action carries no cosmological constant of its own (Lambda_own = 0) and no homogeneous negative energy density; the orbit check shows the vacuum manifold is the full O(1,3) orbit",
    "fails_if": "any F entry above 1e-14 on a time-only jet, or V4(M_vac) above 1e-20, or a negative V4 sample, or V4 above 1e-12 on the orbit",
}

# ---------------- V3 / V10: kinetic norms of the ten vacuum directions ----------
# a small oscillation M = M_vac + eps X(t): the jet is A_0 = eps Xdot, A_i = 0.
Mv = M_vac()
rows = {}
for name, X in basis:
    A = np.zeros((4, 4, 4)); A[0] = X
    i1 = I1_of_A(A)
    kcov = float(sum(np.diag(ETA)[mu] * np.trace(ETA @ A[mu] @ ETA @ A[mu]) for mu in range(4)))
    kt = float(KT.kt_density_np(A[:, None, None, None], Mv[None, None, None], P_TOY)[0, 0, 0])
    kh = kcov + 2.0 * kt
    rows[name] = {"-4I1": -4.0 * i1, "K_cov": kcov, "K_T": kt, "K_h=K_cov+2K_T": kh}
# second: a space-only jet A_x = X gives I1 = 0 too (F needs two derivative directions); mixed jets A_0 = X, A_x = Y
mixed = []
for _ in range(20):
    A = np.zeros((4, 4, 4)); A[0] = sym(rng.normal(size=(4, 4))); A[1] = sym(rng.normal(size=(4, 4)))
    mixed.append(I1_of_A(A))
out["V3_V10_kinetic_norms_about_M_vac"] = {
    "per_direction_(A_0 = X, A_i = 0)": rows,
    "-4I1_vanishes_for_every_single-derivative_jet": bool(all(abs(r["-4I1"]) < 1e-14 for r in rows.values())),
    "I1_on_mixed_(t,x)_jets_max": max(abs(v) for v in mixed),
    "reading": "the curvature term gives no quadratic kinetic norm to any direction about the uniform vacuum (F is bilinear in two different derivative directions); K_T is nonzero on the boosts only; K_cov is sign-indefinite across the ten; K_h = K_cov + 2K_T signs listed per direction",
    "fails_if": "-4I1 nonzero on a single-derivative jet, or K_T nonzero on a non-boost direction, or any K_h sign differing from the package's census when compared at R2",
}

# ---------------- V10: a Frobenius/director quadratic term on a uniaxial hedgehog is linear in R ----------
# S = b 1 + D n n^T with n = x/r: sum_i ||d_i S||_F^2 = D^2 sum_i ||d_i(n n^T)||^2 = 4 D^2 / r^2 (n n^T has 2 free
# unit-tangent directions per axis), so int_0^R 4 pi r^2 (4 D^2 / r^2) dr = 16 pi D^2 R.
rs = np.array([1.0, 2.0, 5.0, 10.0])
coef = []
for r in rs:
    acc = 0.0; cnt = 0
    for _ in range(200):
        n = rng.normal(size=3); n /= np.linalg.norm(n); x = r * n; h = 1e-5
        g = []
        for i in range(3):
            e = np.zeros(3); e[i] = h
            np_ = (x + e) / np.linalg.norm(x + e); nm = (x - e) / np.linalg.norm(x - e)
            g.append((np.outer(np_, np_) - np.outer(nm, nm)) / (2 * h))
        acc += sum(float(np.sum(G ** 2)) for G in g); cnt += 1
    coef.append(acc / cnt * r ** 2)
out["V10_director_term_on_a_hedgehog"] = {
    "r^2 * sum_i ||d_i(n n^T)||^2_(should_be_4)": [float(c) for c in coef],
    "exterior_energy_of_kappa*sum||dS||^2_from_r0_to_R": "16 pi kappa D^2 (R - r0): linear in R",
    "fails_if": "the sampled coefficient differs from 4 beyond 1e-6",
}

# ---------------- V6: the curvature term is homogeneous of degree 4 in the jets, so its stress trace vanishes ------
# Euler: sum_mu <dL_kin/dA_mu, A_mu> = 4 L_kin  (numeric directional derivative along A itself)
eul = []
for _ in range(30):
    A = random_jet(); h = 1e-6
    f = lambda lam: -4.0 * I1_of_A((1 + lam) * A)
    d = (f(h) - f(-h)) / (2 * h)
    eul.append(abs(d - 4 * f(0.0)) / max(1e-30, abs(4 * f(0.0))))
out["V6_stress_trace"] = {
    "max_rel_residual_Euler_degree4_on_-4I1": max(eul),
    "reading": "T^mu_mu = sum_mu <dL/dA_mu, A_mu> - 4 L = 4 L_kin - 4 (L_kin + L_pot) = -4 L_pot = 4 V4 in this sign convention (the author writes -4V with the opposite overall sign); the curvature term drops out of the trace in four dimensions. Static consequence (Derrick): E_F = 3 E_V, E_V / E = 1/4 for any stationary finite-energy state; checked on a stored relaxed hedgehog in part 2",
    "fails_if": "a residual above 1e-8",
}

# ---------------- V14: the EM reading f_{mu nu} = n . (d_mu n x d_nu n) has E.B = 0 identically ----------
# f is the pullback of the area form of S^2 by n: x -> S^2; a 4-form pulled back from a 2-manifold vanishes, so
# eps^{mu nu rho sigma} f_{mu nu} f_{rho sigma} = 0, i.e. E.B = 0, for EVERY map n(t, x).
def eps4():
    e = np.zeros((4, 4, 4, 4))
    import itertools
    for perm in itertools.permutations(range(4)):
        sgn = 1
        p = list(perm)
        for i in range(4):
            for j in range(i + 1, 4):
                if p[i] > p[j]: sgn = -sgn
        e[perm] = sgn
    return e
E4 = eps4()
eb = []
for _ in range(100):
    n = rng.normal(size=3); n /= np.linalg.norm(n)
    dn = rng.normal(size=(4, 3)); dn -= np.outer(dn @ n, n)          # tangent jets d_mu n
    f = np.array([[n @ np.cross(dn[m], dn[k]) for k in range(4)] for m in range(4)])
    eb.append(abs(float(np.einsum("mnrs,mn,rs->", E4, f, f))) / max(1e-30, float(np.sum(f ** 2))))
# contrast: a generic antisymmetric f has E.B != 0
f = rng.normal(size=(4, 4)); f -= f.T
contrast = abs(float(np.einsum("mnrs,mn,rs->", E4, f, f))) / float(np.sum(f ** 2))
out["V14_E_dot_B"] = {
    "max_rel_|eps f f|_for_pullback_f": max(eb),
    "generic_antisymmetric_f_(contrast)": contrast,
    "reading": "exact for the director's area-form reading of the field, by the dimension of S^2; the magnetic moment then has no E.B route and is the circulation of the charge, as the package states",
    "fails_if": "a nonzero value above 1e-12 for a pullback f, or a zero for the generic contrast",
}

# ---------------- V49: L_cert is invariant under internal O(1,3) and spacetime O(1,3) SEPARATELY ----------
def internal_boost(th, ax):
    K = np.zeros((4, 4)); K[0, ax] = K[ax, 0] = th; return expm(K)

def spacetime_boost(th, ax):
    return internal_boost(th, ax)      # the same matrix acting on the index mu

def ruleR_like(M, A):
    """a term contracting the record's timelike eigenvector u (read as a spacetime vector) with d_mu: tr(eta (u.A) eta (u.A))"""
    w, V = np.linalg.eig(M @ ETA)
    best = None
    for k in range(4):
        v = np.real(V[:, k]); nrm = v @ ETA @ v
        if nrm < 0 and (best is None or nrm < best[0]): best = (nrm, v / np.sqrt(-nrm))
    u = best[1]
    uA = np.einsum("m,mab->ab", u, A)
    return float(np.trace(ETA @ uA @ ETA @ uA))

r_int, r_st, r_rr_int, r_rr_st, r_rr_diag = [], [], [], [], []
for _ in range(40):
    M = M_vac() + 0.3 * sym(rng.normal(size=(4, 4))); A = random_jet()
    th = rng.normal() * 0.8; ax = int(rng.integers(1, 4))
    Li = internal_boost(th, ax); Ls = spacetime_boost(th, ax)
    L0 = L_cert(M, A)
    # internal: M -> L M L^T, A_mu -> L A_mu L^T
    Mi = Li @ M @ Li.T; Ai = np.einsum("ab,mbc,dc->mad", Li, A, Li)
    r_int.append(abs(L_cert(Mi, Ai) - L0) / max(1e-30, abs(L0)))
    # spacetime: A_mu -> (Lambda^{-1})^nu_mu A_nu  (the jet transforms as a covector); M unchanged
    Linv = np.linalg.inv(Ls)
    As = np.einsum("nm,nab->mab", Linv, A)
    r_st.append(abs(L_cert(M, As) - L0) / max(1e-30, abs(L0)))
    # the rule-R-like term: invariant only under the diagonal subgroup
    R0 = ruleR_like(M, A)
    r_rr_int.append(abs(ruleR_like(Mi, Ai) - R0) / max(1e-30, abs(R0)))
    r_rr_st.append(abs(ruleR_like(M, As) - R0) / max(1e-30, abs(R0)))
    r_rr_diag.append(abs(ruleR_like(Mi, np.einsum("nm,nab->mab", Linv, Ai)) - R0) / max(1e-30, abs(R0)))
out["V49_separate_invariances"] = {
    "L_cert_internal_O(1,3)_max_rel_residual": max(r_int),
    "L_cert_spacetime_O(1,3)_max_rel_residual": max(r_st),
    "ruleR_like_internal_only_max_rel_residual": max(r_rr_int),
    "ruleR_like_spacetime_only_max_rel_residual": max(r_rr_st),
    "ruleR_like_diagonal_max_rel_residual": max(r_rr_diag),
    "reading": "the certified action is invariant under the two groups separately (residuals at round-off); a term that contracts the record's u with d_mu is invariant only under the diagonal, which is where a fixed clock enters. This is a symmetry statement about the ACTION; the row's open item (a boosted defect measured in-sim) is a dynamics measurement and is not closed by it",
    "fails_if": "either L_cert residual above 1e-10, or the rule-R-like term NOT breaking one of the two factors (both its single-factor residuals below 1e-10)",
}

out["wall_s"] = round(time.time() - t_start, 2)
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "m5_34_identity_checks.json")
json.dump(out, open(dst, "w"), indent=1, default=float)
for k, v in out.items():
    if isinstance(v, dict):
        print(f"== {k}")
        for kk, vv in v.items():
            if kk in ("per_direction_(A_0 = X, A_i = 0)",):
                for nm, r in vv.items(): print(f"   {nm:9s} " + "  ".join(f"{a}={b:+.4g}" for a, b in r.items()))
            elif kk not in ("reading", "fails_if"):
                print(f"   {kk}: {vv}")
print("wall_s", out["wall_s"])
