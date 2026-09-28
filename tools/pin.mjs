import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';

export const root = fileURLToPath(new URL('..', import.meta.url)).replace(/\/$/, '');

// Reads the PIN from VR3D_PIN, or prompts for it without echoing.
export function readPin() {
  if (process.env.VR3D_PIN) return Promise.resolve(process.env.VR3D_PIN);
  return new Promise(resolve => {
    const rl = createInterface({ input: process.stdin, output: process.stdout, terminal: true });
    rl._writeToOutput = s => { if (!rl.muted) process.stdout.write(s); };
    rl.question('PIN: ', pin => { rl.close(); process.stdout.write('\n'); resolve(pin.trim()); });
    rl.muted = true;
  });
}
