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
from models.hydraulic_sawmill.layout import PASS_ANGLE, PASS_SECONDS, PASS_TURNS


def measurements():
    machine=LeonardoHydraulicSawmill()
    machine.set_keyframe(0)
    machine.assemble()
    machine.build_stls()
    top=machine.saw.sash.frame.mesh.bounds[:,2].mean()
    start=machine.carriage.bed.mesh.bounds[:,0].mean()
    rows=[]
    for i in range(721):
        machine.set_keyframe(i/180)
        rows.append([round(float(top-machine.saw.sash.frame.mesh.bounds[:,2].mean()),6),
                     round(float(machine.carriage.bed.mesh.bounds[:,0].mean()-start),6)])
    turn_feed=[]
    for turn in range(PASS_TURNS+1):
        machine.set_keyframe(turn*4)
        turn_feed.append(round(float(machine.carriage.bed.mesh.bounds[:,0].mean()-start),6))
    return {'turn_feed':turn_feed,'notice':'Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.',
            'source':'scripts/readouts.py; measured CAD, not a second motion implementation',
            'pass_angle':PASS_ANGLE,'pass_seconds':PASS_SECONDS,'pass_turns':PASS_TURNS,
            'step':0.5,'feed_per_turn':rows[-1][1],'rows':rows}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data=measurements()
    if args.check:
        assert json.loads((ROOT/'models/hydraulic_sawmill/readouts.json').read_text())==data
        print('PASS: 721 stroke/feed samples and 75 turn endpoints match the actual saw and carriage meshes.')
    else:
        print(json.dumps(data,separators=(',',':')))
