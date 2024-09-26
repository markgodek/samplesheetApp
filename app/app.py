import sys
import os
from tkinter import *
from tkinter import filedialog
import SamplesheetMaker
from ResourcePath import resource_path

appName = 'Samplesheet Maker'

class FilePickerButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_path = None
        self.config(command=self.open_file_picker)

    def open_file_picker(self):
        self.file_path = filedialog.askopenfilename()
        set_button_labels()  # Update UI when file is selected

def load_icon():
    icon_path = resource_path('icon.png')
    try:
        icon = PhotoImage(file=icon_path)
        master.iconphoto(False, icon)
    except Exception as e:
        print(f"Error loading icon: {e}")

def update_ui():
    file_picker_button.file_path = None
    plate_picker_button.file_path = None
    input_file_banner.pack_forget()  # Hide the label initially
    plate_map_banner.pack_forget()

    # Show or hide check_frame based on sequencing technology
    if sequencing_technology.get() == 'SS2':
        check_frame.pack(pady=5, before=button_frame)
    else:
        check_frame.pack_forget()

    # Show or hide plate_map_frame based on use_platemap
    if use_platemap.get():
        plate_map_frame.pack(pady=5)
    else:
        plate_map_frame.pack_forget()

def set_button_labels():
    # Update the input file label based on file path
    if file_picker_button.file_path:
        input_file_banner.config(text=file_picker_button.file_path)
        input_file_banner.pack(after=file_picker_button)  # Show the label
    else:
        input_file_banner.pack_forget()  # Hide the label if no file selected

    if plate_picker_button.file_path:
        plate_map_banner.config(text=plate_picker_button.file_path)
        plate_map_banner.pack()  # Show plate map label
    else:
        plate_map_banner.pack_forget()  # Hide plate map label if no file selected

def generate():
    input_file_path = file_picker_button.file_path
    plate_file_path = plate_picker_button.file_path
    tech = sequencing_technology.get()

    SamplesheetMaker.tech_parser(input_file_path, tech, plate_file_path)

# Create the main window
master = Tk()
master.title(appName)

# Load the icon before any UI setup
load_icon()

# Create all the frames we will use
radio_frame = Frame(master)
check_frame = Frame(master)
plate_map_frame = Frame(check_frame)
button_frame = Frame(master)

sequencing_technology = StringVar(value='SS2')
use_platemap = BooleanVar(value=True)

# Put elements in the frames
banner = Label(master, text='NOTE: CURRENTLY ONLY WORKS FOR SS2')
input_file_banner = Label(button_frame, text='', wraplength=400)  # Add wrap length for long paths
plate_map_banner = Label(plate_map_frame, text='', wraplength=400)

tech_picker_label = Label(radio_frame, text='Select Sequencing Technology:')
tech_picker_label.grid(row=0, column=0, columnspan=3, pady=5)

Radiobutton(radio_frame, text='SS2', variable=sequencing_technology, value='SS2', command=update_ui).grid(row=1, column=0, padx=5)
Radiobutton(radio_frame, text='SeqWell', variable=sequencing_technology, value='SeqWell', command=update_ui).grid(row=1, column=1, padx=5)
#Radiobutton(radio_frame, text='HIVES', variable=sequencing_technology, value='HIVES', command=update_ui).grid(row=1, column=2, padx=5)

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

# Prevent importing functions to other scripts from running app.py
if __name__ == "__main__":
    # Keep the app open
    master.mainloop()
