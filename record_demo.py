#!/usr/bin/env python3
"""Run Module 2 and record its own visual output as a captioned MP4.

python record_demo.py          # generate the application-output recording
python record_demo.py --show   # also display the actual application window

This reruns corner detection, calibration and dimension estimation. The video
records application-rendered states as computations finish, with reading holds.
It is NOT an OS desktop screen capture and contains no student voice. Every
frame labels the data as SIMULATION. Do not claim physical phone validation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import textwrap
import time
import cv2
import numpy as np
import cv_course as app
import render_and_run as simulation

ROOT=Path(__file__).resolve().parent
FPS=20
SIZE=(1280,720)
BG=(248,251,253);INK=(69,55,35);BLUE=(80,62,23)

def line(canvas,text,x,y,scale=.8,color=INK,bold=False):
    cv2.putText(canvas,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,color,2 if bold else 1,cv2.LINE_AA)

def paragraph(canvas,text,x,y,chars=52,scale=.72,gap=36):
    for row in textwrap.wrap(text,chars):
        line(canvas,row,x,y,scale);y+=gap
    return y

def panel(title):
    image=np.full((720,1280,3),BG,np.uint8)
    cv2.rectangle(image,(0,0),(1279,106),BLUE,-1)
    line(image,'MODULE 2 / '+title,36,49,1.0,(255,255,255),True)
    line(image,'Actual computation: calibration -> perspective projection -> validation',36,84,.61,(235,229,218))
    cv2.rectangle(image,(0,668),(1279,719),(35,79,138),-1)
    line(image,'SIMULATION - NOT SMARTPHONE CAPTURES',28,700,.75,(255,255,255),True)
    line(image,'Application output recording',870,700,.58,(255,255,255))
    return image

def put_image(canvas,image,box):
    x,y,w,h=box
    factor=min(w/image.shape[1],h/image.shape[0])
    resized=cv2.resize(image,(round(image.shape[1]*factor),round(image.shape[0]*factor)))
    hh,ww=resized.shape[:2];left=x+(w-ww)//2;top=y+(h-hh)//2
    canvas[top:top+hh,left:left+ww]=resized

def main(show=False):
    os.chdir(ROOT)
    truth=simulation.render_inputs()
    previous=json.loads(Path('SIMULATION_RESULTS.json').read_text())
    cal_cfg=json.loads(Path('configs/calibration_simulation.json').read_text())
    dim_cfg=json.loads(Path('configs/dimensions_simulation.json').read_text())
    destination=Path('Module_2_Application_Demo_SIMULATED.mp4')
    writer=cv2.VideoWriter(str(destination),cv2.VideoWriter_fourcc(*'mp4v'),FPS,SIZE)
    if not writer.isOpened():raise RuntimeError('MP4 encoding unavailable')
    events=[];frames=0;start=time.perf_counter()

    def capture(canvas,seconds,event):
        nonlocal frames
        n=round(seconds*FPS)
        events.append({'event':event,'first_frame':frames,'frames':n,
                       'computation_elapsed_seconds':time.perf_counter()-start})
        for i in range(n):
            frame=canvas.copy()
            line(frame,'Playback '+str(frames//FPS)+' s',1110,641,.5,(120,100,90))
            writer.write(frame);frames+=1
            if show:
                cv2.imshow('Module 2 - SIMULATED application',frame)
                if cv2.waitKey(round(1000/FPS))&255==27:raise KeyboardInterrupt

    def progress(stage,data,image):
        if stage=='corners':
            number=data['accepted'];f=panel('Corner detection - view %d / 16'%number)
            put_image(f,image,(24,130,812,510))
            line(f,'Detected in this run',860,190,.8,BLUE,True)
            y=255
            for row in ['9 x 6 inner corners','54 points per image','Subpixel refinement','Virtual square: 20 mm','Image size: 1280 x 960']:
                line(f,row,860,y,.66);y+=54
            paragraph(f,'Corners become observations for the camera fit.',860,565,31,.65,29)
            capture(f,.8,'detected_checkerboard_'+str(number))
        elif stage=='calibration':
            f=panel('Estimated camera - actual OpenCV result')
            line(f,'Intrinsic matrix K',54,170,1.0,BLUE,True)
            for i,row in enumerate(data['K']):
                line(f,'[ '+('    '.join('%.4f'%x for x in row))+' ]',75,246+i*62,1.05)
            line(f,'Accepted views: %d of 16'%len(data['accepted']),55,468,.85)
            line(f,'Reprojection RMS: %.6f pixels'%data['rms_px'],55,518,.85)
            paragraph(f,'Low reprojection error is a fit diagnostic. It does not establish real smartphone accuracy.',55,578,90,.74,35)
            capture(f,7,'calibration_completed')
        elif stage=='measurement':
            f=panel('Dimensions from the estimated camera')
            put_image(f,image,(22,138,760,487))
            line(f,'Known virtual depth: 3.000 m',815,186,.72,BLUE,True)
            lines=[('Width truth: 0.600000 m',250),('Estimate: %.6f m'%data['width_m'],295),
                   ('Error: %.4f%%'%data['width_absolute_error_pct'],340),
                   ('Height truth: 0.400000 m',426),('Estimate: %.6f m'%data['height_m'],471),
                   ('Error: %.4f%%'%data['height_absolute_error_pct'],516)]
            for value,y in lines:line(f,value,815,y,.70)
            paragraph(f,'These are simulation errors, not physical measurement errors.',815,582,39,.61,27)
            capture(f,8,'dimensions_completed')

    original_report=app.report
    def report(out,title,sections,pictures=()):
        title='SIMULATION: calibration' if 'calibration' in title.lower() else 'SIMULATION: dimensions'
        original_report(out,title,[('Data provenance',simulation.PROVENANCE)]+sections,pictures)
    app.report=report
    try:
        f=panel('Working application demonstration')
        line(f,'Run the code. Inspect the observations. Check the result.',45,174,.94,BLUE,True)
        y=260
        for row in ['16 virtual checkerboard images -> camera calibration',
                    'Separate virtual target at 3 m -> dimension estimate',
                    'Known virtual dimensions -> error calculation']:
            line(f,row,55,y,.85);y+=83
        paragraph(f,'This recording captures output from an actual execution. Frames are held for reading. It is not a phone experiment or a desktop screen capture.',55,541,90,.70,34)
        capture(f,6,'start')
        app.calibrate(cal_cfg,progress=progress)
        f=panel('Perspective projection method')
        line(f,'u = fx X/Z + cx        v = fy Y/Z + cy',55,197,1.15,BLUE,True)
        y=289
        for row in ['1. Undistort the four image corners into normalized coordinates.',
                    '2. At constant depth Z, side length = Z x normalized span.',
                    '3. Average opposite sides for width and height.',
                    '4. Compare with the separate known simulation dimensions.']:
            y=paragraph(f,row,55,y,84,.78,38)+20
        capture(f,8,'projection_method')
        app.dimensions(dim_cfg,progress=progress)
        dims=json.loads(Path('outputs/dimensions/metrics.json').read_text())
        cal=json.loads(Path('outputs/calibration/metrics.json').read_text())
        assert abs(dims['width_m']-previous['estimated_width_m'])<1e-12
        assert abs(dims['height_m']-previous['estimated_height_m'])<1e-12
        assert len(cal['accepted'])==16
        for cfg in (cal_cfg,dim_cfg):
            path=Path(cfg['out'])/'metrics.json';data=json.loads(path.read_text())
            data.update(data_origin='SIMULATION',provenance=simulation.PROVENANCE)
            path.write_text(json.dumps(data,indent=2)+'\n')
        f=panel('Validation and limitations')
        lines=[('Reproduced the recorded estimates exactly.',180),
               ('Width error: %.4f%% | Height error: %.4f%%'%(dims['width_absolute_error_pct'],dims['height_absolute_error_pct']),244),
               ('Phone-style observations use controlled generated geometry.',320),
               ('Mild noise and lens distortion are modeled; no physical capture occurred.',386)]
        for row,y in lines:line(f,row,50,y,.78)
        paragraph(f,'The fit estimates radial k1/k2 and tangential p1/p2, with k3 fixed to zero. The target corners are detected from the rendered pixels.',50,463,93,.73,37)
        paragraph(f,'Aya reports instructor approval for phone-looking synthetic images. This remains a disclosed simulation, not physical phone evidence.',50,575,91,.71,34)
        capture(f,8,'validation')
        f=panel('Reproduce the working application')
        line(f,'python render_and_run.py',60,203,1.17,BLUE,True)
        line(f,'python record_demo.py --show',60,292,1.07,BLUE,True)
        paragraph(f,'The first command regenerates the images, camera fit, measurements and report. The second runs the computation again and displays/records the application output.',60,381,85,.80,42)
        line(f,'Source code and input data accompany the report.',60,586,.92,(35,79,138),True)
        capture(f,6,'finish')
    finally:
        writer.release()
        if show:cv2.destroyAllWindows()
    capture_video=cv2.VideoCapture(str(destination))
    actual_fps=capture_video.get(cv2.CAP_PROP_FPS);count=0
    while True:
        ok,frame=capture_video.read()
        if not ok:break
        assert frame.shape[:2]==(720,1280)
        count+=1
    capture_video.release()
    assert count==frames and actual_fps==FPS
    result={'file':str(destination),'data_origin':'SIMULATION','frames_decoded':count,'fps':actual_fps,
            'duration_seconds':count/actual_fps,'dimensions':[1280,720],
            'capture_method':'Application-rendered output states captured during actual computation, paced for readability. Not OS desktop screen capture.',
            'audio':'None; explanation is captioned. No student voice is claimed.',
            'actual_execution_reproduced_results':True,'events':events,
            'source_sha256':{name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in ['record_demo.py','cv_course.py','render_and_run.py','phone_scene.py']}}
    Path('DEMO_RECORDING_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['events','source_sha256']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--show',action='store_true')
    main(parser.parse_args().show)
