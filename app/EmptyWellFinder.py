import openpyxl
import pandas as pd

def get_empty_wells(path):
    plate = {}
    rowNames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    # Load the workbook
    workbook = openpyxl.load_workbook(path)

    # Select the active worksheet (or specify a worksheet by name)
    sheet = workbook.active
    max_row = sheet.max_row
    max_col = sheet.max_column

    print(max_row)

    # Iterate through each row in the worksheet, putting the plate into a pandas dataframe
    for row in sheet.iter_rows(values_only=True):
        if row[0] == 'Plate ID:':
            plate['name'] = row[1]
        print(row)
        # if row starts with row index A,B,C, etc., begin searching for a empty wells
        #if row[0] in rowNames:


    #print(plate)

path = r"C:\Users\markg\samplesheetApp\app\demo_platemap.xlsx"

get_empty_wells(path)
