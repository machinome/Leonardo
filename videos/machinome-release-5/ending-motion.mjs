// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One analytical phase for the graphic and the real exported waterwheel.
export function wheelAngle(elapsed,{spinDelay,angularAcceleration}){
  return .5*angularAcceleration*Math.max(0,elapsed-spinDelay)**2;
}
export function driverX(elapsed,{arrival,entrySpeedFraction}){
  const u=Math.max(0,elapsed)/arrival;
  return 1830-870*(entrySpeedFraction*u+(1-entrySpeedFraction)*u*u);
}
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
