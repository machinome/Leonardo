// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Whole recorded strokes, driven by measured displacement; no grain-flattened
// saw loop and no continuously oscillating wooden-axle resonators.
import {clamp,smooth} from './synthesis.mjs';
const modulo=(n,m)=>((n%m)+m)%m;
const at=(a,p)=>{
  const x=clamp(p,0,a.length-1),i=Math.floor(x),j=Math.min(i+1,a.length-1);
  return a[i]+(a[j]-a[i])*(x-i);
};
export function createMechanics({sampleRate,duration,controls,assets,recipe}){
  const count=Math.round(sampleRate*duration),stems={saw:new Float32Array(count),wheel:new Float32Array(count)};
  const events=[];let cursor=0,previous=controls.sample(0).phase,creak=null;
  function process(blockSize){
    const end=Math.min(count,cursor+blockSize);
    for(let i=cursor;i<end;i++){
      const c=controls.sample(i),time=i/sampleRate,movement=Math.abs(c.velocity);
      const cutting=c.velocity<0,turn=Math.floor(c.phase/360);
      const progress=clamp((cutting?recipe.topMm-c.bladePosition:c.bladePosition-recipe.bottomMm)/
        (recipe.topMm-recipe.bottomMm));
      const stroke=assets.saw[modulo(turn+(cutting?0:1),assets.saw.length)];
      const envelope=smooth(progress/recipe.turnaroundFraction)*smooth((1-progress)/recipe.turnaroundFraction);
      const gain=Math.pow(clamp(movement/recipe.referenceVelocity),.85)*envelope*c.engaged*c.sawGain*
        (cutting?1:recipe.returnGain);
      // Source advance is proportional to actual travel. Faster travel raises
      // pitch naturally; the cut finishes at the same physical endpoint.
      stems.saw[i]=at(stroke,progress*(stroke.length-1))*gain;
      if(!c.continuous)creak=null;
      const first=Math.floor((previous-recipe.ironOffsetDeg)/recipe.ironEveryDeg)+1;
      const last=Math.floor((c.phase-recipe.ironOffsetDeg)/recipe.ironEveryDeg);
      if(c.continuous&&c.phaseRate>0&&last===first){
        const fraction=(recipe.ironOffsetDeg+last*recipe.ironEveryDeg-previous)/(c.phase-previous);
        const when=(i-1+fraction)/sampleRate;
        const buffer=assets.iron[modulo(last,assets.iron.length)];
        const pitch=clamp(Math.pow(c.phaseRate/recipe.ironReferenceRate,.13),.8,1.3);
        const seconds=Math.min(buffer.length/sampleRate/pitch,recipe.ironEveryDeg/c.phaseRate*.55);
        creak={when,buffer,pitch,seconds};
        if(c.wheelGain>0)events.push({kind:'iron-friction',at:when,phase:recipe.ironOffsetDeg+last*recipe.ironEveryDeg,pitch,seconds});
      }
      previous=c.phase;
      if(creak&&c.phaseRate>0){
        const age=time-creak.when;
        if(age>=creak.seconds)creak=null;
        else if(age>=0){
          const edge=Math.min(.025,creak.seconds*.15);
          const fade=smooth(age/edge)*smooth((creak.seconds-age)/edge);
          stems.wheel[i]=at(creak.buffer,age*sampleRate*creak.pitch)*fade*c.wheelGain;
        }
      }else if(c.phaseRate<=0)creak=null;
    }
    cursor=end;return cursor<count;
  }
  return {process,stems,events};
}
