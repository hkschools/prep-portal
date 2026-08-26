#!/usr/bin/env python3
"""Generate baseline NVR banks from the CAT4 engines (testgen-cat4 skill).

    python3 gen_nvr.py            # regenerates nvr_<band>.json for all bands

Reuses the skill's compute-and-self-check generators (classification/matrices/
recognition + bands.py difficulty model) so every item is a genuine CAT4
sub-type at the band's GL difficulty, with a computed key, doctrine-compliant
distractors, and a structural self-check. Figures render as PNG (rsvg-convert)
with options labelled A-E, then embed as base64 data URIs so the portal pages
stay self-contained.

Band plan (GL level per current school year: Y4=A Y5=B Y6=C Y7=D Y8=E Y9/10=F):
  level-a: 8 engine (FC4+M4 @A easiest-first) + 2 hand GL-style items in the module
  level-b: 9 engine (FC3+M3 @B, FC2+M1 @C) + 3 hand GL-style
  level-c: 12 engine (FC4+M4 @D, FC2+M2 @E) + 4 hand GL-style
  level-d: 14 engine (FC5+M5+FR4 @F) + 6 hand GL-style

SEED_BASE is deliberately distinct from the published drill/paper rounds
(CAT4_SEED 0 / 50000 / 90000), so no baseline item repeats a live drill item.
"""
import base64
import json
import os
import random
import sys

ENGINES = os.path.expanduser("~/.claude/skills/testgen-cat4/engines")
sys.path.insert(0, ENGINES)
os.chdir(ENGINES)  # engines resolve their template/font paths relative to cwd

import bands                     # noqa: E402
import cat4common as C           # noqa: E402
import classification as cl      # noqa: E402
import matrices as mx            # noqa: E402
import recognition as rc         # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, "_nvr_png")
SEED_BASE = 777000               # unique to the baseline; never a drill round seed
VER_STEP = 50021                 # per-version seed offset (v2 = +50021, v3 = +100042)
LET = "ABCDE"
ENG = {"FC": cl, "M": mx, "FR": rc}
BATTERY = {"FC": "Figure Classification", "M": "Figure Matrices", "FR": "Figure Recognition"}

PLAN = {
    "level-a": [("FC", "A", 4, "easy"), ("M", "A", 4, "easy")],
    "level-b": [("FC", "B", 3, "spread"), ("M", "B", 3, "spread"),
                ("FC", "C", 2, "spread"), ("M", "C", 1, "spread")],
    "level-c": [("FC", "D", 4, "spread"), ("M", "D", 4, "spread"),
                ("FC", "E", 2, "spread"), ("M", "E", 2, "spread")],
    "level-d": [("FC", "F", 5, "spread"), ("M", "F", 5, "spread"), ("FR", "F", 4, "spread")],
}


# Sub-types excluded from the baseline: M37 (removed-piece orientation is
# two-readable without the rule text), M13 (count-rule with one-dot options
# that render near-identically at page size), FC-93 (gradient-direction rule
# too subtle at page render), M19 (recolour rule forks positional vs
# shape-type when the example's middle element is also its only triangle).
# All remain fine in the drills.
BLOCK = {"M13", "M37", "FC-93", "M19",
         "FC-27",   # only one 5-cell strip satisfies the rule: match-solvable
         "M15",     # overlap-amount options differ by a few percent: not blind-solvable
         "FC-12"}   # gradient-direction rule + a reversed purple gradient asset


