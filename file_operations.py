from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import Font
from pathlib import Path
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from injury_record import InjuryRecord

# path to service account JSON key file
SERVICE_ACCOUNT_FILE = "drive_creds/sharp-sandbox-455617-e9-ff1eca627cd0.json"

# the Google Drive folder ID
FOLDER_ID = "1EqrtKzLiKc2UpjE_EFJJo5bVGEEhXbMY"


def authenticate_drive():
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
    gauth.credentials = creds
    return GoogleDrive(gauth)

# authenticate + create Google Drive instance
drive = authenticate_drive()

# list files inside the specific folder
query = f"'{FOLDER_ID}' in parents and trashed=false"
file_list = drive.ListFile({'q': query}).GetList()

# debug print file names and IDs
# for file in file_list:
#     print(f"Title: {file['title']}, ID: {file['id']}")


def initialize_master_sheet(filepath):
    pass


def save_record(record: InjuryRecord):
    wb = Workbook()
    ws = wb.active
    ws.title = "Injury Data"

    columns = ["ID", "Type", "Locations", "Area", "Note"]

    ws.append(columns) # adds column names, makes bold
    bold_font = Font(bold=True)
    for cell in ws[1]:  # ws[1] refers to the first row
        cell.font = bold_font

    for injury in record.injury_list:
        ws.append([injury.id, injury.type, injury.get_locations_string(), injury.area, injury.note])

    # TODO: add summary info at bottom, probably with a formula

    # TODO: add graphs?

    # SAVING TO DRIVE
    # get client folder ID from the dictionary
    client_initials_dict = get_client_initials_dict()
    client_folder_id = client_initials_dict[record.client]  # folder is guaranteed to exist

    # save new record to a separate file
    file_name = f"{record.client}_{record.safe_date_format()}_{record.safe_time_format()}.xlsx"
    temp_path = file_name
    wb.save(temp_path)  # save the workbook locally

    # upload the new record file to Google Drive
    file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': client_folder_id}]})
    file_drive.SetContentFile(temp_path)
    file_drive.Upload()

    # remove temp local file
    Path(temp_path).unlink()

    # locate the client-master.xlsx file in Google Drive
    master_file_list = drive.ListFile({
        'q': f"'{client_folder_id}' in parents and title = '{record.client}-master.xlsx' and trashed=false"
    }).GetList()

    if not master_file_list:
        print(f"Error: {record.client}-master.xlsx not found in Google Drive.")
        return

    master_file = master_file_list[0]  # assuming only one master file exists

    # download the master file
    master_temp_path = f"{record.client}-master.xlsx"
    master_file.GetContentFile(master_temp_path)  # download it locally

    # edit master sheet
    master_wb = load_workbook(master_temp_path)
    master_ws = master_wb.active

    # TODO: edit master sheet

    master_wb.save(master_temp_path)  # Save updates

    # re-upload the updated master file
    master_file.SetContentFile(master_temp_path)
    master_file.Upload()

    # remove the temporary master file
    Path(master_temp_path).unlink()


def get_client_data_folder_id():
    # List files at the root level and find the client-data folder
    file_list = drive.ListFile({'q': "title = 'client-data' and trashed = false"}).GetList()

    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            return file['id']
    return None


def get_client_initials_dict():
    # Get the client-data folder ID dynamically
    client_data_folder_id = get_client_data_folder_id()

    if not client_data_folder_id:
        print("Error: 'client-data' folder not found.")
        return {}

    # Initialize the dictionary to hold client initials and their corresponding folder ID
    client_initials_dict = {}

    # List all files and folders inside the client-data folder
    file_list = drive.ListFile({'q': f"'{client_data_folder_id}' in parents and trashed=false"}).GetList()

    # Iterate through the files and add client initials folder to the dictionary
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            client_initials_dict[file['title']] = file['id']

    # Print the dictionary for debugging
    print(client_initials_dict)

    return client_initials_dict


def check_for_client(client_initials):
    # Get the client-data folder ID dynamically
    client_data_folder_id = get_client_data_folder_id()

    if not client_data_folder_id:
        print("Error: 'client-data' folder not found.")
        return

    # Check if the client subfolder (e.g., ABC) exists within the client-data folder
    client_folder = None
    file_list = drive.ListFile({'q': f"'{client_data_folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == client_initials and file['mimeType'] == 'application/vnd.google-apps.folder':
            client_folder = file
            break

    # If the client folder doesn't exist, create it
    if not client_folder:
        client_folder = drive.CreateFile({'title': client_initials, 'mimeType': 'application/vnd.google-apps.folder',
                                          'parents': [{'id': client_data_folder_id}]})
        client_folder.Upload()

    # Create the "client-master.xlsx" file in the client's folder
    master_file_path = f"{client_initials}-master.xlsx"

    # Check if the master file already exists
    master_file = None
    file_list = drive.ListFile({'q': f"'{client_folder['id']}' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == master_file_path:
            master_file = file
            break

    # If the file doesn't exist, create it
    if not master_file:
        new_file = drive.CreateFile({'title': master_file_path, 'parents': [{'id': client_folder['id']}]})
        # Assuming you want to upload a local file to Google Drive
        new_file.Upload()
