// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {spokenAlignment, resolveBeats} from './speech.mjs';
const make = text => ({characters: Array.from(text),
  character_start_times_seconds: Array.from(text, (_, i) => i / 10),
  character_end_times_seconds: Array.from(text, (_, i) => (i + 1) / 10)});
const text = 'código aberto... [long pause]\n\nA roda. VOCÊ';
const input = make(text), before = structuredClone(input);
const output = spokenAlignment(input);
assert.deepEqual(input, before);
assert.equal(output.characters.join(''), text.replace('[long pause]', ''));
const rawAt = Array.from(text.slice(0, text.indexOf('A roda'))).length;
const cue = resolveBeats(output, [{id: 'return', phrase: 'A roda'}], 20)[0];
assert.equal(cue.start, input.character_start_times_seconds[rawAt]);
assert.equal(cue.end, input.character_end_times_seconds[rawAt + 5]);
assert.deepEqual(spokenAlignment(make('Português sem instrução')), make('Português sem instrução'));
assert.equal(spokenAlignment(make('Não remover [surpresa]')).characters.join(''), 'Não remover [surpresa]');
assert.equal(spokenAlignment(null), null);
console.log('Delivery-tag alignment tests pass: unchanged word times, Unicode, no input mutation, unknown tags retained.');
