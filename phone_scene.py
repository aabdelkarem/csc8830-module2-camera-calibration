"""Controlled photographic-style camera simulation with exact scene geometry.

An image-generated oak material is a surface texture only. The camera, poses,
printed checkerboard, object boundary, distortion and noise are explicitly
computed here. These outputs are not photographs from a physical phone.
"""
from pathlib import Path
import hashlib
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parent
SIZE=(1280,960)
K=np.array([[1600.,0.,640.],[0.,1580.,480.],[0.,0.,1.]])
DIST=np.array([-.07,.02,.0006,-.0004,0.])
SQUARE=.020

def project(world,r,t):
    return cv2.projectPoints(np.asarray(world,float),np.asarray(r,float),
        np.asarray(t,float),K,DIST)[0].reshape(-1,2)

def maps(r,t):
    """Cast distorted sensor rays onto the board/table plane in world metres."""
    yy,xx=np.indices(SIZE[::-1],dtype=np.float32)
    xy=cv2.undistortPoints(np.stack((xx,yy),axis=-1).reshape(-1,1,2),K,DIST)
    rays=np.column_stack((xy.reshape(-1,2),np.ones(SIZE[0]*SIZE[1])))
    R=cv2.Rodrigues(np.asarray(r,float))[0];normal=R[:,2]
    depth=np.dot(normal,t)/(rays@normal)
    xyz=(rays*depth[:,None]-np.asarray(t))@R
    return xyz[:,0].reshape(SIZE[::-1]).astype(np.float32),xyz[:,1].reshape(SIZE[::-1]).astype(np.float32)

def material(x,y,seed):
    tex=cv2.imread(str(ROOT/'assets/oak_surface_generated.png'))
    if tex is None:raise RuntimeError('Missing generated surface asset')
    h,w=tex.shape[:2]
    # Reflect the outer material boundary instead of repeating a visible tile seam.
    u=(x/1.5+.52)*(w-1);v=(y/1.125+.51)*(h-1)
    image=cv2.remap(tex,u.astype(np.float32),v.astype(np.float32),cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REFLECT_101)
    return image.astype(np.float32)

