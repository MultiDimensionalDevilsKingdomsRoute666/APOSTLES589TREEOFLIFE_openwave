"""M5.34 R1k: the two optional OpenWave checks of the author's v1.1 kit (NEXT_ROUND_KITS.md item C4), run on OUR
stored data and OUR instruments.

(i)  "the 4x4 clock inertia grows with the box as dkin/dR = 13.48 at delta = 0.3 (V11)": the author's coefficient
     K = 32 pi delta^2 [1 + (1 - delta)^2] against this repo's M5.21.14 bulk-kin base (the same quantity, our radial
     quadrature) and against the certified-lattice box ladder of M5.32 R4 (kin_cert at L = 48, 72, 96), with the
     cube-to-sphere geometry made explicit by a lattice shell sum of 1/r^2 on the same grid.
(ii) "mu = p x pdot / (2e) from the same run (V14)": on the fixed-clock electron of the M5.8.2r electron-ID
     instrument (tilt channel, the only EM-active one), the moment as the instrument reads it, the charge and dipole
     of the hedgehog's radial field, p x pdot / (2e), the dual-reading moment, and the surface term of the moment
     integral (the monopole field is not localized).

Run from this directory: python3 m5_34_kit_checks.py [n ...]  -> ../data/m5_34_kit_checks.json
"""
from __future__ import annotations
import importlib.util, json, os, sys, time, types
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
out: dict = {"versions": {"python": sys.version.split()[0], "numpy": np.__version__}}
t0 = time.time()

# ---------------------------------------------------------------- (i) the clock inertia's box growth
delta = 0.3
c_t = 8 * delta ** 2 * (1 + (1 - delta) ** 2)            # the twist energy density coefficient per r^2 (V11 A)
K_sphere = 4 * np.pi * c_t                              # = 32 pi delta^2 [1 + (1 - delta)^2]
m5_21_14_base = 13.4812                                 # findings/m5_21_14_note.md § 7 row 5 (own shell evaluation, 9-digit audit match)
m5_21_14_dressing, m5_21_14_net = -19.6044, -6.1232     # the same row: the first 1/g dressing term flips the bulk sign
ladder = {}
for tag, L in [("n32_L48", 48.0), ("n48_L72", 72.0), ("n64_L96", 96.0)]:
    d = json.load(open(os.path.join(DATA, f"m5_32_r4_audit_clock_box_{tag}.json")))
    ladder[L] = {"h": d["h"], "kin_cert": d["certified_crosscheck"]["kin_cert"], "E_u_cert": d["certified_crosscheck"]["E_u_cert"]}
Ls = sorted(ladder)
slopes = {f"{Ls[i]:.0f}->{Ls[i+1]:.0f}": (ladder[Ls[i+1]]["kin_cert"] - ladder[Ls[i]]["kin_cert"]) / (Ls[i+1] - Ls[i]) for i in range(len(Ls) - 1)}
# lattice shell sums of 1/r^2 on the R4 grid (h = 1.5, cell centres), between the cubes: the geometry the ladder sees
h = 1.5
def shell_sum(L_in, L_out):
    n = int(round(L_out / h)); xs = (np.arange(n) - (n - 1) / 2) * h
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij"); r2 = X ** 2 + Y ** 2 + Z ** 2
    inner = (np.abs(X) < L_in / 2) & (np.abs(Y) < L_in / 2) & (np.abs(Z) < L_in / 2)
    return float(np.sum(h ** 3 / r2[~inner]))
shells = {f"{Ls[i]:.0f}->{Ls[i+1]:.0f}": shell_sum(Ls[i], Ls[i + 1]) for i in range(len(Ls) - 1)}
# continuum cube integral per unit side (int over the unit cube of 1/|x|^2), by a fine lattice with the singular cell excluded
def I_cube(n=400):
    xs = (np.arange(n) - (n - 1) / 2) / n
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij"); r2 = X ** 2 + Y ** 2 + Z ** 2
    m = r2 > (2.0 / n) ** 2
    return float(np.sum(1.0 / r2[m]) / n ** 3 + 4 * np.pi * (2.0 / n))   # inner ball added analytically
