"""Stock and hand-cut features in the sawmill's millimetre layout frame.

Each record is one piece. See docs/carpentry.md for provenance and cutting.
"""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from dataclasses import dataclass, field

FIT = 0.15
PEG_PLAY = 0.10


@dataclass
class Member:
    code: str
    label: str
    group: str
    stock: tuple
    centre: tuple
    grain: str
    additions: list = field(default_factory=list)
    cuts: list = field(default_factory=list)
    notes: list = field(default_factory=list)


@dataclass
class Peg:
    code: str
    members: tuple
    centre: tuple
    axis: str
    radius: float
    length: float


MEMBERS = []
PEGS = []
JOINTS = []


def timber(code, label, group, stock, centre, grain):
    member = Member(code, label, group, stock, centre, grain)
    MEMBERS.append(member)
    return member


def block(size, centre):
    return ('box', tuple(size), tuple(centre))


def cut(member, size, centre, note):
    member.cuts.append(block(size, centre))
    member.notes.append(note)


def bore(member, radius, length, centre, axis='y', note=''):
    member.cuts.append(('bore', radius, length, tuple(centre), axis))
    if note:
        member.notes.append(note)


def pin(a, b, centre, axis, length, radius=1.2):
    peg = Peg(f'P{len(PEGS)+1:02}', (a.code, b.code), centre, axis, radius, length)
    if axis == 'z' and any(m.code.startswith('R') for m in (a, b)):
        # Set a whittled head below the rolling surface, on a bored shoulder.
        upper = next(m for m in (a, b) if m.code.startswith('R'))
        x, y, z = centre
        bore(upper, radius+1.1, 2.4, (x, y, z+length/2-1), 'z', 'Counterbore for recessed wooden pin head')
        peg.centre = (x, y, z-1.1)
        peg.length -= 2.2
    PEGS.append(peg)
    for member in (a, b):
        bore(member, radius+PEG_PLAY, length+2, centre, axis,
             f'{peg.code}: bore Ø{2*(radius+PEG_PLAY):g} along {axis.upper()} at {centre}')
    return peg


def tenon(member, receiver, size, centre, axis, label):
    member.additions.append(block(size, centre))
    cut(receiver, tuple(v+2*FIT for v in size), centre, label+' mortise')
    member.notes.append(label+f' tenon {size} at {centre}')
    JOINTS.append((member.code, receiver.code, axis, size, centre))


legs = {}
side_rails = {}
stretchers = {}
for side, y in enumerate((-99, 115)):
    rail_y = -115 if side == 0 else 115
    for end, x in enumerate((-335, 335)):
        leg = timber(f'L{side*2+end+1}', 'Table leg', 'bed',
                     (22, 22, 302.9), (x, y, 169.45), 'Z')
        if side == 0:
            leg.additions.append(block((22, 38, 13.9), (x, -107, 313.95)))
            leg.notes.append('Hew from 22 × 38 stock, leaving the offset head full width')
        legs[side, end] = leg
    rail = timber(f'B{side+1}', 'Upper longitudinal side rail', 'bed',
                  (720, 18, 18), (0, rail_y, 330), 'X')
    side_rails[side] = rail
    stretcher = timber(f'S{side+1}', 'Lower longitudinal stretcher', 'bed',
                      (647.8, 18, 20), (0, y, 72), 'X')
    stretchers[side] = stretcher
    for end, x in enumerate((-335, 335)):
        sign = -1 if end == 0 else 1
        leg = legs[side, end]
        tenon(stretcher, leg, (16.2, 8, 6), (sign*331.9, y, 76), 'x', 'High stretcher')
        pin(stretcher, leg, (sign*331, y, 76), 'y', 21.8)
        tenon(leg, rail, (8, 8, 7.7), (x, rail_y, 324.65), 'z', 'Post head')
        pin(leg, rail, (x, rail_y, 325), 'y', 17.8, 1.0)

for end, x in enumerate((-335, 335)):
    lower = timber(f'C{end+1}', 'Lower end crossmember', 'bed',
                   (22, 191.8, 18), (x, 8, 72), 'Y')
    for side, y in enumerate((-93.9, 109.9)):
        tenon(lower, legs[side, end], (8, 12.2, 6), (x, y, 67), 'y', 'Low crossmember')
        pin(lower, legs[side, end], (x, y, 67), 'x', 21.8)
    top = timber(f'C{end+3}', 'Housed upper end crossmember', 'bed',
                 (22, 211.8, 16), (x, 0, 330), 'Y')
    for side, y in enumerate((-115.9, 115.9)):
        top.additions.append(block((22, 20.2, 8), (x, y, 334)))
        cut(side_rails[side], (22+2*FIT, 22, 10.1), (x, y, 334.95),
            'Open top housing; crossmember rests on the 330 mm shoulder')
        pin(top, side_rails[side], (x+7, -115 if side == 0 else 115, 330), 'z', 16)
    for y in (-42, 42):
        cut(top, (24, 12+2*FIT, 5.1), (x, y, 337.45), 'Running rail housing: 0.1 seating allowance')

