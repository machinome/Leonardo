// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import {readFile, writeFile, mkdir} from 'node:fs/promises';
const base = new URL('./', import.meta.url);
await mkdir(new URL('_build/', base), {recursive: true});
const font = await readFile(new URL('../machinome-release-1/assets/SpaceGrotesk.ttf', base));
await writeFile(new URL('_build/fonts.css', base),
  `@font-face{font-family:'Space Grotesk';src:url(data:font/ttf;base64,${font.toString('base64')}) format('truetype');font-weight:300 700;font-style:normal}\n`);
console.log('Prepared local Space Grotesk.');
