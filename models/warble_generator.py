""" Warble tone (FM) generator. 

    Written by: Travis M. Moore
    Last edited: 02/09/2024
"""

###########
# Imports #
###########
# Data Science
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# Audio
import sounddevice as sd


#########
# BEGIN #
#########
def warble_tone(fc, mod_depth, mod_rate, dur, fs=48000):
    """ Generate a warble tone. Optionally, play the tone using the 
        sounddevice library, and display spectrogram and power 
        spectral density plots for inspection.

        Parameters:
        - fc (float): Carrier frequency of the tone in Hertz.
        - mod_depth (float): Modulation depth of the tone in percent.
        - mod_rate (float): Modulation rate of the tone in Hertz.
        - dur (float): Duration of the tone in seconds.
        - fs (int): Sampling rate in samples per second. 

        Returns:
        y: a warble tone

        This function generates a warble tone based on the specified parameters.
        
    """

    #########################
    # Warble tone synthesis #
    #########################
    # Create time vector
    t = np.arange(0, dur, 1/fs)

    # Synthesize warble tone
    wc = fc * 2 * np.pi
    wd = mod_rate * 2 * np.pi
    B = (mod_depth / 100) * wc # in radians
    y = np.sin(wc * t + (B/wd) * (np.sin(wd * t - (np.pi/2)) + 1))


    ##########################
    # Plotting and Listening #
    ##########################
    # Play the audio using sounddevice
    #sd.play(y, fs)

    # # Plot spectrogram of y
    # plt.figure()
    # f, t, Sxx = spectrogram(y, fs, nperseg=1024)
    # plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    # plt.title('Spectrogram')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Frequency (Hz)')
    # plt.show()

    return y
