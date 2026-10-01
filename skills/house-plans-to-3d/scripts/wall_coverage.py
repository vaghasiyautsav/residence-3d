#!/usr/bin/env python3
"""Check that every wall line drawn on a plan sheet is matched by a wall in the model.

The model's walls are read from the page source: `const D = {"walls":[[x0,y0,x1,y1,z0,z1,kind],...],
"arcs":[[cx,cy,r0,r1,a0,a1,z0,z1],...], "openings":[{"r":[x0,y0,x1,y1],...}], "doors":[...]}` (plan mm).
Each black plan line (stroke >= --min-width) is sampled every 50 mm; a sample counts as covered when it
lies on or within --tol mm of a wall box (or arc) that exists at --z, or inside an opening or door.
Segments with uncovered samples are printed: missing walls, walls in the wrong place, or things that are
not walls at all (shower-door swings, balustrades lower than --z). Curved walls are drawn as bezier
curves, so this check skips them: list them with pdf_probe.py --lines and look for 'c' items.

Example (ground floor, checking at 1 m above the floor)
  python3 wall_coverage.py WD.pdf --page 1 --cal 566.64,440.97,0,0 --model src/model.html --z 1000 --box=-100,-100,20500,9100
"""
import argparse, json, math
import fitz


def load_model(path):
    s = open(path, encoding='utf-8').read()
    i = s.index('const D = ')
    j = s.index('\n', i)
    return json.loads(s[i + len('const D = '):j].rstrip().rstrip(';'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pdf')
    ap.add_argument('--page', type=int, required=True)
    ap.add_argument('--cal', required=True, help='px,py,X,Y (see pdf_probe.py)')
    ap.add_argument('--scale', type=float, default=35.2778)
    ap.add_argument('--sx', type=float, default=1)
    ap.add_argument('--sy', type=float, default=1)
    ap.add_argument('--model', required=True, help='page source containing const D = {...}')
    ap.add_argument('--z', type=float, required=True, help='height (mm above GF FFL) at which walls must exist')
    ap.add_argument('--box', help='X0,Y0,X1,Y1: only check plan lines inside this box (the house); write --box=-100,... when it starts with a minus')
    ap.add_argument('--min-width', type=float, default=.9)
    ap.add_argument('--tol', type=float, default=6)
    a = ap.parse_args()

    px, py, X0, Y0 = map(float, a.cal.split(','))
    K = a.scale
    P = lambda x, y: (X0 + a.sx * (x - px) * K, Y0 + a.sy * (y - py) * K)
    D = load_model(a.model)
    t = a.tol
    walls = [w for w in D['walls'] if w[4] <= a.z <= w[5]]
    arcs = [r for r in D.get('arcs', []) if r[6] <= a.z <= r[7]]
    holes = [o['r'] for o in D.get('openings', []) + D.get('doors', [])]

    def covered(x, y):
        if any(w[0] - t <= x <= w[2] + t and w[1] - t <= y <= w[3] + t for w in walls):
            return True
        for cx, cy, r0, r1, a0, a1, *_ in arcs:
            r = math.hypot(x - cx, y - cy)
            ang = math.atan2(y - cy, x - cx) % (2 * math.pi)
            lo, hi = a0 % (2 * math.pi), a1 % (2 * math.pi)
            in_sweep = lo <= ang <= hi if lo <= hi else (ang >= lo or ang <= hi)
            if r0 - t <= r <= r1 + t and in_sweep:
                return True
        return any(h[0] - t <= x <= h[2] + t and h[1] - t <= y <= h[3] + t for h in holes)

    page = fitz.open(a.pdf)[a.page]
    segs = []
    for dr in page.get_drawings():
        c, w = dr.get('color'), dr.get('width') or 0
        if not (c and max(c) < .05 and w >= a.min_width):
            continue
        for it in dr['items']:
            if it[0] == 'l':
                segs.append(P(it[1].x, it[1].y) + P(it[2].x, it[2].y))
            elif it[0] == 're':
                r = it[1]
                (x0, y0), (x1, y1) = P(r.x0, r.y0), P(r.x1, r.y1)
                segs += [(x0, y0, x1, y0), (x1, y0, x1, y1), (x0, y1, x1, y1), (x0, y0, x0, y1)]
    if a.box:
        B = list(map(float, a.box.split(',')))
        segs = [s for s in segs if all(B[0] <= v <= B[2] for v in (s[0], s[2])) and all(B[1] <= v <= B[3] for v in (s[1], s[3]))]

    bad = []
    for x0, y0, x1, y1 in segs:
        n = max(2, int(max(abs(x1 - x0), abs(y1 - y0)) / 50))
        miss = [(round(x0 + (x1 - x0) * k / n), round(y0 + (y1 - y0) * k / n)) for k in range(n + 1)
                if not covered(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n)]
        if len(miss) > 2:
            bad.append(((round(x0), round(y0), round(x1), round(y1)), len(miss), miss[:2]))
    print(f'{len(segs)} wall lines checked, {len(bad)} with uncovered points')
    for b in bad:
        print('  segment', b[0], '-', b[1], 'uncovered samples, e.g.', b[2])


if __name__ == '__main__':
    main()
