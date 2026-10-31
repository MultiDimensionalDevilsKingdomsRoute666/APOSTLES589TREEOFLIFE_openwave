"""Compile the M5.34 reproduction record from the run logs: per script the exit code and wall time, per regenerated
JSON the max relative difference against the shipped copy (from the comparator's output), plus the versions and the
cross-machine timing probe. Usage: m5_34_reproduction_record.py <logs_dir> <out_json>
The logs dir holds r1a_summary.txt, r1c_summary.txt, bench_summary.txt (lines "NAME wall_s=X exit=N"), r1b_<job>.log
(first line "START hh:mm:ss <cmd>", last line "END hh:mm:ss exit=N wall_s=X") and r1a_compare.txt / r1b_compare.txt /
r1c_compare.txt."""
import glob, json, os, re, sys
logs, out = sys.argv[1], sys.argv[2]
rec = {"versions": {}, "bench": [], "r1a": [], "r1b": [], "r1c": [], "compare": {}}
try:
    import numpy, scipy, sympy, mpmath
    rec["versions"] = {"python": sys.version.split()[0], "numpy": numpy.__version__, "scipy": scipy.__version__, "sympy": sympy.__version__, "mpmath": mpmath.__version__}
except Exception as e:
    rec["versions"] = {"error": str(e)}
def summary(fn, key):
    p = os.path.join(logs, fn)
    if not os.path.exists(p): return
    for l in open(p):
        m = re.match(r"(\S+)\s+wall_s=\s*([\d.]+)\s+exit=(\d+)", l.strip())
        if m: rec[key].append({"run": m.group(1), "wall_s": float(m.group(2)), "exit": int(m.group(3))})
summary("r1a_summary.txt", "r1a"); summary("r1c_summary.txt", "r1c"); summary("bench_summary.txt", "bench")
for p in sorted(glob.glob(os.path.join(logs, "r1b_*.log"))):
    lines = open(p, errors="replace").read().strip().split("\n")
    st = re.match(r"START (\d\d:\d\d:\d\d) (.*)", lines[0]) if lines else None
    en = re.match(r"END (\d\d:\d\d:\d\d) exit=(\d+) wall_s=(\d+)", lines[-1]) if lines else None
    rec["r1b"].append({"job": os.path.basename(p)[4:-4], "start": st.group(1) if st else None, "cmd": st.group(2) if st else None,
                       "end": en.group(1) if en else None, "exit": int(en.group(2)) if en else None, "wall_s": int(en.group(3)) if en else None,
                       "finished": bool(en), "errors": [l for l in lines if "Traceback" in l or "Error" in l][:2]})
for cf in ("r1a_compare.txt", "r1b_compare.txt", "r1c_compare.txt"):
    p = os.path.join(logs, cf)
    if not os.path.exists(p): continue
    for l in open(p, errors="replace"):
        m = re.match(r"(\S+) (\S+\.json): (\d+) leaves, max rel diff (\S+) at (\S*) \((.*?)\)(.*)", l.strip())
        if m:
            rec["compare"][m.group(2)] = {"run_dir": m.group(1), "leaves": int(m.group(3)), "max_rel_diff": m.group(4), "at": m.group(5), "values": m.group(6)[:120], "note": m.group(7).strip()[:160]}
        elif ": NEW (no shipped copy)" in l:
            rec["compare"][l.split()[1].rstrip(":")] = {"note": "NEW (no shipped copy)"}
json.dump(rec, open(out, "w"), indent=1)
print(f"r1a {len(rec['r1a'])} runs ({sum(r['exit']==0 for r in rec['r1a'])} exit 0); r1c {len(rec['r1c'])} ({sum(r['exit']==0 for r in rec['r1c'])} exit 0); r1b {len(rec['r1b'])} jobs ({sum(bool(r['finished']) for r in rec['r1b'])} finished, {sum(r['exit']==0 for r in rec['r1b'] if r['finished'])} exit 0); compare {len(rec['compare'])} files")
