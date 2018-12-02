# -*- coding: utf-8 -*-
"""
Prospective Memory and Volition
Script by Jonas Kristoffer Lindeløv, August 2015
"""

from __future__ import division
import random, copy
import numpy as np
from psychopy import visual, monitors, event, core, gui

# Monitor
MON_SIZE = [1366, 1024]  # monitor size in pixels
MON_DISTANCE = 70  # distance in cm from eye lens to monitor
MON_WIDTH = 34  # width of monitor panel in cm

# General presentation parameters
TEXT_HEIGHT = 0.5
GRID_LENGTH = 2  # number of cells in square grid
GRID_SIZE = 1  # height and width of each cell in degrees visual angle.
SHAPE_SCALE = 0.8  # scale of stimulus relative to cell. 1 is same size as cell

# Condition parameters for trials
N_TRIALS = {'pm_exp': 18, 'filler_exp': 72, 'pm_practice': 5, 'filler_practice':16}  # PM and filler trials for experiment (exp) and practice. Should be even numbers.
MIN_FILLERS = 2  # minimum number of fillers before PM trial
KEYS_1 = {'up': 'top', 'down': 'bottom'}
KEYS_2 = {'left': 'left', 'right': 'right'}
KEYS_FEEDBACK = ['return', 'enter']
PRACTICE_TIMELIMIT = 1.5  # number of seconds before an error is presented

# Choice parameters
#COLORS =  ['yellow', 'orange', 'red', 'purple', 'blue', 'turquoise', 'green', 'sienna', 'gray', 'white']  # color options. "sienna" will be displayed as "brown".
COLORS = ['yellow', 'green', 'DodgerBlue', 'red', 'white']
SHAPES = {
    'triangle': np.array([[0,0], [0.5, 1], [1,0]]),
    'square': np.array([[0,0], [0,1], [1,1], [1,0]]),
    'circle': np.array([(np.sin(e*np.pi*2/128), np.cos(e*np.pi*2/128)) for e in xrange(128)]) / 2 + 0.5,
    'rhombus': np.array([[0,0.5], [0.5,1], [1,0.5], [0.5,0]])
}
N_CHOICES = 5  # how many colors to choose between
N_BLOCKS = 12  # maximum len(COLORS)*len(SHAPES) - N_CHOICES - 2 (practice)
SELECT_SIZE = GRID_SIZE * 2  # vertical spacing between color options
KEYS_CHOICE_MOVE = {'left': 1, 'right': -1}
KEYS_CHOICE_ANS = ['return', 'enter']

# Other stuff
KEYS_QUIT = ['escape', 'q']
SAVE_FOLDER = 'data'  # a folder with data

# Texts
TEXT_INSTRUCT = {
    'left-right': u"You'll start by choosing one out of five figures, e.g. a red square or a yellow circle. This figure is the 'target' until next time a new figure is selected.\n\nAfter that, you're presented with a 2x2 grid with a colored figure in it. \n\nIf this figure is NOT the exact figure you chose, press UP ARROW if the square is in the top row and press DOWN-ARROW if it's in the bottom row.\n\nIf the figure is identical to the one you chose (i.e. same shape and color), press LEFT ARROW if the square is in the left column. Press RIGHT ARROW if it's in the right column.\n\nIt is important that you respond as accuractely and fast as you can!",
    'up-down': u"You'll be choosing one out of five figures, e.g. a red square or a yellow circle. This figure is the 'target' until next time a new figure is selected.\n\nAfter that, you're presented with a 2x2 grid with a colored figure in it.\n\nIf this figure is NOT the exact figure you chose, press LEFT ARROW if the square is in the left column. Press RIGHT ARROW if it's in the right column.\n\nIf the figure is identical to the one you chose (i.e. same shape and color), press UP ARROW if the square is in the top row and press DOWN-ARROW if it's in the bottom row.\n\nIt is important that you respond as accurately and fast as you can!"
}
TEXT_CHANGE = u"You are now half-way through the experiment.\n\nYou will continue with the same task, but the response keys change now to the opposite of before. Press ENTER to see the new instructions..."
TEXT_CHOICE_VOLITION = u'Choose a target figure for the next block.'
TEXT_CHOICE_NONVOLITION = u'This is the target figure for the next block.'
TEXT_FEEDBACK = u'Wrong! Press the correct key to continue...'
TEXT_SLOW = u'Too slow! It is important that you respond as fast as you can.'
TEXT_EXPERIMENT = u"Now the experiment begins. There will be no feedback on wrong responses but the task is otherwise the same."
TEXT_END = u'Thank you for your participation!'

