"""Rasterize the owner's Orchid Clock Bézier specimen at Pebble resolutions.

Copyright 2026 Luke Steuber. MIT License. Source paths and freckle placement
come from reference/source.html. Pillow is used only at build time.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent.parent
SIZES={'basalt':(144,168,False),'chalk':(180,180,False),'diorite':(144,168,True),
       'emery':(200,228,False),'flint':(144,168,True),'gabbro':(260,260,False)}

def curve(start, segments):
    points=[start]
    for controls in segments:
        p0=points[-1]
        for i in range(1,25):
            t=i/24;s=1-t
            if len(controls)==3:
                a,b,c=controls;point=tuple(s**3*p0[k]+3*s*s*t*a[k]+3*s*t*t*b[k]+t**3*c[k] for k in (0,1))
            else:
                a,b=controls;point=tuple(s*s*p0[k]+2*s*t*a[k]+t*t*b[k] for k in (0,1))
            points.append(point)
    return points

def make(w,h,mono):
    r=w*(.315 if w==h else .325);cx=w/2;cy=h*.48
    im=Image.new('L',(w,h),0 if mono else 0xea);d=ImageDraw.Draw(im)
    def shape(points,color,origin=(cx,cy),angle=0,outline=None):
        ps=[(round(origin[0]+x*math.cos(angle)-y*math.sin(angle)),round(origin[1]+x*math.sin(angle)+y*math.cos(angle))) for x,y in points]
        d.polygon(ps,fill=color)
        if outline is not None:d.line(ps+[ps[0]],fill=outline,width=1)
        return ps
    for angle,length,width,blush in [(-math.pi/2,1.12,.4,False),(math.pi*.78,1,.34,True),(math.pi*1.22,1,.34,True),(-.35,1.4,.68,False),(math.pi+.35,1.4,.68,False)]:
        length*=r;width*=r
        ps=curve((0,0),[((length*.18,-width*1.05),(length*.55,-width*1.1),(length*.92,-width*.35)),((length*1.02,0),(length*.92,width*.35)),((length*.55,width*1.1),(length*.18,width*1.05),(0,0))])
        shape(ps,1 if mono else (0xfa if blush else 0xff),angle=angle,outline=0 if mono else 0xea)
        vein=curve((length*.12,0),[((length*.4,-width*.12),(length*.7,width*.08),(length*.94,0))])
        v=[(round(cx+x*math.cos(angle)-y*math.sin(angle)),round(cy+x*math.sin(angle)+y*math.cos(angle))) for x,y in vein]
        if not mono:d.line(v,fill=0xea,width=1)
    lip=curve((0,0),[((r*.2,-r*.38*.7),(r*.45,-r*.38*1.15),(r*.7,-r*.38*.85)),((r*.95,-r*.38*.4),(r*1.05,0),(r*.95,r*.38*.4)),((r*.7,r*.38*.85),(r*.45,r*.38*1.15),(r*.2,r*.38*.7))])
    shape(lip,1 if mono else 0xff,origin=(cx,cy+r*.04),angle=math.pi/2,outline=0 if mono else 0xea)
    throat=curve((r*.08,0),[((r*.3,-r*.38*.35),(r*.55,-r*.38*.45),(r*.78,-r*.38*.15)),((r*.82,0),(r*.78,r*.38*.15)),((r*.55,r*.38*.45),(r*.3,r*.38*.35),(r*.08,0))])
    mask=Image.new('1',(w,h));md=ImageDraw.Draw(mask)
    md.polygon([(round(cx-y),round(cy+r*.04+x)) for x,y in throat],fill=1)
    # The column is painted after the nectar in the source.
    column=(round(cx-r*.11),round(cy-r*.22*.88),round(cx+r*.11),round(cy+r*.22*.88))
    md.ellipse(column,fill=0)
    d.ellipse(column,fill=1 if mono else 0xea,outline=0 if mono else 0xff)
    px,py=cx,cy-r*.11;pr=max(2,r*.22*.28)
    d.ellipse((round(px-pr),round(py-pr),round(px+pr),round(py+pr)),fill=1 if mono else 0xfe)
    spots=[(-math.pi/2,.72),(-math.pi/2,.95),(-.35,.85),(-.35,1.15),(-.35,1.35),(math.pi+.35,.85),(math.pi+.35,1.15),(math.pi+.35,1.35),(math.pi*.78,.75),(math.pi*.78,.95),(math.pi*1.22,.75),(math.pi*1.22,.95)]
    hours=[(round(cx+math.cos(a)*r*dist),round(cy+math.sin(a)*r*dist*.92),max(1,round(r*(.028+(i%3)*.006)))) for i,(a,dist) in enumerate(spots)]
    minutes=[]
    for i in range(60):
        row,col=divmod(i,12);u=.28+col/11*.52;v=(1 if row%2 else -1)*(.12+(row//2)*.18)+(col%3-1)*.04
        minutes.append((round(cx-r*.38*v*1.1),round(cy+r*.04+r*u)))
    assert len(set(minutes))==60, 'Minute freckles collapsed at native resolution'
    spans=[]
    for y in range(h):
        xs=[x for x in range(w) if mask.getpixel((x,y))]
        runs=[]
        for x in xs:
            if not runs or x>runs[-1][1]+1:runs.append([x,x])
            else:runs[-1][1]=x
        assert len(runs)<=2, 'Throat row exceeds two visible spans'
        # Keep both sides when the source's column covers the throat center.
        runs += [[1,0]]*(2-len(runs))
        spans.append(tuple(value for run in runs for value in run))
    return im,hours,minutes,spans,round(cy+r*.04),round(r),round(h*.88 if w==h else h*.9)

def main():
    header=['// Copyright 2026 Luke Steuber. MIT License. Generated from source Bézier geometry.']
    for name,(w,h,mono) in SIZES.items():
        im,hours,minutes,spans,throat_y,r,caption_y=make(w,h,mono)
        (ROOT/'resources'/f'{name}.bin').write_bytes(im.tobytes())
        rgb=Image.new('RGB',(w,h));rgb.putdata([(255*p,)*3 if mono else (((p>>4)&3)*85,((p>>2)&3)*85,(p&3)*85) for p in im.getdata()]);rgb.save(ROOT/'build'/f'art-{name}.png')
        header += [f'#ifdef PBL_PLATFORM_{name.upper()}',f'#define ART_WIDTH {w}',f'#define ART_HEIGHT {h}',f'#define THROAT_Y {throat_y}',f'#define FLOWER_R {r}',f'#define CAPTION_Y {caption_y}']
        for label,values,width in [('HOURS',hours,3),('MINUTES',minutes,2),('THROAT',spans,4)]:
            header.append(f'static const int16_t {label}[{len(values)}][{width}]={{'+','.join('{'+','.join(map(str,v))+'}' for v in values)+'};')
        header.append('#endif')
    (ROOT/'src/c/geometry.h').write_text('\n'.join(header)+'\n')
    icon=Image.new('1',(25,25));d=ImageDraw.Draw(icon)
    d.ellipse((2,4,11,16),fill=1);d.ellipse((13,4,22,16),fill=1);d.ellipse((8,12,16,23),fill=1);d.ellipse((10,0,14,13),fill=1)
    icon.save(ROOT/'resources/menu-icon.png')

if __name__=='__main__':main()
