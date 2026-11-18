// make.fun entry — competition news-image-20261118
// "Sum up 18 November's world news in one image"
//
// The day's news is already drawn in entry.png beside this file, so the program
// copies those exact bytes to /output/entry.png. It reads no network, no clock
// and no random source, so the two runs the grader makes write the same bytes.
//
// Before it writes, it checks the bytes really are a PNG of a size the gate
// accepts, so a corrupted file fails loudly here instead of scoring 0 there.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only.

import { closeSync, copyFileSync, mkdirSync, openSync, readSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024; // 1 MiB, the gate's ceiling
const MAX_SIDE = 1024; // 1024x1024, the gate's ceiling

const source = new URL('./entry.png', import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destination = join(outputDir, 'entry.png');

const size = statSync(source).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the gate's ${MAX_BYTES}`);
}

const head = Buffer.alloc(24);
const fd = openSync(source, 'r');
try {
  readSync(fd, head, 0, 24, 0);
} finally {
  closeSync(fd);
}
if (!head.subarray(0, 8).equals(PNG_SIGNATURE)) throw new Error('entry.png is not a PNG');
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the gate's ${MAX_SIDE}px`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, destination);
if (statSync(destination).size !== size) throw new Error(`short write to ${destination}`);

console.log(`entry.png: ${width}x${height}, ${size} bytes -> ${destination}`);