# Handy conversions
color_choices = copy.copy(COLORS)  # will be messed with later
KEYS_TRIAL = dict(KEYS_1.items() + KEYS_2.items())  # combined
attribute_choices = [(shape, color) for shape in SHAPES.keys() for color in COLORS]  # combinations of attributes


"""
FUNCTIONS
"""
def pm_preceeding(n, total, low):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""
    
    new_total = total - (low-1)*n
    dividers = sorted(random.sample(xrange(1, new_total), n - 1))
    return [a - b + 1 for a, b in zip(dividers + [new_total], [0] + dividers)]

def make_trial_list(choice_data, practice, block_no):
    """ Make a trial list that fulfills the conditions/restrictions """
    n_pm = N_TRIALS['pm_exp'] if not practice else N_TRIALS['pm_practice']
    n_filler = N_TRIALS['filler_exp'] if not practice else N_TRIALS['filler_practice']
    
    # Make a sequence of PM and fillers.
    trial_type_sequence = []
    for fillers in pm_preceeding(n_pm, n_filler, MIN_FILLERS):
        trial_type_sequence += ['filler']*fillers + ['pm']
        
    # Make a sequence of balanced left-right and top-bottom position
    square_filler_sequence = KEYS_2.values() * int(np.ceil(n_filler / len(KEYS_2)))
    square_pm_sequence = KEYS_1.values() * int(np.ceil(n_pm / len(KEYS_1)))
    random.shuffle(square_filler_sequence)
    random.shuffle(square_pm_sequence)
    square_filler_iter = square_filler_sequence.__iter__()
    square_pm_iter = square_pm_sequence.__iter__()
    
    # Group cells according to response options
    all_pos = np.arange(GRID_LENGTH**2)
    correct_answer_pos = {
        'left': all_pos[all_pos % GRID_LENGTH < GRID_LENGTH/2],
        'right': all_pos[all_pos % GRID_LENGTH >= GRID_LENGTH/2],
        'top': range(int(GRID_LENGTH**2 / 2)),
        'bottom': range(int(GRID_LENGTH**2 / 2), GRID_LENGTH**2)}
    
    # Allowable attributes for fillers (all non-PM attributes)
    attributes_filler = [attribute for attribute in attribute_choices if attribute is not choice_data['attributes']]
    
    # Now loop through it
    trial_list = []
    for trial_no, trial_type in enumerate(trial_type_sequence):
        correct_answer = square_filler_iter.next() if trial_type == 'filler' else square_pm_iter.next()
        shape, color = random.choice(attributes_filler) if trial_type is 'filler' else choice_data['attributes']

        # Pack all this info into a nice trial
        trial_list += [{
            # General trial info
            'type': trial_type,
            'trial_no': trial_no + 1,
            'block_no': block_no,
            'trial_no_global': trial_no + 1 + (block_no-1) * (n_pm+n_filler),

            # Stimulus properties
            'position': random.choice(correct_answer_pos[correct_answer]),  # choose randomly among allowed cells
            'shape': shape,
            'color': color,
            

            # Answers and scoring
            'response': '',
            'rt': '',
            'correct_answer': correct_answer,

            # Choice data
            'pm_color': choice_data['attributes'][1],
            'pm_shape': choice_data['attributes'][0],
            'volition': int(choice_data['volition']),
            'choice_shifts': choice_data['shifts'],
            'choice_rt': choice_data['rt'],
            'choice_options': choice_data['options'],
            'practice': int(practice),

            # Stuff from dialogue box
            'subject': VARS['subject'],
            'age': VARS['age'],
            'gender': VARS['gender'],
            'volition_first': VARS['volition first'],
            'pm_first': VARS['pm first']
            }]
    
    return trial_list


