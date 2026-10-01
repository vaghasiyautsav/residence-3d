#!/usr/bin/env python3
"""Read an architectural PDF sheet in plan millimetres.

Calibrate each sheet once: one PDF point (px, py) that equals a known plan point (X, Y) in mm,
and the scale in mm per PDF point (1:100 = 25.4/72*100 = 35.2778, 1:200 = 70.5556, 1:50 = 17.6389).
On most sheets plan y grows down the page; pass --sy -1 if it grows up.

Examples
  # what is drawn in a region: lines and curves with colour and stroke width, plus text
  python3 pdf_probe.py WD.pdf --page 1 --cal 566.64,440.97,0,0 --region 3000,4000,8200,8000 --lines --text
  # only the wall lines (black, stroke >= 0.6 pt)
  python3 pdf_probe.py WD.pdf --page 1 --cal 566.64,440.97,0,0 --region 0,0,20400,9100 --lines --black --min-width .6
  # a picture of the region to look at
  python3 pdf_probe.py WD.pdf --page 1 --cal 566.64,440.97,0,0 --region 9600,2500,12100,3700 --png linen.png --dpi 400

Conventions seen on residential working drawings (check the legend of each set):
  black, stroke >= 0.6-1.0 pt  walls and their returns
  grey 0.5-0.6, stroke ~0.36   joinery, fixtures and drawn furniture (sofa, beds, dining set, island)
  light grey fill (0.84)       hatched areas, e.g. "300H dropped bulkheads"
  red dashed                   outline of the floor above / roof over
  bezier curves ('c')          door swings, curved walls (look for an "R200"-style label), basins, trees
"""
import argparse
import fitz  # PyMuPDF


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pdf')
    ap.add_argument('--page', type=int, required=True, help='0-based page index')
    ap.add_argument('--cal', required=True, help='px,py,X,Y: PDF point (px,py) equals plan (X,Y) mm')
    ap.add_argument('--scale', type=float, default=35.2778, help='mm per PDF point (default 1:100)')
    ap.add_argument('--sx', type=float, default=1, help='+1 if plan x grows to the right on the sheet, -1 if left')
    ap.add_argument('--sy', type=float, default=1, help='+1 if plan y grows down the sheet, -1 if up')
    ap.add_argument('--region', help='X0,Y0,X1,Y1 in plan mm (default: whole sheet); write --region=-500,... when it starts with a minus')
    ap.add_argument('--lines', action='store_true', help='list lines, rectangles and curves')
    ap.add_argument('--text', action='store_true', help='list words with their plan position')
    ap.add_argument('--black', action='store_true', help='only black strokes')
    ap.add_argument('--min-width', type=float, default=0, help='minimum stroke width in pt')
    ap.add_argument('--min-len', type=float, default=40, help='skip pieces shorter than this (mm)')
    ap.add_argument('--png', help='render the region to this PNG')
    ap.add_argument('--dpi', type=int, default=300)
    a = ap.parse_args()

    px, py, X0, Y0 = map(float, a.cal.split(','))
    K = a.scale
    to_plan = lambda x, y: (X0 + a.sx * (x - px) * K, Y0 + a.sy * (y - py) * K)
    to_pt = lambda X, Y: (px + a.sx * (X - X0) / K, py + a.sy * (Y - Y0) / K)
    page = fitz.open(a.pdf)[a.page]
    if a.region:
        R = list(map(float, a.region.split(',')))
    else:
        r = page.rect
        (x0, y0), (x1, y1) = to_plan(r.x0, r.y0), to_plan(r.x1, r.y1)
        R = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    inside = lambda P: all(R[0] <= x <= R[2] and R[1] <= y <= R[3] for x, y in P)

    if a.png:
        (ax, ay), (bx, by) = to_pt(R[0], R[1]), to_pt(R[2], R[3])
        clip = fitz.Rect(min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)) & page.rect
        page.get_pixmap(dpi=a.dpi, clip=clip).save(a.png)
        print('wrote', a.png)

    if a.lines:
        seen = set()
        for dr in page.get_drawings():
            c, w = dr.get('color'), dr.get('width') or 0
            if w < a.min_width:
                continue
            black = bool(c) and max(c) < .05
            if a.black and not black:
                continue
            for it in dr['items']:
                if it[0] == 'l':
                    pts = [it[1], it[2]]
                elif it[0] == 're':
                    r = it[1]
                    pts = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y1)]
                elif it[0] == 'qu':
                    q = it[1]
                    pts = [q.ul, q.lr]
                elif it[0] == 'c':
                    pts = [it[1], it[2], it[3], it[4]]   # start, control, control, end
                else:
                    continue
                P = [to_plan(p.x, p.y) for p in pts]
                if not inside(P):
                    continue
                if abs(P[-1][0] - P[0][0]) + abs(P[-1][1] - P[0][1]) < a.min_len:
                    continue
                key = (it[0],) + tuple(round(v / 10) for p in P for v in p)
                if key in seen:
                    continue
                seen.add(key)
                col = 'black' if black else ('grey%.2f' % c[0] if c else 'none')
                fill = ' fill' if dr.get('fill') else ''
                print(it[0], [(round(x), round(y)) for x, y in P], col, round(w, 2), (dr.get('dashes') or '').replace('[] 0', ''), fill)

    if a.text:
        for w in page.get_text('words'):
            X, Y = to_plan(w[0], w[1])
            if R[0] <= X <= R[2] and R[1] <= Y <= R[3]:
                print(round(X), round(Y), repr(w[4]))


if __name__ == '__main__':
    main()
