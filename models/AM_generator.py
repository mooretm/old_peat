""" Pulsed tone (AM) generator. 

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

# Custom Modules
from functions import general


#########
# Begin #
#########
def generate_am_tone(carrier, modulation_depth, duration, sampling_rate):
    """ Generate an amplitude modulated tone.

    Parameters:
        carrier (float): The frequency of the tone in Hz.
        modulation_depth (float): The depth of modulation, ranging from 0 to 1.
        duration (float): The duration of the tone in seconds.
        sampling_rate (int): The number of samples per second.

    Returns:
        numpy.ndarray: Array containing the amplitude modulated tone.
    """
    #############
    # Modulator #
    #############
    # Get number of samples for "on" portion of square wave modulator
    num_samps = int(sampling_rate * (duration + (60/1000)))

    # Create gated "on" portion of square wave
    ungated_on_portion = np.ones(num_samps, dtype=int)
    gated_on_portion = general.doGate(
        sig=ungated_on_portion,
        rampdur=30/1000,
        fs=sampling_rate
    )

    # Add "off" portion of square wave
    #off_portion_samps = sampling_rate * 
    off_portion = np.zeros(num_samps)
    modulator = np.hstack((gated_on_portion, off_portion))


    ###########
    # Carrier #
    ###########
    # Get duration (s) of modulator
    sig_dur = len(modulator) / sampling_rate

    # Create carrier pure tone
    t, sig = general.mkTone(freq=carrier, dur=sig_dur, phi=0, fs=sampling_rate)


    ###########
    # AM Tone #
    ###########
    # Create single cycle of AM tone
    am_one_cycle = sig * modulator

    print(f"\nType: {type(am_one_cycle)}")
    print(f"Shape: {am_one_cycle.shape}")

    # Create train of pulses
    am_tone = np.hstack((am_one_cycle, am_one_cycle, am_one_cycle))
    #am_tone = np.concatenate((np.repeat(am_one_cycle, 3)))

    sd.play(am_tone, sampling_rate)

    plt.plot(am_tone)
    plt.show()



    
    # # Create time vector
    # t = np.linspace(0, duration, int(duration * sampling_rate), 
    #                 endpoint=False)
    
    # # Create AM signal
    # modulating_signal = np.sin(2 * np.pi * carrier * t)
    # modulated_signal = (1 + modulation_depth * modulating_signal) * np.sin(2 * np.pi * carrier * t)
    
    # return modulated_signal
