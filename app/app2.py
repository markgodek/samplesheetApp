import sys, os
from tkinter import *
from tkinter import filedialog

appName = 'Samplesheet Maker'

class FilePickerButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_path = None
        self.config(command=self.open_file_picker)

    def open_file_picker(self):
        self.file_path = filedialog.askopenfilename()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def update_ui():
    # Show or hide check_frame based on sequencing technology
    if sequencing_technology.get() == 'SS2':
        check_frame.pack(pady=5,before=button_frame)
    else:
        check_frame.pack_forget()

    # Show or hide plate_map_frame based on use_platemap
    if use_platemap.get():
        plate_map_frame.pack(pady=5)
    else:
        plate_map_frame.pack_forget()

def generate():
    pass

# Create all the frame we will use
master = Tk()
radio_frame = Frame(master)
check_frame = Frame(master)
plate_map_frame = Frame(check_frame)
button_frame = Frame(master)

# Configure the app
master.title(appName)
icon_path = resource_path('icon.png')
icon = PhotoImage(file=icon_path)
master.iconphoto(False, icon)

sequencing_technology = StringVar(value='SS2')
use_platemap = BooleanVar(value=True)

# Put elements in the frames
banner = Label(master, text='NOTE: CURRENTLY ONLY WORKS FOR SS2')

tech_picker_label = Label(radio_frame, text='Select Sequencing Technology:')
tech_picker_label.grid(row=0, column=0, columnspan=3, pady=5)

# Updated command to call update_ui
Radiobutton(radio_frame, text='SS2', variable=sequencing_technology, value='SS2', command=update_ui).grid(row=1, column=0, padx=5)
Radiobutton(radio_frame, text='SeqWell', variable=sequencing_technology, value='SeqWell', command=update_ui).grid(row=1, column=1, padx=5)
Radiobutton(radio_frame, text='HIVES', variable=sequencing_technology, value='HIVES', command=update_ui).grid(row=1, column=2, padx=5)

Checkbutton(check_frame, text='Use platemap to remove empty wells?', variable=use_platemap, command=update_ui).pack()

plate_picker_button = FilePickerButton(plate_map_frame, text='Select Plate Map File')
plate_picker_button.pack(pady=5)

file_picker_button = FilePickerButton(button_frame, text='Select Input File')
file_picker_button.pack(pady=10)

generate_button = Button(button_frame, text='Generate', command=generate)
generate_button.pack(pady=10)

# Pack the frames
banner.pack()
radio_frame.pack()
plate_map_frame.pack()
button_frame.pack()

# Call update_ui once at the beginning to set the initial state
update_ui()

# Keep the app open
master.mainloop()
