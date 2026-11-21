# Module 2 - phone-style synthetic camera study

Repository: https://github.com/aabdelkarem/csc8830-module2-camera-calibration

**All camera images in this package are synthetic, not physical phone photos.**
Aya reports that the instructor permits synthetic images if they resemble phone
captures. This package uses that reported allowance and preserves disclosure.
The approval was reported by Aya; no teacher message is included or attributed.

[Report PDF](Module_2_SIMULATION_Report.pdf) | [Demonstration video](Module_2_Application_Demo_SIMULATED.mp4) | [Requirement checklist](REQUIREMENTS_CHECKLIST.md)

## What is complete

- Sixteen 1280 x 960 checkerboard views with varied poses, a generated oak
  surface, paper texture, soft shadows, lens distortion, blur, sensor-like noise
  and JPEG artifacts. All images retain a synthetic-data label.
- Actual OpenCV corner detection, subpixel refinement and camera calibration.
- A separate navy rectangular target at a defined virtual axial depth of 3 m.
  Its four corners are detected from image pixels, then undistorted for dimension
  estimation. True object dimensions are used only to calculate validation error.
- An updated PDF report and a verified 55.8-second captioned application-output
  recording of the executed computation.
- Commented source, original generated surface material, configurations, exact
  results, input checksums and demonstration validation records.

## Reproduce

Download the complete repository using **Code > Download ZIP**, then extract it.
Run `prepare_data.py` once to restore the packaged data into their folders.
The root files beginning `module2_upload__` are the exact packaged inputs and
outputs; the setup script checks their SHA-256 hashes before copying them.
It preserves existing files and does not use the network. The full handoff ZIP
already has the folder layout, so the same setup step safely does nothing there.

The generated surface material is required at `assets/oak_surface_generated.png`.

```sh
python prepare_data.py
python -m pip install -r requirements.txt
python render_and_run.py
python record_demo.py
```

Use `python record_demo.py --show` to display the running application's output.
The video records those rendered computation states with reading holds. It is
not an OS desktop screen capture and does not contain student narration.
The tested package versions are in `TESTED_ENVIRONMENT.json`.

## Code and files

| File or folder | Purpose |
| --- | --- |
| `prepare_data.py` | Restore and check packaged data folders after downloading |
| `phone_scene.py` | Exact camera/scene renderer and image-based target corner detection |
| `render_and_run.py` | Reproduce images, calibration, validation and PDF report |
| `cv_course.py` | OpenCV calibration and perspective measurement implementation |
| `record_demo.py` | Rerun the computation and record its application output |
| `assets/` | Generated photographic surface material and its provenance |
| `images/` | The 16 input checkerboard views and separate target image |
| `configs/` | Exact settings used by the numerical functions |
| `outputs/` | Fitted camera, detected corner overlays and measurement results |
| `SIMULATION_GROUND_TRUTH.json` | Defined camera, distortion, poses and target geometry |
| `SIMULATION_RESULTS.json` | Executed numerical results |
| `IMAGE_SHA256.json` | Input image checksums |
| `DEMO_RECORDING_VALIDATION.json` | Video checks, events and source checksums |
| `Module_2_SIMULATION_Report.pdf` | Written method, results, limitations and repository link |
| `Module_2_Application_Demo_SIMULATED.mp4` | Captioned working-application demonstration |
| `real_capture/` | Optional printable target and physical capture checklist |

## Modeling assumptions

Camera intrinsics are fx=1600, fy=1580, cx=640 and cy=480 pixels. The virtual
lens uses k1=-0.07, k2=0.02, p1=0.0006, p2=-0.0004 and k3=0. Calibration
estimates the first four distortion terms while fixing k3 to zero. This is an
explicit model restriction; no true focal length or principal point is supplied
to the calibration function. Checkerboard square size is a scene parameter,
20 mm, with 9 x 6 inner corners.

The target is a front-facing navy rectangle with defined width 0.600 m and
height 0.400 m at virtual depth 3.000 m. Color segmentation and subpixel corner
refinement provide the observed points used by the dimension estimator.
Renderer-projected true corners are retained separately to audit pixel error.

The generated oak image supplies appearance only. It does not supply camera
intrinsics, square counts, object dimensions or measurements. Those are explicit
geometry in the renderer. The material boundary is reflected to avoid hard
repeat seams. Noise, blur, shading and compression are modeled; focus variation
and physical tape-measure errors are not. Synthetic accuracy is not evidence of
physical smartphone accuracy. There is no claimed phone EXIF or device model.

## Coursework materials

The PDF report and MP4 demonstration accompany this repository. Keep the source,
assets, images, configurations and output folders together when reproducing the
work. The synthetic-data disclosure applies to every result in this package.

Review the implementation and results. Review the work and describe actual
contributions accurately.

Sources: [Module 2 assignment](https://docs.google.com/document/d/1p7qrP2FnPR7qcx3Xm8qgpkcufIaLAPvUaH_0kGzYxBw/edit)
and [OpenCV calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).
