import numpy as np
import pandas as pd

from psychopy import visual, core, event, data, gui

# =====================================================
# PARTICIPANT INFO
# =====================================================

exp_info = {
    'participant': '',
    'age': '',
    'gender': '',
    'session': '001'
}

dlg = gui.DlgFromDict(
    dictionary=exp_info,
    title='Blue-Purple QUEST'
)

if not dlg.OK:
    core.quit()

# =====================================================
# WINDOW
# =====================================================

win = visual.Window(
    size=[1000, 800],
    color=[0, 0, 0],
    units='pix'
)

# =====================================================
# QUEST PARAMETERS
# =====================================================

quest = data.QuestHandler(

    # smaller initial threshold
    startVal=3,

    startValSd=1.5,

    pThreshold=0.75,

    gamma=0.5,

    beta=3.5,

    delta=0.01,

    nTrials=40,

    # IMPORTANT:
    # keep k range small
    minVal=0.2,
    maxVal=6
)

# =====================================================
# CIELAB SETTINGS
# =====================================================

# fixed luminance
L = 75

# -----------------------------------------------------
# NEW CENTER
#
# lower chroma
# more ambiguous blue-purple region
# -----------------------------------------------------

center = np.array([5, -18])

# -----------------------------------------------------
# NEW LOCAL AXIS
#
# smaller direction
# more subtle category transition
# -----------------------------------------------------

v = np.array([0.35, 0.15])

# normalize vector
v = v / np.linalg.norm(v)

# =====================================================
# PURE NUMPY LAB -> RGB
# =====================================================

def lab_to_rgb(L, a, b):

    # ---------------------------------
    # LAB -> XYZ
    # ---------------------------------

    y = (L + 16.0) / 116.0
    x = a / 500.0 + y
    z = y - b / 200.0

    xyz = np.array([x, y, z])

    epsilon = 0.008856
    kappa = 903.3

    xyz = np.where(
        xyz ** 3 > epsilon,
        xyz ** 3,
        (116 * xyz - 16) / kappa
    )

    # D65 white point
    Xn = 95.047
    Yn = 100.000
    Zn = 108.883

    X = xyz[0] * Xn
    Y = xyz[1] * Yn
    Z = xyz[2] * Zn

    X /= 100
    Y /= 100
    Z /= 100

    # ---------------------------------
    # XYZ -> linear RGB
    # ---------------------------------

    r =  3.2406 * X - 1.5372 * Y - 0.4986 * Z
    g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    b =  0.0557 * X - 0.2040 * Y + 1.0570 * Z

    rgb = np.array([r, g, b])

    # ---------------------------------
    # gamma correction
    # ---------------------------------

    rgb = np.where(
        rgb > 0.0031308,
        1.055 * (rgb ** (1 / 2.4)) - 0.055,
        12.92 * rgb
    )

    # clip
    rgb = np.clip(rgb, 0, 1)

    return rgb

# =====================================================
# GENERATE STIMULUS
# =====================================================

def generate_stimulus(k, side):

    """
    side:
        -1 = blue side
        +1 = purple side
    """

    point = center + side * k * v

    a = point[0]
    b = point[1]

    rgb = lab_to_rgb(L, a, b)

    return rgb, a, b

# =====================================================
# STIMULUS OBJECT
# =====================================================

patch = visual.Rect(
    win,
    width=250,
    height=250,
    lineColor=None
)

# =====================================================
# TEXT
# =====================================================

instruction = visual.TextStim(
    win,
    text="""
BLUE-PURPLE QUEST

F = MORE BLUE
J = MORE PURPLE

Try to judge subtle differences.

Press SPACE to start
""",
    color='white',
    height=28
)

fixation = visual.TextStim(
    win,
    text="+",
    color='white',
    height=40
)

# =====================================================
# START SCREEN
# =====================================================

instruction.draw()
win.flip()

event.waitKeys(keyList=['space'])

# =====================================================
# RESULTS
# =====================================================

results = []

# =====================================================
# MAIN QUEST LOOP
# =====================================================

for trial_num, k in enumerate(quest):

    # ---------------------------------
    # random category side
    # ---------------------------------

    side = np.random.choice([-1, 1])

    if side == -1:
        correct_key = 'f'
        category = 'blue'
    else:
        correct_key = 'j'
        category = 'purple'

    # ---------------------------------
    # generate stimulus
    # ---------------------------------

    rgb, a_val, b_val = generate_stimulus(k, side)

    # PsychoPy RGB range: -1~1
    psychopy_rgb = rgb * 2 - 1

    patch.fillColor = psychopy_rgb

    # =================================================
    # FIXATION
    # =================================================

    fixation.draw()
    win.flip()

    core.wait(0.5)

    # =================================================
    # STIMULUS
    # =================================================

    patch.draw()
    win.flip()

    clock = core.Clock()

    keys = event.waitKeys(
        keyList=['f', 'j', 'escape'],
        timeStamped=clock
    )

    key, rt = keys[0]

    # ---------------------------------
    # ESCAPE
    # ---------------------------------

    if key == 'escape':
        break

    # ---------------------------------
    # CORRECT?
    # ---------------------------------

    correct = int(key == correct_key)

    # update QUEST
    quest.addResponse(correct)

    # =================================================
    # SAVE TRIAL
    # =================================================

    results.append({

        'participant': exp_info['participant'],
        'age': exp_info['age'],
        'gender': exp_info['gender'],
        'session': exp_info['session'],

        'trial': trial_num + 1,

        'k': k,

        'a': a_val,
        'b': b_val,

        'category': category,

        'response': key,

        'correct': correct,

        'rt': rt
    })

    # =================================================
    # INTER-TRIAL INTERVAL
    # =================================================

    win.flip()

    core.wait(0.5)

# =====================================================
# FINAL THRESHOLD
# =====================================================

threshold = quest.mean()

# =====================================================
# SAVE CSV
# =====================================================

filename = (
    f"{exp_info['participant']}_"
    f"{exp_info['session']}_"
    f"blue_purple_quest.csv"
)

df = pd.DataFrame(results)

df.to_csv(
    filename,
    index=False
)

# =====================================================
# END SCREEN
# =====================================================

end_text = visual.TextStim(
    win,
    text=f"""
Finished

Estimated threshold:

k = {threshold:.2f}

CSV saved:

{filename}

Press SPACE to quit
""",
    color='white',
    height=28
)

end_text.draw()
win.flip()

event.waitKeys(keyList=['space'])

# =====================================================
# PRINT
# =====================================================

print(df.head())

print("\nEstimated threshold:")
print(threshold)

# =====================================================
# CLOSE
# =====================================================

win.close()
core.quit()