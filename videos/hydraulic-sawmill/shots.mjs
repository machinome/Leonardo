// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Draft camera coordinates: existing exhibit presets plus an unreviewed rope view.
const camera = (position, target) => ({position, target, up: [0, 0, 1], fov: 37});
export const cameras = {
  whole: camera([940, -1260, 940], [0, -20, 290]),
  drive: camera([330, -630, 300], [0, -135, 145]),
  saw: camera([335, -470, 505], [0, 0, 445]),
  feed: camera([180, 720, 480], [-105, 115, 337]),
  rope: camera([580, 640, 620], [75, 98, 350]),
};

export const layers = {
  structure: [['Frame and guides', 'Timber stand and guides']],
  water: [['Water drive', 'Water channel'], ['Water drive', 'Water surface']],
};

const model = '../../models/hydraulic_sawmill/';
const evidence = [model + 'docs/reconstruction.md', model + 'model.py'];
const overlay = (from, to, text, position = 'top') => ({from, to, text, position});
export default [
  {
    id: 'hook', start: 0, end: 8, simulation: {from: 8, to: 16},
    camera: [{at: 0, preset: 'saw'}], hiddenLayers: [], narrationId: 'hook',
    overlays: [overlay(0, 8, 'Who moves the log?')], evidence,
  },
  {
    id: 'introduce', start: 8, end: 16, simulation: {from: 16, to: 24},
    camera: [{at: 0, preset: 'saw'}, {at: 3, preset: 'whole'}],
    hiddenLayers: [], narrationId: 'introduce',
    overlays: [overlay(0, 8, 'Leonardo’s hydraulic sawmill'),
      overlay(0, 8, 'Educational reconstruction · Machinome', 'lower-third')], evidence,
  },
  {
    id: 'drive', start: 16, end: 28, simulation: {from: 24, to: 32},
    camera: [{at: 0, preset: 'drive'}, {at: 5, preset: 'drive'}, {at: 9, preset: 'saw'}],
    hiddenLayers: ['structure'], narrationId: 'drive',
    overlays: [overlay(0, 5, 'Water beneath the wheel'),
      overlay(5, 12, 'Rotation → reciprocation')], evidence,
  },
  {
    id: 'hold', start: 28, end: 36, simulation: {from: 32, to: 36},
    camera: [{at: 0, preset: 'saw'}], hiddenLayers: ['structure'], narrationId: 'hold',
    // Four model seconds per turn: first half cuts, second half feeds.
    overlays: [overlay(0, 4, 'DOWNSTROKE · CARRIAGE HOLDS'),
      overlay(4, 8, 'RETURN STROKE · CARRIAGE ADVANCES')],
    evidence: [...evidence, model + 'layout.py', model + 'kinematics.py'],
  },
  {
    id: 'ratchet', start: 36, end: 50, simulation: {from: 36, to: 44},
    camera: [{at: 0, preset: 'feed'}], hiddenLayers: ['structure', 'water'],
    narrationId: 'ratchet',
    overlays: [overlay(0, 7, 'Rocking lever → driving pawl'),
      overlay(7, 14, 'Ratchet + holding pawl')], evidence,
  },
  {
    id: 'rope', start: 50, end: 60, simulation: {from: 44, to: 52},
    camera: [{at: 0, preset: 'feed'}, {at: 4, preset: 'rope'}],
    hiddenLayers: ['structure', 'water'], narrationId: 'rope',
    overlays: [overlay(0, 10, 'Drum → rope → return pulley → carriage')], evidence,
  },
  {
    id: 'rhythm', start: 60, end: 68, simulation: {from: 52, to: 60},
    camera: [{at: 0, preset: 'saw'}], hiddenLayers: ['structure'], narrationId: 'rhythm',
    overlays: [overlay(0, 2, 'CUT'), overlay(2, 4, 'ADVANCE'),
      overlay(4, 6, 'CUT'), overlay(6, 8, 'ADVANCE'),
      overlay(0, 8, 'Cut opening visualized · cutting forces not simulated', 'lower-third')],
    evidence: [...evidence, model + 'openspec/changes/full-timber-pass/design.md'],
  },
  {
    id: 'closing', start: 68, end: 84, simulation: {from: 60, to: 76},
    camera: [{at: 0, preset: 'whole'}], hiddenLayers: [], narrationId: 'closing',
    overlays: [overlay(0, 16, 'Vibecoded by Astra · Made with Machinome'),
      overlay(0, 16, 'Original CAD and code: AGPL-3.0-only\n© 2026 Luis Henrique Cassis Fagundes\nExplore the simulation: description / channel profile', 'lower-third')],
    evidence: ['../../README.md', '../../NOTICE', '../../gallery.toml'],
  },
];
