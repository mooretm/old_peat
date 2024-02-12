""" Main view. """

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Assign attributes
        self.parent = parent

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets. """
        ##########
        # Styles #
        ##########
        # Font size
        self.style = ttk.Style(self)
        self.style.configure('Heading.TLabel', font=('TkDefaultFont', 20))
        self.style.configure('Big.TLabel', font=('TkDefaultFont', 15))
        self.style.configure('Medium.TLabel', font=('TkDefaultFont', 12))
        self.style.configure('Big.TButton', font=('TKDefaultFont', 15))
        self.style.configure('TLabel', font=('TkDefaultFont', 10))
        # Color
        custom_color = 'DeepSkyBlue' # 'SystemWindow' 'DeepSkyBlue'

        ##########
        # Header #
        ##########
        # Heading
        # tk.Label(self, text="P.E.A.T.", 
        #          bg=custom_color, font=('TkDefaultFont', 13)).grid(
        #              row=1, column=5, sticky='nsew')

        #################
        # Create frames #
        #################
        options = {'padx':20, 'pady':20}

        # Main container
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, **options)

        frm_heading = ttk.Frame(frm_main)
        frm_heading.grid(column=5, row=5)

        #frm_buttons = ttk.Frame(frm_main)
        #frm_buttons.grid(column=5, row=10, pady=(30,0))

        ttk.Separator(frm_main, orient='horizontal').grid(row=15, column=5, 
            columnspan=50, sticky='we', pady=20)

        frm_submit = ttk.Frame(frm_main)
        frm_submit.grid(row=20, column=5)

        ##################
        # Create Widgets #
        ##################
        # Interval 1 boxes and labels
        tk.Label(frm_heading, text="1", #borderwidth=1, relief='solid',
                 font=([], 15)).grid(row=5, column=5)
        self.box1 = tk.Canvas(frm_heading, width=80, height=80,
                  borderwidth=3, relief='solid')
        self.box1.grid(row=10, column=5, padx=25)

        # Interval 2 boxes and labels
        tk.Label(frm_heading, text="2", font=([], 15)).grid(row=5, column=10)       
        self.box2 = tk.Canvas(frm_heading, width=80, height=80,
                  borderwidth=3, relief='solid')
        self.box2.grid(row=10, column=10, padx=25)

        # Grab default color
        self._default_color = self.box1['bg']

        # ttk.Button(frm_buttons, text="Yes", command=self._on_yes, 
        #     style='Big.TButton', takefocus=0).grid(row=5, column=5, padx=10)
        #self.parent.bind('1', lambda event: self._on_yes())

        # ttk.Button(frm_buttons, text="No", command=self._on_no,
        #     style='Big.TButton', takefocus=0).grid(row=5, column=10, padx=10)
        #self.parent.bind('2', lambda event: self._on_no())

        # SEPARATOR APPEARS HERE #

        # Response label
        self.text_var = tk.StringVar(value="Your Response:")        
        self.label = ttk.Label(frm_submit, textvariable=self.text_var, 
            style="Big.TLabel", width=18)
        self.label.grid(row=5, column=5, pady=(0,20))

        # Submit button
        self.btn_submit = ttk.Button(frm_submit, text="Submit", 
            style="Big.TButton", command=self._on_submit, takefocus=0, 
            state='disabled', 
            #image=self.submit_button_icon, compound=tk.LEFT
            )
        self.btn_submit.grid(row=10, column=5)


    #############
    # Functions #
    #############
    def _on_1(self):
        self.text_var.set("Your Response: 1")
        self.btn_submit.config(state='enabled')
        self.parent.bind('<Return>', lambda event: self._on_submit())
        self.event_generate('<<MainOne>>')


    def _on_2(self):
        self.text_var.set("Your Response: 2")
        self.btn_submit.config(state='enabled')
        self.parent.bind('<Return>', lambda event: self._on_submit())
        self.event_generate('<<MainTwo>>')


    def _on_submit(self):
        self.btn_submit.config(state='disabled')
        self.parent.unbind('<Return>')
        self.text_var.set("Your Response:")
        self.event_generate('<<MainSubmit>>')


    def interval_1_colors(self):
        self.box1.config(bg='blue')
        self.box2.config(bg=self._default_color)
        self.update_idletasks()


    def interval_2_colors(self):
        self.box1.config(bg=self._default_color)
        self.box2.configure(bg='blue')
        self.update_idletasks()


    def clear_interval_colors(self):
        self.box1.config(bg=self._default_color)
        self.box2.config(bg=self._default_color)
        self.update_idletasks()


    def show_response(self, response):
        self.text_var.set(f"Your Response: {response}")


    def clear_response(self):
        self.text_var.set("Your Response:")
