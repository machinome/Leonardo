// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
import assert from 'node:assert/strict';
import {spokenAlignment, resolveBeats, deliveryTags} from './speech.mjs';
const make = text => ({characters: Array.from(text),
  character_start_times_seconds: Array.from(text, (_, i) => i / 10),
  character_end_times_seconds: Array.from(text, (_, i) => (i + 1) / 10)});
const text = 'código aberto... [long pause]\n\nA roda. VOCÊ';
const input = make(text), before = structuredClone(input);
const output = spokenAlignment(input);
assert.deepEqual(input, before);
assert.equal(output.characters.join(''), text.replace('[long pause]', '').replace(/\s+/g, ' '));
const rawAt = Array.from(text.slice(0, text.indexOf('A roda'))).length;
const cue = resolveBeats(output, [{id: 'return', phrase: 'A roda'}], 20)[0];
assert.equal(cue.start, input.character_start_times_seconds[rawAt]);
assert.equal(cue.end, input.character_end_times_seconds[rawAt + 5]);
assert.deepEqual(spokenAlignment(make('Português sem instrução')), make('Português sem instrução'));
assert.equal(spokenAlignment(make('Não remover [surpresa]')).characters.join(''), 'Não remover [surpresa]');
assert.equal(spokenAlignment(null), null);
for (const tag of deliveryTags) {
  const directed = make(`[${tag}] A roda [${tag}] gira. `);
  const clean = spokenAlignment(directed);
  assert.equal(clean.characters.join(''), 'A roda gira.');
  let position = 0;
  for (let i = 0; i < clean.characters.length; i++) {
    if (!/[\p{L}\p{N}]/u.test(clean.characters[i])) continue;
    while (directed.character_start_times_seconds[position] < clean.character_start_times_seconds[i]) position++;
    assert.equal(clean.characters[i], directed.characters[position]);
    assert.equal(clean.character_end_times_seconds[i], directed.character_end_times_seconds[position]);
  }
}
console.log('Delivery-tag alignment tests pass: unchanged word times, Unicode, no input mutation, unknown tags retained.');
