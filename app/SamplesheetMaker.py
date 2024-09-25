import os, sys, csv
from pathlib import Path
import EmptyWellFinder
from ResourcePath import resource_path

def generateWells():
    wells = []

    # Loop over letters A to H
    for letter in range(ord('A'), ord('H') + 1):
        # Loop over numbers 1 to 12
        for number in range(1, 13):
            # Create coordinate string and append to list
            wells.append(f"{chr(letter)}{number}")
    # return the generated list
    return wells

# function which takes an SS2 input file and returns a dictionary with plate names, i7, and i5 indices
def ss2PlateIndexGetter(input_file_path):
    try:
        with open(input_file_path) as file:
            indices = {}

            reader = csv.reader(file)
            # Skip the first 12 rows
            for row in range(12):
                next(reader)
            # Get the 13th row
            IDs = next(reader)
            i7indices = next(reader)
            i5indices = next(reader)

            for i in range(1, len(IDs)):
                ID = IDs[i]
                # Initialize the dictionary for each sample ID
                indices[ID] = {}
                indices[ID]['i7'] = i7indices[i]
                indices[ID]['i5'] = i5indices[i]
        return indices

    except FileNotFoundError:
        print('\nERROR: ', input_file_path, ' not found. Please correct the information sheet you input.')
        exit()

# function which takes a dictionary with SS2 plates, i7, and i5 indices and
# returns an array which contains the well indices
def ss2WellIndexGetter(indexID,empty_wells=None):
    indexFile = resource_path('indices') + '\\' + indexID + '.csv'
    print(indexFile)


def create_samplesheet(input_file_path, tech, plate_file_path=None):

    if tech == 'SS2':
        empty_wells = EmptyWellFinder.get_empty_wells(plate_file_path)
        indices = ss2PlateIndexGetter(input_file_path)

        for plate, values in indices.items():
            i7_value = values['i7']
            i5_value = values['i5']
            # these will need to be stored in a list or something
            ss2WellIndexGetter(i7_value)
            ss2WellIndexGetter(i5_value)

    if tech == 'SeqWell':
        pass
        #do SeqWell stuff:
    if tech == 'HIVES':
        pass
        #HIVES stuff

    pass
