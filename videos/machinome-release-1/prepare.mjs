// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Embed the pinned local fonts; no network resources enter the film stage.
import {readFile,writeFile,mkdir} from 'node:fs/promises';
const base=new URL('./',import.meta.url);
await mkdir(new URL('_build/',base),{recursive:true});
let css='/* Generated from the fonts and OFL notices in ../assets/. */\n';
for(const [family,file,weight] of [
  ['Space Grotesk','SpaceGrotesk.ttf','300 700'],
  ['IBM Plex Mono','IBMPlexMono-Regular.ttf','400'],
]) {
  const font=await readFile(new URL('assets/'+file,base));
  css+=`@font-face{font-family:'${family}';src:url(data:font/ttf;base64,${font.toString('base64')}) format('truetype');font-weight:${weight};font-style:normal;}\n`;
}
await writeFile(new URL('_build/fonts.css',base),css);
console.log('Prepared local film fonts.');
