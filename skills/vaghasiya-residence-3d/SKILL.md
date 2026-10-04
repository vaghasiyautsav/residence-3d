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

## Drawing revision A (3 Oct 2026) and the first-floor datum
- **Current drawings** (`~/Downloads`): `WD_A_03.10.26.pdf` (8 sheets; sheet 2 is the new slab plan) and `WD_A_03.10.26 - EXT.dwg`.
  - Convert the DWG with `dwg2dxf` (LibreDWG, installed via Homebrew) and read it with `ezdxf`. Units are mm, and y points up.
  - Slab plan in the DWG: plan x = dwg x − 444, plan y = 51416 − dwg y. Ground-floor plan: x − 126151, 51416 − y.
- **Rev A changes** (requested by the builder, Khush Patel of Hills and Harbour):
  - the plumbing stack moved from beside the GF WC into the curved hall corner;
  - new slab plan with set-downs: alfresco, porch and showers 50; garage none; 25 rebate at the garage opening;
  - 50 mm Hebel floor, so the floor zone grows from 420;
  - the garage internal door opens into the garage;
  - GF ensuite shower 1440 wide (was 1540), with a floor trap;
  - alfresco waste at x 590, with hot, cold and gas at about x 1460 / 1690 / 1950.
- **Floor zone:** the drawings show 470. The builder then asked for **450**, and the owner chose 450 on 3 Oct 2026. If a reissue differs, change `FFLIFT`.
- **FFLIFT datum rule.** Every first-floor and roof height in the source (and in the facts below) is on the original datum: first floor 3150, FF plate 5880, upper eave 5801, ridge 7209.
  - `wy()` applies `FFLIFT=30`: heights up to 2730 are unchanged, the floor zone stretches, and everything from 3130 up rises 30. So the real first floor is `UR=3180`.
  - Ground-floor parts above the plate are built with `ZG=1` (lift off): the GF roof, garage portal, front band to 3051, box gutters, stair, steel and joists.
  - Walking heights and the plan cut use real heights.
  - The stair has 17 equal risers, `RISE=UR/17` (187.06). The architect's stair note still says 17 risers at 186.47, which totals 3170 and no longer matches any floor level. Raised with the owner on 3 Oct 2026.
- **Slab-plan set-out now in the model:**
  - stacks at (8380, 4970), in the duct box at the Bed 4 robe corner, and (11639, 3030), in the hall curve;
  - toilets at x 11919 (ensuite) and 13170 (WC); powder vanity at 12010;
  - wastes: laundry (13659, 540), pantry (10000, 360), island (6790, 2340), ensuite floor trap (12170, 6800), alfresco (590, 7820);
  - island power conduit at (5090, 2190).
- **Ground slab** is built as a grid of cells from the slab plan (search "Ground slab per the architect's slab plan"):
  - structural top at −20, with alfresco, porch and the ensuite shower at −70 and the wet areas at −50;
  - a 25 × 100 edge rebate (top −45) around the house and garage for the Hebel, with none along the porch entry wall (x > 19390, y 1350–3280);
  - a 25 rebate across the garage door opening (x > 19300, y 3760–8570);
  - render fills the rebate under the walls.
- **Slab plan view** (button `m-slab`, X-ray mode `slab`): only the slab, footings, under-slab drains and the island conduit, ground level only. The `SLABL` sprites label each penetration and set-down. Exterior, the plan buttons and Walk all leave it.
- **Shower set-down:** the GF ensuite shower (`SHW`, 12370–13810 × 7020–7920) has its slab set down 50, with the tiled floor finishing 25 lower (`SHZ=-25`, an assumed mortar bed). The floor, slab and bathroom tiles are cut around it with `cutR`. The two first-floor showers are not set down: the slab plan covers the ground slab only.
- **Garage portal top:** 3400, per the elevation A dimension (owner confirmed 3 Oct 2026).

