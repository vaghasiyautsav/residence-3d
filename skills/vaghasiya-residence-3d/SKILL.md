---
name: vaghasiya-residence-3d
description: Continue work on the Vaghasiya Residence (20 Telowie Ave, Ingle Farm SA, Studio Forthwall 26002) interactive 3D model, covering edits, checks against the drawings, rebuild, PIN-lock and redeploy to GitHub Pages. Use for any change to that model or its site context.
---

# Vaghasiya Residence 3D: project continuation

This project follows the general method in the `house-plans-to-3d` skill (same repo, `skills/house-plans-to-3d`). Read that first.

## Where things are
- **Repo.** Local clone `~/Developer/residence-3d`, GitHub `vaghasiyautsav/residence-3d` (public).
  - Live at https://vaghasiyautsav.github.io/residence-3d/, Pages from `main` / root.
- **Files.**
  - `index.html` is the PIN-locked page.
  - The readable source is `src/model.html` (git-ignored, ~590 kB, three.js 0.160). Get it with `node tools/decrypt.mjs`, which asks for the PIN.
  - The PIN is in the owner's `HANDOFF.md`; ask the owner if it isn't there. Never write it into repo files, skills or memory.
- **Preview.**
  - `.claude/launch.json` has the config `model` (python http.server on port 8173, serving `src/`).
  - `node tools/testpage.mjs` writes `src/test.html` with `window.__t` hooks; open `http://localhost:8173/test.html?v=N`.
- **Drawings** (`~/Downloads`):
  - `WD_13.07.26 (2).pdf`, pages: 0 site plan (1:100 on A2), 1 GF, 2 FF, 3 elevations, 4 roof plan, 5–6 details (niches, eaves, box gutter, meter box/NBN).
  - `257115-C-COMBINED[B].pdf`: civil C01, with survey, levels and legend.
  - The stamped plans PDF has the same architectural sheets.
- **Sheet calibration** (35.2778 mm/pt):

  | Sheet | PDF point | = plan point |
  |---|---|---|
  | GF | (566.64, 440.97) | (0, 0) |
  | FF | (651.69, 453.39) | (3000, 900) |
  | Site | (390.4, 373.3) | (−6049, −900) |
  | Elevations A, B | FL datum at pt y 489.69 | |
  | Elevations C, D | FL datum at pt y 808.0 | |

## Model facts (as built, checked against the drawings)
- **Coordinates.** Plan mm:
  - x = rear 0 → front 20390;
  - y = D side (No. 22) 0 → B side (Lot 72) 9010;
  - z from GF FFL (RL 99.00).
  - World: `wx=x/1000-10.2`, `wz=y/1000-4.5`, `wy=z/1000`.
  - `LOT={x0:-6049,x1:27491,y0:-900,y1:9010}`. `ground(x)` reaches 950 at the street.
- **Levels:**
  - GF plate 2730, CH 2700, floor zone 420, FF `U=3150`, FF plate 5880, FF ceiling 5850 (coffers 6150 in Bed 1 and Bed 2);
  - windows head 2400 (written), doors 2340.
- **Roof:**
  - eave sheet edges `LB=2651` (GF) and `UB=5801` (upper); ridge 7209; pitch 22.5°; eaves 450;
  - garage roof `2900 + TAN·min(8900−y, x−13800, 19250−x)`, max-combined with the GF field (valleys);
  - boundary wall 2730 with a 300 box gutter (2731–2931); garage portal 3350.
- **Front frame:**
  - outer 2632–6402, bottom band 2632–3051, soffit 5951;
  - open U parapet 190 thick, with 300 box gutters (front 19900–20199, sides y 1092–1400 / 6300–6608);
  - stone piers: GF 0–2632 (x 19990–20410), FF 3051–5951.
- **Curved walls** (`D.arcs`): garage/entry R590 (centre 14400,3920; r 500–590); hall/linen R200 (centre 11611,3128; r 109–200). Both painted.
- **Splashback windows:** kitchen 900–1600 (x 5070–6880); butler's pantry 900–1500 (x 8940–11050).
- **Bulkheads** 2400–2700: kitchen 4790–8190 × 190–890; pantry 8280–11720 × 190–890; laundry 13210–13810 × 190–2090; linen 10070–11460 × 2830–3330; Bed 4 robe 8570–10290 × 4520–5120.
- **Furniture as drawn:**
  - living L-sofa 4191–6898 × 4628–7409, 810 deep, seat 440;
  - TV cabinet 7741–8190 × 5210–7610 with a 55" TV;
  - dining table 1600 × 1000 at 2800–3800 × 1521–3121, six chairs;
  - island 2400 × 900.
