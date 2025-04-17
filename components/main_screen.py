from components.body_map_interface import BodyMapInterface
from components.record_initialization_tabview import RecordInitializationTabview
from file_operations import check_for_client
from injury_record import *
from components.body_maps import *


class MainScreen(CTk):
    def __init__(self):
        super().__init__()

        # deactivate_automatic_dpi_awareness()
        set_appearance_mode("dark")
        set_default_color_theme("blue")

        # self.record = injury_record.InjuryRecord("ABC", "5/7/2024", "A.M.", [])
        self.record = None

        self.geometry("1280x720")
        self.minsize(1280, 720)
        self.maxsize(2560, 1440)
        self.title(f"Injury Location Tracker")

        # saved text

        self.description_text_string = ("Welcome to UF CAN's injury tracker! The purpose of this application is to "
                                        "quantitatively record and store the locations of injuries on clients over time"
                                        " in order to better understand behavioral patterns! Scroll down to see a "
                                        "description of the app's functionality, and how to fully utilize it!\n\n"
                                        "To begin, either select a previously recorded session to view, or enter the "
                                        "parameters to create a new session. \n\nWhen creating a new recording, you can"
                                        " enter client initials manually if a session for this client has not been "
                                        "recorded on this device yet, or choose a client from the list of previously "
                                        "recorded sessions. Make sure that the initials remain the same across "
                                        "sessions, as this allows the program to identify the sessions to be displayed"
                                        " together using the graphing features. \n\nThe current date and a guess of "
                                        "whether a new check will be an AM or PM check are generated automatically"
                                        " but can be changed if desired. \n\nOnce a recording has been selected or "
                                        "created, you may begin viewing/recording data. Use the buttons to select "
                                        "different regions of the body. Some areas are displayed with a darker color "
                                        "to differentiate areas like the neck and ears from the rest of the head. \n\n"
                                        "To record an injury, click on the desired squares to note the injury's "
                                        "location. Selected squares will then appear green. Multiple separate "
                                        "regions of the body may be used to record a single injury. \n\nOnce all "
                                        "desired squares have been selected, choose an injury type from the dropdown"
                                        " menu, and click the \"Save Injury\" button. This will add a recorded injury "
                                        "using the selected squares and injury type, and display it on the overview "
                                        "menu on the right side of the screen. \n\nIf you'd like to edit or remove a "
                                        "previously recorded injury, find it in the menu on the right. Injuries"
                                        " will be displayed in the reverse order from which they were added, but can "
                                        "be edited/removed in any order. Click the delete button and the following "
                                        "prompt to remove it outright, or click the edit button to edit it. Doing this"
                                        " will return all associated squares to the selected state, from which squares"
                                        " can be added or removed, or the injury type can be changed. \n\nWhen "
                                        "recording of data is complete, do not "
                                        "forget to click the save button, or else the recording will be lost if the "
                                        "program stops running.")

        # tkinter variables

        # left frame

        self.left_frame = CTkFrame(master=self, fg_color="transparent", bg_color="transparent")

        self.title_text = CTkTextbox(master=self.left_frame, fg_color="transparent", wrap=WORD, font=(None, 32),
                                     activate_scrollbars=False)
        self.title_text.insert("0.0", "UF CAN Injury Location Tracker")
        self.title_text.configure(state="disabled")

        self.description_text = CTkTextbox(master=self.left_frame, wrap=WORD)
        self.description_text.insert("0.0",
                                     self.description_text_string)
        self.description_text.configure(state="disabled")

        self.record_initialization_tabs = RecordInitializationTabview(master=self.left_frame, record=self.record,
                                                                      record_activation_func=self.create_record)

        # placing left frame

        self.left_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1.00)
        self.title_text.place(relx=0.1, rely=0.035, relwidth=0.8, relheight=0.23)
        self.description_text.place(relx=0.05, rely=0.18, relwidth=0.9, relheight=0.22)
        self.record_initialization_tabs.place(relx=0.05, rely=0.42, relwidth=0.9, relheight=0.56)

        # middle frame

        self.body_map_interface_frame = BodyMapInterface(master=self)

        # placing middle frame

        self.body_map_interface_frame.place(relx=0.25, rely=0, relwidth=0.75, relheight=1.00)

    def create_record(self, client, date, time):
        check_for_client(client)
        self.record = InjuryRecord(client=client, date=date, time=time, injury_list=[])
        self.body_map_interface_frame.set_record(self.record)

    # once parameters have been set/a past session has been chosen, use this to create the body frames