def ask(text='', keyList=None):
    """
    Ask subject something. Shows question and returns answer (keypress)
    and reaction time. Defaults to no text and all keys.
    """
    # Draw the TextStims to visual buffer, then show it and reset timing immediately (at stimulus onset)
    instruct.text = text
    instruct.draw()
    time_flip = win.flip()  # time of core.monotonicClock.getTime() at flip

    # Halt everything and wait for (first) responses matching the keys given in the Q object.
    if keyList:
        keyList += KEYS_QUIT
    key, time_key = event.waitKeys(keyList=keyList, timeStamped=True)[0]  # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.
    if key in KEYS_QUIT:  # Look at first reponse [0]. Quit everything if quit-key was pressed
        core.quit()
    return key, time_key - time_flip  # When answer given, return it.


class csvWriter(object):
    def __init__(self, saveFilePrefix='', saveFolder=''):
        """
        Creates a csv file and appends single rows to it using the csvWriter.write() function.
        Use this function to save trials. Writing is very fast. Around a microsecond.

        :saveFilePrefix: a string to prefix the file with
        :saveFolder: (string/False) if False, uses same directory as the py file
        """
        import csv, time

        # Create folder if it doesn't exist
        if saveFolder:
            import os
            saveFolder += '/'
            if not os.path.isdir(saveFolder):
                os.makedirs(saveFolder)

        # Generate self.saveFile and self.writer
        self.saveFile = saveFolder + str(saveFilePrefix) + ' (' + time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()) +').csv'  # Filename for csv. E.g. "myFolder/subj1_cond2 (2013-12-28 09-53-04).csv"
        self.writer = csv.writer(open(self.saveFile, 'wb'), delimiter=',').writerow  # The writer function to csv. It appends a single row to file
        self.headerWritten = False

    def write(self, trial):
        """:trial: a dictionary"""
        if not self.headerWritten:
            self.headerWritten = True
            self.writer(trial.keys())
        self.writer(trial.values())


"""
STIMULI
"""

# Dialogue box
VARS = {'subject':'', 'age':'', 'gender':['male', 'female'], 'volition first':['volition', 'non-volition'], 'pm first': ['up-down', 'left-right']}
if not gui.DlgFromDict(VARS, order=['subject', 'age', 'gender', 'volition first', 'pm first']).OK:
    core.quit()

# Window
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)
win = visual.Window(size=MON_SIZE, monitor=my_monitor, units='deg', color='black', allowGUI=False, fullscr=False)

# Stimuli
for shape in SHAPES:
    SHAPES[shape] = visual.ShapeStim(win, lineColor=None, interpolate=False, vertices=(SHAPES[shape]*GRID_SIZE - GRID_SIZE / 2)*SHAPE_SCALE)  # replace vertices with a corresponding psychopy stimulus

choice_text = visual.TextStim(win, height=TEXT_HEIGHT)
choice_marker = visual.Rect(win, fillColor='gray', lineColor=None, width=SELECT_SIZE, height=SELECT_SIZE)
instruct = visual.TextStim(win, height=TEXT_HEIGHT, pos=(0, 2))

# Other stuff
writer = csvWriter(str(VARS['subject']), saveFolder=SAVE_FOLDER)  # writer.write(trial) will write individual trials with low latency

# Make grid into a stimulus and make a list of coordinates to present the shapes
grid_coords = []
square_grid = visual.Rect(win, width=GRID_SIZE, height=GRID_SIZE, lineWidth=2, lineColor='white')
for y in range(GRID_LENGTH -1, -1, -1):  # from top to bottom
    for x in range(GRID_LENGTH):  # left to right
        grid_coords += [(GRID_SIZE*(x + 0.5 - 0.5*GRID_LENGTH), 
                         GRID_SIZE*(y + 0.5 - 0.5*GRID_LENGTH))]
        square_grid.pos = grid_coords[-1]  # set to this x, y coordinate
        square_grid.draw()
grid = visual.BufferImageStim(win)  # "screenshot"
win.clearBuffer()  # blank screen - we don't want to show it later


"""
PRESENT STIMULI
"""

