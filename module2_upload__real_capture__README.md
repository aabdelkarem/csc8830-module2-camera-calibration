# Optional real-camera capture kit

These are optional preparation materials, not completed physical experimental
results. Aya reports that the instructor accepts phone-looking synthetic images;
the main report follows that reported allowance. This kit is available for a
separate physical validation experiment if desired.

1. Print `Print_Checkerboard_20mm_Letter.pdf` at 100% / Actual Size, landscape.
2. Follow `Real_Photo_Checklist_and_Measurements.pdf` and fill its second page.
3. Supply 20-25 original calibration photos, two object photos, and your real
   measurements. Use one smartphone and the same camera settings throughout.

`measurements_to_fill.json` is an optional typed alternative to the paper sheet.
Its null values are deliberate: no real phone or measurements have been supplied.

The target is 10 by 7 squares with 9 by 6 inner corners. The intended printed
square is 20 mm. Measure the print; printer scaling can change its actual size.
The board PDF uses US Letter landscape with ample margins. The checkerboard
itself spans exactly 200 by 140 mm in the PDF; the scale bar is exactly 100 mm.

The existing `../cv_course.py` calibration and dimensions commands can process
the real data after we create configurations with the actual filenames and
measurements. Do not run `render_and_run.py` on real photographs: that separate
script regenerates the simulation dataset.

The capture kit does not change the existing simulated results. If real data are
later processed, report those actual results separately and identify their
source accurately. The repository URL is in `../GITHUB_URL.txt`; no Classroom
submission occurs.

Reference: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
