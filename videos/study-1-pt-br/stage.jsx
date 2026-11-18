// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineSet, defineElement} from 'videomaker/stage';
import './stage.css';

const slots = ['backdrop', 'plate', 'ghost', 'stage'];
defineSet({kind: 'portrait', slots, component: () =>
  <div className="portrait">
    {slots.map(name => <Slot key={name} name={name} className={'slot-' + name}/>)}
  </div>
});
defineElement({kind: 'shade', component: () =>
  <div style={{position: 'absolute', inset: 0, background: '#101419'}}/>
});
