""" General functions library. """

###########
# Imports #
###########
# Import system packages
import sys
import os

# Data science
import numpy as np
import scipy.signal as s
from matplotlib import pyplot as plt



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


def warble_tone(dur, fs, fc, phi, mod_rate, mod_depth):
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

    # # Get phase in radians from random value in degrees
    # phi_rad = np.radians(np.random.randint(0, 179))

    # Synthesize warble tone
    wc = fc * 2 * np.pi
    wd = mod_rate * 2 * np.pi
    B = (mod_depth / 100) * wc # in radians
    #y = np.sin(wc * t + (B/wd) * (np.sin(wd * t - (np.pi/2)) + 1)) #static phi
    #y = np.sin(wc * t + (B/wd) * (np.sin(wd * t - phi_rad) + 1)) # rando phi
    y = np.sin(wc * t + (B/wd) * (np.sin(wd * t - phi) + 1))

    # # Plot spectrogram of y
    # plt.figure()
    # f, t, Sxx = s.spectrogram(y, fs, nperseg=1024)
    # plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    # plt.title('Spectrogram')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Frequency (Hz)')
    # plt.show()

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


def deg2rad(deg):
    """ 
        Convert degrees to radians. Takes a single
        value or a list of values.
    """
    try:
        rads = [np.radians(x) for x in deg]
        return rads
    except:
        rads = np.radians(deg)
        return rads
    

def db2mag(db):
    """ 
        Convert decibels to magnitude. Takes a single
        value or a list of values.
    """
    # Must use this form to handle negative db values!
    try:
        mag = [10**(x/20) for x in db]
        return mag
    except:
        mag = 10**(db/20)
        return mag


def mag2db(mag):
    """ 
        Convert magnitude to decibels. Takes a single
        value or a list of values.
    """
    try:
        db = [20 * np.log10(x) for x in mag]
        return db
    except:
        db = 20 * np.log10(mag)
        return db


def calc_RMS_based_on_sources(desired_SPL, num_sources):
    """ Calculate the SPL needed per channel to sum to the
        desired SPL.
    """
    # Convert SPL to intensity
    power_single = 10**(desired_SPL/10)
    # Calculate total intensity
    power_total = power_single * num_sources
    # Find the difference between the total power and a single channel
    diff_power = power_total - power_single
    # Calculate a correction factor by dividing the diff by the number of channels
    cf_power = diff_power / num_sources
    # Calculate the new power for a single channel
    new_power_single = power_single - cf_power
    # Convert single channel power to SPL
    new_spl_level = 10 * np.log10(new_power_single)
    return new_spl_level


def rms(sig):
    """ 
        Calculate the root mean square of a signal. 
        
        NOTE: np.square will return invalid, negative 
            results if the number excedes the bit 
            depth. In these cases, convert to int64
            EXAMPLE: sig = np.array(sig,dtype=int)

        Written by: Travis M. Moore
        Last edited: Feb. 3, 2020
    """
    theRMS = np.sqrt(np.mean(np.square(sig)))
    return theRMS


def setRMS(sig,amp,eq='n'):
    """
        Set RMS level of a 1-channel or 2-channel signal.
    
        SIG: a 1-channel or 2-channel signal
        AMP: the desired amplitude to be applied to 
            each channel. Note this will be the RMS 
            per channel, not the total of both channels.
        EQ: takes 'y' or 'n'. Whether or not to equalize 
            the levels in a 2-channel signal. For example, 
            a signal with an ILD would lose the ILD with 
            EQ='y', so the default in 'n'.

        EXAMPLE: 
        Create a 2 channel signal
        [t, tone1] = mkTone(200,0.1,30,48000)
        [t, tone2] = mkTone(100,0.1,0,48000)
        combo = np.array([tone1, tone2])
        adjusted = setRMS(combo,-15)

        Written by: Travis M. Moore
        Created: Jan. 10, 2022
        Last edited: May 17, 2022
    """
    if len(sig.shape) == 1:
        rmsdb = mag2db(rms(sig))
        refdb = amp
        diffdb = np.abs(rmsdb - refdb)
        if rmsdb > refdb:
            sigAdj = sig / db2mag(diffdb)
        elif rmsdb < refdb:
            sigAdj = sig * db2mag(diffdb)
        # Edit 5/17/22
        # Added handling for when rmsdb == refdb
        elif rmsdb == refdb:
            sigAdj = sig
        return sigAdj
        
    elif len(sig.shape) == 2:
        rmsdbLeft = mag2db(rms(sig[0]))
        rmsdbRight = mag2db(rms(sig[1]))

        ILD = np.abs(rmsdbLeft - rmsdbRight) # get lvl diff

        # Determine lvl advantage
        if rmsdbLeft > rmsdbRight:
            lvlAdv = 'left'
            #print("Adv: %s" % lvlAdv)
        elif rmsdbRight > rmsdbLeft:
            lvlAdv = 'right'
            #print("Adv: %s" % lvlAdv)
        elif rmsdbLeft == rmsdbRight:
            lvlAdv = None

        #refdb = amp - 3 # apply half amp to each channel
        refdb = amp
        diffdbLeft = np.abs(rmsdbLeft - refdb)
        diffdbRight = np.abs(rmsdbRight - refdb)

        # Adjust left channel
        if rmsdbLeft > refdb:
            sigAdjLeft = sig[0] / db2mag(diffdbLeft)
        elif rmsdbLeft < refdb:
            sigAdjLeft = sig[0] * db2mag(diffdbLeft)
        # Adjust right channel
        if rmsdbRight > refdb:
            sigAdjRight = sig[1] / db2mag(diffdbRight)
        elif rmsdbRight < refdb:
            sigAdjRight = sig[1] * db2mag(diffdbRight)

        # If there is a lvl difference to maintain across channels
        if eq == 'n':
            if lvlAdv == 'left':
                sigAdjLeft = sigAdjLeft * db2mag(ILD/2)
                sigAdjRight = sigAdjRight / db2mag(ILD/2)
            elif lvlAdv == 'right':
                sigAdjLeft = sigAdjLeft / db2mag(ILD/2)
                sigAdjRight = sigAdjRight * db2mag(ILD/2)

        sigBothAdj = np.array([sigAdjLeft, sigAdjRight])
        return sigBothAdj


# RETSPL levels for binaural listening in a sound field,
# in a diffuse field. From ANSI S3.6 (Table 9a). 
RETSPL = {
    20: 78.1, 
    25: 68.7,
    31.5: 59.5,
    40: 51.1,
    50: 44,
    63: 37.5,
    80: 31.5,
    100: 26.5,
    125: 22.1,
    160: 17.9,
    200: 14.4,
    250: 11.4,
    315: 8.4,
    400: 5.8,
    500: 3.8,
    630: 2.1,
    750: 1.2,
    800: 1,
    1000: 0.8,
    1250: 1.9,
    1500: 1,
    1600: 0.5,
    2000: -1.5,
    2500: -3.1,
    3000: -4,
    4000: -3.8,
    6000: 1.4,
    6300: 2.5,
    8000: 6.8,
    9000: 8.4,
    10000: 9.8,
    11200: 11.5,
    14000: 23.2,
    16000: 43.7
}
