// Decrypts the model embedded in index.html into src/model.html (git-ignored).
// Usage: node tools/decrypt.mjs            (prompts for the PIN)
//        VR3D_PIN=xxxx node tools/decrypt.mjs
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { webcrypto as crypto } from 'node:crypto';
import { readPin, root } from './pin.mjs';

const html = await readFile(`${root}/index.html`, 'utf8');
const m = html.match(/const SALT="([^"]+)", IV="([^"]+)", CT="([^"]+)", ITER=(\d+);/);
if (!m) throw new Error('Could not find the encrypted payload in index.html');
const [, salt, iv, ct, iter] = m;
const b64 = s => Buffer.from(s, 'base64');

const pin = await readPin();
const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pin), 'PBKDF2', false, ['deriveKey']);
const key = await crypto.subtle.deriveKey(
  { name: 'PBKDF2', salt: b64(salt), iterations: Number(iter), hash: 'SHA-256' },
  base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
let pt;
try { pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64(iv) }, key, b64(ct)); }
catch { console.error('Wrong PIN.'); process.exit(1); }

await mkdir(`${root}/src`, { recursive: true });
await writeFile(`${root}/src/model.html`, Buffer.from(pt));
console.log(`Wrote src/model.html (${pt.byteLength.toLocaleString()} bytes)`);
