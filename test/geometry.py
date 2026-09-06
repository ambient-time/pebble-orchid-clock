"""Check native marks and clipping against captured source geometry.

Copyright 2026 Luke Steuber. MIT License.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('assets',root/'tools/assets.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
fixture=json.loads((root/'test/source-fixtures.json').read_text())
assert fixture['sourceSHA256']==hashlib.sha256((root/'reference/source.html').read_bytes()).hexdigest()
header=(root/'src/c/geometry.h').read_text()

def source_curve(commands):
    """Independent De Casteljau evaluation of the source's recorded canvas path."""
    result=[]
    for command in commands:
        op,*numbers=command
        if op=='M':result.append(tuple(numbers))
        elif op in ('C','Q'):
            controls=[result[-1]]+list(zip(numbers[::2],numbers[1::2]))
            for step in range(1,25):
                points=controls;t=step/24
                while len(points)>1:
                    points=[tuple(p[k]*(1-t)+q[k]*t for k in (0,1)) for p,q in zip(points,points[1:])]
                result.append(points[0])
        else:assert op=='Z'
    return result

for platform,(w,h,mono) in a.SIZES.items():
    im,hours,minutes,spans,_,_,caption=a.make(w,h,mono)
    radius=w*(.315 if w==h else .325);cx=w/2;cy=h*.48
    expected_hours=[(round(cx+x*radius),round(cy+y*radius),max(1,round(r*radius))) for x,y,r in fixture['hours']]
    expected_minutes=[(round(cx-y*radius),round(cy+.04*radius+x*radius)) for x,y in fixture['minutes']]
    assert hours==expected_hours and minutes==expected_minutes,platform+' source mark positions'
    assert len(hours)==12 and len(set((x,y) for x,y,r in hours))==12
    assert len(minutes)==60 and len(set(minutes))==60
    for x,y in [(x,y) for x,y,r in hours]+minutes:
        assert 0<=x<w and 0<=y<h
        if w==h:assert (x-w/2)**2+(y-h/2)**2<(w/2-3)**2
    assert max(y for x,y in minutes)<caption-12
    assert (root/'resources'/f'{platform}.bin').read_bytes()==im.tobytes()

    expected=Image.new('1',(w,h));draw=ImageDraw.Draw(expected)
    draw.polygon([(round(cx-y*radius),round(cy+.04*radius+x*radius)) for x,y in source_curve(fixture['throat'])],fill=1)
    _,_,rx,ry=fixture['column']
    draw.ellipse((round(cx-rx*radius),round(cy-ry*radius),round(cx+rx*radius),round(cy+ry*radius)),fill=0)
    # Both side spans must survive; the column must not be painted over at high seconds.
    actual=Image.new('1',(w,h));draw=ImageDraw.Draw(actual)
    split_rows=0
    for y,(x0,x1,x2,x3) in enumerate(spans):
        if x0<=x1:draw.line((x0,y,x1,y),fill=1)
        if x2<=x3:draw.line((x2,y,x3,y),fill=1);split_rows+=1
    assert split_rows>0,platform+' column/throat overlap fixture missing'
    assert actual.tobytes()==expected.tobytes(),platform+' source throat/column clipping'

    section=header.split('#ifdef PBL_PLATFORM_'+platform.upper()+'\n',1)[1].split('#endif',1)[0]
    for label,values in [('HOURS',hours),('MINUTES',minutes),('THROAT',spans)]:
        match=re.search(r'\b'+label+r'\[\d+\]\[\d+\]=\{(.*)\};',section)
        compiled=[tuple(map(int,row.split(','))) for row in re.findall(r'\{([^}]+)\}',match[1])]
        assert compiled==values,platform+' compiled '+label+' table is stale'
    print(platform, '72 source-position marks; exact throat/column mask; compiled tables and artwork verified')
