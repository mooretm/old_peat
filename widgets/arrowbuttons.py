""" Custom widget with arrow buttons.
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import custom modules
from app_assets import images


#########
# BEGIN #
#########
class ArrowGroup(tk.Frame):
    """ Group of arrow buttons indicating fast/slower 
        and big/small step size
     """
    def __init__(self, parent, button_text, command_args=None, 
    repeat_args=None, **kwargs):
        super().__init__(parent, **kwargs)
        command_args = command_args or {}
        repeat_args = repeat_args or {}

        # Layout
        options = {'padx': 10, 'pady':10}

        # Style
        style = ttk.Style(self)
        style.configure('Big.TLabel', font=("Helvetica", 14))
        style.configure('Big.TButton', font=("Helvetica", 11))

        # LABELS
        # Louder label
        lbl_louder = ttk.Label(self, text="Louder", style="Big.TLabel")
        lbl_louder.grid(row=0, column=0, padx=(5,0))

        # Softer label
        lbl_softer = ttk.Label(self, text="Softer", style="Big.TLabel")
        lbl_softer.grid(row=1, column=0)

        # BUTTONS
        # Big up arrow
        self.big_up_arrow = tk.PhotoImage(file=images.UP_ARROW_BIG)
        ttk.Button(self, takefocus=0, command=command_args['big_up'],
            image=self.big_up_arrow).grid(row=0, column=1, sticky='nsew',
            **options)

        # Small up arrow
        self.small_up_arrow = tk.PhotoImage(file=images.UP_ARROW_SMALL)
        ttk.Button(self, takefocus=0, command=command_args['small_up'],
            image=self.small_up_arrow).grid(row=0, column=2, sticky='nsew',
            **options)       
        
        # Big down arrow
        self.big_down_arrow = tk.PhotoImage(file=images.DOWN_ARROW_BIG)
        ttk.Button(self, takefocus=0, command=command_args['big_down'],
            image=self.big_down_arrow).grid(row=1, column=1, sticky='nsew',
            **options)

        # Small down arrow
        self.small_down_arrow = tk.PhotoImage(file=images.DOWN_ARROW_SMALL)
        ttk.Button(self, takefocus=0, command=command_args['small_down'],
            image=self.small_down_arrow).grid(row=1, column=2, sticky='nsew',
            **options)  

        # Repeat button
        self.btn_repeat = ttk.Button(self, 
            textvariable=button_text, 
            command=repeat_args["start_repeat"],
            style='Big.TButton',
            takefocus=0)
        self.btn_repeat.grid(row=2, column=1, columnspan=2, **options)
