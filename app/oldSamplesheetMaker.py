import os, sys, csv
from pathlib import Path

# a function that generates a list of strings from A1 to H12 for a 96 well plate
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

# a function that takes a Row or Column index file name and a list of indices, constructs the path to the file, reads it, and appends the indices to list
def ss2IndexReader(indexID, indices):
    indexFile = resource_path('indices') + '\\' + indexID + '.csv'

    try:
        with open(indexFile) as file:
            indexIterator = csv.reader(file)
            next(indexIterator) # first row is the header, skip it
            for row in indexIterator:
                indices.append(row[1]) # store the NextSeq index in a list
        return indices
    except FileNotFoundError:
        print('\nERROR: ', indexFile, ' not found. Please correct the information sheet you input.')
        exit()

def create_samplesheet(inputFile,sequencing_technology):
        with open(inputFile, 'r') as runInfo:
                infoReader = csv.reader(runInfo, delimiter=',', quoting=csv.QUOTE_NONE)

                wells = generateWells()
                info = {}
                description = ''
                i7ID = []
                i5ID = []
                i7IDForRow = []
                i5IDForRow = []
                i7Indices = []
                i5Indices = []
                plateIDs = []
                plateIDForRows = []
                wellsForRows = []

                for row in infoReader:
                        if row[0] == 'I7 Index ID':
                                i7ID = row[1:]
                        if row[0] == 'I5 Index ID':
                                i5ID = row[1:]
                        if row[0] == 'Plate ID(s)':
                                plateIDs = row[1:]
                        if row[0] == 'Description':
                                description = ','.join(row[1:])
                        else:
                                info[row[0]] = row[1]
                for idFile in i7ID:
                        i7Indices = ss2IndexReader(idFile, i7Indices)
                for idFile in i5ID:
                        i5Indices = ss2IndexReader(idFile, i5Indices)

                # get how many columns the csv file is, there could be several plates, indice files, etc. and use that to remove commas from description so it prints nice
                csvColumnCount = max(len(i7ID), len(i5ID), len(plateIDs))
                if description[0] == '\"':
                        description = description[1:-csvColumnCount]
                else:
                        description = description[:len(description) - 1]

                # generate sample names for each plate
                sampleNames = []
                for i in range(len(plateIDs)):
                        for well in wells:
                                sampleNames.append(str(plateIDs[i]) + '_' + str(well))
                                i7IDForRow.append(i7ID[i])
                                i5IDForRow.append(i5ID[i])
                                plateIDForRows.append(plateIDs[i])
                                wellsForRows.append(well)

                # "Sample_ID", "index", and "index2" are mandatory column names otherwise BCL2FASTQ will not run
                header = [['[Header]', '', '', '', '', '', '', '', '', ''],
                          ['Investigator Name', info['Investigator Name'], '', '', '', '', '', '', '', ''],
                          ['Run_ID', info['Run_ID'], '', '', '', '', '', '', '', ''],
                          ['Date', info['Date'], '', '', '', '', '', '', '', ''],
                          ['Workflow', info['Workflow'], '', '', '', '', '', '', '', ''],
                          ['Application', info['Application'], '', '', '', '', '', '', '', ''],
                          ['Assay', info['Assay'], '', '', '', '', '', '', '', ''],
                          ['Description', description, '', '', '', '', '', '', '', ''],
                          ['Chemistry', info['Chemistry'], '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', '', ''], ['[Reads]', '', '', '', '', '', '', '', '', ''],
                          [info['Read 1 length'], '', '', '', '', '', '', '', '', ''],
                          [info['Read 2 length'], '', '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', '', ''], ['[Settings]', '', '', '', '', '', '', '', '', ''],
                          ['Adapter', info['Adapter'], '', '', '', '', '', '', '', ''],
                          ['', '', '', '', '', '', '', '', '', ''], ['[Data]', '', '', '', '', '', '', '', '', ''],
                          ['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well', 'I7_Index_ID', 'index',
                           'I5_Index_ID', 'index2', 'Sample_Project']]

                # create sample sheet from manifest
                inputDir = Path(inputFile).parent
                outFileName = str(inputDir) + '\\' + info['Run_ID'] + '_samplesheet.csv'
                with open(outFileName, 'w', newline='') as sampleSheet:
                        out = csv.writer(sampleSheet)
                        out.writerows(header)
                        # for every index, construct a row of the sample sheet and write it
                        for i in range(len(i7Indices)):
                                sampleID = 'sample' + str(i + 1)
                                outstring = sampleID, sampleNames[i], plateIDForRows[i], wellsForRows[i], i7IDForRow[i], \
                                i7Indices[i], \
                                        i5IDForRow[i], i5Indices[i], info['Run_ID']
                                out.writerow(outstring)


