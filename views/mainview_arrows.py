""" Main view for MOA task on the fly.
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import custom modules
from widgets import arrowbuttons


#########
# BEGIN #
#########
class ArrowsAudiometer(ttk.Frame):
    def __init__(self, parent, _button_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self._button_id = _button_id

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        style = ttk.Style(self)
        style.configure('Big.TLabel', font=("Helvetica", 14))
        style.configure('Big.TLabelframe.Label', font=("Helvetica", 11))
        style.configure('Big.TButton', font=("Helvetica", 11))
        style.configure('Red.TFrame', background='red')


        #################
        # Create frames #
        #################
        options = {'padx':10, 'pady':10}

        # Main container
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5)

        # Arrow buttons frame
        self.arrow_frm_text = tk.StringVar(value='Presentation Controls')
        self.arrow_frm_label = ttk.Label(textvariable=self.arrow_frm_text)
        #self.frm_arrows = ttk.LabelFrame(frm_main, text="Presentation Controls")
        self.frm_arrows = ttk.LabelFrame(frm_main, labelwidget=self.arrow_frm_label)
        self.frm_arrows.grid(row=1, column=0, padx=15, pady=15)

        # Button frame
        frm_button = ttk.Frame(frm_main)
        frm_button.grid(row=1, column=1)


        ##################
        # Create Widgets #
        ##################
        # Arrow buttons controls
        self.button_text = tk.StringVar(value="Present")
        arrowbuttons.ArrowGroup(self.frm_arrows, button_text=self.button_text, 
            command_args = {
                'big_up': self.big_up,
                'small_up': self.small_up,
                'big_down': self.big_down,
                'small_down': self.small_down
            },
            repeat_args = {
                'start_repeat': self.start_repeat
            }).grid(row=0, column=0)
        
        # Submit button
        self.btn_submit = ttk.Button(frm_button, text="Submit", 
            command=self._on_submit, style='Big.TButton',
            takefocus=0)
        self.btn_submit.grid(row=0, column=0, padx=(0,15))


    #############
    # Functions #
    #############
    # Button functions
    def big_up(self):
        """ Send button_id and play event """
        self._button_id['button_id'].set("big_up_arrow")
        self.event_generate('<<MainArrowButton>>')


    def small_up(self):
        """ Send button_id and play event """
        self._button_id['button_id'].set("small_up_arrow")
        self.event_generate('<<MainArrowButton>>')


    def big_down(self):
        """ Send button_id and play event """
        self._button_id['button_id'].set("big_down_arrow")
        self.event_generate('<<MainArrowButton>>')


    def small_down(self):
        """ Send button_id and play event """
        self._button_id['button_id'].set("small_down_arrow")
        self.event_generate('<<MainArrowButton>>')


    def start_repeat(self):
        """ Present audio. Can be repeated as many times as 
            the listener wants without incrementing the 
            file list.
        """
        # Create stimulus on first "START"
        if self.flag == 'ready':
            print(f"\nmainview: New trial started")
            print("mainview: Sending create stimulus event to controller")
            self.event_generate('<<MainStart>>')
            self.flag = 'running'
        elif self.flag == 'running':
            self.event_generate('<<MainPlayAudio>>')
   

    def _on_submit(self):
        # Send save data event to app
        self.event_generate('<<MainSave>>')


    def get(self):
        """ Retrieve data as dictionary """
        data = dict()
        for key, variable in self._button_id.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message=f'Error with: {key}.'
                raise ValueError(message)
        return data


    def reset(self):
        """ Clear all values """   
        for var in self._button_id.values():
            var.set('')
        # Disable submit button on press
        # Set focus to play button
        self.btn_submit.config(state="disabled")
