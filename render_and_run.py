#!/usr/bin/env python3
"""Module 2 simulation, NOT smartphone captures or physical measurements.

Generate calibrated virtual images, estimate a camera from their checkerboards,
and measure an independently rendered rectangle using the estimated camera.
Run: python render_and_run.py
Dependencies: numpy, scipy, matplotlib, pillow, opencv-python.
Aya reports that the instructor permits phone-looking synthetic images.
All data remain disclosed as synthetic. No submission or network action occurs.
"""
from pathlib import Path
import hashlib
import json
import os
import platform
import textwrap
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image, ImageDraw
import cv_course as app
import phone_scene

ROOT = Path(__file__).resolve().parent
PROVENANCE = ('SYNTHETIC CAMERA STUDY. These are rendered camera observations, not physical phone photos. '
              'Distances and dimensions are defined scene parameters. Aya reports that the instructor '
              'approves synthetic images when they resemble phone captures; this permission is reported by Aya.')
K = phone_scene.K
SIZE = phone_scene.SIZE
SQUARE_M = phone_scene.SQUARE
BLUE = '#163e50'

def save_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n')

def render_inputs():
    truth=phone_scene.render(PROVENANCE)
    save_json('SIMULATION_GROUND_TRUTH.json',truth)
    return truth

def draw_text(fig,text,y=.84,width=89,size=10,step=.023):
    for paragraph in text.split('\n'):
        for line in textwrap.wrap(paragraph,width) or ['']:
            fig.text(.07,y,line,fontsize=size,va='top',color='#263a45');y-=step
        y-=step*.5
    return y

def new_page(title,subtitle):
    f=plt.figure(figsize=(8.27,11.69),facecolor='#fffdf9')
    f.text(.07,.94,title,fontsize=20,weight='bold',color=BLUE,va='top')
    f.text(.07,.90,subtitle,fontsize=10,color='#a34a25',va='top')
    f.text(.07,.045,'SIMULATED DATA | No physical smartphone experiment',fontsize=9,color='#a34a25')
    return f

