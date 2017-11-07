"""Functions to collect keyboard inputs for self report beharioral data."""


import time
import psychopy
from psychopy import visual
import numpy



def calibrate(SD9, shock_key, finish_key):
    """Shock subject when 'shock_key' is pressed, end with 'finish_key'."""

    done = 0
    while not done:

        # collect input from keyboard to finish or administer shock
        choice = psychopy.event.waitKeys()[0]

        if choice == finish_key:
            done = 1
        elif choice == shock_key:
            SD9.shock()
        else:
            pass
    return

def report_num(window, screen):
    """Take certain keyboard unputs, project onto screen, return string. """
    
    number = ''
    done = 0

    # for legibility throughout, define function
    def draw_text(window, screen, inputs):
        col = [-1, -1, -1]
        text = visual.TextStim(win=window, text=inputs, color=col, height=40)
        text.pos = (0.0, -350)
        screen.draw()
        text.draw()
        window.flip()

    while not done:

        # visualize inputs to keyboard on top of instructions
        draw_text(window, screen, number)

        # wait for inputs
        keys = psychopy.event.waitKeys()

        # conditions on displaying and collecting inputs
        if keys[0] == 'backspace':
            # delete string
            number = ''

        elif keys[0] == 'space':
            # not necessary, but it's cute
            number = number

        elif keys[0] == 'period':
            # not necessary, but cute
            number = number + '.'
        
        elif (keys[0] == 'return'):

            # when subjects choose to submit their input, inspect it

            try:           
                
                # error and restart if they enter a string
                number = float(number) 
                if number <= 100: 
                    final_answer = number
                    done = 1
                else: 
                    number = ''    
            except: 
                number = ''
        
        elif len(keys[0]) == 1: #and type(keys[0]) == int:
            
            try: 
                int(keys[0])
                number = number + keys[0]
            except: 
                pass

    return final_answer
    



def report_word(window, screen):
    """Take certain keyboard unputs, project onto screen, return string. """
    #
    color = ''
    wrong_ans = 0
    done = 0

    # for legibility throughout, define function
    def draw_text(window, screen, inputs):
        col = [-1, -1, -1]
        text = visual.TextStim(win=window, text=inputs, color=col, height=40)
        text.pos = (0.0, -350)
        screen.draw()
        text.draw()
        window.flip()

    while not done:

        # visualize inputs to keyboard on top of instructions
        draw_text(window, screen, color)

        # wait for inputs
        keys = psychopy.event.waitKeys()

        # conditions on displaying and collecting inputs
        if keys[0] == 'backspace':
            # delete string
            color = ''

        elif keys[0] == 'space':
            # not necessary, but it's cure
            color = color + ' '

        elif keys[0] == 'period':
            # not necessary, but cute
            color = color + '.'

        elif (keys[0] == 'return'):

            """When subjects choose to submit their input, inspect it."""

            if (color == 'blue') or (color == 'red'):
                # make sure answer is among observed colors
                # save their choice and close
                final_answer = color
                done = 1

            elif (color == 'void'):
                # experiment can input this to proceed without subject input
                final_answer = 0
                done = 1

            else:

                if wrong_ans < 1:

                    """
                    Give subjects several attemps to enter the right format.
                    """

                    # infor subjects
                    write = 'There were only two colors'
                    wrong_ans = wrong_ans + 1
                    draw_text(window, screen, write)
                    time.sleep(1)
                    color = blank = ''
                    draw_text(window, screen, blank)

                else:

                    """
                    If subjects give non-answers, call an experimentor.
                    """

                    # inform subjects
                    write = 'Call the experimenter.'
                    draw_text(window, screen, write)

                    # get ready for loop
                    waiting = 1
                    inputs_hold = ''

                    while waiting:

                        """
                        Enter 'ok' to return subjects to loop, 'done' to exit.
                        """

                        fix = psychopy.event.getKeys()
                        if len(fix):

                            inputs_hold = inputs_hold + fix[0]

                            if inputs_hold[-2:] == 'ok':

                                # if exp. enters 'ok' return subject to loop
                                color = ''
                                wrong_ans = 0
                                draw_text(window, screen, 'try again')
                                time.sleep(3)
                                waiting = 0

                            elif inputs_hold[-2:] == 'done':

                                # if experimenter enters done exit anyway
                                final_answer = waiting = 0

        elif len(keys[0]) == 1:

            # if they're just entering letters, add them to the string
            color = color + keys[0]

    return final_answer