- **2D plan** (button `t-plan`, `set2D()`): the model seen flat from directly above. The owner asked for the model itself as a plan, not the architect's sheets (an embedded drawing viewer was built and removed on 3 Oct 2026).
  - It uses the same camera, looking straight down from far away through a 2° lens (`fit2D`), which is near enough to parallel.
  - Rotation is off and drag pans.
  - Fog is off, and near/far track the zoom (`near2D`).
  - Portrait phones turn the plan upright.
  - The plan-mode buttons keep the flat view; any elevation view or Walk leaves it.
  - It starts on the ground-floor cut if the view was Exterior.
- **Owner's mark-up PDF:** `src/drawings/WD_A_03.10.26_markup-450.pdf` (git-ignored; a copy is in `~/Downloads`). It shows 450 in red in place of 470 on the Elevations sheet, with a red banner on every sheet saying it is not issued by the architect.

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
  - boundary wall 2730 with a 300 box gutter (2731–2931); garage portal 3400.
- **Front frame:**
  - outer 2632–6402, bottom band 2632–3051, soffit 5951;
  - open U parapet 190 thick, with 300 box gutters (front 19900–20199, sides y 1092–1400 / 6300–6608);
  - stone piers: GF 0–2632 at x 19500–19990, hard against the garage wall and 500 deep (GF plan, elevations B and D; it was wrongly at 19990–20410 until 2026-10-04); FF 3051–5951 at x 19435–20410.
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
  - AC outdoor unit 14000–14940 × 500–900 (GF plan); HWS ×2 at x 7420/8180 (y −380); tank along the D boundary at x −1150…1350, y −850…−100;
  - meter box (proposed) on the y 900 wall, x 16620–17180;
  - bins at x 15490 (yellow), 16100 (green), 16660 (blue);
  - wall lights listed in `WL`, with wall-wash beams.
  - outdoor lights (owner, 2026-10-04: eave lights kept to the bare minimum): `EAVE_DL` holds 4 eave downlights, two over the D-side path (x 3500, 10000), one over the B-side path (x 4800) and one in the first-floor eave over the meter box and bins nook (16300, 675). `WALL_LIGHTS` holds the 10 wall lights. Both lists are top level and feed the fittings, the light pools and wall washes, the Electrical view markers, the estimate row and the outside-lights circuit in X-ray (eave lights through the wall top into the eave space; wall lights down inside their wall).
  - night lighting: `ROOM_LIGHTS` (14 point lights, 8 on phones) go to the room sources nearest the viewer, with sources behind the viewer ranked further away; with the lights on, paint and ceilings keep a soft glow in every room, so distant rooms never read as dark.
  - the entry Buddha is one continuous surface: marching cubes over a signed-distance field with smooth-min fillets (additive metaballs gave a blob). Use the same method for any figure that needs real curves.
  - furniture shapes: `soft(w,h,d,{ax,r,crown,top,pinch,wr,bow})` makes crowned cushions, pillows, duvets and bowed chair backs (`sblk` is the plan-coordinate version); `leg()` makes round tapered splayed legs. Use these for anything upholstered or turned instead of `RB` boxes (sofas, beds, armchair, dining chairs, bar stools, office chairs, benches already do).
  - plan notes built on 2026-10-04: smoke detectors (SD) at (9090,3760) GF hall, (7838,1506) and (14220,2637) FF; floor waste (FT) at (12170,6800) in the GF ensuite; D-side garden tap at x 2650 with the two capped "RWT pump & loop provision" stubs at x 2307 and 2445; ceiling fans in Bed 1 (17300,4400) and Bed 2 (5190,3090) in the coffers.
  - **Swallowed-code check:** a `//` comment followed by code on the same line silently drops that code (seven cases found on 2026-10-04: coffee-table legs, both bedroom fans, plants, a rug, a bath mat). Before publishing, scan for comments that contain `);`.
  - from the elevations, roof plan and sections (checked 2026-10-04): garage door is five 480 sections; meals door ASD 24.30 is four panels (fixed outer quarters, two leaves parting at the centre, `slider(...,true)`); AAW 24.21 and ASW 06.24 are three lights, AFW windows one light; downpipes are 75 mm round; 90 x 12 skirting is generated from the wall boxes after the furniture (stops at doors, joinery and tiling; none in the garage, through the stair or on the curved hall wall).
  - hot water (owner, 2026-10-04): two wall-mounted continuous-flow gas heaters, no storage cylinders. Ground floor: D wall at x 7910, base 1200 (where the plan and elevation D mark HWS). First floor: B wall at x 12430, base 4350, between the office and Ensuite 1 windows (clear of the downpipe at x 9231); it feeds all upstairs hot water through the floor zone. Each has cold, hot, gas and a power point.
  - roof details: apron flashings where the GF and garage roofs meet the FF walls, Colorbond capping on the front-frame parapet (6402) and garage portal (3400), two stack vents with boots through the upper roof, skylight openings cut in the roof sheet (`holes`), flat rectangular skylight glazing.
  - electrical audit (2026-10-04): `ELX` lists fixed equipment that needs power but is not a room light or power point (3 smoke alarms, 5 exhaust fans); each gets a power run, a marker in the Electrical view and a line in the estimate. Bed 1 and Bed 2 fans are in `D.elec` (`fan`) so they are wired and counted. Bathroom power points are at 1100 beside the vanity (the GF ensuite one was inside the shower alcove; the Ensuite 2 one was in the AC shaft). Both water heaters have a weatherproof power point and circuit.
  - exploded view levels: anything without `userData.lvl` is placed by its height; fittings on the first-floor ceilings inside the FF footprint stay with the first floor (`lvlOf`). Give merged meshes that span both floors one mesh per floor (the skirting does).
  - X-ray colour key: `#xrkey` sits above the X-ray badge whenever the options panel is closed, one chip per layer of the current view (`XLEG`), tap to hide or show (`famToggle`). It scrolls sideways on phones.
  - solar (owner, 2026-10-04): premium all-black panels with black frames and rails (black backsheet, half-cut cells with faint gaps), not blue cells in silver frames.
  - gutters: runs that meet at a roof corner are mitred at 45 degrees (outside corners grow with the profile, inside corners shrink); a run that simply stops gets a stop-end plate. Box gutters have stop ends too. Never leave a run as an open channel or let two runs cross at a corner.
  - operable windows (owner): every ASW and AAW window opens in the walk-through (door types `wslide` and `awn`), with a fixed flyscreen. Sliding: the sash slides on the inside track behind the fixed light, flyscreen outside; three-light sliders open both outer lights to the centre. Awning: each light is top-hung and pushes out about 300 at the bottom, flyscreen inside. AFW windows stay one fixed pane. Doors win the walk-through prompt over windows at a similar distance.
  - stormwater pump sump (civil C01 "PUMP" = 250 sq min grated sump symbol; calibrate C01 by the lot boundary: x = -6049 + (pdfX-221.22)/475.38*33540, y = -900 + (pdfY-367.4)/140.46*9910): `SUMP` at (49,1665), 600 grate in a concrete collar ring, 3000 L pump well Ø1600 x 1600 below (C01 notes: 2.0 L/s at 1.5 m head + chamber depth, min 3000 L detention, AS 3500, audible + visual failure alarm). Stormwater inspection point at (1086,1665). Grated trenches: 300 wide across the garage door (x 19500-19800) and 160 wide along the driveway edge by the porch (y 3830-3990), both tilted to the 12.5% driveway fall; gravity line east of the stone pier, under the porch and along the D-side path (y -600) to the sump. Rising main at y -760 to the kerb. Isolator and alarm on the meals rear wall pier (1710,640), dedicated circuit, conduit to the well.
  - steel connections (2026-10-04): `colTop()` runs a column up to the lowest beam that passes over it, or the highest underside of beams that end at it. MO7 and MO8 extend onto the wall plates they bear on; floor beams shallower than the 380 zone get steel packers where they sit on a plate (MO7, MO8 both ends, MO3 at the porch wall). AAC piers hold a concealed SHS post (architect's pier detail): porch corner (20245,1205) under MO6/MO3, and the alfresco corner (145,4365). The stone pier is timber framed (elevation A), no post. Check with `src/audit4.js` (every beam end and column top must bear on something).
  - interior audit `src/audit3.js` (2026-10-04): furniture into walls, furniture in door swings, fittings in joinery, power points with no wall behind or hidden, items in front of awning windows. Fixed then: alfresco garden tap (buried in its wall; removed, the outdoor sink has a tap), front tap moved to the porch pier's garden face (19800,900), kitchen oak board off the bench outlet, alfresco plant and porch olive moved, Bed 1 robe power point onto the wall by the make-up desk (13060,4660,1100), stair handrail 60 mm clear of the wall (was 9), GF heater hot pipe up inside the wall, alfresco hot water branching off the heater line (it still started at the old cylinder).
  - phone layout (owner, 2026-10-04): `body.compact` when the screen is under 641 wide or under 501 tall. A slim dock (`#dock`: Outside, Ground, First, Walk, More) replaces the toolbar; its buttons click the real ones (`data-proxy`) and mirror their `aria-pressed`. More opens the existing `.bar` restyled as a bottom sheet above the dock (sections Show, Layers and tools, View; picks close it except the Site, Surroundings, HQ and Sound toggles). The title card folds into a pill (`#tbpill`, just an ⓘ on phones, name + ⓘ on desktop) at the first drag, wheel or toolbar use; tapping the pill shows it for 6 s. On phones the controls fade to 15% while a finger is on the model. The X-ray badge drops its text on phones (the colour key says it).
  - GF WC: pan centred on the back wall with full-width tiling and ledge; roll holder on the garage-side wall (owner). Pantry: stainless dishwasher under the bench beside the sink (owner).
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
    - Floor: joists about 380 deep at 450, bearing on the GF plates (real 2730–3110, `FT=3110`), then 50 Hebel floor panels (to 3160) and 20 of finishes, avoiding the stair void (13400–19450 × 1100–2090). FF frames stand on the Hebel floor.
    - Roof: trusses at 900 from `ROOFS`. Over the Bed 1 and Bed 2 coffers the bottom chord steps up to 6252; the upper truss lines are offset to clear the skylight shafts.
    - Ceiling batts are 1200 tiles trimmed under the roof near the eaves. Porch and stone piers show as AAC blockwork.
  - **Steel per S-sheets:**
    - floor beams have top of steel 3110;
    - SB3 380 PFC at y 1043 (its rear end, x 1855–2500, is shown tapered because the GF roof is lower than the beam there: an open question for the engineer);
    - SB2/SB1 250 PFC at y 4363 / 6656; SB4 300 PFC at y 6656 (to 20251);
    - GL1 300 PFC at x 19346 over the garage door;
    - L1–L4 150 PFC lintels at 2400–2550;
    - MO1, MO7, MO8 (under FF walls) and MO6, MO3 (front frame) are "members by others", shown at placeholder sizes;
    - C1/C2 SHS 89 and SC1 SHS 75 stub columns.
  - **Footings** (engineer's S02 footing layout plan, `257115-S-COMBINED[B].pdf` page 2; x = (pt − 241.35) · 35.2778, y = (pt − 234.29) · 35.2778). The beam lines are drawn as rows of short dashes: merge the dashes to read them.
    - Slab 125 thick.
    - EB 250 × 700 around the house and garage perimeter.
    - IB 250 × 700 at x 3128 (y 250–4260), 6788, 8234, 10448 and 13860 (y 250–7860) and 16600 (y 1150–8760).
    - IB 250 × 700 at y 1026 (x 10571–13735), 3155 (x 1960–19240), 4386 (x 3250–6663) and 5965 (x 3250–19240).
    - MB 250 × 650 around the alfresco and porch.
    - All beams bottom out at −720.
    - The EB under the living/alfresco wall sits on the engineer's line, x 3000–3250.
    - 11 trench piers (hatched on S02), modelled 1000 deep below the beams. The real depth is to natural soil, decided on site.
    - The slab is 150 thick under the load-bearing wall at 8380–10320 × 4226–4725.
    - Wet areas (laundry, powder room, WC, ensuite) are set down 30 per the engineer's legend (slab top −50). The architect's slab plan does not list this set-down.
  - **Footings view** (button `m-foot`, X-ray mode `footings`): beams solid, slab see-through, with size labels (`FOOTL`). Footing beams are their own family, `foot`.
  - **Services (indicative):**
    - **Sewer:** main along y 7600, under the slab, to the IS at (−3071, 7963). The D-side branch runs along y 500. The two stacks are where the slab plan puts them (see the rev A section). Ensuite 1 drains along the x 12765 wall line to the hall stack. Ensuite 2 and the kitchenette drain to the robe-corner stack. Vents rise in the nearest FF wall.
    - **Stormwater:** charged lines at y −560 / 8585 / x −560 go to the tank inlet (−1640, −480). The tank overflow goes to a pump pit at (136, 2296). The rising main runs along y −760, then y 2973, to the kerb. The front sealed line is at y 211.
    - **Water:** meter at (27150, 3650), main along y −350. Hot comes from the HWS under the eave into the ceiling at y 420.
    - **Gas:** meter at (17880, 820), line along y −680 to the cooktop and BBQ.
    - **Power:** from the MB at (16900, 860). GF cables run at 2722 under the first floor (the cavity between the ceiling lining and the beams) and at 2790 in the roof space elsewhere. FF cables run at 5910 and step up to 6200 over the coffers (`ffPath`). Downlights are chained per room, with GPO drops inside the walls.
    - **Data:** NBN to the NTD, then to the hub at (10770, 2840), then star-wired.
    - **AC:** one ducted system (owner's decision, 3 Oct 2026). Condenser on the D-side path, refrigerant up the D wall to a fan-coil at (11300–12500, 3420–4080, 6280–6560).
      - FF ducts go to Bed 1, Bed 2, the office and the upper hall. The return air grille is in the upper hall at about (12334, 2633), as drawn (RA).
      - GF is fed by droppers through the architect's three "AC" shafts on the FF plan: beside the kitchenette (7280–7730 × 2230–2740), beside the Ensuite 2 shower (8880–9280 × 5800–6610) and in the Bed 2 robe corner (3190–3600 × 6200–6610).
      - From the shafts, ducts run in the floor zone to outlets in the kitchen, meals, Bed 4, hall and living room ×2.
- **Walk and sound:**
  - eye 1650; desktop pointer-lock mouse look, arrows and WASD move;
  - `surfaceAt()` picks the footstep sound: FF carpet except the ensuites; GF timber, with tiles in the wet areas, carpet in Bed 4 and concrete in the garage;
  - `SND` holds the ambience (birds, crickets, wind, rain, doors) and is exposed on `__t.SND`, with `XS` on `__t.XS`.

- **Riser rule:** `pipe()` passes every route through `inWalls()`, which moves indoor risers into the nearest wall (within 250 mm) and around any window or door. Hot water is offset 70 mm from cold. Stubs under 700 mm stay in their joinery.
- **Power points** were re-set on 2026-10-02 so each has a real wall behind it: kitchen and pantry points beside the splashback windows, laundry points on the bench wall, and none in door openings or in open space.
- **Services audit:** `src/audit2.js` (local) checks every pipe, cable and duct for openings, room exposure, roof, coffers, skylights and steel clashes; read `__audit2.sum`. One known leftover: the Ensuite 1 stack is wider than its wall.
- **Square-set openings** (SQ.OP on the plans; the code is height.width in decimetres, so 24.11 = 2400 high × 1100 wide) have wall above them from 2400:
  - kitchen/pantry at x 8190, y 900–1890;
  - living/hall at x 8190, y 3330–4430, with lintel L2 over it at 2400–2550;
  - hall/powder at y 4430, x 11470–12560;
  - FF Bed 2/WIR at y 5090, x 6290–7190;
  - FF Bed 1/WIR at x 15210, y 3820–4720.
- **Downpipes per the DWG plans** (r 60 circles):
  - GF at (13380, −120), (2059, −120), (145, 4100), (260, 8230), (7834, 8230) and the garage rear corner (13590, 9010);
  - FF at x 3200, 8337, 16090 and 18967 on the D side, and 3470, 9392 and 18620 on the B side.
- **Joinery and fixtures audit against the DWG (2026-10-03).** These matched: island (4790–7190 × 1890–2790), kitchen and pantry benches, laundry bench, robe, walk-in robes and desks, kitchenette, towel rails, return-air grille, roof outlines. These were corrected:
  - AC outdoor unit position;
  - alfresco bench start (x 290);
  - first-floor linen cupboard added (9370–9870 × 2230–3180, doors facing the upper hall).
- **Electrical view:** the overlay (`setElec`) and the estimate panel (`elPanel`) are separate.
  - On phones the estimate starts closed.
  - Closing the estimate keeps the points on; a bar (`#elbadge`) shows the legend and the floor, with Estimate and Turn off buttons.
  - Opening X-ray, Sun or Finishes only closes the estimate. Walk turns the overlay off.
- **Flicker (z-fighting) audit:** `src/zfight.js` (local) lists coplanar, same-facing surfaces of different materials; in `test.html` run `await import('/zfight.js')` and read `__zf`.
  - Fixed on 2026-10-04: garage jamb trims, FF slab edges (now 8 inside the wall faces), door liners (5 proud), wall-art prints, shower niche tiles, alfresco soffit and lining, plant soil.
  - The remaining hits are downward faces (`@y-`) or back faces against walls.
  - The orbit camera's near plane now grows with distance.
- **Wall-gap check:** `gaps.py` (session scratch) samples every DWG wall line against the model's wall and opening edges. It found the WC/garage wall stretch lost when the old stack box was removed, and the alfresco corner pier (290 square, not 250).
- **Door swing audit:** `swingDoor` hinge, leaf and open side were compared with the door arcs in the DWG (radius 500–1150, layer 0) on 2026-10-03. All 13 matched; the double doors show one leaf drawn at 45°.
- **Retaining walls** (civil C01 blue lines, details C03/C04; buffers `__ret`, `__retp`, X-ray family `ret`): concrete sleepers 100 × 200 between galvanised posts at 2000.
  - **Rear wall:** across the yard at x −1467…−1289 (`RWX=-1378`).
  - **B-boundary wall:** x −1378…13712, y 8910–9010.
  - **Levels for both:** top RL 98.90 (−100), base RL 98.25 (−750), 0.65 m of fill, "to be confirmed on the neighbouring levels".
  - **Steps** through the rear wall at y 2836–3731 (three 125 risers).
  - **Driveway wall:** B boundary, x 19490–21100, top +150, base −200 (0.35 m cut).
  - **Ground:** `ground(x)` is −750 at the foot of the rear wall, falling to −900 at the rear (sewer shaft lid RL 98.10), and −250 on the platform.
  - **Driveway (civil C01):** paving RL 98.95 at the garage door, 12.5% for 2 m to 99.20, then 20%. The design carries on to RL 100.00 and a 100.15 crest at the boundary. The model caps at verge level 950, so the lot meets the street: an accepted 200 mm difference at the boundary.
  - **Sewer:** the inspection shaft is at (−3071, 7963) with invert RL 96.60 (−2400). The main drops to it from the under-slab run.
  - **Tank:** the owner wants it along the D side, as the architect's site plan draws it (3 Oct 2026); do not turn it along the retaining wall as the civil plan does.
    - Size: a Team Poly Aqua Spring 3000 L slimline, 2500 × 750 × 2000.
    - Position: x −1150…1350, y −850…−100 (centre (100, −475)), just clear of the rear retaining wall. Inlet at the house end, (990, −475).
  - **Pavers:** the stepping pavers line up with the steps (y 2850–3310).
  - **Superseded labels:** the civil PDF holds hidden text (TRW 99.45 / 1.25 m). Read the labels from a render, not from the text layer.
- **Area schedule check (2026-10-03):** the info card (106.6 + 106.0 m² living, 259.5 m² under roof) matches the AREAS table on the rev A plans (106.58, 106.00, garage 32.26, alfresco 12.26, porch 2.40, total 259.50).
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
