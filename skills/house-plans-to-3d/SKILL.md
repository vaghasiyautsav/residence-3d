---
name: house-plans-to-3d
description: Turn a house's architectural working drawings (PDF floor plans, elevations, roof, site and civil plans) plus owner photos into an accurate, realistic, walkable three.js model, with millimetre-checked walls, openings, heights and joinery, real-size furniture, street and neighbour context, and a PIN-locked single-file deploy. Use when building, checking or refining a 3D house or residence model from drawings.
---

# House plans → accurate, interactive 3D house

The result is one self-contained HTML page (three.js) that the owner can open on a phone. It has:
- an orbit exterior;
- ground and first floor plan cut-aways, showing each room's size;
- a first-person walk-through with working doors;
- sun, weather and lights controls;
- finishes pickers;
- an electrical estimate;
- a measure tool;
- a toggle to show or hide the surroundings;
- a PIN lock.

The owner compares it with the drawings and with the real site, so the priorities are **accuracy first, then realism, then styling.** Keep the styling sparse; owners find busy rooms cramped.

Bundled:
- `scripts/pdf_probe.py` reads a drawing sheet in plan millimetres: lines, curves, text and image crops.
- `scripts/wall_coverage.py` proves every drawn wall exists in the model.
- Reference project: `github.com/vaghasiyautsav/residence-3d`. Its `tools/` folder holds encrypt, decrypt and test-page scripts, and its `skills/` folder holds this skill and a worked project skill.

## 1. Read the drawings properly

**Calibrate every sheet** before reading anything off it.
- Scale in mm per PDF point = 25.4/72 × scale denominator: 1:100 → 35.2778, 1:200 → 70.5556, 1:50 → 17.6389.
- Sheets marked "1:100 @ A3" but issued on A2 are still 1:100 on the A2 sheet. Check this against the scale bar's tick labels and one long written dimension.
- Pick an origin: one wall corner whose plan coordinates you define. Then `pdf_probe.py --cal px,py,X,Y`.
- Plan convention:
  - x runs the house length, rear 0 → front;
  - y runs side to side;
  - z is height from the GF finished floor level.
- Write the calibration of each sheet down.

**Look before you trust numbers.** Render crops (`pdf_probe.py --png`), and read the legend and the general notes on every sheet.

