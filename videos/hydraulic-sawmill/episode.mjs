// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import narration from './narration.mjs';
import shots, {cameras, layers} from './shots.mjs';

export default {
  format: 'machinome-video-draft/0.1',
  id: 'leonardo-hydraulic-sawmill',
  title: 'Leonardo’s Sawmill: One Wheel, Two Jobs',
  status: 'rehearsal-source-only',
  learningGoal: 'Explain how one waterwheel coordinates the saw stroke and intermittent timber feed.',
  output: {width: 1920, height: 1080, fps: 30, durationSeconds: 84},
  model: {
    manifest: '../../export/hydraulic_sawmill/manifest.json',
    expectedDurationSeconds: 108,
    timeMode: 'normalized-loop',
    sourceRevision: null,
    readiness: 'Full-timber-pass model is being updated independently; re-export and pin after its validation.',
  },
  credits: {
    project: 'Leonardo da Vinci Gallery',
    creator: 'Vibecoded by Astra',
    copyright: 'Copyright (C) 2026 Luis Henrique Cassis Fagundes',
    license: 'AGPL-3.0-only',
    licenseFile: '../../LICENSE',
    historicalReferences: [
      {title: 'Milan museum hydraulic saw (IGB-37)', url: 'https://www.museoscienza.org/en/collections/objects/hydraulic-saw'},
      {title: 'Leonardo, Codex Atlanticus 1078r', url: 'https://www.leonardodigitale.com/en/browse/Codex-atlanticus/1078-r/'},
    ],
    interpretation: 'Original educational CAD informed by Leonardo’s drawing and the later Milan museum reconstruction; not a measured Renaissance artifact.',
  },
  release: {
    simulationUrl: null,
    sourceUrl: null,
    descriptionTemplate: './description.md',
    publish: false,
  },
  style: {
    background: '#faf7ef', foreground: '#222222', accent: '#237c86',
    fontFamily: 'sans-serif', captions: 'bottom-safe-area',
    safeInsetFraction: 0.08,
    note: 'Landscape rehearsal; a vertical edit needs deliberate reframing, not a center crop.',
  },
  audio: {
    provider: null, model: null, voice: null,
    direction: 'Curious, clear, conversational. Leave space to watch the mechanism. No music in the rehearsal.',
    pronunciation: {Machinome: 'Confirm with the pilot before voice generation', pawl: 'rhymes with ball', AGPL: 'A G P L'},
    timing: 'Generate and measure each beat; align speech and captions, then revise the draft shot timing.',
  },
  cameras, layers, narration, shots,
};
