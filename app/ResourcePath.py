import os,sys

# both app and SamplesheetMaker use this function
# importing it via a third script prevents circular imports
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)