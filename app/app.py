import sys, os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from SamplesheetMaker import *

# Function to determine the correct path
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both development and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

appName = 'Samplesheet Maker'
master = Tk()
master.title(appName)

# Use resource_path to get the icon path
icon_path = resource_path('icon.png')
icon = PhotoImage(file=icon_path)
master.iconphoto(False, icon)

class FilePickerButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_path = None  # Attribute to store the file path
        self.config(command=self.open_file_picker)  # Set the command to the method

    def open_file_picker(self):
        self.file_path = filedialog.askopenfilename()
        #if self.file_path:
        #    print(f'Selected file: {self.file_path}')  # Print the stored file path

def show_platemap_picker():
    if use_platemap.get() == 1:
        plate_picker_button.pack(pady=10,before=radio_frame)
    else:
        plate_picker_button.pack_forget()

def generate():
    input_file = file_picker_button.file_path
    if plate_picker_button.file_path:
        # remove the wells based on the plate map using another script
        print('removing wells based on plate map')
    else:
        print('No plate map!') # remove this eventually
    #print(f'Input file: {input_file}')
    #SamplesheetMaker.create_samplesheet(input_file)
    create_samplesheet(input_file)

banner = Label(master, text='NOTE: CURRENTLY ONLY WORKS FOR SS2')
banner.pack()

use_platemap = IntVar()
Checkbutton(master, text='Use platemap to remove empty wells?', variable=use_platemap, command=show_platemap_picker).pack()

# Create a button for selecting plate map
plate_picker_button = FilePickerButton(master, text='Select Plate Map File')
plate_picker_button.pack_forget()  # Initially hidden

# Create a frame for the radio buttons in the main frame
radio_frame = Frame(master)
radio_frame.pack(pady=5)

tech_picker_label = Label(radio_frame, text='Select Sequencing Technology:')
tech_picker_label.pack(pady=5)

sequencing_technology = IntVar()
Radiobutton(radio_frame, text='SS2', variable=sequencing_technology, value=1).pack(side=LEFT)
Radiobutton(radio_frame, text='HIVES', variable=sequencing_technology, value=2).pack(side=RIGHT)


button_frame = Frame(master)

file_picker_button = FilePickerButton(button_frame, text='Select Input File')
file_picker_button.pack(pady=10)
generate_button = Button(button_frame, text='Generate', command=generate)
generate_button.pack(pady=10)
button_frame.pack()

# file paths are stored in
#plate_picker_button.file_path
#file_picker_button.file_path

master.mainloop()
