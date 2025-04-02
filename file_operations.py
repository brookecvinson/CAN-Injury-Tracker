from openpyxl import *
from openpyxl.styles import Font
from pathlib import Path

from injury_record import InjuryRecord

def initialize_master_sheet(filepath):
    pass

def save_record(record: InjuryRecord):

    wb = Workbook()
    ws = wb.active
    ws.title = "Injury Data"

    columns = ["ID", "Type", "Locations", "Area", "Note"]

    # add column names
    ws.append(columns)

    bold_font = Font(bold=True)
    for cell in ws[1]:  # ws[1] refers to the first row
        cell.font = bold_font

    for injury in record.injury_list:
        ws.append([injury.id, injury.type, injury.get_locations_string(), injury.area, injury.note])

    wb.save(f"client-data/{record.client}/{record.client}_{record.safe_date_format()}.xlsx")

def get_client_initials_dict():
    root = Path("client-data")
    client_initials_dict = {}

    for subdir in root.rglob('*'):
        if subdir.is_dir():
            client_initials_dict[subdir.name] = subdir  # Store the name as key, path as value
    print(client_initials_dict)
    return client_initials_dict

def check_for_client(client_initials):
    client_initials_dict = get_client_initials_dict()
    if client_initials not in client_initials_dict:
        directory_path = Path(f"client-data/{client_initials}")
        file_path = directory_path / f"{client_initials}-master.xlsx"
        # Create the directory if it doesn't exist
        directory_path.mkdir(parents=True, exist_ok=True)
        # create excel master graph
        file_path.touch()

