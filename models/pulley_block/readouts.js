// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Read-only explanatory arithmetic. All CAD, motion, controls and rope
// evaluation belong to the actual machinome export in the iframe.
// The browser smoke compares these labels against independently measured
// Python geometry, including fractional run and timeline positions.
"use strict";
const exhibit = document.getElementById("exhibit");
const outputs = Object.fromEntries(
  ["rise", "pull", "span-a", "span-b", "span-c", "span-d", "rope-total"]
    .map(id => [id, document.getElementById(id)])
);
let previous = "";
function updateLengths() {
  const state = exhibit.contentWindow?.readPulleyState?.();
  if (state) {
    const key = [state.phase, state.run, state.time].join("/");
    if (key !== previous) {
      previous = key;
      const angle = state.phase * Math.PI / 180;
      const blend = state.run;
      const t = state.time;
      const h = 20 * (1 - ((1-blend)*Math.cos(angle) + blend*Math.cos(angle+2*Math.PI*t)));
      const spans = [124-h, 140-h, 140-h, 30+3*h];
      const values = [h, 3*h, ...spans, spans.reduce((a,b) => a+b, 6+58*Math.PI)];
      Object.values(outputs).forEach((output, index) => {
        output.value = values[index].toFixed(1);
      });
    }
  }
  requestAnimationFrame(updateLengths);
}
requestAnimationFrame(updateLengths);
