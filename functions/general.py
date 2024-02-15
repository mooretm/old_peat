""" General functions library. """

###########
# Imports #
###########
# Import system packages
import sys
import os

# Data science
import numpy as np


#########
# Funcs #
#########
def resource_path(relative_path):
    """ Create the absolute path to compiled resources
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def truncate_path(long_path, **kwargs):
    """ Truncate path (if necessary) and return 
        shortened path for display
    """
    if 'length' in kwargs:
        length = kwargs['length']
    else:
        length = 60

    if len(long_path) >= length:
        short = '...' + long_path[-(length-5):]
        return short
    else:
        if long_path == "":
            return 'Please select a file'
        else:
            return long_path


def add_channels(data, reps):
    """ For creating """


def warble_tone(dur, fs, fc, mod_rate, mod_depth):
    """ Create a warble tone. 

        Parameters:
            dur: duration in seconds
            fs: sampling rate in Hz
            fc: center frequency of the warble tone
            mod_rate: modulation rate in percent
            mod_depth: modulation depth in percent

        Returns: a single-channel warble tone
        
        Example:
            warble = _warble_tone(3, 44100, 1000, 5, 5)

        Written by: Travis M. Moore
        Created: 12/01/2023
        Last edited: 02/12/2024
    """
    # Create time vector
    t = np.arange(0, dur, 1/fs)

    # Grab random phase value in degrees
    phi_rad = np.radians(np.random.randint(0, 179))
    #print(f"\ngeneral: Phase: {phi_rad}")


    # Synthesize warble tone
    wc = fc * 2 * np.pi
    wd = mod_rate * 2 * np.pi
    B = (mod_depth / 100) * wc # in radians
    #y = np.sin(wc * t + (B/wd) * (np.sin(wd * t - (np.pi/2)) + 1))
    y = np.sin(wc * t + (B/wd) * (np.sin(wd * t - phi_rad) + 1))

    return y


def doGate(sig, rampdur=0.02, fs=48000):
    """
        Apply rising and falling ramps to signal SIG, of 
        duration RAMPDUR. Takes a 1-channel or 2-channel 
        signal. 

            SIG: a 1-channel or 2-channel signal
            RAMPDUR: duration of one side of the gate in 
                seconds
            FS: sampling rate in samples/second

            Example: 
            [t, tone] = mkTone(100,0.4,0,48000)
            gated = doGate(tone,0.01,48000)

        Original code: Anonymous
        Adapted by: Travis M. Moore
        Last edited: Jan. 13, 2022          
    """
    gate =  np.cos(np.linspace(np.pi, 2*np.pi, int(fs*rampdur)))
    # Adjust envelope modulator to be within +/-1
    gate = gate + 1 # translate modulator values to the 0/+2 range
    gate = gate/2 # compress values within 0/+1 range
    # Create offset gate by flipping the array
    offsetgate = np.flip(gate)
    # Check number of channels in signal
    if len(sig.shape) == 1:
        # Create "sustain" portion of envelope
        sustain = np.ones(len(sig)-(2*len(gate)))
        envelope = np.concatenate([gate, sustain, offsetgate])
        gated = envelope * sig
    elif len(sig.shape) == 2:
        # Create "sustain" portion of envelope
        sustain = np.ones(len(sig[0])-(2*len(gate)))
        envelope = np.concatenate([gate, sustain, offsetgate])
        gatedLeft = envelope * sig[0]
        gatedRight = envelope * sig[1]
        gated = np.array([gatedLeft, gatedRight])
    return gated


def mkTone(freq, dur, phi=0, fs=48000):
    """ 
    Create a pure tone. Returns the signal 
        AND the time base. 
    
        FREQ: frequency in Hz
        DUR: duration in SECONDS
        PHI: phase in DEGREES
        FS: sampling rate

        EXAMPLE: [t, sig] = (500,0.2,0,48000)

    Written by: Travis M. Moore
    Last edited: 1/12/2022
    """
    phi = np.deg2rad(phi) # to radians
    t = np.arange(0,dur,1/fs) # time base
    sig = np.sin(2*np.pi*freq*t+phi)
    return [t, sig]


def string_to_list(string):
    """ Return a list of ints from a string. 
    
        Expects: a string of comma-separated integers
        Returns: a list of integers
    """
    my_list = [int(val) for val in string.split(', ')]
    return my_list