def show_choice(volition):
    """ Select color - either yourself (volition==True) or not (volition==False) """
    # Instruction
    instruct.text = TEXT_CHOICE_VOLITION if volition else TEXT_CHOICE_NONVOLITION
    
    # Choose a pair of attributes
    selected = random.randint(0, N_CHOICES - 1)  # pre-select a random color
    options = random.sample(attribute_choices, N_CHOICES)
    return_data = {'rt': core.monotonicClock.getTime(), 'volition': volition, 'shifts':0, 'color':'', 'options': ', '.join([str(pair[0]) + '-' + str(pair[1]) for pair in options])}
    
    while True:
        for i, option in enumerate(options):
            shape, color = option  # unpack
            stim = SHAPES[shape]
            x = (N_CHOICES / 2 - i) * SELECT_SIZE  # y coordinate
            
            # Marker
            if i == selected:
                choice_marker.pos = (x, 0)
                choice_marker.draw()
            
            # Texts
            stim.fillColor = color
            stim.pos = (x, 0)            
            stim.draw()
        
        # Present
        instruct.draw()
        win.flip()
        
        # Get and handle response
        response, time_resp = event.waitKeys(keyList = KEYS_CHOICE_MOVE.keys() + KEYS_CHOICE_ANS + KEYS_QUIT, timeStamped=True)[0]
        if response in KEYS_QUIT:
            core.quit()
        if response in KEYS_CHOICE_ANS:
            attribute_choices.remove(options[selected])  # this response option is used now
            return_data['attributes'] =  options[selected]
            return_data['rt'] = time_resp - return_data['rt']
            return_data['options'] = ','.join([str(pair[0]) + '-' + str(pair[1]) for pair in options])
            return return_data  # return this color and remove it from COLOR_CHOICES simultaneously
        
        # Move cursor if allowed
        if volition:
            selected += KEYS_CHOICE_MOVE[response]
            selected = 0 if selected == N_CHOICES else N_CHOICES -1 if selected == -1 else selected  # change location
            return_data['shifts'] += 1
        

block_no = 0
def run_block(choice_data, practice):
    """ Run trials: PM and fillers """
    global block_no
    block_no += 1  # first block is 1
    
    # Loop through trials
    trial_list = make_trial_list(choice_data, practice, block_no)
    for trial in trial_list:
        # Prepare stimulus
        stim = SHAPES[trial['shape']]
        stim.pos = grid_coords[trial['position']]
        stim.fillColor = trial['color']
        
        # Present stimulus
        grid.draw()
        stim.draw()
        
        # Collect response
        key, rt = ask(keyList=KEYS_TRIAL.keys())
        trial['rt'] = rt
        trial['response'] = KEYS_TRIAL[key]
        trial['score'] = int(KEYS_TRIAL[key] == trial['correct_answer'])  # score for for filler trials

        # Save after each trial
        writer.write(trial)

        # If practice: Require correct answer
        if practice:
            if trial['rt'] > PRACTICE_TIMELIMIT:
                grid.draw()
                stim.draw()
                ask(text=TEXT_SLOW)
            while not KEYS_TRIAL[key] == trial['correct_answer']:
                grid.draw()
                stim.draw()
                key, rt = ask(text=TEXT_FEEDBACK, keyList=KEYS_TRIAL.keys())
                
    

"""
INITIATE!
"""
# Set up given info in start dialogue
volition_sequence = ([True, False]*100)[:N_BLOCKS] if VARS['volition first'] == 'volition' else ([False, True]*100)[:N_BLOCKS]  # alternate conditions per block
if VARS['pm first'] == 'left-right':
    KEYS_1, KEYS_2 = KEYS_2, KEYS_1  # swap response keys

# Practice
ask(TEXT_INSTRUCT.pop(VARS['pm first']))  # show and remove it from the dict
choice_data = show_choice(volition=True)
run_block(choice_data, practice=True)

# Loop through blocks
ask(TEXT_EXPERIMENT)
for block, volition in enumerate(volition_sequence):  # this is the number of possible runs with unique colors and all choice options
     # swap response keys half-way and practice anew
    if block +1 == N_BLOCKS / 2:
        KEYS_1, KEYS_2 = KEYS_2, KEYS_1  # swap response keys
        ask(TEXT_CHANGE)
        ask(TEXT_INSTRUCT.popitem()[1])  # use the remaining text
        choice_data = show_choice(volition=True)
        run_block(choice_data, practice=True)

    choice_data = show_choice(volition=volition)  # pick a color
    run_block(choice_data, practice=False)  # trials

ask(TEXT_END)
