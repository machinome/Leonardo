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
from bisect import bisect_left

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
os.environ['SOLID_BUILD_DIR']=str(ROOT/'_build/sawmill_readouts')
logging.disable(logging.CRITICAL)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill
from models.hydraulic_sawmill.rope_drive import PASS_ANGLE, PASS_SECONDS, PASS_TURNS
from models.hydraulic_sawmill.layout import TURN_SECONDS


def measurements():
    machine=LeonardoHydraulicSawmill()
    machine.set_keyframe(0)
    machine.assemble()
    machine.build_stls()
    top=machine.saw.sash.frame.mesh.bounds[:,2].mean()
    start=machine.carriage.bed.mesh.bounds[:,0].mean()
    rows=[]
    for i in range(721):
        machine.set_keyframe(i*TURN_SECONDS/720)
        rows.append([round(float(top-machine.saw.sash.frame.mesh.bounds[:,2].mean()),6),
                     round(float(start-machine.carriage.bed.mesh.bounds[:,0].mean()),6)])
    # Measure eight positions within each tooth, not just whole-turn endpoints:
    # the upper rope's approach angle changes appreciably near the end of a cut.
    first=[row[1] for row in rows[:361]]
    fractions=[]
    for j in range(8):
        target=first[-1]*j/8
        i=max(1,bisect_left(first,target))
        fractions.append((i-1+(target-first[i-1])/(first[i]-first[i-1]))/720)
    feed_samples=[]
    for turn in range(PASS_TURNS):
        for fraction in fractions:
            machine.set_keyframe((turn+fraction)*TURN_SECONDS)
            feed_samples.append(round(float(start-machine.carriage.bed.mesh.bounds[:,0].mean()),6))
    machine.set_keyframe(PASS_SECONDS)
    feed_samples.append(round(float(start-machine.carriage.bed.mesh.bounds[:,0].mean()),6))
    return {'feed_samples':feed_samples,'feed_subdivisions':8,
            'turn_feed':feed_samples[::8],'notice':'Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.',
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
        print(f"PASS: 721 stroke/feed samples and {len(data['feed_samples'])} full-pass feed samples match CAD meshes.")
    else:
        print(json.dumps(data,separators=(',',':')))
