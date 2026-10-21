"""Compile the M5.33 reproduction record from the run logs: per script, the command's exit code, wall time, the interpreter
and library versions printed at the top of each log, and the max relative difference of the regenerated JSON against the
shipped copy (from m5_33_compare_json.py's output). Usage: m5_33_reproduction_record.py <run_root> <out_json>
The run root holds r1a_<S>.log, r1s_run.log, r1b_logs/*.log and the compare outputs r1a_compare.txt / r1b_compare.txt."""
import json, os, re, sys
root, out = sys.argv[1], sys.argv[2]
rec = {"versions": {}, "r1a": [], "r1s": [], "r1b": []}
def parse(logpath, tag):
    txt = open(logpath).read()
    v = re.search(r"^versions (.*)$", txt, re.M)
    runs = re.findall(r"===== (.+?) start (\d\d:\d\d:\d\d)\n(.*?)real ([\d.]+)\n.*?===== .*?exit (\d+) end (\d\d:\d\d:\d\d)", txt, re.S)
    rows = []
    for name, t0, body, real, code, t1 in runs:
        tb = body.strip().split("\n"); tb = [l for l in tb if "Traceback" in l or "Error" in l]
        rows.append({"log": os.path.basename(logpath), "run": name.strip(), "start": t0, "end": t1, "wall_s": float(real), "exit": int(code), "errors": tb[:2]})
    return (v.group(1) if v else None), rows
cmp = {}
for cf in ("r1a_compare.txt", "r1b_compare.txt"):
    p = os.path.join(root, cf)
    if os.path.exists(p):
        for l in open(p):
            m = re.match(r"(\S+) (\S+\.json): (\d+) leaves, max rel diff (\S+) at (\S*) \((.*)\)(.*)", l.strip())
            if m: cmp[m.group(2)] = {"dir": m.group(1), "leaves": int(m.group(3)), "max_rel_diff": float(m.group(4)), "at": m.group(5), "values": m.group(6), "flags": m.group(7).strip()}
for f in sorted(os.listdir(root)):
    if f.startswith("r1a_") and f.endswith(".log"):
        v, rows = parse(os.path.join(root, f), "r1a"); rec["versions"][f] = v; rec["r1a"] += rows
    if f == "r1s_run.log":
        v, rows = parse(os.path.join(root, f), "r1s"); rec["versions"][f] = v; rec["r1s"] += rows
lg = os.path.join(root, "r1b_logs")
if os.path.isdir(lg):
    for f in sorted(os.listdir(lg)):
        v, rows = parse(os.path.join(lg, f), "r1b"); rec["versions"]["r1b/" + f] = v; rec["r1b"] += rows
rec["json_vs_shipped"] = cmp
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps({k: (len(v) if isinstance(v, list) else len(v)) for k, v in rec.items()}))
