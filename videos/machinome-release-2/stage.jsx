// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineElement, defineSet, useReport} from 'videomaker/stage';
import './stage.css';
import './_build/fonts.css';

const sets={
  exhibition:['ghost','stage','graphic','heading','note'],
  mechanism:['ghost','stage','note'], archive:['picture','note'],
  workbench:['stage','imports','code'], 'source-room':['code'],
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
  useReport({sourceSha256:state.props.digest,text:state.props.code});
  return <div className="listing" data-source-sha256={state.props.digest}>
    <div className="listing-file">{state.props.file}</div>
    <pre>{state.props.code.split('\n').map((line,i)=><div key={i} className={token&&line.includes(token)?'lit-line':''}>
      <span className="line-number">{String(i+1).padStart(2,'0')}</span>{syntax(line)}</div>)}</pre>
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
  const {names,mark,title,driver,arrival,acceleration,rate}=state.props;
  const reveal=name=>state.actions.find(a=>a.action==='reveal'&&a.params.name===name);
  const drive=state.actions.find(a=>a.action==='drive');
  const dt=Math.max(0,elapsed(drive)-arrival);
  const rotation=dt<acceleration?rate*dt*dt/(2*acceleration):rate*(dt-acceleration/2);
  useReport({rotation,visible:names.filter(n=>reveal(n)),driver});
  return <div className="constellation">
    <div className="graph-title">{title}</div>
    <svg viewBox="0 0 1920 1080" className="spokes">
      <path d="M1920 800 L1150 800 Q1070 800 1000 750" fill="none" stroke="#79a7b9" strokeWidth="2" opacity={drive?.45:0}/>
      <g transform={`rotate(${rotation} 960 540)`}>
        <circle cx="960" cy="540" r="275" fill="none" stroke="#8c9ba8" strokeWidth="1" opacity=".22"/>
        {names.map((name,i)=>{
          const a=-Math.PI/2+i*Math.PI/4, r=reveal(name);
          const opacity=r?smooth(elapsed(r)/.35):0;
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
      {drive&&elapsed(drive)<arrival&&<text className="incoming" textAnchor="middle"
        x={1900-850*smooth(elapsed(drive)/arrival)} y={800-45*smooth(elapsed(drive)/arrival)}>{driver}</text>}
    </svg>
    <div className="hub-mark" dangerouslySetInnerHTML={{__html:mark}}/>
  </div>;
}
defineElement({kind:'listing',component:Listing});
defineElement({kind:'signature',component:Signature});
defineElement({kind:'constellation',component:Constellation});
