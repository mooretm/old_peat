""" Model to calculate thresholds from P.E.A.T. """

###########
# Imports #
###########
# GUI
from tkinter import filedialog

# Data Science
import numpy as np
import pandas as pd

# System
import glob
import os


class ScoringModel:
    def __init__(self):
        """ Display system file browser and save data dir. """
        try:
            self.directory = filedialog.askdirectory()
        except KeyError:
            pass

        self._organize_data()


    def _organize_data(self):
        """ Concatenate data from all CSVs in dir. """
        # Get all .csv file names from provided directory
        all_files = glob.glob(os.path.join(self.directory, "*.csv"))

        # Create single dataframe
        li = []
        for file in all_files:
            df = pd.read_csv(file)
            li.append(df)
        self.data = pd.concat(li)
        self.data.reset_index(drop=True, inplace=True)


    def _avg_revs(self, df, num_reversals) -> float:
        """ Custom function for use with Pandas apply().
            Called from score().
            Find last n reversals and average to calculate thresholds.

            Returns: a single threshold value (rounded)
        """
        # Get indexes of last n reversals
        last_n_indexes = df.index[df['reversal']==True].to_list()[-num_reversals:]
        # Calculate thresholds
        thresholds = np.round(np.mean(df['desired_level_dB'][last_n_indexes]), 2)
        return thresholds
        

    def score(self, num_reversals):
        """ Calculate thresholds and write to CSV. """
        # Validation
        if num_reversals <= 0:
            raise ValueError("Number of reversals cannot be 0 or negative!")

        # Get dataframe of thresholds derived from the last n reversals
        thresholds = self.data.groupby(
            by=[
                'subject', 
                'condition', 
                'test_freq'
            ]
        ).apply(self._avg_revs, num_reversals=num_reversals)

        # Organize dataframe
        thresholds_df = thresholds.reset_index()
        self.thresholds_df = thresholds_df.rename(columns={0:'threshold'})

        self.write_to_csv(self.thresholds_df)


    def write_to_csv(self, data_to_write):
        """ Wrapper 'to_csv' function for easier unit testing. """
        # Write thresholds to CSV
        data_to_write.to_csv('thresholds.csv', index=False)
        print(f"\nscoringmodel: Thresholds written to CSV successfully")
