// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineElement, defineSet, useReport} from 'videomaker/stage';
import {wheelAngle,driverX,driverY,streamPath,approachScale,logoScale} from './ending-motion.mjs';
import './stage.css';
import './_build/fonts.css';

const sets={
  exhibition:['ghost','backdrop','stage','graphic','heading','note','veil'],
  mechanism:['backdrop','plate','ghost','stage','note'], archive:['picture','note'],
  'source-room':['code'],
};
for(const [kind,slots] of Object.entries(sets))
  defineSet({kind,slots,component:()=> <div className={'set '+kind}>
    {slots.map(name=><Slot key={name} name={name} className={'slot-'+name}/>)}</div>});

// StudioSurface lays out the model slot together with the photographed UI.
// Its boxes follow cue progress synchronously; no DOM measurement drives motion.
defineSet({kind:'workbench',slots:['stage','imports','code','surface'],component:()=>
  <div className="set workbench">
    <Slot name="imports" className="slot-imports"/><Slot name="code" className="slot-code"/>
    <Slot name="surface" className="slot-surface"/>
  </div>});
defineSet({kind:'studio',slots:['surface','stage'],component:()=>
  <div className="set studio"><Slot name="surface" className="slot-surface"/></div>});
defineSet({kind:'test-bench',slots:['surface','stage','detail','code','note'],component:()=>
  <div className="set test-bench"><Slot name="surface" className="slot-surface"/>
    <Slot name="code" className="slot-code"/><Slot name="note" className="slot-note"/></div>});

