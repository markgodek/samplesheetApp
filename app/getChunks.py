def get_chunks(sheet):
    max_row = sheet.max_row
    max_col = sheet.max_column
    chunks = []
    empty_row_counter = 0
    new_chunk = openpyxl.Workbook().create_sheet()

    #read 14 rows, discard 2 rows
    for row in sheet.iter_rows(values_only=True):
        #print(row)
        #print('empty row counter: ',empty_row_counter)
        if empty_row_counter >= 2 and row[0] is not None:
            new_chunk.append(row)
        if empty_row_counter == 4:
            print(*[row for row in new_chunk.iter_rows(values_only=True)], sep='\n')
            chunks.append(new_chunk)  # append the constructed chunk to chunks to return
            new_chunk = openpyxl.Workbook().create_sheet()  # reset chunk to return
            empty_row_counter = 0
        if row[0] is None:
            empty_row_counter += 1

    return chunks


def get_empty_wells(path):
    plate = {}
    rowNames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    # Load the workbook
    workbook = openpyxl.load_workbook(path)

    # Select the active worksheet (or specify a worksheet by name)
    sheet = workbook.active

    chunks = get_chunks(sheet)


path = r"C:\Users\markg\samplesheetApp\app\full_platemap.xlsx"
get_empty_wells(path)