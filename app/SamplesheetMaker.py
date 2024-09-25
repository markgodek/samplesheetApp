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


# function which takes an SS2 input file
# returns a tuple which contains the header for the final samplesheet and
# a dictionary of plate names and indices for further processing
def ss2InputFileParser(input_file_path):
    try:
        with open(input_file_path) as file:
            indices = {}
            info = {}

            reader = csv.reader(file)
            for row in reader:
                if row and row[0]:  # Ensure the row is not empty and has a valid key
                    non_empty_values = [value for value in row[1:] if value]  # Filter out empty strings

                    # Store directly if there's only one non-empty value
                    if len(non_empty_values) == 1:
                        info[row[0]] = non_empty_values[0]
                    else:
                        info[row[0]] = non_empty_values  # Store as list if multiple values

            plate_ids = info['Plate ID(s)']
            i5_indices = info['I5 Index ID']
            i7_indices = info['I7 Index ID']

            # Populate the indices dictionary
            for i, plate_id in enumerate(plate_ids):
                indices[plate_id] = {
                    'i5': i5_indices[i],
                    'i7': i7_indices[i]
                }

            # "Sample_ID", "index", and "index2" are mandatory column names otherwise BCL2FASTQ will not run
            header = [['[Header]', '', '', '', '', '', '', '', '', ''],
                      ['IEMFileVersion', info['IEMFileVersion'], '', '', '', '', '', '', '', ''],
                      ['Investigator Name', info['Investigator Name'], '', '', '', '', '', '', '', ''],
                      ['Run_ID', info['Run_ID'], '', '', '', '', '', '', '', ''],
                      ['Date', info['Date'], '', '', '', '', '', '', '', ''],
                      ['Workflow', info['Workflow'], '', '', '', '', '', '', '', ''],
                      ['Application', info['Application'], '', '', '', '', '', '', '', ''],
                      ['Assay', info['Assay'], '', '', '', '', '', '', '', ''],
                      ['Description', info['Description'], '', '', '', '', '', '', '', ''],
                      ['Chemistry', info['Chemistry'], '', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', '', '', ''], ['[Reads]', '', '', '', '', '', '', '', '', ''],
                      [info['Read 1 length'], '', '', '', '', '', '', '', '', ''],
                      [info['Read 2 length'], '', '', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', '', '', ''], ['[Settings]', '', '', '', '', '', '', '', '', ''],
                      ['Adapter', info['Adapter'], '', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', '', '', ''], ['[Data]', '', '', '', '', '', '', '', '', ''],
                      ['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well', 'I7_Index_ID', 'index',
                       'I5_Index_ID', 'index2', 'Sample_Project']]

        return header, info, indices
    except FileNotFoundError:
        print('\nERROR: ', input_file_path, ' not found. Please correct the information sheet you input.')
        exit()


# function which takes a dictionary with SS2 plates, i7, and i5 indices and
# returns an array which contains the well indices
def ss2WellIndexGetter(indexID, empty_wells=None):
    indexFile = resource_path('indices') + '\\' + indexID + '.csv'
    wells = generateWells()
    outList = []

    try:
        with open(indexFile) as file:
            indexIterator = csv.reader(file)
            next(indexIterator)  # first row is the header, skip it
            for i, row in enumerate(indexIterator):
                well = wells[i]
                if well not in empty_wells:
                    outList.append([well, row[1]])
        return outList

    except FileNotFoundError:
        print('\nERROR: ', indexFile, ' not found. Please correct the information sheet you input.')
        exit()


# function which write the samplesheet to file
def create_samplesheet(input_file_path, header, info, final_indices):
    inputDir = Path(input_file_path).parent
    outFileName = str(inputDir) + '\\' + info['Run_ID'] + '_samplesheet.csv'
    print(outFileName)
    #print(info)
    pass


# receives outputs from generate button in main app and processes them based on
# which sequencing technology was selected
def tech_parser(input_file_path, tech, plate_file_path=None):
    if tech == 'SS2':
        if tech == 'SS2':
            plate_empty_wells = None
            final_indices = {}
            empty_wells = EmptyWellFinder.get_empty_wells(plate_file_path)
            header, info, indices = ss2InputFileParser(input_file_path)

            for plate, values in indices.items():
                if plate in empty_wells.keys():  # pass the empty wells if a plate has them
                    plate_empty_wells = empty_wells[plate]
                else:
                    plate_empty_wells = None  # Initialize to None if no empty wells

                i7_value = values['i7']
                i5_value = values['i5']

                # Initialize the plate in final_indices if it doesn't exist
                if plate not in final_indices:
                    final_indices[plate] = {}

                final_indices[plate]['i7'] = ss2WellIndexGetter(i7_value, plate_empty_wells)
                final_indices[plate]['i5'] = ss2WellIndexGetter(i5_value, plate_empty_wells)
            create_samplesheet(input_file_path, header, info, final_indices)

    if tech == 'SeqWell':
        pass
        #do SeqWell stuff:
    if tech == 'HIVES':
        pass
        #HIVES stuff

    pass


#tech_parser('C:/Users/markg/SheetApp/app/demo_input.csv', 'SS2', 'C:/Users/markg/SheetApp/app/demo_platemap.xlsx')
tech_parser('C:/Users/markg/SheetApp/app/demo_files/full_input.csv', 'SS2',
            'C:/Users/markg/SheetApp/app/demo_files/full_platemap.xlsx')
