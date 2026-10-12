// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One analytical phase for the graphic and the real exported waterwheel.
export function wheelAngle(elapsed,{spinDelay,angularAcceleration}){
  return .5*angularAcceleration*Math.max(0,elapsed-spinDelay)**2;
}
// Each label gets its own stationary reading beat, then launches from rest.
export function driverX(elapsed,{arrival,entrySpeedFraction,hold=0}){
  const u=Math.max(0,elapsed-hold)/(arrival-hold);
  return 1830-870*(entrySpeedFraction*u+(1-entrySpeedFraction)*u*u);
}
// Read at right/mid-height, then descend smoothly to the wheel's lower edge.
// Keep the approved horizontal clock: only the stream's height changes.
export function driverY(x){
  const p=Math.max(0,Math.min(1,(1830-x)/870));
  return 540+280*p*p*(3-2*p);
}
// The cubic's equally spaced x controls give the same smoothstep as driverY,
// with a 15px gap beneath the label baseline and level entry/exit tangents.
export const streamPath='M1920 555 H1830 C1540 555 1250 835 960 835 H0';
// Ease out: advance promptly from the distance, then settle on the first name.
export function approachScale(progress){
  const p=Math.max(0,Math.min(1,progress));
  return .18+.82*(1-(1-p)**3);
}
// Project the closing mark from the wheel-centre vanishing point, then settle.
// Its opacity stays constant: only its apparent distance changes.
export function logoScale(progress){
  const p=Math.max(0,Math.min(1,progress));
  return .002+.998*p*p*(3-2*p);
}
