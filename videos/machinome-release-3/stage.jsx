// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineElement, defineSet, useReport} from 'videomaker/stage';
import {wheelAngle,driverX} from './ending-motion.mjs';
import './stage.css';
import './_build/fonts.css';

const sets={
  exhibition:['ghost','stage','graphic','heading','note'],
  mechanism:['ghost','stage','note'], archive:['picture','note'],
  workbench:['stage','imports','code'], 'source-room':['code'],
  'test-bench':['stage','code','note'],
};
for(const [kind,slots] of Object.entries(sets))
  defineSet({kind,slots,component:()=> <div className={'set '+kind}>
    {slots.map(name=><Slot key={name} name={name} className={'slot-'+name}/>)}</div>});

const smooth=x=>{const p=Math.max(0,Math.min(1,x));return p*p*(3-2*p);};
const elapsed=a=>a?a.progress*(a.until-a.since):0;
function syntax(line){
  return line.split(/("[^"\n]*"|'[^'\n]*'|\b(?:class|from|import|def|return)\b)/g)
    .map((s,i)=><span key={i} className={/^["']/.test(s)?'string':/^(class|from|import|def|return)$/.test(s)?'keyword':''}>{s}</span>);
}
function Listing({state}){
  const token=state.actions.find(a=>a.action==='focus')?.params.token;
  const blink=state.actions.find(a=>a.action==='blink')?.params;
  const typing=state.actions.find(a=>a.action==='write');
  // Before its typing cue, this panel is empty; other listings start complete.
  const progress=typing?.progress??(state.props.file.endsWith('/model.py')&&
    !state.actions.some(a=>a.action==='blink')?null:1);
  // The persistent typed amount is supplied as an explicit cue by finish.mjs.
  const reveal=state.actions.find(a=>a.action==='complete');
  const shown=progress===null?(reveal?state.props.code:''):
    state.props.code.slice(0,Math.ceil(state.props.code.length*progress));
  useReport({sourceSha256:state.props.digest,text:shown,blink:blink??null});
  const renderLine=(line,i)=>{
    if(!blink||state.props.numbers[i]!==blink.line)return syntax(line);
    let at=-1;
    for(let n=0;n<=blink.occurrence;n++)at=line.indexOf(blink.token,at+1);
    if(at<0)throw Error(`Missing highlighted token ${blink.token} at ${blink.line}`);
    return <>{syntax(line.slice(0,at))}<mark className="blink-token">{line.slice(at,at+blink.token.length)}</mark>{syntax(line.slice(at+blink.token.length))}</>;
  };
  return <div className="listing" data-source-sha256={state.props.digest}>
    <div className="listing-file">{state.props.file}</div>
    <pre>{shown.split('\n').map((line,i)=><div key={i} className={token&&line.includes(token)?'lit-line':''}>
      <span className="line-number">{state.props.numbers[i]}</span>{renderLine(line,i)}</div>)}</pre>
  </div>;
}
function Signature({state}){
  const p=state.actions.find(a=>a.action==='enter');
  return <div className={'signature'+(state.props.compact?' compact':'')}>
    <div className="wordmark" dangerouslySetInnerHTML={{__html:state.props.svg}}/>
    <div className="tagline">{state.props.tagline}</div>
    <div className="question" style={{opacity:p?smooth(elapsed(p)/.65):0}}>{state.props.question}</div>
  </div>;
}
function Constellation({state}){
  const {names,mark,title,driver,timeOffset=0,fadeDuration=0}=state.props;
  const reveal=name=>state.actions.find(a=>a.action==='reveal'&&a.params.name===name);
  const drive=state.actions.find(a=>a.action==='drive');
  const driverElapsed=elapsed(drive)+timeOffset;
  const rotation=wheelAngle(driverElapsed,state.props),x=driverX(driverElapsed,state.props);
  const opacity=fadeDuration?1-smooth(elapsed(drive)/fadeDuration):1;
  useReport({rotation,driverElapsed,driverX:x,opacity,visible:names.filter(n=>reveal(n)),driver});
  return <div className="constellation" style={fadeDuration?{background:'#101419',opacity}:undefined}>
    <div className="graph-title">{title}</div>
    <svg viewBox="0 0 1920 1080" className="spokes">
      <path d="M1920 835 H0" fill="none" stroke="#79a7b9" strokeWidth="2" opacity={drive?.45:0}/>
      <g transform={`rotate(${rotation} 960 540)`}>
        <circle cx="960" cy="540" r="275" fill="none" stroke="#8c9ba8" strokeWidth="1" opacity=".22"/>
        {names.map((name,i)=>{
          const a=-Math.PI/2+i*Math.PI/4, r=reveal(name);
          const opacity=timeOffset?1:r?smooth(elapsed(r)/.35):0;
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
      {drive&&<text className="incoming" textAnchor="middle"
        x={x} y={820}>{driver}</text>}
    </svg>
    <div className="hub-mark" dangerouslySetInnerHTML={{__html:mark}}/>
  </div>;
}
defineElement({kind:'listing',component:Listing});
defineElement({kind:'signature',component:Signature});
defineElement({kind:'constellation',component:Constellation});
