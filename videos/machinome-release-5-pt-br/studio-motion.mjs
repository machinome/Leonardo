// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Film edit only: real exported poses, never a second mechanical simulation.
import assert from 'node:assert/strict';

export const smooth=x=>{const p=Math.max(0,Math.min(1,x));return p*p*(3-2*p);};
export function shortCamera(from,to,progress){
  const p=smooth(progress),lerp=(a,b)=>a+(b-a)*p;
  const offset=c=>c.position.map((v,i)=>v-c.target[i]);
  const a=offset(from),b=offset(to);
  const azA=Math.atan2(a[1],a[0]),azB=Math.atan2(b[1],b[0]);
  const turn=Math.atan2(Math.sin(azB-azA),Math.cos(azB-azA));
  const az=azA+turn*p;
  const radius=lerp(Math.hypot(a[0],a[1]),Math.hypot(b[0],b[1]));
  const target=from.target.map((v,i)=>lerp(v,to.target[i]));
  return {position:[target[0]+radius*Math.cos(az),target[1]+radius*Math.sin(az),
    target[2]+lerp(a[2],b[2])],target,up:from.up,fov:from.fov};
}

export function finishStudio(doc,measured,clock){
  const chapter=doc.chapters[0],timed=measured.chapters[0];
  const studio=chapter.shots.find(s=>s.id==='studio');
  const timing=timed.shots.find(s=>s.id==='studio');
  const fps=doc.output.fps,grid=t=>Math.round(t*fps)/fps;
  const actionCue=(shot,action)=>shot.cues.find(c=>c.actions.some(a=>a.action===action));
  const move=actionCue(studio,'move'),moveTiming=actionCue(timing,'move');
  const cameraStart=grid(moveTiming.at),cameraEnd=grid(moveTiming.actions[0].until);
  studio.cues=studio.cues.filter(c=>c!==move);
  const count=Math.round((cameraEnd-cameraStart)*fps);
  assert.ok(count>=2,'The short turn needs at least two frames.');
  for(let i=1;i<=count;i++){
    const name=`studio-angle-${String(i).padStart(3,'0')}`;
    doc.cameras[name]=i===count?structuredClone(doc.cameras.test):shortCamera(doc.cameras.source,doc.cameras.test,i/count);
    studio.cues.push({at:cameraStart+(i-1)/fps,actions:[
      {element:'mill',action:'move',camera:name,ease:'linear',until:cameraStart+i/fps},
    ]});
  }
  const slider=timing.cues.find(c=>c.actions.some(a=>a.action==='focus'&&a.params.area==='timeline'));
  const rewindStart=grid(slider.at+.3),rewindEnd=grid(slider.until);
  assert.ok(cameraEnd<=slider.at&&rewindEnd>rewindStart+.5,
    'Highlight model and finish the angle change before highlighting/dragging the slider.');
  const originalDuration=timing.end-timing.start;
  const rewindFrom=clock(timing.start+rewindStart);
  const clockAction=(start,end)=>({element:'studio-ui',action:'model-clock',params:{start,end}});
  // The timeline overlays the photographed viewer and follows its exact clock,
  // even during the initial source-to-browser layout move.
  const face=chapter.shots.find(s=>s.id==='face-reveal');
  face.cues.push({at:0,until:face.until,actions:[clockAction(face.model.from,face.model.to)]});
  studio.model={from:clock(timing.start),to:rewindFrom};
  // Resolve all pre-scrub cues before shortening this shot; anchors later than
  // the boundary would otherwise extend beyond their shot.
  studio.cues=studio.cues.map(c=>{
    if(c.actions.some(a=>a.action==='move'))return c;
    const original=timing.cues.find(t=>JSON.stringify(t.actions.map(a=>[a.element,a.action,a.params]))===
      JSON.stringify(c.actions.map(a=>[a.element,a.action,a.params])));
    if(!original)return c; // sampled camera microsegment already numeric
    return {...c,at:original.at,...(original.until!==undefined?{until:Math.min(original.until,rewindStart)}:{})};
  }).filter(c=>c.at<rewindStart);
  studio.until=rewindStart;
  studio.cues.push({at:0,until:rewindStart,actions:[clockAction(studio.model.from,rewindFrom)]});
  // The public movie contract forbids decreasing time *inside* a shot.
  // A scrub is an edit across real poses: one held-pose shot per film frame,
  // same set, same view identity and same held camera. No renderer patch,
  // autonomous viewer clock, audio edit or geometry rewrite is involved.
  const slices=[],frames=Math.round((originalDuration-rewindStart)*fps);
  assert.ok(frames>0);
  for(let i=0;i<frames;i++){
    const at=rewindStart+i/fps;
    // Absolute spoken anchors avoid cumulative floating-point drift from
    // adding 1/24 repeatedly (which can otherwise leave a cue one frame old).
    const until={spoken:'O Machinome também oferece',
      plus:grid(timing.start+rewindStart+(i+1)/fps)-timing.end};
    const seconds=rewindFrom*(1-smooth((at-rewindStart)/(rewindEnd-rewindStart)));
    const actions=[{element:'studio-ui',action:'settled',params:{}},
      {element:'studio-ui',action:'prompt-complete',params:{}},clockAction(seconds,seconds)];
    if(at<slider.until)actions.push({element:'studio-ui',action:'focus',params:{area:'timeline'}});
    slices.push({id:`studio-rewind-${String(i).padStart(3,'0')}`,set:'studio',
      places:structuredClone(studio.places),until,model:{from:seconds,to:seconds},
      direction:'Timeline scrub: one real exported model pose at the film frame; no pointer.',
      cues:[{at:0,until,actions}]});
  }
  const index=chapter.shots.indexOf(studio);chapter.shots.splice(index+1,0,...slices);
  const testing=chapter.shots.find(s=>s.id==='testing');
  const testingTiming=timed.shots.find(s=>s.id==='testing');
  const departure=actionCue(testing,'depart'),typing=actionCue(testingTiming,'write');
  const departureEnd=timing.end+actionCue(testingTiming,'depart').until;
  const typingStart=timing.end+typing.at;
  assert.ok(typingStart>timing.end+chapter.elements['studio-ui'].props.departureFade&&
    typingStart<departureEnd&&departureEnd-typingStart<=1,
    'Source typing starts after Studio clears, during the final second of model travel.');
  testing.cues.push({at:0,until:departure.until,actions:[clockAction(0,0)]});
  return {cameraStart:timing.start+cameraStart,cameraEnd:timing.start+cameraEnd,
    sliderHighlight:timing.start+slider.at,rewindStart:timing.start+rewindStart,
    rewindEnd:timing.start+rewindEnd,rewindFrom,frames,testingStart:timing.end,
    departureEnd,typingStart,typingEnd:timing.end+typing.until};
}
