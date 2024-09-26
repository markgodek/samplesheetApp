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
            index_IDs = {}
            info = {}

            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i < 12:
                    info[row[0]] = row[1]
                else:
                    info[row[0]] = row[1:]

            plate_ids = info['Plate ID(s)']
            i5_index_IDs = info['I5 Index ID']
            i7_index_IDs = info['I7 Index ID']

            # Populate the indices dictionary
            for i, plate_id in enumerate(plate_ids):
                index_IDs[plate_id] = {
                    'i5': i5_index_IDs[i],
                    'i7': i7_index_IDs[i]
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

        return header, info, index_IDs
    except FileNotFoundError:
        print('\nERROR: ', input_file_path, ' not found. Please correct the information sheet you input.')
        exit()


def seqWellInputFileParser(input_file_path):
    try:
        with open(input_file_path) as file:
            info = {}

            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i < 12:
                    info[row[0]] = row[1]
                else:
                    info[row[0]] = row[1:]

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

        return header, info
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
                if empty_wells: # if there are empty wells, look at them
                    if well not in empty_wells:
                        outList.append([well, row[1]])
                else: # if there are no empty wells, add everything
                    outList.append([well, row[1]])
        return outList

    except FileNotFoundError:
        print('\nERROR: ', indexFile, ' not found. Please correct the information sheet you input.')
        exit()


def seqWellIndexGetter(info):
    indexFile = resource_path('indices') + '\\Dual_Indexing_SeqWell_Barcodes.csv'
    samples = list(info.keys())[14:]
    indices = []
    return_indices = []
    try:
        for sample in samples:
            indices.append(info[sample][0])

        with open(indexFile) as file:
            indexIterator = csv.reader(file)
            next(indexIterator) # discard header
            for i, row in enumerate(indexIterator):
                if row[0] in indices: # if the index is one we want, store it
                    return_indices.append([row[0],row[2],row[4]])
        return return_indices

    except FileNotFoundError:
        print('\nERROR: ', indexFile, ' not found. Please correct the information sheet you input.')
        exit()

# function which write the samplesheet to file
def create_samplesheet(input_file_path, header, info, indices=None,plate_file_path=None):
    inputDir = Path(input_file_path).parent
    outFileName = str(inputDir) + '\\' + info['Run_ID'] + '_samplesheet.csv'

    empty_wells = EmptyWellFinder.get_empty_wells(plate_file_path)
    well_counter = 1    # samples are named based relative to run, not plate

    with open(outFileName, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the header
        for row in header:
            writer.writerow(row)

        if indices: # SS2 gets indices in a 2-step manner
            # Write the data
            for plate, values in indices.items():
                if empty_wells and plate in empty_wells.keys():  # pass the empty wells if a plate has them
                    plate_empty_wells = empty_wells[plate]
                else:
                    plate_empty_wells = None  # Initialize to None if no empty wells

                i7_index_ID = values['i7']
                i5_index_ID = values['i5']

                plate_i7_indices = ss2WellIndexGetter(i7_index_ID, plate_empty_wells)
                plate_i5_indices = ss2WellIndexGetter(i5_index_ID, plate_empty_wells)
                for i in range(0, len(plate_i7_indices)):
                    well = plate_i7_indices[i][0]
                    i7_index = plate_i7_indices[i][1]
                    i5_index = plate_i5_indices[i][1]
                    outstring = 'sample' + str(well_counter), str(plate + '_' + str(well)), \
                    plate, well, i7_index_ID, i7_index, i5_index_ID, i5_index, info['Run_ID']
                    writer.writerow(outstring)
                    well_counter += 1
        else:   # get indices in a 1-step manner
            indices = seqWellIndexGetter(info)
            samples = list(info.keys())[14:]
            for i in range(0,len(indices)):
                outstring = 'sample' + str(i+1), samples[i], info['Plate ID(s)'][0], indices[i][0], \
                'N700_' + str(indices[i][0]), indices[i][1], 'N700_' + str(indices[i][0]), indices[i][2], info['Run_ID']
                writer.writerow(outstring)


# receives outputs from generate button in main app and processes them based on
# which sequencing technology was selected
def tech_parser(input_file_path, tech, plate_file_path=None):
    if tech == 'SS2':
        if tech == 'SS2':
            header, info, indices = ss2InputFileParser(input_file_path)
            create_samplesheet(input_file_path, header, info, indices, plate_file_path)

    if tech == 'SeqWell':
        header, info = seqWellInputFileParser(input_file_path)
        create_samplesheet(input_file_path, header, info)

    if tech == 'HIVES':
        # HIVES stuff
        pass
