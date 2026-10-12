// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One native recorded scrape per actual half-stroke. No stretching, looping,
// grain synthesis, resampling or oscillator. Film timing never changes timbre.
import {clamp,smooth} from './synthesis.mjs';
const modulo=(n,m)=>((n%m)+m)%m;
export function createManualSaw({sampleRate,duration,controls,strokes,recipe}){
  const count=Math.round(sampleRate*duration),audio=new Float32Array(count),events=[];
  let cursor=0,voice=null,played=null;
  function process(blockSize){
    const end=Math.min(count,cursor+blockSize);
    for(let i=cursor;i<end;i++){
      const c=controls.sample(i),cutting=c.velocity<0,direction=cutting?'cut':'return';
      const turn=Math.floor(c.phase/360),key=`${turn}:${direction}`;
      const progress=clamp((cutting?recipe.topMm-c.bladePosition:c.bladePosition-recipe.bottomMm)/
        (recipe.topMm-recipe.bottomMm));
      if(!c.continuous){voice=null;played=null;continue;}
      if(!c.engaged||Math.abs(c.velocity)<.001||c.sawGain<=0){voice=null;continue;}
      if(voice&&voice.key!==key)voice=null;
      if(played!==key&&progress>=recipe.startProgress&&progress<.94){
        const variant=modulo(turn+(cutting?0:1),strokes.length),source=strokes[variant];
        const gain=cutting?1:recipe.returnGain;
        // At unusually fast motion the reversal cancels the tail; it never
        // accelerates the recording into a whine or repeats it into a drone.
        voice={key,start:i,source,gain};played=key;
        events.push({at:i/sampleRate,startSample:i,kind:direction,variant,gain,
          sourceSamples:source.length,playbackRate:1,bladePosition:c.bladePosition});
      }
      if(voice){
        const age=i-voice.start;
        if(age>=voice.source.length)voice=null;
        else{
          const edge=recipe.edgeSeconds*sampleRate;
          const fade=smooth(age/edge)*smooth((voice.source.length-1-age)/edge)*smooth((1-progress)/.035);
          audio[i]=voice.source[age]*voice.gain*fade*c.sawGain;
        }
      }
    }
    cursor=end;return cursor<count;
  }
  return {process,audio,events};
}
