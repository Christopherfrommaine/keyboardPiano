import pygame
from pygame.locals import *
from waveforms import *


# Params
VOLUME = 0.4
WAVEFORM = organ  # Waveform generation function
TUNING = 'Extended'

CACHE = True  # Memory intensive cache for waveforms. Better for more computationally intensive waveforms
BUFFER_DURATION = 20  # Larger value increases lag and memory use, but decreases occasional popping sounds
CHANNELS = 10  # Maximum number of notes to play simultaneously


# Main Code:
def generateKeyFrequencies(tuning='12TET', A=440):
    notesInOrder12 = 'zsxdcvgbhnjm,l.;/\''.upper()
    notesInOrder17 = 'zwsxedcvtgbyhnujm,'.upper()  # These are used through an eval() call
    notesInOrder19 = 'zwsxedcfvtgbyhnujmk,'.upper()
    notesInOrder24 = 'zws3xed4cfvtg6byh7nuj8mk,'.upper()
    notesInorder12Extended = ('azsxdcvgbhnjm,l.;/\''.upper(), '`1q2w3er5t6y7ui9o0p[=]\\'.upper())

    C = A * 2 ** (3 / 12)
    if tuning[-3:] == 'TET':
        notesPerOct = int(tuning[:-3])
        match notesPerOct:
            case 12:
                notesInOrder = notesInOrder12
            case 17:
                notesInOrder = notesInOrder17
            case 19:
                notesInOrder = notesInOrder19
            case 24:
                notesInOrder = notesInOrder24
            case _:
                if notesPerOct < 12:
                    notesInOrder = notesInOrder12[:notesPerOct]
                else:
                    notesInOrder = notesInOrder24[:notesPerOct]
        return {key: C * 2 ** (i / notesPerOct) for i, key in enumerate(notesInOrder)}
    elif tuning == 'Pythagorean':
        ratios = [1/1, 256/243, 9/8, 32/27, 81/64, 4/3, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128, 2/1]  # Sorry, no augmented fourth for you!
        return {key: C * ratios[i] for i, key in enumerate(notesInOrder12)}
    elif tuning == 'Extended':
        lowerOct = {key: (1/2) * C * 2 ** ((i - 2) / 12) for i, key in enumerate(notesInorder12Extended[1])}
        upperOct = {key: C * 2 ** ((i - 1) / 12) for i, key in enumerate(notesInorder12Extended[0])}
        upperOct.update(lowerOct)
        return upperOct
    else:
        return generateKeyFrequencies()  # TODO
keyFreqs = generateKeyFrequencies(TUNING)


active_notes = {}
def octToFactor():
    """
    Returns the factor to scale frequencies with by octave keys pressed
    :return: float | int
    """
    o = 0
    if 'L' in octave_notes:
        o += 1
    if 'C' in octave_notes:
        o -= 1
    if 'A' in octave_notes:
        o *= 2
    return 2 ** (o - 1)


toneCache = {}
def generateWaveform(frequency, cache=CACHE):
    if cache:
        if not int(frequency) in toneCache.keys():
            toneCache.update({int(frequency): generateWaveform(frequency, False)})
        return toneCache[int(frequency)]
    else:
        return np.int16(WAVEFORM(frequency, VOLUME, BUFFER_DURATION) * 32767)


def playNote(note):
    frequency = keyFreqs.get(note.upper(), None)
    if frequency:
        frequency *= octToFactor()
        print(f'Playing: {note} | {frequency}Hz')

        waveform = generateWaveform(frequency)
        sound = pygame.mixer.Sound(waveform)
        sound.play(loops=-1)  # Play the note indefinitely
        active_notes[note] = sound
def stopNote(note):
    note_obj = active_notes.get(note.upper(), None)
    if note_obj:
        # note_obj.stop()
        note_obj.fadeout(100)
        del active_notes[note.upper()]


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(CHANNELS)
pygame.display.set_mode((1, 1))  # Hidden window to capture key events


# Prefill Tone Cache
if CACHE:
    VOLUME *= 0.1
    for possibleChar in '`1q2w3e4r5t6y7u8i9o0p-[=]\\azsxdcfvgbhnjmk,l.;/\'':
        for oNotes in (['C', 'A'], ['C'], ['S'], ['S', 'A'], []):
            octave_notes = oNotes
            playNote(possibleChar.upper())
            stopNote(possibleChar.upper())
    VOLUME *= 10
else:
    octave_notes = []  # Notes that control the octave that something is played at.


# Main Loop
running = True
while running:
    for event in pygame.event.get():
        try:
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LSHIFT:
                    octave_notes.append('L')
                elif event.key == pygame.K_LCTRL:
                    octave_notes.append('C')
                elif event.key == pygame.K_LALT:
                    octave_notes.append('A')
                else:
                    keyPressed = chr(event.key).upper()
                    if keyPressed in keyFreqs:
                        playNote(keyPressed)
            elif event.type == KEYUP:
                if event.key == pygame.K_LSHIFT:
                    octave_notes.remove('L')
                elif event.key == pygame.K_LCTRL:
                    octave_notes.remove('C')
                elif event.key == pygame.K_LALT:
                    octave_notes.remove('A')
                else:
                    keyPressed = chr(event.key).upper()
                    if keyPressed in keyFreqs:
                        stopNote(keyPressed)
        except ValueError:  # accidental key presses
            pass
pygame.quit()