Ic = I_cube()
pred = {k: c_t * v / 24.0 for k, v in shells.items()}      # c_t x (shell sum of 1/r^2) per unit side
out["i_clock_inertia_box_growth"] = {
    "author_K_sphere_32pi_delta2[1+(1-delta)^2]_per_unit_radius": K_sphere,
    "our_M5.21.14_base_per_unit_radius": m5_21_14_base,
    "ratio_author_over_ours": K_sphere / m5_21_14_base,
    "our_M5.21.14_dressing_per_unit_radius": m5_21_14_dressing,
    "our_M5.21.14_net_per_unit_radius": m5_21_14_net,
    "R4_certified_lattice_ladder_h1.5": {f"L_{L:.0f}": ladder[L] for L in Ls},
    "measured_dkin_dL_per_unit_side": slopes,
    "lattice_shell_sum_1_over_r2_between_cubes": shells,
    "continuum_cube_integral_per_unit_side": Ic,
    "sphere_integral_per_unit_radius_4pi": 4 * np.pi,
    "predicted_dkin_dL_from_c_t_x_shell_sum": pred,
    "measured_over_predicted": {k: slopes[k] / pred[k] for k in slopes},
    "reading": "the author's coefficient IS our M5.21.14 base coefficient (the undressed twist of the uniaxial exterior, same number to the printed digits); the certified-lattice ladder grows linearly with the box as that coefficient times the cube's 1/r^2 content (measured over predicted listed); what V11 does not carry is M5.21.14's finding that the first dressing term is extensive too and steeper, so the dressed bulk kin per unit radius is negative (net -6.12)",
    "fails_if": "the two per-radius coefficients differ beyond the printed digits, or the lattice ladder is not linear in L, or measured/predicted is far from 1 without a stencil reason",
}

# ---------------------------------------------------------------- (ii) mu = p x pdot / (2e) on the electron-ID instrument
# the instrument's imports name a retired layout (research.sandbox_v6 / sandbox_v8 / sandbox_vn); the files live in scripts/.
# Shim the package path so the instrument loads unmodified.
def _shim(pkg_path, modname, filename):
    parts = pkg_path.split(".")
    for i in range(1, len(parts) + 1):
        name = ".".join(parts[:i])
        if name not in sys.modules:
            m = types.ModuleType(name); m.__path__ = []; sys.modules[name] = m
    full = pkg_path + "." + modname
    if full in sys.modules: return sys.modules[full]
    spec = importlib.util.spec_from_file_location(full, os.path.join(HERE, filename))
    m = importlib.util.module_from_spec(spec); sys.modules[full] = m; spec.loader.exec_module(m)
    return m
BASE = "openwave.xperiments.m5_liquid_crystal.research"
_shim(BASE + ".sandbox_v6", "m5_6_2a_biaxial_hedgehog", "m5_6_2a_biaxial_hedgehog.py")
_shim(BASE + ".sandbox_v8", "m5_8_2a_4d_hamiltonian", "m5_8_2a_4d_hamiltonian.py")
_shim(BASE + ".sandbox_v8", "m5_8_2c1_full_evolution", "m5_8_2c1_full_evolution.py")
_shim(BASE + ".sandbox_v8", "m5_8_2cb_taichi_constrained", "m5_8_2cb_taichi_constrained.py")
_shim(BASE + ".sandbox_vn", "m5_8_2h_omega_attractor", "m5_8_2h_omega_attractor.py")
spec = importlib.util.spec_from_file_location("eid", os.path.join(HERE, "m5_8_2r_electron_id.py"))
eid = importlib.util.module_from_spec(spec); spec.loader.exec_module(eid)
central = eid.central

def div(V, h):
    return central(V[..., 0], 0, h) + central(V[..., 1], 1, h) + central(V[..., 2], 2, h)

def coords(n, h):
    c = (n - 1) / 2.0
    return (np.indices((n, n, n)).transpose(1, 2, 3, 0) - c) * h

