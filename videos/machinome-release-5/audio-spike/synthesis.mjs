// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// No file access, browser, movie, model imports, or graphics-frame clock.
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export const smooth=x=>{const p=clamp(x);return p*p*(3-2*p);};
export function random(seed){let n=seed>>>0;return()=>{n^=n<<13;n^=n>>>17;n^=n<<5;return(n>>>0)/4294967296;};}
export function rms(a){let sum=0;for(const v of a)sum+=v*v;return Math.sqrt(sum/a.length);}
export function normalized(a,target){const gain=target/Math.max(1e-8,rms(a));return Float32Array.from(a,v=>v*gain);}
export function sample(a,p){const q=((p%a.length)+a.length)%a.length,i=Math.floor(q);return a[i]+(a[(i+1)%a.length]-a[i])*(q-i);}

// Flatten a recording's original hand-stroke rhythm into reusable texture.
// Overlapped grains keep texture pitch independent from the new event cadence.
export function texture(source,sampleRate,seconds,seed){
  const rng=random(seed),n=Math.round(seconds*sampleRate),out=new Float32Array(n);
  const weight=new Float32Array(n),size=Math.round(.065*sampleRate),hop=Math.round(size/4);
  const candidates=[];
  for(let p=0;p+size<source.length;p+=size){
    const r=rms(source.subarray(p,p+size));if(r>.006)candidates.push([p,r]);
  }
  if(!candidates.length)throw Error('No active texture grains');
  for(let at=-size;at<n;at+=hop){
    const [start,level]=candidates[Math.floor(rng()*candidates.length)];
    const gain=Math.min(6,.15/level);
    for(let j=0;j<size;j++){
      const i=at+j;if(i<0||i>=n)continue;
      const w=.5-.5*Math.cos(2*Math.PI*j/(size-1));
      out[i]+=source[start+j]*gain*w;weight[i]+=w;
    }
  }
  for(let i=0;i<n;i++)out[i]/=Math.max(weight[i],1e-8);
  // Make a periodic texture with an equal-gain overlap at its join.
  const blend=Math.round(.15*sampleRate),loop=out.slice(0,n-blend);
  for(let i=0;i<blend;i++){
    const p=i/blend;loop[i]=out[n-blend+i]*(1-p)+out[i]*p;
  }
  return normalized(loop,.15);
}

// controls has a sample(i) returning continuous phase, blade velocity,
// engagement and explicit film-mix gains. A renderer can feed other controls.
export function createRenderer({sampleRate,duration,controls,assets,recipe}){
  const count=Math.round(sampleRate*duration);
  const stems=Object.fromEntries(['water','paddles','wheel','saw'].map(k=>[k,new Float32Array(count)]));
  const rng=random(recipe.seed);let cursor=0,sawCursor=0,waterCursor=0,low=0;
  const events=[],splashes=[];let previous=controls.sample(0).phase;
  const telemetry={pitchMin:Infinity,pitchMax:0,waterPlaybackRate:1,events};
  function process(blockSize){
    const end=Math.min(count,cursor+blockSize);
    for(let i=cursor;i<end;i++){
      const c=controls.sample(i),t=i/sampleRate;
      const movement=Math.abs(c.velocity),motion=clamp(movement/recipe.saw.referenceVelocityMmPerSecond);
      const pitch=clamp(Math.pow(Math.max(.01,movement)/recipe.saw.referenceVelocityMmPerSecond,.32),...recipe.saw.pitchRange);
      telemetry.pitchMin=Math.min(telemetry.pitchMin,pitch);telemetry.pitchMax=Math.max(telemetry.pitchMax,pitch);
      const cutting=c.velocity<0,active=c.engaged*(cutting?1:recipe.saw.returnGain);
      stems.saw[i]=sample(assets.saw,sawCursor)*Math.pow(motion,.62)*active*c.sawGain;
      sawCursor+=pitch;
      stems.water[i]=sample(assets.water,waterCursor++)*c.waterGain*recipe.water.flowIntensity;
      // Declare discontinuities: do not emit a backlog across a seek or reset.
      const pitchStep=360/recipe.paddles.count,offset=recipe.paddles.phaseOffsetDeg;
      const first=Math.floor((previous-offset)/pitchStep)+1,last=Math.floor((c.phase-offset)/pitchStep);
      if(c.continuous&&last>=first&&last-first<32){
        for(let k=first;k<=last;k++){
          const frac=(offset+k*pitchStep-previous)/(c.phase-previous);
          const at=(i-1+frac)/sampleRate;
          events.push({kind:'paddle',at,phase:offset+k*pitchStep,pitch:1});
          splashes.push({at,offset:Math.floor(rng()*assets.water.length),gain:.85+.3*rng()});
        }
      }
      previous=c.phase;
      let splash=0;
      for(let j=splashes.length-1;j>=0;j--){
        const e=splashes[j],age=t-e.at;
        if(age>.6){splashes.splice(j,1);continue;}
        if(age>=0)splash+=sample(assets.water,e.offset+age*sampleRate)*
          (1-Math.exp(-age/.006))*Math.exp(-age/recipe.paddles.decaySeconds)*e.gain;
      }
      stems.paddles[i]=splash*c.waterGain;
      const noise=rng()*2-1;low+=.035*(noise-low);
      const cycle=c.phase*Math.PI/180;
      const creak=(.35+.65*Math.pow(Math.abs(Math.sin(cycle+.2)),3));
      let resonant=0;
      for(const f of recipe.wheel.resonancesHz)
        resonant+=Math.sin(2*Math.PI*f*t+.8*Math.sin(cycle))*low;
      stems.wheel[i]=(resonant+low*.8)*creak*c.wheelGain*(c.phaseRate>0?1:0);
    }
    cursor=end;return cursor<count;
  }
  return {process,stems,telemetry};
}
