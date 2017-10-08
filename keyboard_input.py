"""Functions to collect keyboard inputs for self report beharioral data."""


import psychopy
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


def reportNum(win, screen):
    """Report numeric inputs, anticipate errors and return subject to input."""

    done = 0
    count = 0
    scale = list('    ')
    shade = [-1, -1, -1]

    while not done:
        inputs = psychopy.event.waitKeys()

        # if they press return
        if inputs[0] == 'return':

            # make sure there's some number in the scale
            try:
                # this will error out if not an integer
                int(scale[0])
                done = 1

            except:
                scale = list('    ')
                count = 0
                done = 0
                text = psychopy.visual.TextStim(win=win, text='', color=shade)

        # if they pressed delete reset
        elif numpy.logical_or(inputs[0] == 'backspace', inputs[0] == 'space'):
            scale = list('    ')
            count = 0 ; done = 0
            text = psychopy.visual.TextStim(win=win, text='', color=shade)

        else:

            try:
                # check if they entered numbers
                type(int(inputs[0])) == int
                scale[count] = inputs[0]
                count = count + 1
                value = int("".join(scale[0:count]))
                text = psychopy.visual.TextStim(win=win, text=value, color=shade, height=50)
                text.pos = (0.0, -350)
                # catch error if they go over 100

                if int("".join(scale)) > 100:
                    text = psychopy.visual.TextStim(win=win, text='    ', color=shade, height=40)
                    scale = list('    ')
                    count = 0
                    text.pos = (0.0, -350)

            # incase they entered another key
            except ValueError:

                text = psychopy.visual.TextStim(win=win, text='   ', color=shade, height=40)
                text.pos = (0.0, -350)

        screen.draw()
        text.draw()
        win.flip()
    return value


def reportWord(win, screen):
    done = 0
    color = ''
    while not done:
        keys = psychopy.event.waitKeys()
        if keys[0] == 'return':
            finalWord = color
            done = 1
            # save color here eventually
            color = ''
        elif keys[0] == 'backspace':
            color = ''
        elif keys[0] == 'space':
            color = color + ' '
        elif keys[0] == 'period':
            color = color + '.'
        else:
            color = color + keys[0]

        text = psychopy.visual.TextStim(win=win, text=color, color=[-1, -1, -1], height=40)
        text.pos = (0.0, -350)
        screen.draw()
        text.draw()
        win.flip()

    return finalWord
