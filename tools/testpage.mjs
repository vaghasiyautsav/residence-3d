// Writes src/test.html: src/model.html plus debug hooks on window.__t, for local checks and screenshots.
// Usage: node tools/testpage.mjs [src/model.html] [src/test.html], then open http://127.0.0.1:8173/test.html
//   __t.walk('Kitchen')         enter walk mode at a "Go to" spot
//   __t.look(x, y, yaw, pitch, lvl)   stand at plan mm on level 0/1 (eye 1600 up); yaw 0 faces -y, π/2 faces -x (rear)
//   __t.time(21); __t.lights(true)
import { readFile, writeFile } from 'node:fs/promises';
import { root } from './pin.mjs';

const [inp = 'src/model.html', out = 'src/test.html'] = process.argv.slice(2);
const html = await readFile(`${root}/${inp}`, 'utf8');
const anchor = 'let lastT=performance.now();';
if (!html.includes(anchor)) throw new Error(`Render loop anchor not found in ${inp}`);
const hook = `window.__t={THREE,scene,camera,controls,renderer,W,ENV,FUR, get composer(){ return composer; },
  walk(n){ if(!W.on) enterWalk(); const s=SPOTS.find(s=>s[0]===n); if(s) goSpot(s); },
  look(x,y,yaw=0,pitch=0,lvl=0){ if(!W.on) enterWalk(); W.x=x; W.y=y; W.lvl=lvl; W.yaw=yaw; W.pitch=pitch; W.h=floorH(x,y,lvl); },
  time(h){ const r=document.getElementById('tod'); r.value=h; r.dispatchEvent(new Event('input',{bubbles:true})); r.dispatchEvent(new Event('change',{bubbles:true})); },
  lights(on){ setLights(on); ENV.userLights=true; } };
`;
await writeFile(`${root}/${out}`, html.replace(anchor, () => hook + anchor));
console.log(`Wrote ${out}`);
