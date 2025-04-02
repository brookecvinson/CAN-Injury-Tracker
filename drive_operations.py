from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

# path to service account JSON key file
SERVICE_ACCOUNT_FILE = "sharp-sandbox-455617-e9-ff1eca627cd0.json"

# the Google Drive folder ID
FOLDER_ID = "1EqrtKzLiKc2UpjE_EFJJo5bVGEEhXbMY"

def authenticate_drive():
    gauth = GoogleAuth()

    # define the required scopes
    scope = ["https://www.googleapis.com/auth/drive"]

    # Authenticate using the service account JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)

    gauth.credentials = creds  # Assign credentials to gauth

    return GoogleDrive(gauth)


# Authenticate and create a Google Drive instance
drive = authenticate_drive()

# List files inside the specific folder
query = f"'{FOLDER_ID}' in parents and trashed=false"
file_list = drive.ListFile({'q': query}).GetList()

# Print file names and IDs
for file in file_list:
    print(f"Title: {file['title']}, ID: {file['id']}")

