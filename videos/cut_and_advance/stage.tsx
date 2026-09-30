// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// The film's template: the sets Leonardo and LeonardoSplit and the element
// Jobs, declared in movie.py beside this file. Every word on screen comes
// from the movie document (the set's props, the element's props); the layout
// and the look are this file's and stage.css's.
import {Chrome, Slot, defineElement, defineSet} from 'videomaker/stage';
import type {ElementComponentProps, SetComponentProps} from 'videomaker/stage';
import type {JobsState, LeonardoProps, LeonardoSplitProps} from 'videomaker/movie';
import './stage.css';

// The masthead: the series at the left in the accent, the brand at the right,
// muted. Drawn in Chrome so it stays still and sharp above pictures and joins.
// No rule, no bar, no progress: where a viewer is in the film is the player's.
function Masthead({series, brand}: {series: string; brand: string}) {
  return (
    <Chrome>
      <div className="leonardo-series">{series}</div>
      <div className="leonardo-brand">{brand}</div>
    </Chrome>
  );
}

// The root set: the mill fills the page below the masthead; a plate over the
// whole frame for a picture; a headline band at the top of the stage; a card
// column at the right.
function Leonardo({props}: SetComponentProps<LeonardoProps>) {
  return (
    <div className="leonardo">
      <Masthead series={props.series} brand={props.brand}/>
      <Slot name="stage" className="leonardo-stage"/>
      <Slot name="plate" className="leonardo-plate"/>
      <Slot name="aside" className="leonardo-aside"/>
      <Slot name="headline" className="leonardo-headline"/>
    </div>
  );
}

// Derived by composition: Leonardo's masthead, two containers side by side,
// the source at the left and the model at the right, the headline over the
// source column.
function LeonardoSplit({props}: SetComponentProps<LeonardoSplitProps>) {
  return (
    <div className="leonardo">
      <Masthead series={props.series} brand={props.brand}/>
      <Slot name="left" className="leonardo-left"/>
      <Slot name="right" className="leonardo-right"/>
      <Slot name="headline" className="leonardo-headline leonardo-headline-split"/>
    </div>
  );
}

// The two-jobs card: an ordered list of the jobs; the one a `light` action
// names by key is filled with the accent while the action lasts.
type Job = {key: string; text: string};
function Jobs({state}: ElementComponentProps<JobsState>) {
  const lit = state.actions.find(action => action.action === 'light')?.params.job;
  const jobs = state.props.jobs as Job[];
  return (
    <ol className="jobs">
      {jobs.map(job => (
        <li key={job.key} className={job.key === lit ? 'jobs-item jobs-lit' : 'jobs-item'}>{job.text}</li>
      ))}
    </ol>
  );
}

defineSet({kind: 'leonardo', slots: ['stage', 'plate', 'headline', 'aside'], component: Leonardo});
defineSet({kind: 'leonardo-split', slots: ['left', 'right', 'headline'], component: LeonardoSplit});
defineElement({kind: 'jobs', component: Jobs});
