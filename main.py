import pygame
from pygame.locals import *

from waveforms import *
from keyFrequencyGeneration import *


# Params
VOLUME = 0.4
WAVEFORM = organ  # Waveform generation function
TUNING = 'Extended'

CACHE = True  # Memory intensive cache for waveforms. Better for more computationally intensive waveforms
BUFFER_DURATION = 20  # Larger value increases lag and memory use, but decreases occasional popping sounds
CHANNELS = 10  # Maximum number of notes to play simultaneously


def octToFactor():
    """
    Finds the factor by which to scale frequencies based on octave modifying keys pressed.

    Returns:
        float | int
    """

    o = 0
    if 'L' in octaveModifyingKeys:
        o += 1
    if 'C' in octaveModifyingKeys:
        o -= 1
    if 'A' in octaveModifyingKeys:
        o *= 2
    return 2 ** (o - 1)


toneCache = {}
def generateWaveform(frequency, cache=CACHE):
    """
        Generates and caches a waveform at a specified frequency from the WAVEFORM function.

        Params:
           frequency (int|float): the frequency to play the note at
           cache (dict): whether or not to cache the waveform

        Returns:
            np.ndarray of int16
    """

    if cache:
        if not int(frequency) in toneCache.keys():
            toneCache.update({int(frequency): generateWaveform(frequency, False)})
        return toneCache[int(frequency)]
    else:
        return np.int16(WAVEFORM(frequency, VOLUME, BUFFER_DURATION) * 32767)


currentlyActiveNotes = {}
def playNote(note):
    """
        Begins playing the specified note.

        Params:
            note (str): keyboard charachter pressed
    """
    frequency = keyFreqs.get(note.upper(), None)
    if frequency:
        frequency *= octToFactor()
        print(f'Playing: {note} | {frequency}Hz')

        waveform = generateWaveform(frequency)
        sound = pygame.mixer.Sound(waveform)
        sound.play(loops=-1)  # Play the note indefinitely
        currentlyActiveNotes[note] = sound
def stopNote(note):
    """
        Stops playing the specified note.

        Params:
            note (str): keyboard charachter pressed
    """
    noteObj = currentlyActiveNotes.get(note.upper(), None)
    if noteObj:
        # noteObj.stop()
        noteObj.fadeout(100)
        del currentlyActiveNotes[note.upper()]


# Initialization
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(CHANNELS)
pygame.display.set_mode((1, 1))  # Small window to capture key events

keyFreqs = generateKeyFrequencies(TUNING)


# Prefill Tone Cache
if CACHE:
    VOLUME *= 0.1
    for possibleChar in '`1q2w3e4r5t6y7u8i9o0p-[=]\\azsxdcfvgbhnjmk,l.;/\'':
        for oNotes in (['C', 'A'], ['C'], ['S'], ['S', 'A'], []):
            octaveModifyingKeys = oNotes
            playNote(possibleChar.upper())
            stopNote(possibleChar.upper())
    VOLUME *= 10
else:
    octaveModifyingKeys = []  # Notes that control the octave that something is played at.


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

                # Octave Modifyers
                if event.key == pygame.K_LSHIFT:
                    octaveModifyingKeys.append('L')
                elif event.key == pygame.K_LCTRL:
                    octaveModifyingKeys.append('C')
                elif event.key == pygame.K_LALT:
                    octaveModifyingKeys.append('A')

                # Note Pressed
                else:
                    keyPressed = chr(event.key).upper()
                    if keyPressed in keyFreqs:
                        playNote(keyPressed)

            elif event.type == KEYUP:
                # Octave Modifyers
                if event.key == pygame.K_LSHIFT:
                    octaveModifyingKeys.remove('L')
                elif event.key == pygame.K_LCTRL:
                    octaveModifyingKeys.remove('C')
                elif event.key == pygame.K_LALT:
                    octaveModifyingKeys.remove('A')

                # Note Pressed
                else:
                    keyPressed = chr(event.key).upper()
                    if keyPressed in keyFreqs:
                        stopNote(keyPressed)
        except ValueError:  # accidental key presses
            pass
pygame.quit()
