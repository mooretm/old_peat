""" P.sychophysical E.stimation of A.uditory T.hresholds (PEAT)
    
    Threshold estimation app for SoundGear NRR measurements. 
    For use in the sound field, PEAT presents warble tones (FM)
    to a given number of speakers. RETSPLs have been applied to
    equal loudness. Starting phase and sound field summation of
    the warble tones are accounted for. 

    PEAT uses a 2IAFC task with a 1-up 2-down rule, tracking at 
    the 70.7% correct level (Levitt, 1971). 
    
    Calibrate using a mono 1 kHz warble tone scaled to -40 dB. 

    Written by: Travis M. Moore
    Created: January 4, 2024
"""

###########
# Imports #
###########
# GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# System
from pathlib import Path
import time

# Misc
import webbrowser
import markdown

# Custom Modules
# Menus
from menus import mainmenu
# Exceptions
from exceptions import audio_exceptions
# Models
from models import sessionmodel
from models import versionmodel
from models import audiomodel
from models import calmodel
from models import csvmodel
from models import stimulusmodel
from models import staircase
# Views
from views import mainview
from views import sessionview
from views import audioview
from views import calibrationview
from views import dataview
# Images
from app_assets import images
# Help
from app_assets import README


#########
# BEGIN #
#########
class Application(tk.Tk):
    """ Application root window. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #############
        # Constants #
        #############
        self.NAME = 'P.E.A.T.'
        self.VERSION = '2.0.0'
        self.EDITED = 'February 29, 2024'

        # Create menu settings dictionary
        self._app_info = {
            'name': self.NAME,
            'version': self.VERSION,
            'last_edited': self.EDITED
        }

        # Sampling rate (Hz)
        self.FS = 48000

        # Intervals
        self.INTERVALS = [1, 2]

        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Setup main window
        self.withdraw() # Hide window during setup
        self.resizable(False, False)
        self.title(self.NAME)
        self.taskbar_icon = tk.PhotoImage(
            file=images.LOGO_FULL_PNG
            )
        self.iconphoto(True, self.taskbar_icon)

        # Assign special quit function on window close
        self.protocol('WM_DELETE_WINDOW', self._quit)

        # First trial flag
        self._first_run_flag = True

        # Trial number tracker
        self.trial = 0

        # Load current session parameters from file
        # or load defaults if file does not exist yet
        # Check for version updates and destroy if mandatory
        self.sessionpars_model = sessionmodel.SessionParsModel(self._app_info)
        self._load_sessionpars()

        # Load CSV writer model
        self.csvmodel = csvmodel.CSVModel(self.sessionpars)

        # Load calibration model
        self.calmodel = calmodel.CalModel(self.sessionpars)

        # Load stimulus model
        self.stim_model = stimulusmodel.StimulusModel(self.sessionpars)

        # Load main view
        self.main_frame = mainview.MainFrame(self)
        self.main_frame.grid(row=5, column=5)

        # Add progress bar after loading mainview
        self._progress_bar()

        # Load menus
        self.menu = mainmenu.MainMenu(self, self._app_info)
        self.config(menu=self.menu)

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileSession>>': lambda _: self._show_session_dialog(),
            '<<FileStart>>': lambda _: self.start_new_run(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Data menu
            '<<DataCalculateThresholds>>': lambda _: self.show_scoring_dialog(),

            # Help menu
            '<<HelpREADME>>': lambda _: self._show_help(),
            '<<HelpChangelog>>': lambda _: self._show_changelog(),

            # Session dialog commands
            '<<SessionSubmit>>': lambda _: self._save_sessionpars(),

            # Calibration dialog commands
            '<<CalPlay>>': lambda _: self.play_calibration_file(),
            '<<CalStop>>': lambda _: self.stop_audio(),
            '<<CalibrationSubmit>>': lambda _: self._calc_offset(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),

            # Main View commands
            '<<MainOne>>': lambda _: self._on_1(),
            '<<MainTwo>>': lambda _: self._on_2(),
            '<<MainSubmit>>': lambda _: self._on_submit(),
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        """ Temporarily disable help menu until ready. """
        #self.menu.help_menu.entryconfig('README...', state='disabled')

        # Center main window
        self.center_window()

        # Check for updates
        if (self.sessionpars['check_for_updates'].get() == 'yes') and \
        (self.sessionpars['config_file_status'].get() == 1):
            _filepath = self.sessionpars['version_lib_path'].get()
            u = versionmodel.VersionChecker(_filepath, self.NAME, self.VERSION)
            if u.status == 'mandatory':
                messagebox.showerror(
                    title="New Version Available",
                    message="A mandatory update is available. Please install " +
                        f"version {u.new_version} to continue.",
                    detail=f"You are using version {u.app_version}, but " +
                        f"version {u.new_version} is available."
                )
                self.destroy()
            elif u.status == 'optional':
                messagebox.showwarning(
                    title="New Version Available",
                    message="An update is available.",
                    detail=f"You are using version {u.app_version}, but " +
                        f"version {u.new_version} is available."
                )
            elif u.status == 'current':
                pass
            elif u.status == 'app_not_found':
                messagebox.showerror(
                    title="Update Check Failed",
                    message="Cannot retrieve version number!",
                    detail=f"'{self.NAME}' does not exist in the version library."
                 )
            elif u.status == 'library_inaccessible':
                messagebox.showerror(
                    title="Update Check Failed",
                    message="The version library is unreachable!",
                    detail="Please check that you have access to Starfile."
                )


    #####################
    # General Functions #
    #####################
    def center_window(self):
        """ Center the root window. """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _progress_bar(self):
        """ Create and position task progress bar. The progress 
            bar updates based on the number of frequencies 
            remaining to test in a given session.
        """
        self.progress_bar = ttk.Progressbar(
            master=self,
            orient='horizontal',
            mode='determinate',
            length=self.winfo_width()
        )
        self.progress_bar.grid(row=10, column=5, columnspan=40, sticky='nsew')


    def bind_keys(self):
        """ Bind keys to main_frame response functions. """
        self.bind('1', lambda event: self.main_frame.on_1())
        self.bind('2', lambda event: self.main_frame.on_2())


    def unbind_keys(self):
        """ Unbind keys to main_frame response functions. """
        self.unbind('1')
        self.unbind('2')


    def _quit(self):
        """ Exit the application. """
        self.destroy()


    ###################
    # File Menu Funcs #
    ###################
    def start_new_run(self):
        """ 1. Disable "Start Task" from file menu.
            2. Get number of frequencies to test (for progress bar).
            3. Create staircase.
            4. Present first trial.
            Repeat steps 2 - 4 for each new run (i.e., frequency).
        """
        # Check for first run
        if self._first_run_flag:
            # Disable "Start Task" from File menu
            self.menu.file_menu.entryconfig('Start Task', state='disabled')

            # Get frequencies
            # Query AFTER the task starts to capture updates to sessioninfo
            self.freqs, self.NUM_FREQS = self.stim_model.get_test_freqs()

            # Set first run flag to False
            self._first_run_flag = False
            
        # Get next frequency or end
        try:
            self.current_freq = self.freqs.pop(0)
            print(f"\ncontroller: Testing {self.current_freq} Hz")
            messagebox.showinfo(
                title="Ready",
                message="When you are ready, close this window to continue."
            )
        except IndexError:
            print(f"\ncontroller: Session ended by start_new_run")
            messagebox.showinfo(
                title="Task Complete",
                message="You have finished this task. Please let the "
                    "investigator know."
            )
            self._quit()
            return

        # Generate stimulus
        self.stim = self.stim_model.create_stimulus(
            dur=self.sessionpars['duration'].get(),
            fs=self.FS,
            fc=self.current_freq,
            mod_rate=5,
            mod_depth=5
        )

        # Update progress bar
        if self.progress_bar['value'] < 100:
            self.progress_bar['value'] += 100/self.NUM_FREQS

        # Convert step_sizes to list of ints
        steps = self.sessionpars['step_sizes'].get()
        steps = [int(val) for val in steps.split(', ')]

        # Create staircase
        self.staircase = staircase.Staircase(
            start_val=self.sessionpars['starting_level'].get(),
            step_sizes=steps,
            nUp=1,
            nDown=2,
            nTrials=0,
            nReversals=self.sessionpars['num_reversals'].get(),
            rapid_descend=self.sessionpars['rapid_descend_bool'].get(),
            min_val=self.sessionpars['min_level'].get(),
            max_val=self.sessionpars['max_level'].get()
        )

        # Start first trial
        self._new_trial()


    def _new_trial(self):
        """ Present a 2IAFC trial. """
        # Print message to console
        self.msg = f"Trial {self.trial}: {self.current_freq} Hz"
        print('')
        print('*' * 60)
        print(self.msg)
        print('*' * 60)

        # Assign stimulus to an interval
        self.stim_interval = self.stim_model.assign_stimulus_interval(
            intervals=self.INTERVALS
        )
        print(f"controller: Stimulus is in interval {self.stim_interval}")

        # Calculate the RETSPL-adjusted, single channel level
        final_single_chan_level = self.stim_model.calc_presentation_lvl(
            stair_lvl=self.staircase.current_level,
            freq = self.current_freq
        )

        # Apply offset to desired dB level
        # (Also update sessionpars)
        self._calc_level(final_single_chan_level)

        # # Print values to console
        # print(f"Staircase level: {self.staircase.current_level}")
        # print(f"Unscaled final single chan level: {final_single_chan_level}")
        # print(f"Scaled final single chan level: " +
        #       f"{self.sessionpars['adjusted_level_dB'].get()}")

        # Pause
        time.sleep(0.5)
        
        # Interval 1
        self.main_frame.interval_1_colors()
        if self.stim_interval == 1:
            self.present_audio(
                audio=self.stim,
                pres_level=self.sessionpars['adjusted_level_dB'].get(),
                sampling_rate=self.FS
            )
        time.sleep(self.sessionpars['duration'].get() + 0.15)

        # ISI
        self.main_frame.clear_interval_colors()
        time.sleep(0.5)

        # Interval 2
        self.main_frame.interval_2_colors()
        if self.stim_interval == 2:
            self.present_audio(
                audio=self.stim,
                pres_level=self.sessionpars['adjusted_level_dB'].get(),
                sampling_rate=self.FS
            )
        time.sleep(self.sessionpars['duration'].get() + 0.15)

        # End
        self.main_frame.clear_interval_colors()

        # Wait to bind keys until after trial has finished
        #   to avoid multiple submissions during the presentation
        self.after(10, lambda: self.bind_keys())


    ########################
    # Main View Functions #
    ########################
    def _on_1(self):
        """ Set response value to 1 (yes). """
        self.response = 1


    def _on_2(self):
        """ Set response value to 0 (no). """
        self.response = 2


    def _on_submit(self):
        """ Assign response value and save to file.
            Update key bindings.
            Present next trial.
        """
        # Assign response value
        if (self.response == 1) and (self.stim_interval == 1):
            self.staircase.add_response(1)
        elif (self.response == 2) and (self.stim_interval == 2):
            self.staircase.add_response(1)
        else: 
            self.staircase.add_response(-1)

        # Save the trial data
        self._save_trial_data()

        # Update trial counter
        self.trial += 1

        # Unbind keys for the start of the next trial
        self.unbind_keys()

        # Check for end of staircase
        if not self.staircase.status:
            print(f"\ncontroller: End of staircase!")
            if self.sessionpars['disp_plots'].get() == 1:
                self.staircase.plot_data()
            # Call start_new_run to get next frequency
            self.start_new_run()
        else:
            self._new_trial()


    def _save_trial_data(self):
        """ Select data to save and write to CSV. """
        # Get tk variable values
        converted = dict()
        for key in self.sessionpars:
            converted[key] = self.sessionpars[key].get()

        # Add most recent datapoint object attributes to dict
        converted.update(self.staircase.dw.datapoints[-1].__dict__)

        # Add 1 to trial number
        converted['trial'] = self.trial + 1

        # Add current test frequency to dict
        converted['test_freq'] = self.current_freq

        # Define selected items for writing to file
        save_list = [
            'trial', 'subject', 'condition', 'min_level', 'max_level', 
            'duration', 'step_sizes', 'num_reversals', 'rapid_descend', 
            'slm_reading', 'cal_level_dB', 'slm_offset', 'adjusted_level_dB',
             'desired_level_dB', 'test_freq', 'response', 'reversal'
        ]

        # Create new dict with desired items
        try:
            data = dict((k, converted[k]) for k in save_list)
        except KeyError as e:
            print('\ncontroller: Unexpected variable when attempting ' +
                  f'to save: {e}')
            messagebox.showerror(
                title="Undefined Variable",
                message="Data not saved!",
                detail=f'{e} is undefined.'
            )
            self.destroy()
            return

        # Write data to file
        print('\ncontroller: Attempting to save record')
        try:
            self.csvmodel.save_record(data)
        except PermissionError as e:
            print(e)
            messagebox.showerror(
                title="Access Denied",
                message="Data not saved! Cannot write to file!",
                detail=e
            )
            self.destroy()
            return


    ############################
    # Session Dialog Functions #
    ############################
    def _show_session_dialog(self):
        """ Show session parameter dialog. """
        print("\ncontroller: Calling session dialog...")
        self.update_idletasks()
        sessionview.SessionDialog(self, self.sessionpars)


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict. """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from session model fields
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("\ncontroller: Loaded sessionpars model fields into " +
            "running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save current runtime parameters to file. """
        print("\ncontroller: Calling sessionpars model set and save funcs")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()


    ########################
    # Tools Menu Functions #
    ########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog. """
        print("\ncontroller: Calling audio dialog")
        audioview.AudioDialog(self, self.sessionpars)

    def _show_calibration_dialog(self):
        """ Display the calibration dialog window. """
        print("\ncontroller: Calling calibration dialog")
        calibrationview.CalibrationDialog(self, self.sessionpars)


    #######################
    # Data Menu Functions #
    #######################
    def show_scoring_dialog(self):
        """ Display the threshold calculation dialog. """
        print("\ncontroller: Calling threshold dialog")
        dataview.ThresholdDialog(self)


    ################################
    # Calibration Dialog Functions #
    ################################
    def play_calibration_file(self):
        """ Load calibration file and present. """
        # Get calibration file
        try:
            self.calmodel.get_cal_file()
        except AttributeError:
            messagebox.showerror(
                title="File Not Found",
                message="Cannot find internal calibration file!",
                detail="Please use a custom calibration file."
            )
        # Present calibration signal
        self.present_audio(
            audio=Path(self.calmodel.cal_file), 
            pres_level=self.sessionpars['cal_level_dB'].get()
        )


    def _calc_offset(self):
        """ Calculate offset based on SLM reading. """
        # Calculate new presentation level
        self.calmodel.calc_offset()
        # Save level - this must be called here!
        self._save_sessionpars()


    def _calc_level(self, desired_spl):
        """ Calculate new dB FS level using slm_offset. """
        # Calculate new presentation level
        self.calmodel.calc_level(desired_spl)
        # Save level - this must be called here!
        self._save_sessionpars()


    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html README file and display in browser. """
        print(f"\ncontroller: Calling README file (will open in browser)")
        # Read markdown file and convert to html
        with open(README.README_MD, 'r') as f:
            text = f.read()
            html = markdown.markdown(text)

        # Create html file for display
        with open(README.README_HTML, 'w') as f:
            f.write(html)

        # Open README in default web browser
        webbrowser.open(README.README_HTML)


    def _show_changelog(self):
        """ Create html CHANGELOG file and display in browser. """
        print(f"\ncontroller: Calling CHANGELOG file (will open in browser)")
        # Read markdown file and convert to html
        with open(README.CHANGELOG_MD, 'r') as f:
            text = f.read()
            html = markdown.markdown(text)

        # Create html file for display
        with open(README.CHANGELOG_HTML, 'w') as f:
            f.write(html)

        # Open README in default web browser
        webbrowser.open(README.CHANGELOG_HTML)


    ###################
    # Audio Functions #
    ###################
    def present_audio(self, audio, pres_level, **kwargs):
        """ Attempt to create and present audio object. """
        # Load audio
        try:
            self._create_audio_object(audio, **kwargs)
        except audio_exceptions.InvalidAudioType as e:
            messagebox.showerror(
                title="Invalid Audio Type",
                message="The audio type is invalid!",
                detail=f"{e} Please provide a Path or ndarray object."
            )
            return
        except audio_exceptions.MissingSamplingRate as e:
            messagebox.showerror(
                title="Missing Sampling Rate",
                message="No sampling rate was provided!",
                detail=f"{e} Please provide a Path or ndarray object."
            )
            return

        # Play audio
        self._play(pres_level)


    def _create_audio_object(self, audio, **kwargs):
        """ Create audio object from audiomodel. """
        try:
            self.a = audiomodel.Audio(
                audio=audio,
                **kwargs
            )
        except FileNotFoundError:
            messagebox.showerror(
                title="File Not Found",
                message="Cannot find the audio file!",
                detail="Go to File>Session to specify a valid audio path."
            )
            self._show_session_dialog()
            return
        except audio_exceptions.InvalidAudioType:
            raise
        except audio_exceptions.MissingSamplingRate:
            raise


    def _play(self, pres_level):
        """ Format channel routing, present audio and catch 
            exceptions.
        """
        # Attempt to present audio
        try:
            self.a.play(
                level=pres_level,
                device_id=self.sessionpars['audio_device'].get(),
                routing=self._format_routing(
                    self.sessionpars['channel_routing'].get())
            )
        except audio_exceptions.InvalidAudioDevice as e:
            print(e)
            messagebox.showerror(
                title="Invalid Device",
                message="Invalid audio device! Go to Tools>Audio Settings " +
                    "to select a valid audio device.",
                detail = e
            )
            # Open Audio Settings window
            self._show_audio_dialog()
        except audio_exceptions.InvalidRouting as e:
            print(e)
            messagebox.showerror(
                title="Invalid Routing",
                message="Speaker routing must correspond with the " +
                    "number of channels in the audio file! Go to " +
                    "Tools>Audio Settings to update the routing.",
                detail=e
            )
            # Open Audio Settings window
            self._show_audio_dialog()
        except audio_exceptions.Clipping:
            print("controller: Clipping has occurred! Aborting!")
            messagebox.showerror(
                title="Clipping",
                message="The level is too high and caused clipping.",
                detail="The waveform will be plotted when this message is " +
                    "closed for visual inspection."
            )
            self.a.plot_waveform("Clipped Waveform")


    def stop_audio(self):
        """ Stop audio presentation. """
        try:
            self.a.stop()
        except AttributeError:
            print("\ncontroller: Stop called without audio object!")


    def _format_routing(self, routing):
        """ Convert space-separated string to list of ints
            for speaker routing.
        """
        routing = routing.split()
        routing = [int(x) for x in routing]

        return routing


if __name__ == "__main__":
    app = Application()
    app.mainloop()