def paper(image,x,y,bounds,texture):
    x0,y0,x1,y1=bounds
    inside=((x>=x0)&(x<=x1)&(y>=y0)&(y<=y1)).astype(np.float32)
    # A soft displaced contact shadow makes the mounted paper visibly separate.
    shadow=cv2.GaussianBlur(inside,(0,0),4.5)
    shadow=np.roll(np.roll(shadow,5,axis=0),4,axis=1)*(1-inside)
    image*=1-.26*shadow[...,None]
    h,w=texture.shape[:2]
    u=(x-x0)/(x1-x0)*(w-1);v=(y-y0)/(y1-y0)*(h-1)
    foreground=cv2.remap(texture,u.astype(np.float32),v.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    # Subpixel boundary blending is a rendering operation, not recovered evidence.
    alpha=cv2.GaussianBlur(inside,(0,0),.42)
    return image*(1-alpha[...,None])+foreground.astype(float)*alpha[...,None]

def finish(image,seed,caption):
    rng=np.random.default_rng(seed)
    yy,xx=np.indices(SIZE[::-1],dtype=float)
    xn=(xx-640)/640;yn=(yy-480)/480
    lighting=(1+.045*xn-.025*yn)*(1-.035*(xn*xn+yn*yn))
    image=image*lighting[...,None]
    image=cv2.GaussianBlur(image.astype(np.float32),(0,0),.38)
    image+=rng.normal(0,1.25,image.shape)
    image=np.clip(image,0,255).astype(np.uint8)
    ok,encoded=cv2.imencode('.jpg',image,[cv2.IMWRITE_JPEG_QUALITY,94])
    assert ok
    image=cv2.imdecode(encoded,cv2.IMREAD_COLOR)
    cv2.rectangle(image,(0,906),(1279,959),(38,42,47),-1)
    cv2.putText(image,'SYNTHETIC CAMERA IMAGE - NOT A PHYSICAL PHONE PHOTO',
        (18,929),cv2.FONT_HERSHEY_SIMPLEX,.52,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(image,caption,(18,950),cv2.FONT_HERSHEY_SIMPLEX,.43,(223,228,232),1,cv2.LINE_AA)
    return image

def board_texture():
    # Physical bounds: [-.03,.19] x [-.03,.13], with a 10 mm white border.
    w,h=2200,1600
    yy,xx=np.indices((h,w))
    im=np.empty((h,w,3),np.float32);im[:]=(239,244,246)
    mask=(xx>=100)&(xx<2100)&(yy>=100)&(yy<1500)
    black=(((xx-100)//200+(yy-100)//200)%2==0)&mask
    im[black]=(24,25,25)
    noise=np.random.default_rng(3401).normal(0,.7,(h,w,1))
    im=np.clip(im+noise,0,255).astype(np.uint8)
    cv2.putText(im,'CAMERA CALIBRATION  /  20 mm squares',(180,62),cv2.FONT_HERSHEY_SIMPLEX,.8,(105,105,105),1,cv2.LINE_AA)
    return im

def target_texture():
    # The navy inner rectangle, not the paper margin, is the measured object.
    im=np.full((880,1280,3),(240,244,246),np.uint8)
    cv2.rectangle(im,(40,40),(1239,839),(116,64,28),-1)
    cv2.putText(im,'DIMENSION TARGET',(235,390),cv2.FONT_HERSHEY_SIMPLEX,1.55,(237,239,242),3,cv2.LINE_AA)
    cv2.putText(im,'MODULE 2',(470,475),cv2.FONT_HERSHEY_SIMPLEX,1.0,(217,226,230),2,cv2.LINE_AA)
    return im

def find_target(image):
    b,g,r=cv2.split(image.astype(np.int16))
    mask=((b-r>32)&(b-g>20)&(b>55)&(b<180)).astype(np.uint8)*255
    mask[900:]=0
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c=max(contours,key=cv2.contourArea)
    p=cv2.approxPolyDP(c,.02*cv2.arcLength(c,True),True).reshape(-1,2).astype(np.float32)
    if len(p)!=4:raise RuntimeError('Expected four visible target corners')
    # Order clockwise starting at top-left, independently of known target geometry.
    center=p.mean(0);p=p[np.argsort(np.arctan2(p[:,1]-center[1],p[:,0]-center[0]))]
    p=np.roll(p,-int(np.argmin(p.sum(1))),axis=0)
    p=np.ascontiguousarray(p.reshape(4,1,2),dtype=np.float32)
    p=cv2.cornerSubPix(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY),p,(5,5),(-1,-1),
        (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,50,1e-4)).reshape(-1,2)
    return p.astype(float)

def render(provenance):
    out=ROOT/'images/calibration';out.mkdir(parents=True,exist_ok=True)
    texture=board_texture();poses=[]
    centers=[(640,450),(450,330),(820,340),(450,600),(830,590),
        (620,300),(640,650),(410,460),(880,460),(520,370),(760,570),
        (530,590),(790,350),(620,460),(480,470),(810,470)]
    for i,(u,v) in enumerate(centers):
        r=np.array([.32*np.sin(i*1.4+.3),.39*np.cos(i*.9),.18*np.sin(i*.73)])
        z=.57+.012*(i%7)
        center_cam=np.array([(u-K[0,2])/K[0,0]*z,(v-K[1,2])/K[1,1]*z,z])
        t=center_cam-cv2.Rodrigues(r)[0]@np.array([.08,.05,0])
        edge=project([[-.03,-.03,0],[.19,-.03,0],[.19,.13,0],[-.03,.13,0]],r,t)
        assert edge[:,0].min()>15 and edge[:,0].max()<1265
        assert edge[:,1].min()>15 and edge[:,1].max()<895
        x,y=maps(r,t);im=paper(material(x,y,i),x,y,(-.03,-.03,.19,.13),texture)
        im=finish(im,1000+i,'Controlled virtual camera | checkerboard view %02d | generated surface material'%(i+1))
        name='sim_checkerboard_%02d.png'%(i+1)
        assert cv2.imwrite(str(out/name),im)
        poses.append({'image':'images/calibration/'+name,'rvec_world_to_camera':r.tolist(),
                      't_world_to_camera_m':t.tolist()})
    r=np.zeros(3);t=np.array([0.,0.,3.])
    x,y=maps(r,t);im=paper(material(x,y,90),x,y,(-.32,-.22,.32,.22),target_texture())
    im=finish(im,1090,'Held-out navy rectangle | virtual axial depth 3.000 m | corners detected from pixels')
    observed=find_target(im)
    true=project([[-.3,-.2,0],[.3,-.2,0],[.3,.2,0],[-.3,.2,0]],r,t)
    assert np.max(np.linalg.norm(observed-true,axis=1))<3
    assert cv2.imwrite(str(ROOT/'images/sim_object_at_3m.png'),im)
    return {'provenance':provenance,'camera_model':'virtual pinhole with Brown-Conrady distortion',
        'image_size_px':list(SIZE),'K_ground_truth':K.tolist(),'distortion_ground_truth':DIST.tolist(),
        'square_size_m':SQUARE,'inner_corner_shape':[9,6],'calibration_poses':poses,
        'appearance':{'material':'image-generated oak surface; not a physical capture',
            'material_sha256':hashlib.sha256((ROOT/'assets/oak_surface_generated.png').read_bytes()).hexdigest(),
            'sensor_noise_std':1.25,'jpeg_quality':94,'blur_sigma_px':.38,
            'note':'Photographic appearance is simulated. Camera geometry is defined analytically, not inferred from image-generation prompts.'},
        'target':{'image':'images/sim_object_at_3m.png','width_m':.6,'height_m':.4,'axial_depth_m':3.,
            'corners_tl_tr_br_bl':observed.tolist(),'projected_ground_truth_corners':true.tolist(),
            'corner_detection_max_error_px':float(np.max(np.linalg.norm(observed-true,axis=1))),
            'corner_source':'navy-color segmentation, quadrilateral contour and subpixel refinement; ground-truth corners used only to check error'}}
