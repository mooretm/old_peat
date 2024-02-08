""" Model to calculate thresholds from PET.
"""

###########
# Imports #
###########
# GUI
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Data Science
import pandas as pd

# System
import glob
import os


class ScoringModel:
    def __init__(self):
        try:
            self.directory = filedialog.askdirectory()
        except KeyError:
            pass

        self._organize_data()


    def _organize_data(self):
        # Get all .csv file names from provided directory
        all_files = glob.glob(os.path.join(self.directory, "*.csv"))

        # Create single dataframe
        li = []
        for file in all_files:
            df = pd.read_csv(file)
            li.append(df)
        self.data = pd.concat(li)
        self.data.reset_index(drop=True, inplace=True)


    def score(self, num_reversals):
        # Validation
        if num_reversals <= 0:
            raise ValueError("Number of reversals cannot be 0 or negative!")
        
        # Calculate thresholds
        thresholds = []
        for sub in self.data['subject'].unique():
            for freq in self.data['test_freq'].unique():
                # Isolate the rows of interest
                freq_mask = self.data['test_freq'] == freq
                temp = self.data[freq_mask].copy()
                reversal_mask = temp['reversal'] == True
                temp = temp[reversal_mask]
                temp.reset_index(drop=True, inplace=True)
                print(temp)

                # Calculate threshold and append to list
                t = temp['desired_level_dB'][-num_reversals:].mean()
                print(t)
                thresholds.append((sub, freq, t,))

        # Create dataframe from list of tuples
        df = pd.DataFrame(thresholds, columns=['subject', 'freq', 'threshold'])
        df.to_csv('thresholds.csv', index=False)

        print(df)