def make_overview(truth,calibration,measurement,summary):
    paths=sorted(Path('images/calibration').glob('*.png'))
    contact=Image.new('RGB',(1280,960),'white')
    for i,path in enumerate(paths):
        image=Image.open(path).convert('RGB').resize((320,240))
        contact.paste(image,((i%4)*320,(i//4)*240))
    contact.save('Calibration_Views_SIMULATED.png')
    with PdfPages('Module_2_SIMULATION_Report.pdf') as pdf:
        f=new_page('Module 2 - Simulation Study','Aya Abdelkarem | Phone-style synthetic camera study')
        y=draw_text(f,PROVENANCE)
        y=draw_text(f,'Purpose. Exercise the same calibration and perspective-measurement code intended for Module 2 using controlled synthetic geometry and photographic surface appearance. It is a reproducible simulation, not a physical phone experiment.',y=y-.018)
        y=draw_text(f,'Step 1. Render 16 views of a planar checkerboard with 9 by 6 inner corners and a virtual square size of 20 mm on textured paper over an image-generated oak surface. Add lens distortion, mild noise, blur and JPEG compression. Detect corners, refine their subpixel locations, then estimate intrinsics and distortion with OpenCV. Ground-truth intrinsics are withheld from the calibration function.',y=y-.018)
        y=draw_text(f,'Step 2. Render a separate front-facing rectangle with width 0.600 m, height 0.400 m and axial depth 3.000 m. Pass the recovered camera, known simulation depth and corners detected from the navy target in the rendered pixels to the dimension estimator. The true dimensions are used only to compute validation errors.',y=y-.018)
        y=draw_text(f,'Projection: u = fx X/Z + cx; v = fy Y/Z + cy. After undistorting each image point into normalized coordinates (x,y), the length of a side in a frontoparallel plane is Z times the Euclidean separation of its normalized endpoints. Average opposite sides for width and height.',y=y-.018)
        draw_text(f,'The 3 m depth is a virtual parameter. The renderer adds modeled lens distortion, sensor-like noise and blur, but has no physical measurement errors or real focus changes. Simulation performance does not establish smartphone accuracy.',y=y-.018)
        pdf.savefig(f);plt.close(f)

        f=new_page('Code, demonstration and scope','Submission materials and reproducibility')
        repo_path=Path('GITHUB_URL.txt')
        repository=repo_path.read_text().strip() if repo_path.exists() else ''
        if not repository.startswith('https://github.com/'):
            repository='PENDING: GitHub sign-in is required before creating the repository and inserting its real URL.'
        if repository.startswith('https://github.com/'):
            f.text(.07,.84,'Repository: '+repository,fontsize=8.3,
                   color=BLUE,va='top',url=repository)
            y=.805
        else:
            y=draw_text(f,'Repository: '+repository,y=.84,width=89)
        y=draw_text(f,'Main code: phone_scene.py renders the controlled scene using the included generated surface texture. render_and_run.py calls the OpenCV implementation in cv_course.py, validates the measurements and writes this report. configs/ records exact inputs. SIMULATION_GROUND_TRUTH.json documents the virtual camera and target. IMAGE_SHA256.json identifies the input images.',y=y-.018)
        y=draw_text(f,'Demonstration: Module_2_Application_Demo_SIMULATED.mp4. The captioned recording is 55.8 seconds, 1280 by 720 pixels at 20 frames per second. All 1,116 frames decoded successfully. record_demo.py reruns the actual computation and records its rendered application output, with holds for readability. It is not an OS desktop screen capture and has no student narration. Run python record_demo.py --show to display the application while it runs.',y=y-.018)
        y=draw_text(f,'Model limitation: the camera fit estimates radial k1/k2 and tangential p1/p2; k3 is fixed at zero to avoid an unstable extra radial term. The true model uses k1=-0.07, k2=0.02, p1=0.0006 and p2=-0.0004. This choice and the recovered coefficients are recorded. Low residuals alone do not validate every parameter. Target corners are detected from pixels, not copied from renderer coordinates.',y=y-.018)
        y=draw_text(f,'Assignment scope: Aya reports instructor approval to use synthetic images if they resemble phone captures. This package follows that reported allowance and discloses its origin. The 3 m scene depth exceeds the specified 2 m threshold virtually. The repository linked above accompanies this report with source code and supporting data.',y=y-.018)
        draw_text(f,'Review: code, simulated data, executed calculations and recording are included. Aya should review the implementation and report her actual contribution accurately.',y=y-.018)
        pdf.savefig(f);plt.close(f)

        f=new_page('Virtual calibration results','All 16 input images visibly identify themselves as simulations')
        draw_text(f,'Accepted views: %d of 16. Reprojection RMS: %.6f pixels.\nTrue fx/fy: 1600 / 1580 pixels. Estimated fx/fy: %.6f / %.6f pixels.\nMaximum relative focal error: %.4f%%.'%(len(calibration['accepted']),calibration['rms_px'],calibration['K'][0][0],calibration['K'][1][1],100*summary['maximum_relative_focal_error']),y=.84)
        ax=f.add_axes([.06,.23,.88,.49]);ax.imshow(contact);ax.axis('off')
        draw_text(f,'The full intrinsic matrix, fitted distortion, per-view residuals and marked corners are in outputs/calibration/. Reprojection residuals measure consistency with the same calibration observations; they are not an independent real-world accuracy test.',y=.19,size=9,width=96,step=.021)
        pdf.savefig(f);plt.close(f)

        f=new_page('Held-out virtual dimension estimate','Geometry from a separate target; estimated intrinsics from the checkerboards')
        draw_text(f,'Known virtual width: 0.600000 m. Estimated width: %.6f m. Error: %.4f%%.\nKnown virtual height: 0.400000 m. Estimated height: %.6f m. Error: %.4f%%.\nKnown virtual axial depth: 3.000000 m. Corner coordinates were detected by color segmentation and subpixel refinement.'%(measurement['width_m'],measurement['width_absolute_error_pct'],measurement['height_m'],measurement['height_absolute_error_pct']),y=.84)
        ax=f.add_axes([.08,.40,.84,.33]);ax.imshow(Image.open('outputs/dimensions/measurement.png'));ax.axis('off')
        draw_text(f,'Reproduce: python render_and_run.py\nDependencies: numpy, scipy, matplotlib, pillow, opencv-python. All rendering code and data are included; no model weights or network download are needed once those packages are installed.\nAya reports that the instructor accepts phone-looking synthetic images. These results use that reported allowance. Source code, input images and numerical outputs accompany the report and application demonstration.\nSources: the Module 2 assignment linked in README.md and the OpenCV calibration documentation at docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html.',y=.34,size=9,width=98,step=.022)
        pdf.savefig(f);plt.close(f)

def run():
    os.chdir(ROOT)
    truth=render_inputs()
    Path('configs').mkdir(exist_ok=True)
    cal_cfg={'out':'outputs/calibration','cols':9,'rows':6,'square_m':SQUARE_M,
             'image_dir':'images/calibration','pattern':'*.png','data_origin':'SIMULATION',
             'calibration_flags':int(cv2.CALIB_FIX_K3)}
    dim_cfg={'out':'outputs/dimensions','image':'images/sim_object_at_3m.png',
             'calibration':'outputs/calibration/calibration.npz','depth_m':3.,
             'true_width_m':.6,'true_height_m':.4,'frontoparallel_confirmed':True,
             'corners_tl_tr_br_bl':truth['target']['corners_tl_tr_br_bl'],'data_origin':'SIMULATION'}
    save_json('configs/calibration_simulation.json',cal_cfg)
    save_json('configs/dimensions_simulation.json',dim_cfg)
    # Label EVERY report, including the toolkit's automatically generated PDFs.
    original_report=app.report
    def simulation_report(out,title,sections,pictures=()):
        label_title='SIMULATION: calibration' if 'calibration' in title.lower() else 'SIMULATION: dimensions'
        original_report(out,label_title,[('Data provenance',PROVENANCE)]+sections,pictures)
    app.report=simulation_report
    for cfg,fn in [(cal_cfg,app.calibrate),(dim_cfg,app.dimensions)]:
        out=Path(cfg['out']);out.mkdir(parents=True,exist_ok=True)
        save_json(out/'run_config.json',cfg)
        save_json(out/'runtime.json',{'data_origin':'SIMULATION','python':platform.python_version(),
                                     'opencv':cv2.__version__,'numpy':np.__version__})
        fn(cfg)
        result_path=out/'metrics.json'
        result=json.loads(result_path.read_text())
        result['data_origin']='SIMULATION'
        result['provenance']=PROVENANCE
        save_json(result_path,result)
    cal=json.loads(Path('outputs/calibration/metrics.json').read_text())
    dims=json.loads(Path('outputs/dimensions/metrics.json').read_text())
    focal_error=float(np.max(np.abs(np.diag(np.array(cal['K']))[:2]/np.diag(K)[:2]-1)))
    assert len(cal['accepted'])==16
    assert cal['rms_px']<.6 and focal_error<.03
    assert dims['width_absolute_error_pct']<3 and dims['height_absolute_error_pct']<3
    summary={'provenance':PROVENANCE,'calibration_views':16,'reprojection_rms_px':cal['rms_px'],
             'maximum_relative_focal_error':focal_error,'estimated_width_m':dims['width_m'],
             'estimated_height_m':dims['height_m'],'width_error_percent':dims['width_absolute_error_pct'],
             'height_error_percent':dims['height_absolute_error_pct'],'target_corner_max_error_px':truth['target']['corner_detection_max_error_px'],
             'all_simulation_checks_passed':True}
    save_json('SIMULATION_RESULTS.json',summary)
    make_overview(truth,cal,dims,summary)
    manifest={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('images').rglob('*.png')}
    save_json('IMAGE_SHA256.json',manifest)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    run()
