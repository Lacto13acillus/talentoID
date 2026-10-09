# app/utils/draw_gate.py
# Visualisasi gate cone, trajectory bola, panah passing, dan panel statistik
import cv2
import numpy as np
from typing import Tuple, List, Optional


def draw_rounded_rect(img, pt1, pt2, color, radius, thickness=-1):
    x1,y1 = pt1; x2,y2 = pt2
    r = min(radius, (x2-x1)//2, (y2-y1)//2)
    if r < 1: cv2.rectangle(img, pt1, pt2, color, thickness); return
    if thickness == -1:
        cv2.rectangle(img, (x1+r,y1), (x2-r,y2), color, -1)
        cv2.rectangle(img, (x1,y1+r), (x2,y2-r), color, -1)
        cv2.circle(img, (x1+r,y1+r), r, color, -1)
        cv2.circle(img, (x2-r,y1+r), r, color, -1)
        cv2.circle(img, (x1+r,y2-r), r, color, -1)
        cv2.circle(img, (x2-r,y2-r), r, color, -1)
    else:
        cv2.line(img,(x1+r,y1),(x2-r,y1),color,thickness)
        cv2.line(img,(x1+r,y2),(x2-r,y2),color,thickness)
        cv2.line(img,(x1,y1+r),(x1,y2-r),color,thickness)
        cv2.line(img,(x2,y1+r),(x2,y2-r),color,thickness)
        cv2.ellipse(img,(x1+r,y1+r),(r,r),180,0,90,color,thickness)
        cv2.ellipse(img,(x2-r,y1+r),(r,r),270,0,90,color,thickness)
        cv2.ellipse(img,(x1+r,y2-r),(r,r),90,0,90,color,thickness)
        cv2.ellipse(img,(x2-r,y2-r),(r,r),0,0,90,color,thickness)


def draw_gate_on_frame(frame, gate_cone_left, gate_cone_right, is_active=False,
                       gate_color_normal=(0,220,255), gate_color_active=(0,255,80),
                       alpha=0.30, line_thickness=2, show_width_label=True):
    output = frame.copy()
    color = gate_color_active if is_active else gate_color_normal
    gl = (int(gate_cone_left[0]), int(gate_cone_left[1]))
    gr = (int(gate_cone_right[0]), int(gate_cone_right[1]))
    gh = 70
    poly = np.array([gl, gr, (gr[0],gr[1]-gh), (gl[0],gl[1]-gh)], dtype=np.int32)
    ov = output.copy(); cv2.fillPoly(ov, [poly], color)
    cv2.addWeighted(ov, alpha, output, 1-alpha, 0, output)
    cv2.line(output, gl, gr, color, line_thickness+1)
    cv2.circle(output, gl, 10, color, -1); cv2.circle(output, gr, 10, color, -1)
    cv2.circle(output, gl, 12, (255,255,255), 2); cv2.circle(output, gr, 12, (255,255,255), 2)
    return output


def draw_ball_trajectory_on_frame(frame, trajectory, color=(255,120,0), max_points=30, fade=True):
    output = frame.copy()
    recent = trajectory[-max_points:] if len(trajectory) > max_points else trajectory
    n = len(recent)
    if n == 0: return output
    for i, pt in enumerate(recent):
        px, py = int(pt[0]), int(pt[1])
        if fade and n > 1:
            ratio = (i+1)/n; fc = tuple(int(c*ratio) for c in color); pr = max(2, int(5*ratio))
        else: fc = color; pr = 4
        cv2.circle(output, (px,py), pr, fc, -1)
        if i > 0:
            prev = (int(recent[i-1][0]), int(recent[i-1][1]))
            cv2.line(output, prev, (px,py), fc, 1)
    last = (int(recent[-1][0]), int(recent[-1][1]))
    cv2.circle(output, last, 7, color, 2)
    return output


def draw_pass_arrow(frame, from_pos, to_pos, success, from_name, to_name, distance):
    output = frame.copy()
    color = (0,220,0) if success else (0,0,220)
    label = "SUKSES" if success else "GAGAL"
    fp = (int(from_pos[0]), int(from_pos[1]))
    tp = (int(to_pos[0]), int(to_pos[1]))
    cv2.arrowedLine(output, fp, tp, color, 3, tipLength=0.12)
    mx, my = (fp[0]+tp[0])//2, (fp[1]+tp[1])//2
    pl = f"{from_name}->{to_name} | {label}"
    dl = f"{distance:.0f}px"
    (lw,lh),_ = cv2.getTextSize(pl, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(output, (mx-lw//2-3,my-lh-16), (mx+lw//2+3,my-6), (30,30,30), -1)
    cv2.putText(output, pl, (mx-lw//2,my-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    cv2.putText(output, dl, (mx-15,my+12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
    return output


def draw_stats_panel(frame, stats, position=(20,20), panel_width=320):
    output = frame.copy()
    px, py = position; pad = 14
    BG = (25,25,30); BG_H = (50,42,35); ACC = (230,200,0)
    GR = (80,220,60); RD = (70,70,230); YL = (50,210,255)
    WH = (255,255,255); GL = (200,200,200); GM = (140,140,140)
    GD = (70,70,70); BB = (50,50,55)
    pp = stats.get('per_player', {}); np_ = len(pp)
    hh = 44; sh = 70; ah = 42; dp = 12; prh = 50
    psh = (dp+22+prh*np_) if np_ > 0 else 0
    th = hh+sh+ah+psh+12
    x1,y1,x2,y2 = px,py,px+panel_width,py+th
    ov = output.copy(); draw_rounded_rect(ov,(x1,y1),(x2,y2),BG,14)
    cv2.addWeighted(ov,0.88,output,0.12,0,output)
    draw_rounded_rect(output,(x1,y1),(x2,y2),GD,14,thickness=1)
    oh = output.copy(); draw_rounded_rect(oh,(x1+1,y1+1),(x2-1,y1+hh),BG_H,13)
    cv2.rectangle(oh,(x1+1,y1+hh-13),(x2-1,y1+hh),BG_H,-1)
    cv2.addWeighted(oh,0.95,output,0.05,0,output)
    cv2.line(output,(x1+pad,y1+hh),(x2-pad,y1+hh),ACC,2)
    icx,icy = x1+pad+11,y1+hh//2
    cv2.circle(output,(icx,icy),11,YL,-1); cv2.circle(output,(icx,icy),11,WH,1)
    cv2.putText(output,"PASSING ANALYTICS",(icx+18,y1+hh//2+6),cv2.FONT_HERSHEY_SIMPLEX,0.56,WH,2)
    ry = y1+hh+8; cw = (panel_width-2*pad)//3
    tp_ = stats.get('total_passes',0); sp = stats.get('successful_passes',0); fp_ = stats.get('failed_passes',0)
    items = [(tp_,"Total",ACC),(sp,"Sukses",GR),(fp_,"Gagal",RD)]
    for idx,(val,lb,cl) in enumerate(items):
        ccx = x1+pad+idx*cw+cw//2
        vs = str(val); (vw,vh),_ = cv2.getTextSize(vs,cv2.FONT_HERSHEY_SIMPLEX,1.05,2)
        cv2.putText(output,vs,(ccx-vw//2,ry+32),cv2.FONT_HERSHEY_SIMPLEX,1.05,cl,2)
        (lw2,_),_ = cv2.getTextSize(lb,cv2.FONT_HERSHEY_SIMPLEX,0.36,1)
        cv2.putText(output,lb,(ccx-lw2//2,ry+50),cv2.FONT_HERSHEY_SIMPLEX,0.36,GM,1)
    for idx in range(1,3):
        dx = x1+pad+idx*cw; cv2.line(output,(dx,ry+8),(dx,ry+50),GD,1)
    ay = ry+sh; apct = stats.get('accuracy_pct',0.0)
    cv2.putText(output,"Akurasi",(x1+pad,ay+2),cv2.FONT_HERSHEY_SIMPLEX,0.42,GL,1)
    pc = GR if apct >= 70 else (YL if apct >= 40 else RD)
    ps = f"{apct:.0f}%"; (pw,_),_ = cv2.getTextSize(ps,cv2.FONT_HERSHEY_SIMPLEX,0.52,2)
    cv2.putText(output,ps,(x2-pad-pw,ay+3),cv2.FONT_HERSHEY_SIMPLEX,0.52,pc,2)
    bx1,bx2 = x1+pad,x2-pad; by1 = ay+12; by2 = by1+16; btw = bx2-bx1
    draw_rounded_rect(output,(bx1,by1),(bx2,by2),BB,8)
    fw = int(btw*min(apct/100.0,1.0))
    if fw > 6: draw_rounded_rect(output,(bx1,by1),(bx1+fw,by2),pc,8)
    if pp:
        sy = by2+dp; cv2.line(output,(x1+pad,sy),(x2-pad,sy),GD,1); sy += 6
        cv2.putText(output,"Per Pemain",(x1+pad,sy+12),cv2.FONT_HERSHEY_SIMPLEX,0.40,GM,1); sy += 22
        for name, ps2 in pp.items():
            pt2,psc,pac = ps2.get('total',0),ps2.get('success',0),ps2.get('accuracy_pct',0.0)
            bxx,bxy,bxw,bxh = x1+pad,sy+2,50,22
            bc2 = (180,120,0) if '19' in str(name) else (0,120,180)
            ob = output.copy(); draw_rounded_rect(ob,(bxx,bxy),(bxx+bxw,bxy+bxh),bc2,6)
            cv2.addWeighted(ob,0.85,output,0.15,0,output)
            jl = str(name); (jw,_),_ = cv2.getTextSize(jl,cv2.FONT_HERSHEY_SIMPLEX,0.42,1)
            cv2.putText(output,jl,(bxx+(bxw-jw)//2,bxy+16),cv2.FONT_HERSHEY_SIMPLEX,0.42,WH,1)
            rs2 = f"{psc}/{pt2}"; cv2.putText(output,rs2,(bxx+bxw+10,sy+16),cv2.FONT_HERSHEY_SIMPLEX,0.44,GL,1)
            mbx1,mbx2 = bxx+bxw+55,x2-pad-48; mby1 = sy+6; mby2 = mby1+12; mbw = mbx2-mbx1
            draw_rounded_rect(output,(mbx1,mby1),(mbx2,mby2),BB,6)
            mf = int(mbw*min(pac/100.0,1.0)); mc = GR if pac >= 70 else (YL if pac >= 40 else RD)
            if mf > 4: draw_rounded_rect(output,(mbx1,mby1),(mbx1+mf,mby2),mc,6)
            pps = f"{pac:.0f}%"; cv2.putText(output,pps,(x2-pad-40,sy+17),cv2.FONT_HERSHEY_SIMPLEX,0.42,mc,1)
            sy += prh
    return output


def draw_target_cone_on_frame(frame, target_pos, proximity_radius=120.0, is_active=False,
                              color_normal=(0,165,255), color_active=(0,255,80), alpha=0.25):
    output = frame.copy()
    color = color_active if is_active else color_normal
    cx, cy = int(target_pos[0]), int(target_pos[1]); r = int(proximity_radius)
    ov = output.copy(); cv2.circle(ov,(cx,cy),r,color,-1)
    cv2.addWeighted(ov,alpha,output,1-alpha,0,output)
    cv2.circle(output,(cx,cy),r,color,2)
    ll = 18
    cv2.line(output,(cx-ll,cy),(cx+ll,cy),color,2)
    cv2.line(output,(cx,cy-ll),(cx,cy+ll),color,2)
    cv2.circle(output,(cx,cy),10,color,-1); cv2.circle(output,(cx,cy),12,(255,255,255),2)
    lb = "TARGET"; (lw,lh),_ = cv2.getTextSize(lb,cv2.FONT_HERSHEY_SIMPLEX,0.6,2)
    lx,ly = cx-lw//2,cy-r-14
    cv2.rectangle(output,(lx-4,ly-lh-2),(lx+lw+4,ly+4),color,-1)
    cv2.putText(output,lb,(lx,ly),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)
    return output
