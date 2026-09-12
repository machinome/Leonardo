#!/usr/bin/env python3
"""Print the exhibit's read-only measurement table, or verify its checked-in copy.

Run from the gallery: python models/hydraulic_sawmill/scripts/readouts.py --check
No alternate JavaScript linkage is needed: all labels derive from CAD meshes.
"""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
import json
import logging
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
os.environ['SOLID_BUILD_DIR']=str(ROOT/'_build/sawmill_readouts')
logging.disable(logging.CRITICAL)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill


def measurements():
    machine=LeonardoHydraulicSawmill()
    machine.set_state(phase=0,time=0,playback=0)
    machine.assemble()
    machine.build_stls()
    top=machine.sash.frame.mesh.bounds[:,2].mean()
    start=machine.carriage.bed.mesh.bounds[:,0].mean()
    rows=[]
    for i in range(721):
        machine.set_state(phase=i/2)
        rows.append([round(float(top-machine.sash.frame.mesh.bounds[:,2].mean()),6),
                     round(float(machine.carriage.bed.mesh.bounds[:,0].mean()-start),6)])
    return {'notice':'Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.',
            'source':'scripts/readouts.py; measured CAD, not a second motion implementation',
            'step':0.5,'feed_per_turn':rows[-1][1],'rows':rows}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data=measurements()
    if args.check:
        assert json.loads((ROOT/'models/hydraulic_sawmill/readouts.json').read_text())==data
        print('PASS: 721 readout samples match the actual saw and carriage meshes.')
    else:
        print(json.dumps(data,separators=(',',':')))
