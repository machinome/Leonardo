// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineElement, defineSet} from 'videomaker/stage';
import './stage.css';
import './_build/fonts.css';

function Exhibition() {
  return <div className="exhibition">
    <Slot name="stage" className="model-stage"/>
    <Slot name="graphic" className="graphic-stage"/>
    <Slot name="heading" className="heading-stage"/>
    <Slot name="note" className="note-stage"/>
  </div>;
}
function Workbench() {
  return <div className="exhibition workbench">
    <Slot name="right" className="split-model"/>
    <Slot name="imports" className="source-imports"/>
    <Slot name="code" className="source-relationship"/>
    <Slot name="heading" className="heading-stage"/>
    <Slot name="note" className="note-stage"/>
  </div>;
}
function SourceRoom() {
  return <div className="exhibition source-room">
    <Slot name="code" className="film-source"/>
    <Slot name="heading" className="heading-stage"/>
    <Slot name="note" className="note-stage"/>
  </div>;
}
defineSet({kind:'exhibition', slots:['stage','heading','note','graphic'], component:Exhibition});
defineSet({kind:'workbench', slots:['right','imports','code','heading','note'], component:Workbench});
defineSet({kind:'source-room', slots:['code','heading','note'], component:SourceRoom});

function Card({state}) {
  return <div className={state.props.small ? 'card small' : 'card'}>
    {state.props.eyebrow && <div className="eyebrow">{state.props.eyebrow}</div>}
    <div>{state.props.text}</div>
  </div>;
}

// Escape through React; only lexical color is added to the literal source.
function syntax(line) {
  const parts=line.split(/("[^"\n]*"|'[^'\n]*'|\b(?:class|from|import|until|model|cues|def|return)\b)/g);
  return parts.map((part,i)=><span key={i} className={/^["']/.test(part)?'string':/^(class|from|import|def|return)$/.test(part)?'keyword':''}>{part}</span>);
}
function Listing({state}) {
  const token=state.actions.find(a=>a.action==='focus')?.params.token;
  return <div className="listing" data-source-sha256={state.props.digest}>
    <div className="listing-file">{state.props.file}</div>
    <pre>{state.props.code.split('\n').map((line,i)=><div key={i} className={token&&line.includes(token)?'lit-line':''}>
      <span className="line-number">{String(i+1).padStart(2,'0')}</span>{syntax(line)||' '}
    </div>)}</pre>
  </div>;
}

const smooth=x=>{const p=Math.max(0,Math.min(1,x));return p*p*(3-2*p);};
function Constellation({state}) {
  const p=state.actions.find(a=>a.action==='unfold')?.progress??1;
  const arrival=smooth(p*3);
  const {names,notes,mark,title,subtitle}=state.props;
  // A separate ring recalls the eight paddle stations. The mark never deforms.
  return <div className="constellation">
    <div className="constellation-title">{title}</div>
    <svg viewBox="0 0 1920 1080" className="spokes">
      <circle cx="960" cy="555" r="289" fill="none" stroke="#66727c" strokeWidth="1" opacity=".28"/>
      {names.map((name,i)=>{
        const angle=-Math.PI/2+i*Math.PI/4;
        const r=210+arrival*79;
        const x=960+Math.cos(angle)*r, y=555+Math.sin(angle)*r;
        return <g key={name} opacity={smooth(p*5-i*.10)}>
          <line x1={960+Math.cos(angle)*125} y1={555+Math.sin(angle)*125} x2={x} y2={y} stroke="#e9b778" strokeWidth="1.5"/>
          <circle cx={x} cy={y} r="5" fill="#e9b778"/>
          <text x={960+Math.cos(angle)*(r+87)} y={555+Math.sin(angle)*(r+65)} textAnchor="middle" dominantBaseline="middle" className="tech-label">{name}</text>
          <text x={960+Math.cos(angle)*(r+87)} y={584+Math.sin(angle)*(r+65)} textAnchor="middle" className="tech-note">{notes[i]}</text>
        </g>;
      })}
    </svg>
    <div className="hub-mark" dangerouslySetInnerHTML={{__html:mark}}/>
    <div className="constellation-subtitle">{subtitle}</div>
  </div>;
}
function Signature({state}) {
  const p=state.actions.find(a=>a.action==='enter')?.progress;
  return <div className="signature">
    <div className="wordmark" dangerouslySetInnerHTML={{__html:state.props.svg}}/>
    <div className="signature-tagline">{state.props.tagline}</div>
    <div className="question" style={{opacity:p===undefined?0:smooth(p*5)}}>{state.props.question}</div>
  </div>;
}
defineElement({kind:'card',component:Card});
defineElement({kind:'listing',component:Listing});
defineElement({kind:'constellation',component:Constellation});
defineElement({kind:'signature',component:Signature});
