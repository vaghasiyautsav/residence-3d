# Vaghasiya Residence – 3D model

Interactive 3D model of the Vaghasiya Residence, 20 Telowie Avenue, Ingle Farm SA (Studio Forthwall project 26002).

**Live site:** https://vaghasiyautsav.github.io/residence-3d/

The page is PIN protected. Ask the owner for the PIN.

## What you can do
- Orbit the exterior, or switch to the ground floor and first floor plan cut-aways (each room shows its inside size)
- Walk through the house in first person and open or close the doors
- Change the time of day, weather and lights (wall lights and the street light come on at dusk)
- Show or hide the surroundings: the street, neighbouring houses and their trees
- Choose the flooring (timber or tiles), the tapware finish, and the interior and exterior wall colours
- Show the electrical estimate: downlights, power points, data and TV points, and the NBN connection
- Measure distances

Walls, openings, heights, roof and joinery follow the approved drawings (Studio Forthwall 26002) to within a few millimetres; furniture is at real catalogue sizes.

Works in any modern browser on desktop or mobile. The published page is a single file (`index.html`).

## Editing
`index.html` is a PIN screen wrapping the model, which is encrypted (AES-256-GCM, key from the PIN via PBKDF2-SHA256).
The readable model lives in `src/model.html`, which git ignores. This repo is public, so never commit `src/`.

```bash
node tools/decrypt.mjs   # index.html -> src/model.html (asks for the PIN)
node tools/build.mjs     # src/model.html -> index.html (asks for the PIN; this becomes the page's PIN)
```

Preview while editing: `python3 -m http.server 8173 --directory src`, then open http://127.0.0.1:8173/model.html.
`node tools/testpage.mjs` writes `src/test.html`, the same page with debug hooks on `window.__t` (jump to a spot, set the time, switch the lights).

## Reusing the method
[`skills/`](skills/README.md) holds the playbooks behind this model: a general method for turning working drawings into an accurate 3D house (with drawing-reading scripts), and this project's facts and workflow.
