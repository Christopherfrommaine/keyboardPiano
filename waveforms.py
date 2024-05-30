import numpy as np
from scipy.fft import fft, ifft
from math import log2


def pureTone(freq, dur):
    return np.sin(freq * np.pi * np.linspace(0, dur, 44100 * dur, endpoint=False))


def lowPass(func, cutoffFreq=1000, sample_rate=44100):
    def cutFrequencies(samples):
        spectrum = fft(samples)

        # Determine frequencies corresponding to spectrum bins
        freqs = np.fft.fftfreq(len(samples), 1 / sample_rate)

        # Calculate the Hann window
        hann_window = 0.5 * (1 - np.cos(2 * np.pi * freqs / (2 * cutoffFreq)))

        # Apply the Hann window to the spectrum
        filtered_spectrum = spectrum * hann_window

        # Transform back to time domain
        filtered_samples = np.real(ifft(filtered_spectrum))

        return filtered_samples

    return lambda x, y, z: cutFrequencies(func(x, y, z))


def sine(freq, vol, dur):
    """Generates a Pure Tone Waveform"""
    return vol * np.tile(np.sin(np.pi * freq * np.linspace(0, (2 / freq), int(44100 * 2 / freq), endpoint=False)), int(1 + (dur / (2 / freq))))[:44100 * dur]


def square(freq, vol, dur):
    # Highest frequencies are out of tune for some reason.
    return 0.1 * vol * (2 * np.round((pureTone(freq, dur) + 1) * 0.5) - 1)


def organ(freq, vol, dur):
    """Generates a Waveform mimicing an Organ"""
    db = [-30.9, -29.1, -31.5, -31.8, -39.8, -37.1, -59.0, -29.9, -54.9, -56.0, -80.9, -77.9, -37.4, -106.6, -67.0, -61.5, -41.8]
    frequencies = [1/8, 1/4, 1/2] + [i + 1 for i in range(len(db))]
    fourier = [0.0, 0.2, 0.7] + [10 ** (dbi / 20) for dbi in db]
    o = 0 * pureTone(440, dur)
    for i in range(len(frequencies)):
        o += fourier[i] * pureTone(2 * frequencies[i] * freq, dur)
    adjustmentAmount = 4
    adjustedVol = vol * (1 + adjustmentAmount * (3.13976 - log2(log2(freq + 50))))
    return (adjustedVol / sum(fourier)) * o
