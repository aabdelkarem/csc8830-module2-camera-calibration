# Module 2 requirement mapping

Assignment: https://docs.google.com/document/d/1p7qrP2FnPR7qcx3Xm8qgpkcufIaLAPvUaH_0kGzYxBw/edit

This package is a disclosed synthetic camera study. Aya reports instructor
permission to use synthetic images that resemble phone captures. The written
assignment itself specifies a smartphone experiment; no physical capture or
tape-measured distance is claimed here.

| Requirement | Prepared evidence |
| --- | --- |
| Step 1: camera calibration with OpenCV or MATLAB | OpenCV estimates intrinsics and distortion from 16 generated checkerboard views; see `outputs/calibration/` |
| Step 2: implement perspective-based 2D dimension estimation | `cv_course.py` undistorts image-detected target corners and uses known depth to estimate width and height |
| Step 3: validate with an object at a distance greater than 2 m | A separate virtual target is placed at a defined 3.000 m axial depth; estimated dimensions are compared with independent scene dimensions |
| Commented source and execution documentation | Root Python files and `README.md`; run `python prepare_data.py` once, then `python render_and_run.py` and `python record_demo.py` |
| Working-system demonstration | `Module_2_Application_Demo_SIMULATED.mp4`: 55.8 seconds of actual application-output states, with captions |
| PDF containing an accessible repository link | `Module_2_SIMULATION_Report.pdf` |
| PDF and video submission in Classroom | Reserved for Aya; the assistant must not turn in the assignment |

## Reproducibility checks

- All 16 views were accepted by checkerboard detection.
- Reprojection RMS: 0.1973689171 pixels.
- Estimated width: 0.6006721815 m; error: 0.1120302544%.
- Estimated height: 0.4015272125 m; error: 0.3818031341%.
- The separate target corners were detected from pixels, not copied from
  ground-truth projected coordinates.
- `IMAGE_SHA256.json` and `DEMO_RECORDING_VALIDATION.json` identify the input
  images and the source used to produce the demonstration.

These are simulation errors and do not establish physical smartphone accuracy.
The recording is application-output capture, not an OS desktop screen recording,
and contains no claimed student narration.