ns = [int(a) for a in sys.argv[1:]] or [24, 32]
rows = {}
dphi, dphi2 = 1e-4, 1e-3
for n in ns:
    for b in (0.0, eid.B_STAR):
        tag = f"tilt_n{n}_b{b:.2f}"
        gr, W, M, Mth, act = eid.grid_and_seed(n, b=b, plane=(1, 2), phi=0.0)
        h = gr["h"]; X = coords(n, h)
        def eb(ph):
            _, Wx, _, _, _ = eid.grid_and_seed(n, b=b, plane=(1, 2), phi=ph)
            n0 = eid.director_of(Wx)
            _, Wy, _, _, _ = eid.grid_and_seed(n, b=b, plane=(1, 2), phi=ph + dphi)
            return eid.EB_of(n0, (eid.director_of(Wy) - n0) / dphi, h)
        E0, B0 = eb(0.0); E1, B1 = eb(dphi2)
        mu_inst, jmax, Emax = eid.mu_of(gr, (E0, B0), (E1, B1), dphi2, act)
        # the hedgehog's radial field is the spatial 2-form (the instrument's B): its source is the topological charge
        rho0 = div(B0, h); rho1 = div(B1, h)
        e_tot = float(rho0[act].sum() * h ** 3)          # over the instrument's active mask (core excluded)
        inter = np.zeros(rho0.shape, bool); inter[2:-2, 2:-2, 2:-2] = True
        e_full = float(rho0[inter].sum() * h ** 3)       # over the whole interior, core included: the topological charge
        k = 2                                            # the flux of B through the faces of the interior cube
        flux = (B0[-1 - k, k:-k, k:-k, 0].sum() - B0[k, k:-k, k:-k, 0].sum() + B0[k:-k, -1 - k, k:-k, 1].sum() - B0[k:-k, k, k:-k, 1].sum()
                + B0[k:-k, k:-k, -1 - k, 2].sum() - B0[k:-k, k:-k, k, 2].sum()) * h ** 2
        p0 = (X * rho0[..., None])[act].sum(axis=0) * h ** 3
        p1 = (X * rho1[..., None])[act].sum(axis=0) * h ** 3
        pdot = eid.OMEGA * (p1 - p0) / dphi2
        mu_pred = np.cross(p0, pdot) / (2 * e_tot) if abs(e_tot) > 0 else np.full(3, np.nan)
        # the instrument's current split and the surface term: 1/2 int x x curl B = int B + surface term for a localized B
        curlB = eid.curl(B0, h)
        term_curl = 0.5 * np.cross(X, curlB)[act].sum(axis=0) * h ** 3
        term_disp = -0.5 * np.cross(X, eid.OMEGA * (E1 - E0) / dphi2)[act].sum(axis=0) * h ** 3
        intB = B0[act].sum(axis=0) * h ** 3
        # the dual reading (the radial 2-form read as the ELECTRIC field): j_dual = -curl E - d_t B
        j_dual = -eid.curl(E0, h) - eid.OMEGA * (B1 - B0) / dphi2
        mu_dual = 0.5 * np.cross(X, j_dual)[act].sum(axis=0) * h ** 3
        rows[tag] = {
            "n": n, "h": h, "b": b, "cells_in_act": int(act.sum()),
            "mu_instrument_(1/2 int x X (curl B - omega dE/dphi))": mu_inst.tolist(), "|mu_instrument|": float(np.linalg.norm(mu_inst)),
            "term_curl_B": term_curl.tolist(), "term_displacement": term_disp.tolist(), "int_B_dV_(localized identity target)": intB.tolist(),
            "charge_e_=_sum_div_B_over_act_mask": e_tot, "charge_e_full_interior": e_full, "flux_of_B_through_the_interior_faces": float(flux), "4pi": float(4 * np.pi), "L_box": float(eid.L), "dipole_p_=_sum_x_div_B": p0.tolist(), "|p|/e": float(np.linalg.norm(p0) / abs(e_tot)) if e_tot else None,
            "pdot": pdot.tolist(), "mu_pred_=_p_x_pdot/(2e)": (mu_pred.tolist() if np.all(np.isfinite(mu_pred)) else None),
            "|mu_pred|": float(np.linalg.norm(mu_pred)) if np.all(np.isfinite(mu_pred)) else None,
            "mu_dual_reading_(1/2 int x X (-curl E - omega dB/dphi))": mu_dual.tolist(), "|mu_dual|": float(np.linalg.norm(mu_dual)),
            "jmax": jmax, "Emax": Emax,
        }
        print(f"{tag}: h {h:.3f} |mu_inst| {np.linalg.norm(mu_inst):.4e}  e_act {e_tot:.4f} e_full {e_full:.4f} flux {flux:.4f}  |p|/e {np.linalg.norm(p0)/abs(e_tot):.3e}  |mu_pred| {np.linalg.norm(mu_pred):.3e}  |mu_dual| {np.linalg.norm(mu_dual):.4e}  curl-term {np.linalg.norm(term_curl):.3e} disp-term {np.linalg.norm(term_disp):.3e} intB {np.linalg.norm(intB):.3e}  [{time.time()-t0:.0f} s]", flush=True)
out["ii_mu_identity_on_the_electron_id_instrument"] = {
    "rows": rows,
    "reading": "the instrument's moment is the moment of the source current of the pullback field read with the radial 2-form as B; the hedgehog's charge sits at the centre (|p|/e listed), so the author's identity predicts |mu| = |p x pdot|/(2e) at the listed value; the curl-B term of the instrument's integral is a moment of a monopole field, which is not localized, so its value carries the box (the M5.8.2r ladder 0.221 / 0.248 / 0.277); the displacement term and the dual-reading moment are listed beside it",
    "fails_if": "the instrument's |mu| equals |p x pdot|/(2e) within its own box scatter (then the readout is NOT a residue of zero), or |p|/e is not small for the centred hedgehog",
}
out["wall_s"] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(DATA, "m5_34_kit_checks.json"), "w"), indent=1, default=float)
i = out["i_clock_inertia_box_growth"]
print("K_sphere", round(i["author_K_sphere_32pi_delta2[1+(1-delta)^2]_per_unit_radius"], 5), "M5.21.14 base", m5_21_14_base, "ratio", round(i["ratio_author_over_ours"], 6))
print("ladder slopes", {k: round(v, 4) for k, v in slopes.items()}, "predicted", {k: round(v, 4) for k, v in pred.items()}, "meas/pred", {k: round(v, 4) for k, v in i["measured_over_predicted"].items()}, "I_cube", round(Ic, 4))
print("wall_s", out["wall_s"])
