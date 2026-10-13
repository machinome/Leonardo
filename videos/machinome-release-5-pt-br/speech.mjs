// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// The pilot approved proposal 7. Rendering never generates another take.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const manifest=JSON.parse(await readFile(new URL('_build/approved/narration-manifest.json',import.meta.url)));
assert.ok(!process.argv.includes('--generate'),'Use the approved cache, not a new audition.');
const digest=createHash('sha256').update(await readFile(manifest.cacheFile)).digest('hex');
assert.equal(digest,'d2dc2542d7a15e0fdb83451e002dea8a2c8dbbf4d6b71564d68086bcc23e2b2d');
assert.equal(manifest.sha256,digest);
console.log('Approved Jessica proposal 7 is intact; no speech request made.');
