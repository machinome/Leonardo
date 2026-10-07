// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One analytical phase for the graphic and the real exported waterwheel.
export function wheelAngle(elapsed,{arrival,angularAcceleration}){
  return .5*angularAcceleration*Math.max(0,elapsed-arrival)**2;
}
export function driverX(elapsed,{arrival,entrySpeedFraction}){
  const u=Math.max(0,elapsed)/arrival;
  return 1830-870*(entrySpeedFraction*u+(1-entrySpeedFraction)*u*u);
}