def pick(code, band, n, mode):
    pool = [s for s in (bands.pool(code, band) or [f"{code}-01"]) if s not in BLOCK] \
        or [f"{code}-01"]
    pool = sorted(pool, key=lambda s: (bands.ORDER.index(bands.ENTRY[code][s]), s))
    if mode == "easy":
        return [pool[i % len(pool)] for i in range(n)]
    if len(pool) <= n:
        return [pool[i % len(pool)] for i in range(n)]
    if n == 1:
        return [pool[len(pool) // 2]]
    idx, seen = [], set()
    for i in range(n):
        j = round(i * (len(pool) - 1) / (n - 1))
        while j in seen:
            j = (j + 1) % len(pool)
        seen.add(j)
        idx.append(j)
    return [pool[j] for j in sorted(idx)]


def answer_positions(key, n):
    seq = [i % 5 for i in range(n)]
    random.Random(sum(ord(c) for c in key) * 31 + SEED_BASE).shuffle(seq)
    return seq


def gen_band(bandkey, plan, version=1, seen_hashes=None):
    """seen_hashes: cross-version (and cross-band) PNG-hash set. A slot whose
    rendered figure collides with an already-emitted one retries with a bumped
    seed (attempt 0 = the original seed, so non-colliding slots are unchanged)."""
    import hashlib
    os.makedirs(TMP, exist_ok=True)
    if seen_hashes is None:
        seen_hashes = set()
    items = []
    fr_targets = set()
    used_subtypes = set()        # avoid repeating a rule within one paper
    qi = 0
    voff = VER_STEP * (version - 1)
    total = sum(n for _, _, n, _ in plan)
    band_aps = answer_positions(bandkey + f"v{version}", total)   # balanced over the WHOLE band
    ap_cursor = 0
    for code, glband, n, mode in plan:
        eng = ENG[code]
        base = SEED_BASE + voff + sum(ord(ch) for ch in code) * 13 + (ord(glband) - 64) * 137
        aps = band_aps[ap_cursor:ap_cursor + n]
        ap_cursor += n
        for i, st in enumerate(pick(code, glband, n, mode)):
            qi += 1
            png = os.path.join(TMP, f"{bandkey}_{qi:02d}_{code}_{glband}.png")
            # try the planned sub-type first; if its variation space is exhausted,
            # fall back to sibling sub-types from the same GL-band pool
            sibs = [p for p in (bands.pool(code, glband) or []) if p != st and p not in BLOCK]
            candidates = [c for c in [st] + sibs if c not in used_subtypes] \
                or [st] + sibs   # fall back to reuse only if the pool is exhausted
            q = None
            for cand in candidates:
                for attempt in range(40):
                    kw = {"avoid": set(fr_targets)} if code == "FR" else {}
                    try:
                        qq = eng.make(cand, band=glband, seed=base + i * 9 + attempt * 100003,
                                      answer_pos=aps[i], **kw)
                    except Exception:
                        continue
                    ok = qq["checks"].get("exactly_one_satisfies",
                                          qq["checks"].get("exactly_one_correct")) and qq["checks"]["no_duplicate_options"]
                    if not ok:
                        continue
                    opt_svgs = [(o["svg"] if isinstance(o, dict) else o) for o in qq["options"]]
                    stem_svgs = [(s["svg"] if isinstance(s, dict) else s) for s in qq["stems"]]
                    if any(s in opt_svgs for s in stem_svgs):
                        continue        # an option identical to a stimulus is solvable by matching
                    if code == "FC":
                        # if colour is NOT the rule, monochrome stimuli invite a colour reading
                        ruletxt = qq["rule"].lower()
                        colour_rule = any(w in ruletxt for w in (
                            "colour", "color", "red", "blue", "green", "orange", "purple",
                            "yellow", "grey", "gray", "black", "white", "shade", "shaded", "tone"))
                        if not colour_rule:
                            import re as _re
                            fills = set()
                            for s in stem_svgs:
                                fills.update(f for f in _re.findall(r'fill="([^"]+)"', s)
                                             if f.lower() not in ("none", "#fff", "#ffffff", "white"))
                            if len(fills) < 2:
                                continue
                    opts = [(o["svg"] if isinstance(o, dict) else o) for o in qq["options"]]
                    C.render_question(png, "", "", qq["stems"], opts,   # stem text lives in the page, not the PNG
                                      opt_labels=list("ABCDE"),
                                      stem_boxed=(code == "M"), extra_defs=qq.get("extra_defs", ""))
                    h = hashlib.md5(open(png, "rb").read()).hexdigest()
                    if h in seen_hashes:
                        continue                                 # identical figure already used: reseed
                    seen_hashes.add(h)
                    used_subtypes.add(cand)
                    q, st = qq, cand
                    break
                if q is not None:
                    break
            if q is None:
                raise SystemExit(f"NO UNIQUE ITEM after all sub-types: {bandkey} v{version} {code} {st}")
            if code == "FR" and q.get("target"):
                fr_targets.add(q["target"])
            b64 = base64.b64encode(open(png, "rb").read()).decode()
            items.append({
                "battery": BATTERY[code], "subtype": st, "gl_band": glband,
                "instruction": q["instruction"],
                "img": "data:image/png;base64," + b64,
                "answer": LET[q["correct_index"]],
                "rule": q["rule"],
            })
    out = os.path.join(HERE, f"nvr_{bandkey}_v{version}.json")
    json.dump(items, open(out, "w"))
    dist = {}
    for it in items:
        dist[it["answer"]] = dist.get(it["answer"], 0) + 1
    kb = sum(len(it["img"]) for it in items) // 1024
    print(f"{bandkey} v{version}: {len(items)} items · answers {dict(sorted(dist.items()))} · figures ~{kb} KB · {out}")


if __name__ == "__main__":
    import sys as _sys
    versions = [int(v) for v in _sys.argv[1:]] or [1]
    seen = set()                 # shared across every band and version this run
    banned = os.path.join(HERE, "banned_hashes.txt")
    if os.path.exists(banned):   # hashes of items vetoed in QA: force a reseed
        seen.update(x.strip() for x in open(banned) if x.strip())
    for version in versions:
        for bandkey, plan in PLAN.items():
            gen_band(bandkey, plan, version, seen_hashes=seen)