**Line meanings** (confirm with each set's legend):

| Mark | Meaning |
|---|---|
| Black, ≥0.6–1.0 pt | Walls |
| Grey, ~0.36 pt | Joinery, fixtures, drawn furniture |
| Light-grey hatch | Usually dropped bulkheads (e.g. "300H dropped bulkheads") |
| Red dashed | Floor or roof above |
| Dashed | Overhead items (headers, high shelves) |
| Bezier curves | Door swings, curved walls (look for an "R200"-style label), basins, trees |

**Written beats scaled.** The disclaimer usually says "use written dimensions only". The general notes give:
- door heights (seen: 2340 internal and external);
- CH (2700);
- window head ("2400 windows H/HT");
- obscure glazing ("1500 OBS");
- floor zone (420) and plates (2730).

Scaled values are only for what isn't written. When elevations draw heads 50 mm off the written value, keep the written one.

**Garbled text.** Custom drawing fonts can garble digits in the extracted text; seen: `\x14`=3 and `\x18`=7, so "2\x1800 CH" = 2700 CH. Decode against known strings; never guess.

**Window codes.** `TYPE HH.WW` = height × width in 100 mm:
- ASW 06.21 = 600 high × 2100 wide sliding window;
- AAW 24.06 = 2400 × 600 awning window.

Head comes from the H/HT note, so sill = head − height. Then check every window on the elevations:
- kitchen and butler's pantry windows are often splashback windows at bench height (seen 900–1600 and 900–1500);
- side windows are often high.

**Furniture drawn on the plans** (sofa, TV unit, dining set, island, sometimes beds) is the architect's intended size. Model it exactly. Owners compare.

**Details hide geometry:**
- shower-niche elevations (seen: full-width niche, 450 high at 1100, under the window);
- box gutters (300W × 250H) and eaves (450);
- cladding and stone veneer notes;
- typical meter box, NBN and gas details.

### Elevations → every height
1. Find each elevation's FL datum from its dimension stack (e.g. 2730 / 420 / 2730 = plate / floor zone / plate).
2. Map its horizontal axis to plan x or y using two known features (a wall end, a window jamb).
3. Measure:
   - eave sheet edge and fascia;
   - ridge;
   - roof junctions with upper walls;
   - parapet and frame bands;
   - garage portal and boundary walls;
   - window and door heads;
   - the order of stone, render and cladding.
4. Accept a value only when all four elevations agree. Cross-check the geometry: eave edge + run × tan(pitch) must reproduce the ridge and the junction lines.
   - Seen: GF eave 2651; upper eave 5801; ridge 7209; GF roof meeting the upper walls at 3210 and 3380.
   - Guessing roof bases as "plate + 50" put the whole roof 130 mm too high.

### Roof plan
- Ridges and hips give the plan geometry. With equal pitches, hips run at 45° from the eave corners.
- Note:
  - box gutters, with their sizes;
  - fall arrows;
  - rainheads and downpipes;
  - parapets;
  - sub-roofs at their own levels (e.g. a garage roof falling to a box gutter on a 2730 boundary wall, hipped at its ends).

### Site plan and civil survey
- **What it gives:**
  - boundaries (bearings and lengths) and levels (TBM, TK top of kerb, WT water table, RL);
  - kerb lines, footpath edges, crossover width (seen 5000);
  - existing trees to be removed;
  - pits and poles in the legend.
- **Street.** Build it from these lines, not from a typical section. Footpaths jog around old crossovers, and kerbs aren't parallel to the boundary.
- **Off-lot items** (neighbours' houses, fences, power poles, current trees):
  - use satellite and Street View for massing;
  - use the owner's recent photos and words for what is there now.
  - The owner beats old imagery, e.g. "the pole is on the far side of the next lot".

### Verify the extraction (every round)
- Run `scripts/wall_coverage.py` per floor. The only leftovers should be door swings, shower-door swings and balustrades lower than the check height.
- Find curved walls separately: `pdf_probe.py --lines --black` and look for `c` items. A missing one leaves a hole in the wall.
- Snap model wall faces to the drawn lines, within 2 mm. Window widths must equal their codes.

## 2. Coordinates and helpers (write them at the top of the source)
- **World units.** World metres: `wx(x)=x/1000-OX`, `wz(y)=y/1000-OY`, `wy(z)=z/1000`.
- **Constants:** first floor `U`, eave bases, `TAN=tan(pitch)`, `LOT`, and `ground(x)` (finished ground level, from the levels).
- **Data.** Keep the plan data inline as `const D = {walls:[[x0,y0,x1,y1,z0,z1,kind]], arcs:[[cx,cy,r0,r1,a0,a1,z0,z1]], openings, doors, elec, labels}`, with `kind` ∈ render/stone/frame/dark/pier/balus.
- **Helpers:**
  - `blk(mat,x0,y0,x1,y1,z0,z1,r)` makes rounded boxes in plan millimetres.
  - `grp(x,y,z,face)` builds wall-mounted groups (face `x+ x- y+ y-`, local +x out of the wall).
  - `sgrp` snaps that group onto the real wall face by marching to the nearest `D.walls` box, so fixtures never float off or sink into a wall.
  - `fronts`, `baseRun` and `slabH` handle joinery, with a floor-level argument so first-floor joinery isn't built at ground level.
- **Helper order.** Define helpers before use. A `const` helper used earlier in the file throws a temporal-dead-zone error; seen with `RB`/`cyl` in early site code. Use raw three.js geometry there.

## 3. Building shell
- **Walls.**
  - Boxes, with openings carved into jamb, sill and head pieces.
  - Each face is coloured inside (paint) or outside (render) by testing a point 60 mm off it against the footprint rectangles.
  - Curved walls are arcs and take interior paint when they are inside.
- **Roof as a height field** over the union of eave rectangles, sampled on a 50 mm grid:
  ```js
  // comp = rectangles covering the complement of the union; d = Chebyshev distance to it
  h = base + TAN * min over comp of max(dx, dy)
  ```
  - Merge planar runs.
  - Convex creases get folded capping: an extruded profile, never cylinders.
  - Eave edges (h = base) get a fascia and an extruded gutter profile.
  - Raked or box-gutter edges get a fascia from min(h) − 200.
- **Sub-roofs at another level:** `h = max(mainField, subField)`, where subField = its base + TAN·min(distance to its own eave lines). The max produces the valleys.
- **Parapet frames:** an open U-shaped parapet, a soffit, and 300 box gutters behind it. Stop the roof region at the gutter line; a solid lid looks wrong from above.
- **Garage sectional/panel door.** The vertical track must reach the door head before curving (R ≈ 200), then run horizontal under the ceiling. If the curve starts below the head, the top panel tips in when closed.
- **Stair handrail:** about 900 above the nosings, starting over the first tread. Return both ends into the wall so no stub pokes past a wall end.
- **Stone veneer as real stones**, not a photo texture (that reads as flat wallpaper with visible repeats). Stones are 18–38 mm proud of a mortar-coloured core. To match an irregular random pattern like the one on the elevations:
  1. Scatter seeds in staggered rows (rows 110–180 high, stones 200–420 long).
  2. Compute Voronoi cells in a space squashed in x (×0.6) so cells come out about 2:1.
  3. Clip each cell with half-planes and inset it ~9 mm for the joint.
  4. Extrude 18–38 mm with a 4–5 mm bevel, and warp the front face (4–9 mm of sine noise).
  5. Tilt each stone ±1.5° and tint it with vertex colours on one shared material.
  6. Merge everything into one mesh.
  7. Front faces extend 40 mm past the corners so the corners interlock.

  For coursed ashlar instead, use rows of rectangles 100–250 high and 150–450 long.
- **Mirrors.** three.js `Reflector`, made visible only while walking within ~6 m, so it costs nothing elsewhere. A static mirror material reads as a grey board.

## 4. Site, street and context
- **Lot surfaces.** Lawn, concrete, aggregate and pavers come from the site-plan legend polygons. The tank sits on its pad, never on a slope.
- **Lawn** is instanced 3D grass over a patchy turf texture:
  - each tuft is 9 thin triangles, 35–80 mm tall, base shade 0.42 and tip 0.86, normals up;
  - per-tuft colour about HSL(86–106°, 0.42–0.6, 0.24–0.34);
  - 240 tufts/m² on desktop, 110 on phones;
  - keep it off beds, pavers, pads and pillars, and give it no shadow casting.
- **Street,** from the survey, as `ShapeGeometry` polygons:
  - verge (nature strip), footpath with its jogs, a gravel strip;
  - 150 upright kerb + 320 water table, then the road;
  - laybacks (ramps) at crossovers;
  - verge level from TK.
- **Surroundings group** (`ctx`): the street, neighbours, their trees, poles and mains. Give it a Surroundings button.
  - The side and rear elevation views switch it off, because neighbours block them; the button shows the change.
  - Fences stay with the lot.
- **Neighbours:** simple boxes with hip roofs, coloured from the owner's photos. Model fences per side (colour, plinth) from photos.
- **Power poles** (Adelaide: Stobie poles):
  - tapered concrete web between steel channels, ~10.5 m;
  - LED luminaire on a 3 m outreach arm, crossarm with insulators, sagging conductors and an aerial bundled cable;
  - a SpotLight whose intensity follows sun elevation, so it comes on from dusk (≈240 cd, decay 1.8).
  - Keep it out of the opening camera view.
- **Services:**
  - AC condenser, heat-pump hot water units, taps, wall lights, downpipes from the civil DP positions;
  - the meter box, NBN NTD and gas meter per the typical detail, labelled as proposed;
  - council bins beside the meter box: 240 L = 580 × 730 × 1080; 140 L = 480 × 555 × 940.
- **Wall up/down lights** need visible output:
  - additive-blended cone planes on the wall above and below each fitting;
  - a shader with width growing along the beam and falloff (1−v)^1.5, plus a hot core;
  - glow sprites at the lens ends;
  - all in the light-effects group that follows the lights switch.

  Small emissive discs alone look switched off.

## 5. Interiors at real size (so the leftover floor reads true)

| Item | Real dimensions (mm) |
|---|---|
| Sofa | seat 430–450 high, arms 600–650, back 800–900, depth 800–1000, seat depth 550–650 |
| L-sofa | as drawn (seen 2707 × 2781) |
| Coffee table | 400–450 high, ~900 diameter |
| Side table | 500–600 high |
| TV | 55" = 1232 × 712, 65" = 1450 × 830. Low cabinet 400–480 high, ~450 deep |
| Dining table | 750 high. Table for 6 is 1600–1800 × 900–1000; for 8 it is 2000+ |
| Dining chairs | seat 450–470 high, ~450 wide |
| Counter stools | seat ~650 for a 900–920 bench. Pendants hang ~750 above the bench |
| Beds (AU mattress) | queen 1530 × 2030, king 1830 × 2030, double 1370 × 1880. Mattress top ~530; base adds ~40 a side. Bedhead 1.0–1.3 high |
| Bedside table | 450–500 × 400 × 550–600 |
| Bench at bed end | ~450 high |
| Lounge chair | ~800 × 800, seat ~400 |
| Desk | 1500–1600 × 700–750 × 730–750 |
| Two-seater | 1300–1700 long, seat 440 |
| Robes | 500–550 hanging, 350 shelving. Walk-in robes keep ≥ 500–900 walkway |
| Make-up desk | as drawn (seen 500 deep) |
| Benches | 900–920 including the stone top. Overheads 350 deep, under a 300 bulkhead to the 2700 ceiling |
| Baths | as drawn (seen 1480 × 752) |
| Showers | as drawn, with a centre waste and the rose where drawn. Door hinge placed so the swing clears the toilet |
| Garage door | 2400 high (2 panels × 1200) |

- **Common oversizing mistakes:** sofa seat 545 and back 1000 made a 5.0 × 3.4 m living room look tiny. A 75" TV and full-height media towers that aren't on the plan did the same.
- **Bulkheads** go wherever the plan hatches them, from the top of the joinery (2400) to the ceiling.
- **Wet areas:** tiles stop at the window sill; niches per detail; shared tapware material so one picker recolours every tap and rail.
- **Plants** stay out of door swings and off walls and glass; nudge them clear of consoles.
- **Doors and cupboards.** Swing leaves snap to the jambs. Linen and robe cupboards get doors unless the plan shows them open.

## 6. Interaction and UX
- **Modes.** Exterior orbit / GF plan / FF plan / walk.
- **Plan labels** show each room's inside size, e.g. "LIVING 5.00 × 3.41 m", taken from wall inside faces.
- **Opening camera:** a three-quarter view clear of poles, wires and trees.
- **Orbit FOV:** 40° vertical on landscape. On portrait phones use `fov = min(76, 2·atan(tan(19.5°)/aspect))` so the whole house fits the width.
- **Walk mode** (game-style, like Pascal's walkthrough):
  - FOV set by horizontal angle (78° portrait, 84° landscape), eye at 1650;
  - on desktop (`(hover:hover) and (pointer:fine)`), click locks the pointer for mouse look, W A S D and the arrow keys move and strafe, Shift runs, and a click while locked opens the door under the crosshair;
  - Esc frees the mouse; a second Esc leaves walk mode (time the `pointerlockchange`);
  - drag-to-look stays as the fallback, because some embedded views refuse pointer lock (`WrongDocumentError`). Catch both requestPointerLock promises;
  - phones get the joystick, drag-look and pinch zoom; hide the joystick on desktop;
  - eased velocity (about 1.55 m/s walking, 3.4 m/s running);
  - head bob of 14 to 24 mm with a tiny roll, a footstep on every half stride, and collision that kills only the blocked axis;
  - stairs follow the floor height, smoothed.
- **"Go to" spots:** check every spot's 250 mm radius against walls and furniture. Seen: a bedroom spot inside an armchair and a living spot inside the coffee table. Face each one at a good composition.
- **Panels:**
  - time-of-day on the local sun path, weather, lights;
  - finishes (floors, tiles, tapware, wall colours, saved in localStorage inside try/catch);
  - electrical estimate (spacing rules, GPOs at 1100 over benches and 300 elsewhere, data/TV/NBN, marked as a budget estimate);
  - measure tool.
- **Toolbar** rows scroll sideways on phones. Keep labels short.

### X-ray, structure and services layer
- **Tag every mesh** with a level (0 GF, 1 FF, 2 upper roof) as the geometry is built. Use a buffer key suffix, so merged meshes never mix floors; split glass and gutters by level too. Tag each mesh with its material key so it can be given a family.
- **Families:**
  - finishes: roof, walls, ceilings, floors, openings, furniture/fittings, ground;
  - structure: frames, AAC, insulation, joists, trusses/battens, steel, slab/footings;
  - services: sewer, stormwater, cold, hot, gas, power, data, HVAC.
- **Each family is Solid, Ghost or Hidden.** Display modes (Finished / X-ray / Structure / Services) only set the defaults. Implement it this way:
  - **Hidden:** `layers.set(31)`. Don't toggle `visible`, which other code owns. Layers also drop the mesh from shadows and raycasts.
  - **Ghost:** swap in a cached clone of the material (`copy`, then transparent, depthWrite false, low opacity) and turn its shadow off. Leave the shared materials alone.
  - **Material swaps by other code:** if the mesh's material is not the one you last set, adopt it as the new original.
  - **Never ghost** a Reflector or a ShaderMaterial or `onBeforeCompile` material (grass): hide it instead.
- **Ghost stacking:** overlapping slab and floor rectangles stack many ghost faces and blank out what is under the slab. In the Services mode default, floors and slab are Hidden, and the ground is ghosted.
- **Explode:** offset each level group's `position.y` by about 3.6 m per level, calling `updateMatrix` for static meshes. Reset it when entering walk mode.
- **Section:** add a second clipping plane to every house material once, and move it along x or y. Make the roof double-sided while a section is active.
- **Framing generated from the wall boxes** (InstancedMesh, ~10 draw calls):
  - Frame each wall piece. Pieces over openings get headers and pieces under them get sill tracks. Studs sit on a global 600 grid; jambs and corners are doubled. A nogging row goes at 1350.
  - Find the outside face of a wall by testing 60 mm out against the interior footprint. Put the 75 AAC panels (600 wide) on that face, and the batts between the studs.
  - Roof trusses at 900 c/c are sections of the roof height field, with the top chord about 95 under the sheet. The webs alternate over the footprint. The battens follow the field.
  - Floor joists at 450 c/c split at the floor beams. Beams, columns and footings come from the engineer's sheets.
  - Use lipped C ExtrudeGeometry for studs, joists and PFCs.
- **Services are polylines** of plan points: an instanced cylinder per segment plus a sphere per joint. Use `emissiveIntensity ~0.2` so they read through ghosts.
  - Route underground at ground −350…−600, under the slab with a real fall to the connection point, in the ceiling void (GF 2770), and in the joist zone (FF 2980).
  - Put stacks in wall cavities that line up on both floors.
  - Take stormwater from the civil drawing: sealed lines to the tank, then overflow to a pump pit and a rising main to the kerb.
  - Mark the whole layer indicative until the trades' drawings arrive.

### Ambient sound (procedural WebAudio, no files)
- **Start the AudioContext** on the first pointer or key event, honour a Sound toggle (saved in localStorage), and suspend it when the tab is hidden.
- **Buses:** ambience goes through a lowpass "muffle" (about 650 Hz and half gain indoors), then a compressor. Birds and crickets also feed a generated-impulse convolver for garden reverb.
- **Birds** (by day, densest at dawn and dusk, fewer in rain) are short enveloped sine glides with random pan:
  - tweets 2.5–3.8 kHz;
  - fluty 1–1.8 kHz whistles;
  - a soft AM trill;
  - chips.
  Keep the gains at 0.02–0.05 so it stays calm.
- **Night:** crickets are about 4.5 kHz triple pulses per voice with rests.
- **Weather:** wind is band-passed brown noise. Rain is band-limited white noise.
- **Footsteps** are band-passed noise bursts by surface (timber, tile, carpet, concrete, paving, grass) plus a heel thump.
- **Doors:** a latch click and a swish. The garage door gets a motor rumble.

## 7. Build, lock, deploy
- **Source.** The readable source (`src/model.html`) is git-ignored. `index.html` is a PIN gate holding the model encrypted with AES-256-GCM, key from PBKDF2-SHA256 with 600k iterations, decrypted with WebCrypto.
- **Tools** (reference repo): `node tools/decrypt.mjs`, `VR3D_PIN=… node tools/build.mjs`, `node tools/testpage.mjs` (adds `window.__t` debug hooks).
- **Verify the build:** decrypt the new `index.html` and compare byte-for-byte with the source.
- **Publish** on GitHub Pages (public repo, main/root). Then poll the live page until its embedded `SALT` matches the new build before telling the owner it's live.
- **Never commit** the unlocked source, the PIN, a handoff file containing the PIN, or a source bundle. The repo is public.
- **Attribution.** Commit as the owner. If they ask, include no AI attribution lines.

## 8. QA every round
- **Test page hooks:** `__t.look(x,y,yaw,pitch,lvl)` (yaw 0 faces −y, π/2 faces −x; positive pitch looks down), `__t.walk(spot)`, `__t.time(h)`, `__t.lights(on)`, `__t.D/DOORS/FUR/scene/camera/controls`. Use `?v=N` to bust the cache.
- **Audits** (in the page, after `scene.updateMatrixWorld(true)`):
  1. Furniture boxes vs wall boxes: penetration > 30 mm outside openings. Sloped rails give bounding-box false positives, so confirm by hand.
  2. Every swing door's sector (sampled radii × angles, 100–1900 above the floor) vs furniture bounds.
  3. Walk spots vs walls and furniture.
  4. `wall_coverage.py` vs the plans.
  5. Console errors and warnings.
- **Look at it:** day and night, every elevation, each room, the opening view, and phone portrait.
  - Look for floating, clipped or buried items, gaps, z-fighting, lights that don't read as on, doors not closing flat, stubs past wall ends, and mirrors.
  - Treat each glitch as a class: search the whole house for the same mistake.
- **Pitfalls:**
  - A hidden browser pane lags screenshots ~10 s and throttles frames. Wait, or read pixels.
  - Free the preview port (stop stray servers) before starting the configured one.
  - argparse needs `--box=-100,...` for values that start with a minus.

## 9. Working with the owner
- **Rounds:** deliver in rounds. Each round: verify, rebuild, lock, push, confirm live, then give a short summary of what changed and what remains uncertain.
- **Questions:** don't ask what the drawings answer. Ask about what they leave open: finishes, the PIN, deployment, off-lot facts.
- **Proposals:** where you must choose (a pole position, a meter box), choose sensibly, say so, and offer to move it.
- **Owner's word wins:** owner corrections beat your reading of the plan. Their photos show the site today.
- **Reporting accuracy:** state what is verified (walls, openings, heights, joinery, drawn furniture) and what isn't fully defined by the drawings (scaled-only heights, undrawn furniture, off-lot features).