- **Undrawn furniture** is at catalogue sizes. Queen beds; Bed 1 could be a king if the owner asks.
- **Wet areas:**
  - Ens 1 shower 12810–14210 × 5710–6610; Ens 2 shower 7280–8790 × 5710–6610; both have full-width 450 niches at 1100 under the window;
  - Ens 2 bath 1480 × 752 at (8330, 3351), spout on the y 2830 wall.
- **Robes and cupboards:**
  - WIR 1: 500 hanging along y 3270, 12810–15210, plus a make-up desk 12810–13310 × 3771–4720;
  - WIR 2: 500 hanging 3690–7190 × 6110–6610, plus a desk 3190–3690 × 5181–6110;
  - kitchenette bench 7820–9280 × 2140–2740;
  - linen cupboard has three flush doors.
- **Services:**
  - AC 14300–15150 × 350–700; HWS ×2 at x 7420/8180 (y −380); tank at x −800, y −480 on a pad;
  - meter box (proposed) on the y 900 wall, x 16620–17180;
  - bins at x 15490 (yellow), 16100 (green), 16660 (blue);
  - wall lights listed in `WL`, with wall-wash beams.
- **Street** (survey):
  - nature strip to 30240;
  - brick footpath 30240–31760 (jogs to ~29450–30700 between y −1378 and 2887 around the old crossover apron);
  - gravel 31760–31870, kerb 31870–32020, water table 32020–32343, road to 39743;
  - our crossover y 4009–9011 with a layback.
  - Stobie pole at (30000, 18750): the far B side of Lot 72, per the owner. Its street light comes on from dusk.
- **Context** (`ctx` group, Surroundings button):
  - No. 22: tan brick, sage roof;
  - Lot 72: new brick house x 3000–20500 × y 10100–18000, yard bare earth;
  - No. 18 beyond;
  - behind the rear fence: brown gable shed, red-brick house, white house with a tile roof, pencil pine;
  - three houses across the road.
  - Fences: both sides dark grey `0x4b4e50` on plinths (D 250, B 400); rear brown (D half) and zincalume (B half).
- **Views:**
  - opening camera `hero` at plan (36300, 15800), 7.5 m, clear of the pole;
  - B/C/D elevation buttons switch the surroundings off;
  - walk spots checked clear (Living 7300,4900; Bed 1 16000,2900).

- **X-ray layer** (module just before `const MATS=new Set()`; panel `#xrp`, button `t-xray`).
  - **Structure is indicative LGS:** the drawings are timber, but the owner builds in steel, and the frame supplier's drawings are still to come.
    - Walls: 89 C-studs at 600, with 75 Hebel and batts on the external walls.
    - Floor: joists about 380 deep at 450, bearing on the GF plates (2730–3110, `FT=3110`), avoiding the stair void (13400–19450 × 1100–2090). FF frames stand on the sheet flooring at 3130.
    - Roof: trusses at 900 from `ROOFS`. Over the Bed 1 and Bed 2 coffers the bottom chord steps up to 6252; the upper truss lines are offset to clear the skylight shafts.
    - Ceiling batts are 1200 tiles trimmed under the roof near the eaves. Porch and stone piers show as AAC blockwork.
  - **Steel per S-sheets:**
    - floor beams have top of steel 3110;
    - SB3 380 PFC at y 1043 (its rear end, x 1855–2500, is shown tapered because the GF roof is lower than the beam there: an open question for the engineer);
    - SB2/SB1 250 PFC at y 4363 / 6656; SB4 300 PFC at y 6656 (to 20251);
    - GL1 300 PFC at x 19346 over the garage door;
    - L1, L3, L4 150 PFC lintels at 2400–2550; L2 (hall opening, full height) sits in the floor zone;
    - MO1, MO7, MO8 (under FF walls) and MO6, MO3 (front frame) are "members by others", shown at placeholder sizes;
    - C1/C2 SHS 89 and SC1 SHS 75 stub columns.
  - **Footings:** 250 × 700 edge beams, plus internal beams at y 1030/3160/4390/5970 and x 3130/6780/8240/10450/16600.
  - **Services (indicative):**
    - **Sewer:** main along y 7600, under the slab, to the IS at (−3071, 7963). The D-side branch runs along y 500. FF stacks are at (12850, 6700) and (8235, 6700), with vents.
    - **Stormwater:** charged lines at y −560 / 8585 / x −560 go to the tank inlet (−1640, −480). The tank overflow goes to a pump pit at (136, 2296). The rising main runs along y −760, then y 2973, to the kerb. The front sealed line is at y 211.
    - **Water:** meter at (27150, 3650), main along y −350. Hot comes from the HWS under the eave into the ceiling at y 420.
    - **Gas:** meter at (17880, 820), line along y −680 to the cooktop and BBQ.
    - **Power:** from the MB at (16900, 860), the GF hub is at 2770 and the FF hub at 5910. Downlights are chained per room, with GPO drops.
    - **Data:** NBN to the NTD, then to the hub at (10770, 2840), then star-wired.
    - **AC:** condenser, then refrigerant up the D wall to a fan-coil at (11300–12500, 3420–4080, 6280–6560), with ducts to Bed 1, Bed 2, the office and the upper hall, plus a return. The ground floor has a second ducted system:
      - outdoor unit on the B-side path at x 4700–5550, y 8150–8500;
      - slim fan-coil in the roof strip over the living room (4200–5300 × 6850–7300, z 2745–2995);
      - ducts to the living room ×2 and Bed 4, to meals over the alfresco through the rear-wing roof, and to the hall plus a return between the joists at x 10425 / 9075 (`PLVO=0` keeps them on level 0).
