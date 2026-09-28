// Encrypts src/model.html back into index.html with a fresh salt and IV.
// Usage: node tools/build.mjs              (prompts for the PIN)
//        VR3D_PIN=xxxx node tools/build.mjs
// The PIN used here becomes the PIN for the published page.
import { readFile, writeFile } from 'node:fs/promises';
import { webcrypto as crypto } from 'node:crypto';
import { readPin, root } from './pin.mjs';

const ITER = 600000;
const html = await readFile(`${root}/index.html`, 'utf8');
const payload = /const SALT="[^"]+", IV="[^"]+", CT="[^"]+", ITER=\d+;/;
if (!payload.test(html)) throw new Error('Could not find the encrypted payload in index.html');

const model = await readFile(`${root}/src/model.html`);
const pin = await readPin();
const salt = crypto.getRandomValues(new Uint8Array(16));
const iv = crypto.getRandomValues(new Uint8Array(12));
const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pin), 'PBKDF2', false, ['deriveKey']);
const key = await crypto.subtle.deriveKey(
  { name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' },
  base, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, model);

const b64 = u => Buffer.from(u).toString('base64');
const line = `const SALT="${b64(salt)}", IV="${b64(iv)}", CT="${b64(ct)}", ITER=${ITER};`;
await writeFile(`${root}/index.html`, html.replace(payload, () => line));
console.log(`Encrypted src/model.html (${model.byteLength.toLocaleString()} bytes) into index.html`);
