// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import React from 'react';
import {Slot, defineSet} from 'videomaker/stage';
import './stage.css';
import './_build/fonts.css';

const slots = ['backdrop', 'ghost', 'stage', 'heading', 'note'];
defineSet({kind: 'portrait', slots, component: () =>
  <div className="portrait">
    {slots.map(name => <Slot key={name} name={name} className={'slot-' + name}/>)}
  </div>
});