const smooth=x=>{const p=Math.max(0,Math.min(1,x));return p*p*(3-2*p);};
// Zero velocity and acceleration at both ends soften the testing layout move.
const smoother=x=>{const p=Math.max(0,Math.min(1,x));return p*p*p*(10+p*(-15+6*p));};
const elapsed=a=>a?a.progress*(a.until-a.since):0;
function StudioSurface({state}){
  const {geometry:g,screenshot,prompt}=state.props;
  const arriving=state.actions.find(a=>a.action==='arrive');
  const settled=state.actions.some(a=>a.action==='settled');
  const reveal=state.actions.find(a=>a.action==='reveal');
  const p=settled?1:arriving?smooth(arriving.progress):0;
  const departure=state.actions.find(a=>a.action==='depart');
  const departed=state.actions.some(a=>a.action==='departed');
  const leave=departed?1:departure?smoother(departure.progress):0;
  // Clear the photographed UI and full-machine context early; retain the
  // separately drawn timber/blade at full opacity for the rest of its travel.
  const cleared=departed?1:departure?smooth(elapsed(departure)/state.props.departureFade):0;
  const opacity=(arriving||settled?1:reveal?smooth(reveal.progress):0)*(1-cleared);
  const initial={x:.6,y:.05,width:.4,height:.9};
  const final={x:g.model.x/g.viewport.width,y:g.model.y/g.viewport.height,
    width:g.model.width/g.viewport.width,height:g.model.height/g.viewport.height};
  const box=Object.fromEntries(Object.keys(initial).map(k=>[k,initial[k]+(final[k]-initial[k])*p]));
  const testing={x:.64,y:.17,width:.36,height:.83};
  for(const k of Object.keys(box))box[k]+=(testing[k]-box[k])*leave;
  const startScale=initial.height/final.height;
  const scale=startScale+(1-startScale)*p;
  const tx=(initial.x+initial.width/2-(final.x+final.width/2)*startScale)*(1-p);
  const ty=(initial.y+initial.height/2-(final.y+final.height/2)*startScale)*(1-p);
  const focus=state.actions.find(a=>a.action==='focus')?.params.area;
  const typing=state.actions.find(a=>a.action==='type-prompt');
  const text=typing?prompt.slice(0,Math.ceil(prompt.length*typing.progress)):
    state.actions.some(a=>a.action==='prompt-complete')?prompt:'';
  const rect=r=>({left:`${100*r.x/g.viewport.width}%`,top:`${100*r.y/g.viewport.height}%`,
    width:`${100*r.width/g.viewport.width}%`,height:`${100*r.height/g.viewport.height}%`});
  const timeline={x:g.model.x+12,y:g.model.y+g.model.height-42,width:g.model.width-24,height:32};
  const modelClock=state.actions.find(a=>a.action==='model-clock');
  const seconds=modelClock?modelClock.params.start+(modelClock.params.end-modelClock.params.start)*modelClock.progress:0;
  const fraction=seconds/state.props.duration;
  const modelStyle={left:`${box.x*100}%`,top:`${box.y*100}%`,width:`${box.width*100}%`,height:`${box.height*100}%`};
  useReport({progress:p,departure:leave,cleared,opacity,scale,tx,ty,modelBox:box,focus:focus??null,prompt:text,
    modelSeconds:seconds,timelineFraction:fraction});
  return <div className="studio-surface">
    <div style={{position:'absolute',inset:0,background:'#101419',opacity}}/>
    <div className="studio-photograph" style={{opacity,
      transform:`translate(${100*tx}%,${100*ty}%) scale(${scale})`}}>
      <img src={screenshot}/>
    </div>
    {(departure||departed)&&<Slot name="detail" className="studio-detail" style={modelStyle}/>}
    <Slot name="stage" className="studio-model" style={{...modelStyle,opacity:1-cleared}}/>
    <div className="studio-controls" style={{opacity,transform:`translate(${100*tx}%,${100*ty}%) scale(${scale})`}}>
      {modelClock&&<div className="studio-timeline" style={rect(timeline)} data-seconds={seconds}>
        <svg viewBox="0 0 16 16" className="studio-play"><path d="M4 3h3v10H4zm5 0h3v10H9z"/></svg>
        <div className="studio-track"><div className="studio-track-fill" style={{width:`${fraction*100}%`}}/>
          <div className="studio-thumb" style={{left:`${fraction*100}%`}}/></div>
        <span className="studio-time">{seconds.toFixed(1)} / {state.props.duration} {state.props.seconds_unit}</span>
      </div>}
      {focus&&<div className="studio-focus" data-focus={focus} style={rect(focus==='timeline'?timeline:g[focus])}/>}
      {text&&<div className="studio-prompt" style={rect(g.input)}>{text}<span className="studio-caret"/></div>}
    </div>
  </div>;
}
function syntax(line){
  return line.split(/("[^"\n]*"|'[^'\n]*'|\b(?:class|from|import|def|return)\b)/g)
    .map((s,i)=><span key={i} className={/^["']/.test(s)?'string':/^(class|from|import|def|return)$/.test(s)?'keyword':''}>{s}</span>);
}
function Listing({state}){
  const token=state.actions.find(a=>a.action==='focus')?.params.token;
  const blinks=state.actions.filter(a=>a.action==='blink').map(a=>a.params);
  const all=state.actions.find(a=>a.action==='blink-all')?.params.token;
  const typing=state.actions.find(a=>a.action==='write');
  const reveal=state.actions.find(a=>a.action==='complete');
  const progress=typing?.progress??(reveal||!state.props.initiallyEmpty?1:0);
  const shown=state.props.code.slice(0,Math.ceil(state.props.code.length*progress));
  const concealed=state.actions.some(a=>a.action==='conceal');
  useReport({sourceSha256:state.props.digest,text:shown,concealed,blink:blinks[0]??null,blinks,all:all??null});
  const renderLine=(line,i)=>{
    if(all){
      const matches=[...line.matchAll(/[A-Za-z_][A-Za-z_0-9]*/g)].filter(m=>m[0]===all);
      let end=0;const pieces=[];
      for(const match of matches){
        pieces.push(<React.Fragment key={match.index}>{syntax(line.slice(end,match.index))}
          <mark className="blink-token">{match[0]}</mark></React.Fragment>);
        end=match.index+match[0].length;
      }
      return <>{pieces}{syntax(line.slice(end))}</>;
    }
    const blink=blinks.find(mark=>mark.line===state.props.numbers[i]);
    if(!blink)return syntax(line);
    let at=-1;
    for(let n=0;n<=blink.occurrence;n++)at=line.indexOf(blink.token,at+1);
    if(at<0)throw Error(`Missing highlighted token ${blink.token} at ${blink.line}`);
    return <>{syntax(line.slice(0,at))}<mark className="blink-token">{line.slice(at,at+blink.token.length)}</mark>{syntax(line.slice(at+blink.token.length))}</>;
  };
  return concealed?null:<div className="listing" data-source-sha256={state.props.digest}>
    <div className="listing-file">{state.props.file}</div>
    <pre>{shown.split('\n').map((line,i)=><div key={i} className={token&&line.includes(token)?'lit-line':''}>
      <span className="line-number">{state.props.numbers[i]}</span>{renderLine(line,i)}</div>)}</pre>
  </div>;
}
function Signature({state}){
  const p=state.actions.find(a=>a.action==='enter');
  const opacity=p?smooth(p.progress):1;
  const approach=state.actions.find(a=>a.action==='approach');
  const waiting=state.actions.some(a=>a.action==='wait');
  const scale=waiting?0:approach?logoScale(approach.progress):1;
  const link=state.actions.find(a=>a.action==='link');
  const linkOpacity=link?smooth(link.progress):state.actions.some(a=>a.action==='linked')?1:0;
  useReport({opacity,scale,linkOpacity});
  return <div className={'signature'+(state.props.compact?' compact':'')} style={{opacity}}>
    <div className="logo-approach" style={{position:'absolute',inset:0,
      transform:`scale(${scale})`,transformOrigin:'50% 50%'}}>
      <div className="wordmark" dangerouslySetInnerHTML={{__html:state.props.svg}}/>
    </div>
    {state.props.tagline&&<div className="tagline">{state.props.tagline}</div>}
    {state.props.url&&<div className="repository-url" style={{opacity:linkOpacity}}>{state.props.url}</div>}
    {state.props.license&&<div className="repository-license" style={{opacity:linkOpacity}}>{state.props.license}</div>}
    {state.props.question&&<div className="question" style={{opacity:p?smooth(elapsed(p)/.65):0}}>{state.props.question}</div>}
  </div>;
}
function Curtain({state}){
  const p=state.actions.find(a=>a.action==='darken');
  // Be completely dark for the last two frames before the logo starts.
  const opacity=p?smooth(elapsed(p)/.4):0;
  useReport({opacity});
  return <div className="wheel-exit" style={{position:'absolute',inset:0,background:'#101419',opacity}}/>;
}
function Constellation({state}){
  const {names,mark,title,drivers,stagger,streamDuration,streamDelay=0,timeOffset=0,fadeDuration=0}=state.props;
  const reveal=name=>state.actions.find(a=>a.action==='reveal'&&a.params.name===name);
  const technologyOpacity=name=>{
    const cue=reveal(name);
    return timeOffset?1:cue?smooth(elapsed(cue)/.35):0;
  };
  const drive=state.actions.find(a=>a.action==='drive');
  const driverElapsed=elapsed(drive)+timeOffset;
  const streamElapsed=driverElapsed-streamDelay;
  const rotation=wheelAngle(driverElapsed,state.props);
  const approach=state.actions.find(a=>a.action==='approach');
  const scale=approach?approachScale(approach.progress):1;
  const positions=drivers.map((name,i)=>{
    const x=driverX(streamElapsed-i*stagger,state.props);
    return {name,x,y:driverY(x)};
  });
  const opacity=fadeDuration?1-smooth(elapsed(drive)/fadeDuration):1;
  const streamOpacity=drive&&streamElapsed>=0?1-smooth((driverElapsed-streamDuration+.15)/.15):0;
  useReport({rotation,driverElapsed,streamElapsed,scale,opacity,streamOpacity,visible:names.filter(n=>reveal(n)),
    drivers:positions});
  return <div className="constellation" style={{transform:`scale(${scale})`,transformOrigin:'50% 50%'}}>
    <div style={{position:'absolute',inset:0,background:'#101419',opacity}}/>
    <div className="graph-title" style={{opacity}}>{title}</div>
    <svg viewBox="0 0 1920 1080" className="spokes">
      <path className="stream-path" d={streamPath} fill="none" stroke="#79a7b9" strokeWidth="2" opacity={.45*streamOpacity}/>
      <g opacity={opacity} transform={`rotate(${rotation} 960 540)`}>
        <circle cx="960" cy="540" r="275" fill="none" stroke="#8c9ba8" strokeWidth="1" opacity={.22*technologyOpacity(names[0])}/>
        {names.map((name,i)=>{
          const a=-Math.PI/2+i*Math.PI/4;
          const opacity=technologyOpacity(name);
          const x=960+Math.cos(a)*275,y=540+Math.sin(a)*275;
          return <g key={name} opacity={opacity}>
            <line x1={960+Math.cos(a)*110} y1={540+Math.sin(a)*110} x2={x} y2={y} stroke="#e9b778" strokeWidth="2"/>
            <circle cx={x} cy={y} r="5" fill="#e9b778"/>
            <g transform={`translate(${960+Math.cos(a)*370} ${540+Math.sin(a)*340}) rotate(${-rotation})`}>
              <text textAnchor="middle" dominantBaseline="middle" className="tech-label">{name}</text>
            </g>
          </g>;
        })}
      </g>
      {drive&&positions.map(({name,x,y},i)=><text key={name} className="incoming" textAnchor="middle"
        opacity={streamElapsed>=i*stagger?streamOpacity:0} x={x} y={y}>{name}</text>)}
    </svg>
    <div className="hub-mark" style={{opacity}} dangerouslySetInnerHTML={{__html:mark}}/>
  </div>;
}
defineElement({kind:'listing',component:Listing});
defineElement({kind:'studio-surface',component:StudioSurface});
defineElement({kind:'signature',component:Signature});
defineElement({kind:'curtain',component:Curtain});
defineElement({kind:'shade',component:()=> <div style={{position:'absolute',inset:0,background:'#101419'}}/>});
defineElement({kind:'constellation',component:Constellation});