- **Walk and sound:**
  - eye 1650; desktop pointer-lock mouse look, arrows and WASD move;
  - `surfaceAt()` picks the footstep sound: FF carpet except the ensuites; GF timber, with tiles in the wet areas, carpet in Bed 4 and concrete in the garage;
  - `SND` holds the ambience (birds, crickets, wind, rain, doors) and is exposed on `__t.SND`, with `XS` on `__t.XS`.

- **Structure audit:** `src/audit.js` (local, git-ignored) lists every structure member that pokes through a roof, sits in an opening, coffer, skylight or the stair void, or hangs in a room. In `test.html`, run `await import('/audit.js')` and read `__audit.sum`. Two known false positives remain: MO7 at the stair-void edge, and the bounding box of the tapered SB3 end.
- **Garage portal wall:** the 3350 upstand applies only beyond the first floor (y 6800–8570). Under the first floor it stops at 3051, so it no longer blocks the bottom of the Bed 1 window.

## Edit → check → lock → publish
1. Edit `src/model.html`, run `node tools/testpage.mjs`, and preview with the `model` launch config.
2. Check:
   - console;
   - screenshots of the changed area, day and night, plus phone portrait;
   - the audits (walls, door swings, walk spots);
   - `skills/house-plans-to-3d/scripts/wall_coverage.py` with the calibrations above.
3. Build: `VR3D_PIN=<PIN> node tools/build.mjs`. Keep the current PIN. Then decrypt-compare the new `index.html` against the source.
4. Commit and push:
   - commit `index.html` (and README/skills when changed) as `vaghasiyautsav`, using the `vaghasiyautsav` gh account;
   - **no AI attribution of any kind**: no Co-Authored-By, no "Generated with".
5. Poll the live page until its `SALT` matches the new build, then summarise for the owner in short bullets.
- **Never commit** `src/`, `HANDOFF.md` (contains the PIN) or a source zip. The repo is public.

## Owner preferences
- Follow the plans to the millimetre, but the owner's corrections and site knowledge win.
- Sparse, uncluttered styling; real sizes so rooms read true.
- The front yard is lawn only: no front tree, no shrub border.
- No car in the garage; black tapware by default.
- Stone is irregular random stone as drawn on elevation A, in 3D.
- Lawn is real 3D grass.
- Both side fences grey.
- Fix whole classes of glitches (clipping, floating, buried fittings, door clashes, lights that look off), not single instances.
- Mobile matters.

## Open items
- Meter box and NBN position are a proposal until the builder confirms.
- Footpath material in front of the lot: the survey says brick; 2024 Street View showed concrete.
- Options to offer: a king bed in Bed 1; a smaller sofa (three-seater + chaise, ~2.7 × 1.6 m) if the drawn L feels big.
- The Stobie pole position is approximate (owner's description).
- Frame and services are indicative. Replace them with the steel frame supplier's layout and the plumber's and electrician's runs when the owner sends them.
