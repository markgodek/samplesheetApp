from tkinter import *
from tkinter import filedialog
from tkinter import ttk

appName = 'Samplesheet Maker'
master = Tk()
master.title(appName)

def open_file_picker():
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f'Selected file: {file_path}')

def show_platemap_picker():
    print(use_platemap.get())
    if use_platemap.get() == 1:
        plate_picker_button = Button(plate_picker_frame, text='Select Plate Map File', command=open_file_picker)
        plate_picker_button.pack(pady=10,before=radio_frame)
    else:
        plate_picker_frame.pack_forget()

def show_combobox():
    if sequencing_technology.get() == 1:
        combobox_frame.pack(pady=10,before=button_frame)
        r_index_picker.pack(pady=10)
        c_index_picker.pack(pady=10)
    else:
        combobox_frame.pack_forget()

banner = Label(master,text='Shalek Lab Samplesheet Maker')
banner.pack()

plate_picker_frame = Frame(master)
plate_picker_frame.pack()

use_platemap = IntVar()
Checkbutton(master,text='Use platemap to remove empty wells?',variable=use_platemap,command=show_platemap_picker).pack()

# Create a frame for the radio buttons in the main frame
radio_frame = Frame(master)
radio_frame.pack(pady=5)

tech_picker_label = Label(radio_frame,text='Select Sequencing Technology:')
tech_picker_label.pack(pady=5)

sequencing_technology = IntVar()
Radiobutton(radio_frame, text='SS2', variable=sequencing_technology, value=1,command=show_combobox).pack(side=LEFT)
Radiobutton(radio_frame, text='HIVES', variable=sequencing_technology, value=2,command=show_combobox).pack(side=RIGHT)

combobox_frame = Frame(master)

# Define the Combobox
r_index_picker = ttk.Combobox(combobox_frame)
r_index_picker['values'] = ['R1','R2','R3','R4','R5','R6','R7','R8','R9' ]
r_index_picker.set('Select an R index')  # Set a default prompt

c_index_picker = ttk.Combobox(combobox_frame)
c_index_picker['values'] = ['C1','C2','C3','C4','C5','C6','C7','C8','C9' ]
c_index_picker.set('Select a C index')  # Set a default prompt

button_frame = Frame(master)

filePickerButton = Button(button_frame, text='Select File', command=open_file_picker)
filePickerButton.pack(pady=10)
generate_button = Button(button_frame, text='Generate', command=master.destroy)
generate_button.pack(pady=10)
button_frame.pack()

master.mainloop()