running = []
for i, y in enumerate((-42, 42)):
    rail = timber(f'R{i+1}', 'Continuous carriage running rail', 'bed',
                  (760, 12, 10), (0, y, 340), 'X')
    running.append(rail)
    bore(rail, 3.6, 16, (-370, y, 340), note='Upper roller journal Ø7.2')
    bore(rail, 5.6, 16, (115, y, 330), note='Underside relief for the ratchet shaft; preserve its 0.6 mm running play')
    for end, x in enumerate((-335, 335)):
        top = next(m for m in MEMBERS if m.code == f'C{end+3}')
        pin(rail, top, (x, y, 335), 'z', 20, 1.0)

for side, rail in side_rails.items():
    bore(rail, 5.6, 24, (115, rail.centre[1], 330), note='Ratchet journal Ø11.2')
    for x, z in ((235, 330), (37, 340)):
        if side == 1:
            bore(rail, 3.6, 24, (x, 115, z), note='Iron pivot clearance Ø7.2')
for side in (0, 1):
    bore(legs[side, 0], 6.6, 26, (-335, legs[side, 0].centre[1], 285),
         note='Compound shaft journal Ø13.2')

for i, (x, lo, z) in enumerate(((235, 28, 330), (37, 64, 340))):
    bearer = timber(f'F{i+1}', 'Feed pivot bearer', 'bed',
                    (20, 105.9-lo, 24), (x, (105.9+lo)/2, z), 'Y')
    tenon(bearer, side_rails[1], (16, 14.2, 6), (x, 112.9, 324 if i == 0 else 333),
          'y', 'Feed bearer')
    bore(bearer, 3.6, 110, (x, 76, z), note='Iron pivot Ø7.2 through the bearer')
    pin(bearer, side_rails[1], (x+6, 114, 330), 'z', 18, 1.0)
    if i == 0:
        cut(bearer, (22, 12+2*FIT, 10.1), (x, 42, 339.95), 'Running rail housing: 0.1 seating allowance')
        pin(bearer, running[1], (x+6, 42, 336), 'z', 18, 1.0)

sole = timber('T1', 'Lower tower and inner-bearing bearer', 'tower',
              (22, 195.8, 18), (0, 8, 72), 'Y')
for side, y in enumerate((-95.9, 111.9)):
    tenon(sole, stretchers[side], (8, 12.2, 8), (0, y, 72), 'y', 'Tower bearer end')
    pin(sole, stretchers[side], (0, y, 72), 'z', 20)

posts = []
for i, y in enumerate((-78, 78)):
    post = timber(f'T{i+2}', 'Grooved fixed saw upright', 'tower',
                  (26, 20, 627), (0, y, 331.5), 'Z')
    posts.append(post)
    cut(post, (17.2, 12.4, 405), (0, -66 if y < 0 else 66, 416.5), 'Plough sash guide 17.2 wide')
    cut(post, (17.2, 24, 66), (0, y, 267), 'Saw journal slot, Z=234…300')
    cut(post, (13+FIT, 22, 18+2*FIT), ((-13+FIT)/2, y, 72), 'Side-open half housing for T1')
    cut(sole, (12, 20+2*FIT, 20), (6, y, 72), 'Halve T1 at the upright crossing')
    pin(sole, post, (0, y, 72), 'x', 28, 1.4)
    bore(post, 9 if y < 0 else 4.8, 26, (0, y, 120),
         note='Wheel shaft clearance' if y < 0 else 'Lower idler journal Ø9.6')

cap = timber('T4', 'Tower top crosshead', 'tower', (26, 135.8, 16), (0, 0, 637), 'Y')
for post in posts:
    y = post.centre[1]
    tenon(cap, post, (8, 20.2, 16), (0, y*77.9/78, 637), 'z', 'Open-top bridle')
    pin(cap, post, (0, y, 637), 'x', 28, 1.4)

for i, sign in enumerate((-1, 1)):
    tie = timber(f'T{i+5}', 'Tower-to-bed shoulder tie', 'tower',
                 (22, 17.8, 16), (0, sign*97, 330), 'Y')
    tenon(tie, posts[i], (8, 6.2, 8), (0, sign*85.1, 330), 'y', 'Tower tie inner')
    tenon(tie, side_rails[i], (8, 14.2, 8), (0, sign*112.9, 330), 'y', 'Tower tie outer')
    pin(tie, posts[i], (0, sign*85, 330), 'x', 28, 1.0)
    pin(tie, side_rails[i], (0, sign*114, 330), 'z', 18, 1.0)

for code, y, foot in (('A1', -207, 18), ('A2', -32, 81.1)):
    bearing = timber(code, 'Wheel-side wooden bearing' if code == 'A1' else 'Inner wooden bearing',
                     'tower', (38, 14, 137-foot), (0, y, (137+foot)/2), 'Z')
    for x in (-14, 14):
        cut(bearing, (10, 16, 10), (x, y, 134), 'Saw the stepped journal cheek')
    bore(bearing, 6.6, 20, (0, y, 120), note='Round iron journal Ø13.2')
    if code == 'A2':
        tenon(bearing, sole, (8, 10, 10.2), (0, y, 76.1), 'z', 'Bearing foot')
        pin(bearing, sole, (0, y, 76), 'x', 24, 1.2)

BY_CODE = {member.code: member for member in MEMBERS}
