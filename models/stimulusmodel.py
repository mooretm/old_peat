""" Class for importing matrix file and preparing trials.
"""

###########
# Imports #
###########
# Data science packages
import pandas as pd

# System packages
import random
import os
from pathlib import Path

# Custom modules
from functions import general


#########
# BEGIN #
#########
class StimulusModel:
    def __init__(self, sessionpars):

        # Assign variables
        self.sessionpars = sessionpars


    def _create_stimulus_dict(self):
        test_freqs = self.sessionpars['test_freqs'].get()
        test_freqs = general.string_to_list(test_freqs)

        stim_dict = {}
        for f in test_freqs:
            stim_dict[f] = general.warble_tone(
                dur=self.sessionpars['duration'].get(),
                fs=48000,
                fc=f,
                mod_rate=5,
                mod_depth=5
            )
        return stim_dict
