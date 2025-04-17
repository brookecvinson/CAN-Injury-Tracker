from customtkinter import *

from file_operations import get_client_initials_dict
from injury_record import *
from time import *


def is_valid_date(date_str):
    try:
        # Attempt to parse the string as a date with the specified format
        strptime(date_str, '%m/%d/%Y')
        return True
    except ValueError:
        # If parsing fails, it's not a valid date
        return False


class RecordInitializationTabview(CTkTabview):
    def __init__(self, master, record, record_activation_func):
        super().__init__(master=master)

        self.record = record
        self.record_activation_func = record_activation_func

        self.tab1 = self.add("Create New Record")

        self.date_string = f"Current Date: {strftime('%m/%d/%Y')}, "
        self.error_text = StringVar(value="")

        self.time_label = CTkLabel(master=self.tab1)
        self.frame1 = CTkFrame(master=self.tab1, fg_color="transparent")
        self.instructions_label = CTkLabel(master=self.frame1, text="Enter Date/Time of Recording")
        self.entry_frame = CTkFrame(master=self.frame1, fg_color="transparent")
        self.date_entry = CTkEntry(master=self.entry_frame, placeholder_text="mm/dd/yyyy")
        self.date_button = CTkButton(master=self.entry_frame, text="Use Current Date", command=self.set_date_button)
        self.time_segmented_button = CTkSegmentedButton(master=self.entry_frame, values=["AM", "PM"])
        self.time_button = CTkButton(master=self.entry_frame, text="Use Current Time", command=self.set_time_button)
        self.client_combobox = CTkComboBox(master=self.entry_frame, values=list(get_client_initials_dict().keys()))
        self.client_combobox.set("Client Initials")
        self.client_clear_button = CTkButton(master=self.entry_frame, text="Clear Text",
                                             command=self.clear_client_combobox)
        self.create_record_button = CTkButton(master=self.frame1, text="Create Record", command=self.create_record)
        self.error_label = CTkLabel(master=self.tab1, textvariable=self.error_text)

        self.entry_frame.columnconfigure(0, weight=1)
        self.entry_frame.columnconfigure(1, weight=1)
        self.entry_frame.rowconfigure(0, weight=1)
        self.entry_frame.rowconfigure(1, weight=1)
        self.entry_frame.rowconfigure(2, weight=1)

        self.time_label.pack(pady=12)
        self.frame1.place(relx=0, rely=0.15, relwidth=1, relheight=0.7)
        self.instructions_label.pack()
        self.entry_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.6)
        self.date_entry.grid(row=0, column=0, padx=10, pady=12)
        self.date_button.grid(row=0, column=1, padx=10, pady=12)
        self.time_segmented_button.grid(row=1, column=0, padx=10, pady=12)
        self.time_button.grid(row=1, column=1, padx=10, pady=12)
        self.client_clear_button.grid(row=2, column=1, padx=10, pady=12)
        self.client_combobox.grid(row=2, column=0, padx=10, pady=12)
        self.error_label.pack(side="bottom", pady=10)
        self.create_record_button.pack(side="bottom", pady=12)

        self.tab2 = self.add("View Past Record")

        self.update_time()

    def update_time(self):
        self.time_label.configure(text=self.date_string + strftime("%I:%M:%S %p"))
        self.after(1000, self.update_time)

    def set_time_button(self):
        self.time_segmented_button.set(strftime("%p"))

    def set_date_button(self):
        self.date_entry.delete(0, len(self.date_entry.get()))
        self.date_entry.insert(0, strftime('%m/%d/%Y'))

    def clear_client_combobox(self):
        self.client_combobox.set("")

    # creates a new record based on input information
    def create_record(self):
        # check to make sure user input for creating a record is valid
        if not is_valid_date(self.date_entry.get()):
            self.error_text.set("Please enter a date in mm/dd/yyyy format")
        # check that something is selected for the time
        elif self.time_segmented_button.get() == "":
            self.error_text.set("Please select a time")
        elif self.client_combobox.get() == "" or self.client_combobox.get() == "Client Initials":
            self.error_text.set("Please enter/select a client")
        else:
            self.error_text.set("")
            self.record_activation_func(self.client_combobox.get().upper(),
                                        self.date_entry.get(),
                                        self.time_segmented_button.get())
