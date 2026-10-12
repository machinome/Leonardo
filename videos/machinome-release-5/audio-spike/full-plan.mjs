// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Film editorial decisions, separate from both the CAD and the sound renderer.
import {smooth} from './synthesis.mjs';

export function createFilmPlan(movie){
  const shots=movie.chapters.flatMap(c=>c.shots);
  const named=id=>{
    const s=shots.find(s=>s.id===id);
    if(!s)throw Error(`Full soundtrack requires shot ${id}`);
    return s;
  };
  const reveal=named('ancestor'),document=named('document');
  const browser=named('face-reveal'),studio=named('studio');
  const ending=named('wheel-returns');
  const fade=s=>s.transition?.duration??.4;
  const spans=[
    {name:'opening-machine',start:0,end:document.start+fade(document)},
    {name:'browser-machine',start:browser.start,end:studio.end},
    {name:'returning-wheel',start:ending.start,end:ending.end},
  ];
  return {shots,spans,duration:movie.output.durationSeconds,
    active(t){return spans.some(s=>t>=s.start&&t<=s.end);},
    gains(t){
      let waterGain=0,wheelGain=0,sawGain=0;
      if(t>=0&&t<spans[0].end){
        const out=1-smooth((t-document.start)/fade(document));
        waterGain=smooth(t/.18)*out;
        wheelGain=smooth((t-.25)/1.1)*out;
        sawGain=smooth((t-reveal.start)/fade(reveal))*out;
      }else if(t>=browser.start&&t<studio.end){
        // Quieter under the code/browser explanation; fade before scrubbing.
        const gain=.65*smooth((t-browser.start)/fade(browser))*
          smooth((studio.end-t)/.3);
        waterGain=wheelGain=sawGain=gain;
      }else if(t>=ending.start&&t<ending.end){
        // This is the real wheel's arrival, not the technology names moving.
        const gain=smooth((t-ending.start)/1.25)*smooth((ending.end-t)/.5);
        waterGain=wheelGain=gain;
      }
      return {waterGain,wheelGain,sawGain};
    },
  };
}

export function createControls({rows,controlHz,sampleRate,plan}){
  // Missing rows mean intentionally silent editorial spans, not zero poses.
  const held=[];let previous=[0,0,0,0,0];
  for(const row of rows){if(row)previous=row;held.push(previous);}
  const valid=(a,b)=>a&&b&&b[0]>=a[0]&&b[0]-a[0]<.1;
  return {sample(i){
    const t=i/sampleRate,x=t*controlHz,j=Math.min(rows.length-2,Math.floor(x)),u=x-j;
    const a=rows[j],b=rows[j+1],moving=valid(a,b);
    const continuous=Boolean(moving&&(j===0||valid(rows[j-1],a)));
    const mix=k=>moving?a[k]+(b[k]-a[k])*u:held[j][k];
    return {phase:mix(1),phaseRate:moving?(b[1]-a[1])*controlHz:0,
      bladePosition:mix(2),velocity:moving?(b[2]-a[2])*controlHz:0,
      engaged:moving?Math.min(a[4],b[4]):0,continuous,...plan.gains(t)};
  }};
}
