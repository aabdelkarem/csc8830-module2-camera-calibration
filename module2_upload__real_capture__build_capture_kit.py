"""Create exact-scale print target and the real-camera collection guide.

These files are capture aids, not photographs or experimental results.
Run with the same matplotlib environment as the Module 2 toolkit.
"""
from pathlib import Path
import json
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent
TEAL = '#153d4b'
INK = '#243842'
RUST = '#9c501d'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42})

def board():
    width, height = 279.4, 215.9  # US Letter landscape, millimetres
    fig = plt.figure(figsize=(width/25.4, height/25.4), facecolor='white')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, width), ylim=(0, height))
    ax.axis('off')
    ax.text(width/2, 205, 'MODULE 2 / PRINTABLE CALIBRATION BOARD',
            ha='center', fontsize=15, weight='bold', color=TEAL)
    ax.text(width/2, 198, '10 x 7 squares | 9 x 6 inner corners | 20 mm intended square size',
            ha='center', fontsize=9, color=INK)
    left, bottom, square = (width-200)/2, 50, 20
    for row in range(7):
        for col in range(10):
            ax.add_patch(Rectangle((left+col*square, bottom+row*square), square, square,
                         facecolor='black' if (row+col)%2 == 0 else 'white',
                         edgecolor='none', antialiased=False))
    ax.text(width/2, 40, 'The checkerboard above must measure 200 mm wide x 140 mm high.',
            ha='center', fontsize=9, color=INK)
    x0 = width/2-50
    ax.plot([x0, x0+100], [29, 29], color='black', lw=1)
    for x in [x0, x0+100]:
        ax.plot([x, x], [27, 31], color='black', lw=1)
    ax.text(width/2, 22, 'Scale check: this line must measure 100 mm after printing',
            ha='center', fontsize=9, color=INK)
    ax.text(width/2, 11, 'PRINT AT 100% / ACTUAL SIZE, LANDSCAPE. DO NOT USE FIT TO PAGE.',
            ha='center', fontsize=10, weight='bold', color=RUST)
    fig.savefig(ROOT/'Print_Checkerboard_20mm_Letter.pdf')
    plt.close(fig)

def page(title, subtitle, number):
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.text(.08, .94, title, fontsize=20, weight='bold', color=TEAL)
    fig.text(.08, .905, subtitle, fontsize=10, color=RUST)
    fig.text(.08, .045, 'Module 2 | Real-camera capture aid | No real experiment has been recorded yet',
             fontsize=8, color=INK)
    fig.text(.92, .045, str(number), ha='right', fontsize=8, color=INK)
    return fig

def block(fig, y, title, text):
    fig.text(.08, y, title, fontsize=11, weight='bold', color=TEAL)
    y -= .027
    for line in textwrap.wrap(text, 98):
        fig.text(.08, y, line, fontsize=9.2, color=INK)
        y -= .019
    return y - .018

def guide():
    with PdfPages(ROOT/'Real_Photo_Checklist_and_Measurements.pdf') as pdf:
        fig = page('Take the real Module 2 photos', 'Use one borrowed smartphone for the entire experiment.', 1)
        y = .86
        sections = [
          ('1 / Gather the equipment', 'A working smartphone, the printed checkerboard, a flat rigid backing, a ruler, a tape measure, and a flat rectangular object with clearly visible corners. A large poster or flat cardboard rectangle is easier to see from 3 metres away.'),
          ('2 / Print and measure the board', 'Print Print_Checkerboard_20mm_Letter.pdf in landscape at Actual Size / 100%. Check the 100 mm scale bar. Measure five adjacent squares horizontally and vertically, then divide each length by five. Intended square size is 20 mm. If the two directions are not equal, reprint. Mount the sheet flat; do not bend it.'),
          ('3 / Keep the camera consistent', 'Use the same rear camera, 1x zoom, ordinary Photo mode, landscape orientation and resolution throughout. Avoid automatic lens switching, portrait mode, panoramas, cropping and digital zoom. Use good light. Keep focus fixed if possible while keeping the board sharp; otherwise record autofocus as a limitation.'),
          ('4 / Capture 20-25 checkerboard photos', 'Keep the whole board and its white margin visible. Vary its tilt, position and size in the frame, including near the centre and image edges. Avoid glare, motion blur and extreme tilts. Do not take 20 copies of the same view. We need at least 10 successful corner detections; extra varied photos help.'),
          ('5 / Measure and photograph the object', 'Measure the real object width and height with a ruler. Face its flat surface directly toward the camera, with the lens level with the object centre. Use about 3 metres of straight viewing distance, strictly greater than 2 metres. Measure from the active rear lens to the object front face; record this practical camera-centre approximation and tape precision. Record the actual distance, even if it is not exactly 3 metres. Take two sharp object photos without changing camera settings.'),
          ('6 / Send the original files and measurements', 'Upload the original calibration photos, the two object photos and the completed next page together in a ZIP if convenient. Keep original files; do not send screenshots or social-media copies. JPEG/PNG are easiest; original HEIC files can be converted consistently before processing. Do not crop or resize individual photos.'),
        ]
        for title, body in sections:
            y = block(fig, y, title, body)
        assert y > .08, y
        pdf.savefig(fig); plt.close(fig)

        fig = page('Record these measurements', 'Leave unknown values blank. Do not copy simulation values.', 2)
        y = .86
        fields = [
          'Capture date and smartphone make/model',
          'Camera/lens and zoom used (for example: rear main, 1x)',
          'Image resolution and orientation',
          'Focus locked for all photos? Yes / No / Unknown',
          'Width of five adjacent printed squares: __________ mm; divide by 5 = __________ mm',
          'Height of five adjacent printed squares: _________ mm; divide by 5 = __________ mm',
          'Object description',
          'Actual object width: __________________ cm',
          'Actual object height: _________________ cm',
          'Actual lens-to-front-face distance: __________________ cm (must exceed 200 cm)',
          'Tape reference point and measurement precision / uncertainty',
          'Lens, focus or image-size changes? Other capture problems?',
        ]
        for label in fields:
            fig.text(.08, y, label, fontsize=9.5, color=INK)
            fig.add_artist(plt.Line2D([.08,.92],[y-.027,y-.027],transform=fig.transFigure,color='#b5c4c9',lw=.7))
            y -= .047
        y = block(fig, y-.015, 'What happens next', 'This capture kit is optional for a physical validation extension. Aya reports instructor approval for phone-looking synthetic images; the main report now uses that reported allowance. If real photos are later supplied, they can be processed separately. The code repository is listed in GITHUB_URL.txt. Nothing is submitted automatically.')
        fig.text(.08, .095, 'Method reference: docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html', fontsize=8, color=INK)
        assert y > .11, y
        pdf.savefig(fig); plt.close(fig)

if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    board()
    guide()
    print('Created board PDF (1 page) and real-photo checklist PDF (2 pages).')
