// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineElement, defineSet, useReport} from 'videomaker/stage';
import {wheelAngle,driverX,approachScale,logoScale} from './ending-motion.mjs';
import './stage.css';
import './_build/fonts.css';

const sets={
  exhibition:['ghost','backdrop','stage','graphic','heading','note','veil'],
  mechanism:['backdrop','plate','ghost','stage','note'], archive:['picture','note'],
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
  const all=state.actions.find(a=>a.action==='blink-all')?.params.token;
  const typing=state.actions.find(a=>a.action==='write');
  const reveal=state.actions.find(a=>a.action==='complete');
  const progress=typing?.progress??(reveal||!state.props.initiallyEmpty?1:0);
  const shown=state.props.code.slice(0,Math.ceil(state.props.code.length*progress));
  useReport({sourceSha256:state.props.digest,text:shown,blink:blink??null,all:all??null});
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
  const opacity=p?smooth(p.progress):1;
  const approach=state.actions.find(a=>a.action==='approach');
  const scale=approach?logoScale(approach.progress):1;
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
  const {names,mark,title,drivers,stagger,streamDuration,timeOffset=0,fadeDuration=0}=state.props;
  const reveal=name=>state.actions.find(a=>a.action==='reveal'&&a.params.name===name);
  const drive=state.actions.find(a=>a.action==='drive');
  const driverElapsed=elapsed(drive)+timeOffset;
  const rotation=wheelAngle(driverElapsed,state.props);
  const approach=state.actions.find(a=>a.action==='approach');
  const scale=approach?approachScale(approach.progress):1;
  const positions=drivers.map((name,i)=>({name,x:driverX(driverElapsed-i*stagger,state.props)}));
  const opacity=fadeDuration?1-smooth(elapsed(drive)/fadeDuration):1;
  const streamOpacity=drive?1-smooth((driverElapsed-streamDuration+.15)/.15):0;
  useReport({rotation,driverElapsed,scale,opacity,streamOpacity,visible:names.filter(n=>reveal(n)),
    drivers:positions});
  return <div className="constellation" style={{transform:`scale(${scale})`,transformOrigin:'50% 50%'}}>
    <div style={{position:'absolute',inset:0,background:'#101419',opacity}}/>
    <div className="graph-title" style={{opacity}}>{title}</div>
    <svg viewBox="0 0 1920 1080" className="spokes">
      <path d="M1920 835 H0" fill="none" stroke="#79a7b9" strokeWidth="2" opacity={.45*streamOpacity}/>
      <g opacity={opacity} transform={`rotate(${rotation} 960 540)`}>
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
      {drive&&positions.map(({name,x},i)=><text key={name} className="incoming" textAnchor="middle"
        opacity={driverElapsed>=i*stagger?streamOpacity:0} x={x} y={820}>{name}</text>)}
    </svg>
    <div className="hub-mark" style={{opacity}} dangerouslySetInnerHTML={{__html:mark}}/>
  </div>;
}
defineElement({kind:'listing',component:Listing});
defineElement({kind:'signature',component:Signature});
defineElement({kind:'curtain',component:Curtain});
defineElement({kind:'shade',component:()=> <div style={{position:'absolute',inset:0,background:'#101419'}}/>});
defineElement({kind:'constellation',component:Constellation});
