""" Class for creating stimuli and calculating presentation level.
"""

###########
# Imports #
###########
# Data Science
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# System
import random

# Custom Modules
from functions import general


#########
# BEGIN #
#########
class StimulusModel:
    def __init__(self, sessionpars):

        # Assign variables
        self.sessionpars = sessionpars

        # RETSPL levels for binaural listening in a sound field,
        # in a diffuse field. From ANSI S3.6 (Table 9a). 
        self.RETSPL = {
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


    def get_test_freqs(self):
        freqs = self.sessionpars['test_freqs'].get()
        self.FREQS = [int(val) for val in freqs.split(', ')]
        self.freqs = self.FREQS
        self.NUM_FREQS = len(self.FREQS)

        return self.freqs, self.NUM_FREQS


    def assign_stimulus_interval(self, intervals):
        """ Randomly assign stimulus to an interval. """
        stim_interval = random.sample(intervals, 1)
        return stim_interval[0]


    def calc_presentation_lvl(self, stair_lvl, freq):
        """ Calculate the final presentation level based on:
                1. Staircase level
                2. RETSPL @ current frequency
                3. Adjust for number of sound field channels
        """
        # Get RETSPL and add to desired level
        my_level = stair_lvl
        retspl = self.RETSPL[freq]
        retspl_adj_level = my_level + retspl

        # Calculate desired RMS level based on 
        # number of channels and desired SPL
        multichan_lvl = general.calc_RMS_based_on_sources(
            desired_SPL=retspl_adj_level,
            num_sources=self.sessionpars['num_stim_chans'].get()
        )

        return multichan_lvl


    def _get_random_phis(self):
        """ Generate n random phi values, in radians, based 
            on the number of sources/channels.
        """
        # Get number of sources/channels
        stim_chans = self.sessionpars['num_stim_chans'].get()
        
        # # Create range of phase values in degrees, 
        # #   separated by at least 10 degs.
        # degrees = range(0, 180, 10)
        # # Remove 180
        # degrees = [x for x in degrees if x != 180] 
        # # Set random seed for reproducible random numbers
        
        # List of possible starting phases that Daniel Smieja
        # vetted for me.
        degrees = [0, 40, 80, 120, 150, -40, -80, -120, -150]
        # Create an independent random number rng
        rng = random.Random(217)
        # Get list of random phases in degrees
        random_degs = rng.sample(degrees, k=stim_chans)
        # Return random phases in radians
        return np.radians(random_degs)


    def create_stimulus(self, dur, fs, fc, mod_rate, mod_depth):
        # Get number of sources/channels
        stim_chans = self.sessionpars['num_stim_chans'].get()

        # Get random phi values in radians based on number of sources
        phi_rad = self._get_random_phis()
        
        # Generate an n-channel warble tone array
        sig_list = []
        for ii in range(0, stim_chans):
            # Generate warble tone based on current freq
            wt = general.warble_tone(
                dur=dur,
                fs=fs, 
                fc=fc,
                phi=phi_rad[ii],
                mod_rate=mod_rate,
                mod_depth=mod_depth
            )
            # Apply gating
            wt = general.doGate(wt, rampdur=0.04, fs=fs)

            # Scale to -40 (default for this system)
            wt = general.setRMS(wt, -40)

            # # Plot first two cycles to illustrate random starting phase
            # period = 1/fc
            # samps = int(period * fs)
            # samps = samps * 2
            # plt.plot(wt[:samps])
            # plt.show()
            # plt.close()

            # Add individual wt to list
            sig_list.append(np.array(wt))

        sig_list = np.array(sig_list).T
        #print(f"\ncontroller: signal shape: {sig_list.shape}")

        #import soundfile as sf
        #sf.write('1kHz_-40.wav', sig_list, 48000)

        return sig_list




    # def _create_stimulus_dict(self):
    #     test_freqs = self.sessionpars['test_freqs'].get()
    #     test_freqs = general.string_to_list(test_freqs)

    #     stim_dict = {}
    #     for f in test_freqs:
    #         stim_dict[f] = general.warble_tone(
    #             dur=self.sessionpars['duration'].get(),
    #             fs=48000,
    #             fc=f,
    #             mod_rate=5,
    #             mod_depth=5
    #         )
    #     return stim_dict
