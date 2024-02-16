""" Session parameters dialog
"""

###########
# Imports #
###########
# GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from idlelib.tooltip import Hovertip


#########
# BEGIN #
#########
class SessionDialog(tk.Toplevel):
    """ Dialog for setting session parameters
    """
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        self.withdraw()
        self.resizable(False, False)
        self.title("Settings")
        self.grab_set()


        #################
        # Create Frames #
        #################
        # Shared frame settings
        frame_options = {'padx': 10, 'pady': 10}
        widget_options = {'padx': 5, 'pady': 5}

        # Session info frame
        frm_session = ttk.Labelframe(self, text='Session Information')
        frm_session.grid(row=5, column=5, **frame_options, sticky='nsew')

        # Stimulus options frame
        frm_stimulus = ttk.Labelframe(self, text='Stimulus Options')
        frm_stimulus.grid(row=10, column=5, **frame_options, sticky='nsew')

        # Staircase options frame
        frm_staircase = ttk.Labelframe(self, text='Staircase Options')
        frm_staircase.grid(row=15, column=5, **frame_options, sticky='nsew')

        # # Audio file browser frame
        # frm_audiopath = ttk.Labelframe(self, text="Audio File Directory")
        # frm_audiopath.grid(row=15, column=5, **frame_options, ipadx=5, 
        #     ipady=5)

        # # Matrix file browser frame
        # frm_matrixpath = ttk.Labelframe(self, text='Matrix File Path')
        # frm_matrixpath.grid(row=20, column=5, **frame_options, ipadx=5, 
        #     ipady=5)


        ################
        # Draw Widgets #
        ################
        tt_delay = 1000 # ms

        # SESSION #
        # Subject
        lbl_sub = ttk.Label(frm_session, text="Subject:")
        lbl_sub.grid(row=5, column=5, sticky='e', **widget_options)
        sub_tt = Hovertip(
            anchor_widget=lbl_sub, 
            text="A unique subject identifier.\nCan be alpha, numeric, or both.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['subject']
            ).grid(row=5, column=10, sticky='w')

        # Condition
        lbl_cond = ttk.Label(frm_session, text="Condition:")
        lbl_cond.grid(row=10, column=5, sticky='e', **widget_options)
        cond_tt = Hovertip(
            anchor_widget=lbl_cond, 
            text="A unique condition name.\nCan be alpha, numeric, or both.\nSeparate words with underscores.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['condition']
            ).grid(row=10, column=10, sticky='w')

        # Plots
        chk_plots = ttk.Checkbutton(frm_session, text="Display Plots",
            takefocus=0, variable=self.sessionpars['disp_plots'])
        chk_plots.grid(row=15, column=5,  columnspan=20, sticky='w', 
            **widget_options)
        plots_tt = Hovertip(
            anchor_widget=chk_plots,
            text="Display staircase plots after each threshold.",
            hover_delay=tt_delay
        )


        # STIMULUS #
        # Number of channels for stimulus
        lbl_num_chans = ttk.Label(frm_stimulus, text="Channels:")
        lbl_num_chans.grid(row=5, column=5, sticky='e', **widget_options)
        num_chans_tt = Hovertip(
            anchor_widget=lbl_num_chans,
            text="The number of channels for audio playback.\nUpdate channel routing accordingly.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_stimulus, width=20, 
            textvariable=self.sessionpars['num_stim_chans']
            ).grid(row=5, column=10, sticky='w')

        # Duration
        lbl_dur = ttk.Label(frm_stimulus, text="Duration (s):")
        lbl_dur.grid(row=10, column=5, sticky='e', **widget_options)
        dur_tt = Hovertip(
            anchor_widget=lbl_dur,
            text="Duration of the stimulus (per interval) in seconds.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_stimulus, width=20, 
            textvariable=self.sessionpars['duration']
            ).grid(row=10, column=10, sticky='w')

        # Test Frequencies
        lbl_freqs = ttk.Label(frm_stimulus, text="Frequencies (Hz):")
        lbl_freqs.grid(row=15, column=5, sticky='e', **widget_options)
        freqs_tt = Hovertip(
            anchor_widget=lbl_freqs,
            text="Frequencies to test in a given session.\nSeparate multiple frequencies with a comma and space.\nFrequencies will be tested in the order provided.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_stimulus, width=50, 
            textvariable=self.sessionpars['test_freqs']
            ).grid(row=15, column=10, sticky='w', padx=(0,10))


        # STAIRCASE #
        # Starting Level
        lbl_level = ttk.Label(frm_staircase, text="Starting Level (dB):")
        lbl_level.grid(row=5, column=5, sticky='e', **widget_options)
        level_tt = Hovertip(
            anchor_widget=lbl_level,
            text="The starting level for each new threshold search.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_staircase, width=20, 
            textvariable=self.sessionpars['starting_level']
            ).grid(row=5, column=10, sticky='w')

        # Minimum Level
        lbl_min_lvl = ttk.Label(frm_staircase, text="Minimum Level (dB):")
        lbl_min_lvl.grid(row=10, column=5, sticky='e', **widget_options)
        min_lvl_tt = Hovertip(
            anchor_widget=lbl_min_lvl,
            text="The minimum permissible output level.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_staircase, width=20, 
            textvariable=self.sessionpars['min_level']
            ).grid(row=10, column=10, sticky='w')
        
        # Maximum Level
        lbl_max_lvl = ttk.Label(frm_staircase, text="Maximum Level (dB):")
        lbl_max_lvl.grid(row=15, column=5, sticky='e', **widget_options)
        max_lvl_tt = Hovertip(
            anchor_widget=lbl_max_lvl,
            text="The maximum permissible output level.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_staircase, width=20, 
            textvariable=self.sessionpars['max_level']
            ).grid(row=15, column=10, sticky='w')
        
        # Step Sizes
        lbl_steps = ttk.Label(frm_staircase, text="Step Size(s):")
        lbl_steps.grid(row=20, column=5, sticky='e', **widget_options)
        steps_tt = Hovertip(
            anchor_widget=lbl_steps,
            text="The step size(s) used by the staircase to bracket a " + \
                "threshold.\nThe last step size will be repeated until " + \
                "all reversals have been collected.\nSeparate multiple " + \
                "values with a comma and space.",
                hover_delay=tt_delay
        )
        ttk.Entry(frm_staircase, width=20, 
            textvariable=self.sessionpars['step_sizes']
            ).grid(row=20, column=10, sticky='w')

        # Number of Reversals
        lbl_num_revs = ttk.Label(frm_staircase, text="Reversals:")
        lbl_num_revs.grid(row=25, column=5, sticky='e', **widget_options)
        num_revs_tt = Hovertip(
            anchor_widget=lbl_num_revs,
            text="The number of reversals to obtain before stopping the procedure.",
            hover_delay=tt_delay
        )
        ttk.Entry(frm_staircase, width=20, 
            textvariable=self.sessionpars['num_reversals']
            ).grid(row=25, column=10, sticky='w')

        # Rapid Descend
        lbl_descend = ttk.Label(frm_staircase, text="Rapid Descend:")
        lbl_descend.grid(row=30, column=5, sticky='e', **widget_options)
        descend_tt = Hovertip(
            anchor_widget=lbl_descend,
            text="Initial decrease with 1-down rule to reach threshold faster.",
            hover_delay=tt_delay
        )
        vlist = ["Yes", "No"]
        ttk.Combobox(
            frm_staircase, 
            textvariable=self.sessionpars['rapid_descend'], 
            values=vlist,
            state='readonly'
        ).grid(row=30, column=10, sticky='w')

        # Number of Presentations
        # ttk.Label(frm_stimulus, text="Presentations:"
        #     ).grid(row=30, column=5, sticky='e', **widget_options)
        # ttk.Entry(frm_stimulus, width=20, 
        #     textvariable=self.sessionpars['presentations']
        #     ).grid(row=30, column=10, sticky='w')

        # # Randomize
        # #self.random_var = tk.IntVar(value=self.sessionpars['randomize'])
        # chk_random = ttk.Checkbutton(frm_stimulus, text="Randomize",
        #     takefocus=0, variable=self.sessionpars['randomize'])
        # chk_random.grid(row=5, column=5,  columnspan=20, sticky='w', 
        #     **widget_options)

        # # Repetitions
        # ttk.Label(frm_stimulus, text="Presentation(s):"
        #     ).grid(row=10, column=5, sticky='e', **widget_options)
        # ttk.Entry(frm_stimulus, width=20, 
        #     textvariable=self.sessionpars['repetitions']
        #     ).grid(row=10, column=10, sticky='w')


        # ###################
        # # Audio Directory #
        # ###################
        # # Descriptive label
        # ttk.Label(frm_audiopath, text="Path:"
        #     ).grid(row=20, column=5, sticky='e', **widget_options)

        # # Retrieve and truncate previous audio directory
        # short_audio_path = general.truncate_path(
        #     self.sessionpars['audio_files_dir'].get()
        # )

        # # Create textvariable
        # self.audio_var = tk.StringVar(value=short_audio_path)

        # # Audio directory label
        # ttk.Label(frm_audiopath, textvariable=self.audio_var, 
        #     borderwidth=2, relief="solid", width=60
        #     ).grid(row=20, column=10, sticky='w')
        # ttk.Button(frm_audiopath, text="Browse", 
        #     command=self._get_audio_directory,
        #     ).grid(row=25, column=10, sticky='w', pady=(0, 10))


        # ####################
        # # Matrix Directory #
        # ####################
        # # Descriptive label
        # ttk.Label(frm_matrixpath, text="Path:"
        #     ).grid(row=30, column=5, sticky='e', **widget_options)
        
        # # Retrieve and truncate existing audio directory
        # short_matrix_path = general.truncate_path(
        #     self.sessionpars['matrix_file_path'].get()
        # )

        # # Create textvariable
        # self.matrix_var = tk.StringVar(value=short_matrix_path)

        # # Matrix file label
        # ttk.Label(frm_matrixpath, textvariable=self.matrix_var, 
        #     borderwidth=2, relief="solid", width=60
        #     ).grid(row=30, column=10, sticky='w')
        # ttk.Button(frm_matrixpath, text="Browse", 
        #     command=self._get_matrix_file).grid(row=35, column=10, 
        #     sticky='w', pady=(0, 10))


        # Submit button
        btn_submit = ttk.Button(self, text="Submit", command=self._on_submit)
        btn_submit.grid(row=40, column=5, columnspan=2, pady=(0, 10))

        # Center the session dialog window
        self.center_window()


    #############
    # Functions #
    #############
    def center_window(self):
        """ Center the TopLevel window over the root window. """
        # Get updated window size (after drawing widgets)
        self.update_idletasks()

        # Calculate the x and y coordinates to center the window
        x = self.parent.winfo_x() \
            + (self.parent.winfo_width() - self.winfo_reqwidth()) // 2
        y = self.parent.winfo_y() \
            + (self.parent.winfo_height() - self.winfo_reqheight()) // 2

        # Set the window position
        self.geometry("+%d+%d" % (x, y))

        # Display window
        self.deiconify()


    def _check_reversals(self):
        revs = self.sessionpars['num_reversals'].get() 
        steps = int(len(self.sessionpars['step_sizes'].get().split()))

        return revs >= steps


    def _check_levels(self):
        min_level = self.sessionpars['min_level'].get()
        max_level = self.sessionpars['max_level'].get()

        return max_level > min_level


    def _on_submit(self):
        """ Check number of presentations != 0.
            Send submit event to controller.
        """
        # Make sure the number of presentations isn't 0
        #self._check_presentations()

        # Make sure the number of reversals at least matches
        # the number of steps
        if not self._check_reversals():
            messagebox.showerror(
                title="Not Enough Reversals",
                message="The number of reversals must at least equal the " + 
                    "number of steps."
            )
            return
        
        if not self._check_levels():
            messagebox.showerror(
                title="Invalid Levels",
                message="The maximum level must exceed the minimum level."
            )
            return

        print("\nviews_sessiondialog: Sending save event...")
        self.parent.event_generate('<<SessionSubmit>>')
        self.destroy()

    # def _get_audio_directory(self):
    #     """ Get path to audio files
    #     """
    #     # Get directory from dialog
    #     filename = filedialog.askdirectory(title="Audio File Directory")

    #     # Update sessionpars with audio files dir
    #     self.sessionpars['audio_files_dir'].set(filename)

    #     # Update audio label
    #     self.audio_var.set(general.truncate_path(filename))


    # def _get_matrix_file(self):
    #     """ Get path to matrix file
    #     """
    #     # Get file from dialog
    #     filename = filedialog.askopenfilename(title="Matrix File", 
    #         filetypes=[("CSV", "*.csv")])
        
    #     # Update sessionpars with matrix file path
    #     self.sessionpars['matrix_file_path'].set(filename)

    #     # Update matrix label
    #     self.matrix_var.set(general.truncate_path(filename))


    # def _check_presentations(self):
    #     if self.sessionpars['repetitions'].get() == 0:
    #         self.sessionpars['repetitions'].set(1)
    #         messagebox.showwarning(title="Seriously?",
    #             message="Invalid number of presentations!",
    #             detail="You must have at least 1 round of presentations! " +
    #                 "Updating to 1 presentation."
    #         )
