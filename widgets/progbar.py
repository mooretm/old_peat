""" Custom progress bar widget.
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk


#########
# Begin #
#########
class ProgressBar(tk.Toplevel):
    """ Class for indeterminate progress bar. Called from 
        within a thread.
    """
    def __init__(self, parent, pb_length):
        tk.Toplevel.__init__(self, parent)
        self.focus_force()
        self.grab_set()
        self.title("Preparing Hearing Aids...")

        # Create progress bar
        self.progbar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='indeterminate',
            length=pb_length
        )
        self.progbar.grid(row=5, column=5, padx=5, pady=5)
