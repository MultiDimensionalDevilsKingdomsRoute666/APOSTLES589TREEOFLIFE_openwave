"""Compare regenerated JSON files against the shipped copies: max relative difference per file.
Usage: compare_json.py <shipped_dir> <run_dir> [<run_dir> ...]
A JSON in run_dir counts as regenerated when its mtime is newer than field3d.py's copy time in that dir."""
import json, os, sys, math
def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b: out.append((path + "/" + str(k), "missing", float("inf"))); continue
            walk(a[k], b[k], path + "/" + str(k), out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): out.append((path, "len %d vs %d" % (len(a), len(b)), float("inf"))); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, path + "[%d]" % i, out)
    elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        if a != b: out.append((path, "%r vs %r" % (a, b), float("inf")))
    else:
        try:
            a = float(a); b = float(b)
            if math.isnan(a) and math.isnan(b): return
            d = abs(a - b); r = d / max(abs(a), abs(b), 1e-300)
            out.append((path, "%.10g vs %.10g" % (a, b), r if d > 0 else 0.0))
        except Exception as e:
            out.append((path, "uncomparable %r vs %r" % (a, b), float("inf")))
shipped = sys.argv[1]
for rd in sys.argv[2:]:
    t0 = os.path.getmtime(os.path.join(rd, "field3d.py"))
    for fn in sorted(os.listdir(rd)):
        if not fn.endswith(".json"): continue
        fp = os.path.join(rd, fn)
        if os.path.getmtime(fp) <= t0 + 1: continue
        sp = os.path.join(shipped, fn)
        if not os.path.exists(sp): print(f"{os.path.basename(rd)} {fn}: NEW (no shipped copy)"); continue
        out = []; walk(json.load(open(sp)), json.load(open(fp)), "", out)
        n = len(out); worst = max(out, key=lambda t: t[2]) if out else ("", "", 0.0)
        bad = [t for t in out if t[2] == float("inf")]
        print(f"{os.path.basename(rd)} {fn}: {n} leaves, max rel diff {worst[2]:.3g} at {worst[0]} ({worst[1]})" + (f"; {len(bad)} NON-NUMERIC MISMATCH e.g. {bad[0]}" if bad else ""))
