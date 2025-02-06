from customtkinter import *

import colors
from injury_record import *
from body_maps import *
from injury_display import InjuryDisplayCard


# holds everything for the middle frame: body maps, info for adding injuries, current client info, etc
# needs to have at least two states: one for before a record has been set when the application starts, and one with
# an active record; maybe a third mode that's read only?

class BodyMapInterface(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")

        # values for segmented buttons used to select body parts
        self.front_segmented_values = ["Front Head", "Front Torso", "Front Arms", "Front Hands", "Front Legs"]
        self.back_segmented_values = ["Back Head", "Back Torso", "Back Arms", "Back Hands", "Back Legs"]

        # types of injuries users can select
        self.injury_types = ["Bruise", "Open Wound", "Closed Wound", "Redness", "Other"]

        # record to add injuries to, body maps, and current viewed body map
        self.record = None
        self.body_maps_dict = {}
        self.current_body_map = None

        # stores staged injury indices and locations
        self.staged_injury_indices = set()
        self.staged_locations = set()
        self.staged_locations_string = "None"
        self.staged_area_string = ""

        self.client_name_string = "Client: "
        self.date_string = "Date: "
        self.time_string = "Time: "

        # holds the left part
        self.interface_frame = CTkFrame(master=self)

        # displays information about the record being viewed/edited
        self.record_info_frame = CTkFrame(master=self.interface_frame, fg_color="transparent")
        self.client_name_label = CTkLabel(master=self.record_info_frame, text=self.client_name_string)
        self.date_label = CTkLabel(master=self.record_info_frame, text=self.date_string)
        self.time_label = CTkLabel(master=self.record_info_frame, text=self.time_string)

        # holds the body frame and buttons for switching between them
        self.body_map_frame = CTkFrame(master=self.interface_frame)
        self.segmented_button_frame = CTkFrame(master=self.body_map_frame, fg_color="transparent",
                                               bg_color="transparent", height=50)

        self.front_body_segmented_button = CTkSegmentedButton(master=self.segmented_button_frame,
                                                              values=self.front_segmented_values,
                                                              command=self.front_body_button)
        self.front_body_segmented_button.configure(state="disabled")
        self.back_body_segmented_button = CTkSegmentedButton(master=self.segmented_button_frame,
                                                             values=self.back_segmented_values,
                                                             command=self.back_body_button)
        self.back_body_segmented_button.configure(state="disabled")

        self.body_map_holder = CTkFrame(master=self.body_map_frame)

        # holds information about injury data
        self.injury_edit_frame = CTkFrame(master=self.interface_frame, border_width=3)
        self.add_injuries_label = CTkLabel(master=self.injury_edit_frame, text="Add Injury")
        self.injury_locations_label = CTkLabel(master=self.injury_edit_frame, text="Injury Locations: ")
        self.injury_area_label = CTkLabel(master=self.injury_edit_frame, text="Area Covered: 0 cm²")
        self.injury_type_combobox = CTkComboBox(master=self.injury_edit_frame, values=self.injury_types,
                                                state="readonly")
        self.injury_type_combobox.set("Injury Type")
        self.injury_note_entry = CTkEntry(master=self.injury_edit_frame, placeholder_text="Injury Note (Optional)")
        self.unselect_all_button = CTkButton(master=self.injury_edit_frame, text="Deselect All", state="disabled",
                                             command=self.deselect_all_buttons)
        self.create_injury_button = CTkButton(master=self.injury_edit_frame, text="Record Injury",
                                              fg_color=colors.GREEN, hover_color=colors.DARK_GREEN,
                                              command=self.record_injury, state="disabled")
        self.injury_error_label = CTkLabel(master=self.injury_edit_frame, text="")


########################################################################################################################
        # THE INJURY DISPLAY

        self.injury_display_frame = CTkFrame(master=self, fg_color="transparent")
        self.injury_display = CTkScrollableFrame(master=self.injury_display_frame,
                                                 label_text="Recorded Injuries",
                                                 fg_color="transparent")

        # PLACING WIDGETS

        self.interface_frame.place(relx=0, rely=0, relwidth=0.65, relheight=1)
        self.record_info_frame.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.03)
        self.record_info_frame.rowconfigure(0, weight=1)
        self.record_info_frame.columnconfigure(0, weight=1)
        self.record_info_frame.columnconfigure(1, weight=1)
        self.record_info_frame.columnconfigure(2, weight=1)
        self.client_name_label.grid(row=0, column=0)
        self.date_label.grid(row=0, column=1)
        self.time_label.grid(row=0, column=2)

        self.body_map_frame.place(relx=0.02, rely=0.05, relwidth=0.96, relheight=0.68)
        self.segmented_button_frame.pack(fill="x", padx=10, pady=10)
        self.front_body_segmented_button.pack(fill="x")
        self.back_body_segmented_button.pack(fill="x", pady=2)
        # self.body_map_holder.place(relx=0.02, rely=0.18, relwidth=0.96, relheight=0.8)
        self.body_map_holder.pack(fill="both", expand=True, padx=10, pady=10)

        self.injury_edit_frame.place(relx=0.02, rely=0.75, relwidth=0.96, relheight=0.23)
        self.injury_edit_frame.rowconfigure(0, weight=1)
        self.injury_edit_frame.rowconfigure(1, weight=1)
        self.injury_edit_frame.rowconfigure(2, weight=1)
        self.injury_edit_frame.rowconfigure(3, weight=1)
        self.injury_edit_frame.columnconfigure(0, weight=1)
        self.injury_edit_frame.columnconfigure(1, weight=1)
        self.injury_edit_frame.columnconfigure(2, weight=1)
        self.add_injuries_label.grid(row=0, column=1)
        self.injury_locations_label.grid(row=1, column=0)
        self.injury_area_label.grid(row=2, column=0)
        self.injury_type_combobox.grid(row=1, column=1)
        self.injury_note_entry.grid(row=2, column=1)
        self.unselect_all_button.grid(row=1, column=2)
        self.create_injury_button.grid(row=2, column=2)
        self.injury_error_label.grid(row=3, column=1)

        self.injury_display_frame.place(relx=0.65, rely=0, relwidth=0.35, relheight=1)
        self.injury_display.place(relx=0.05, rely=0.025, relwidth=0.9, relheight=0.95)

    # called by main screen when importing/creating a record
    def set_record(self, record):
        self.record = record
        self.client_name_label.configure(text=self.client_name_string + self.record.client)
        self.date_label.configure(text=self.date_string + self.record.date)
        self.time_label.configure(text=self.time_string + self.record.time)
        self.front_body_segmented_button.configure(state="normal")
        self.back_body_segmented_button.configure(state="normal")
        self.create_injury_button.configure(state="normal")
        self.unselect_all_button.configure(state="normal")
        self.body_maps_dict["Front Head"] = CustomBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                            body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                "front head"])
        self.body_maps_dict["Back Head"] = CustomBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                           body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                               "back head"])
        self.body_maps_dict["Front Torso"] = SimpleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                             body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                 "front torso"])
        self.body_maps_dict["Back Torso"] = SimpleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                            body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                "back torso"])
        self.body_maps_dict["Front Arms"] = MirroredDoubleBodyFrame(master=self.body_map_holder,
                                                                    body_map_interface=self,
                                                                    left_body_map_tuple=
                                                                    body_map_data.BODY_MAP_INIT_DICT[
                                                                        "front left arm"],
                                                                    right_body_map_tuple=
                                                                    body_map_data.BODY_MAP_INIT_DICT[
                                                                        "front right arm"])
        self.body_maps_dict["Back Arms"] = MirroredDoubleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                                   left_body_map_tuple=
                                                                   body_map_data.BODY_MAP_INIT_DICT[
                                                                       "back left arm"],
                                                                   right_body_map_tuple=
                                                                   body_map_data.BODY_MAP_INIT_DICT[
                                                                       "back right arm"])
        self.body_maps_dict["Front Hands"] = DoubleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                             left_body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                 "front right hand"],
                                                             right_body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                 "front left hand"])
        self.body_maps_dict["Back Hands"] = DoubleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                            left_body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                "back right hand"],
                                                            right_body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                "back left hand"])
        self.body_maps_dict["Front Legs"] = SimpleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                            body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                                "front legs"])
        self.body_maps_dict["Back Legs"] = SimpleBodyFrame(master=self.body_map_holder, body_map_interface=self,
                                                           body_map_tuple=body_map_data.BODY_MAP_INIT_DICT[
                                                               "back legs"])
        for injury in self.record.injury_list:
            # do whatever needs to be done to add the injury to the GUI
            pass

    # when button in front segment is clicked, unselect back segment
    def front_body_button(self, body_map_name):
        self.back_body_segmented_button.set("")
        self.place_body_map(body_map_name)

    # when button in back segment is clicked, unselect front segment
    def back_body_button(self, body_map_name):
        self.front_body_segmented_button.set("")
        self.place_body_map(body_map_name)

    def stage_injury(self, index):
        if index in self.staged_injury_indices:
            self.staged_injury_indices.remove(index)
            self.determine_staged_locations()
        else:
            self.staged_injury_indices.add(index)
            self.staged_locations.add(find_location(index))
        # self.set_staged_locations_string()
        print(self.staged_injury_indices)
        self.set_staged_locations_label()
        self.set_injury_area_label()

    def determine_staged_locations(self):
        self.staged_locations.clear()
        for index in self.staged_injury_indices:
            self.staged_locations.add(find_location(index))

    def set_staged_locations_label(self):
        if self.is_staged_injuries_empty():
            self.injury_locations_label.configure(text="Injury Locations: None")
        else:
            new_string = "Injury Locations: "
            for location in self.staged_locations:
                new_string += f"{location}, "
            self.injury_locations_label.configure(text=new_string[:-2])

    def is_staged_injuries_empty(self):
        if len(self.staged_injury_indices) == 0:
            return True
        else:
            return False

    def deselect_all_buttons(self):
        # toggles the buttons on the GUI
        for body_map in self.staged_locations:
            self.body_maps_dict[body_map].deselect_body_map_buttons()
        self.staged_injury_indices.clear()
        self.staged_locations.clear()
        self.set_staged_locations_label()
        self.set_injury_area_label()

    # retrieves button of a given index in constant time
    def get_button(self, index):
        for location, index_range in body_map_data.body_part_range_dict.items():
            if index_range[0] <= index <= index_range[1]:
                pass
                # return the button so you can do shit to it?

    def calculate_injury_coverage(self):
        # use the values given in the original study to estimate surface area of injury coverage
        injury_coverage = 0
        # need to access the actual button from the body map
        for location in self.staged_locations:
            injury_coverage += self.body_maps_dict[location].get_map_selected_area(
                body_map_data.body_part_area_dict[location])
        return round(injury_coverage, 3)

    def set_injury_area_label(self):
        injury_coverage = self.calculate_injury_coverage()
        self.injury_area_label.configure(text=f"Area Covered: {str(injury_coverage)} cm²")

    def record_injury(self):
        # check to see if parameters are valid
        if self.injury_type_combobox.get() == "Injury Type":
            self.injury_error_label.configure(text="Please select an injury type")
            self.injury_error_label.after(3000, lambda: self.injury_error_label.configure(text=""))
        elif self.is_staged_injuries_empty():
            self.injury_error_label.configure(text="Please select at least one injury location")
            self.injury_error_label.after(3000, lambda: self.injury_error_label.configure(text=""))
        else:
            # create an injury, send to backend

            print(f"Staged Locations Before Creating Injury: {self.staged_locations}")

            self.record.create_injury(injury_type=self.injury_type_combobox.get(),
                                      indices=self.staged_injury_indices,
                                      locations=self.staged_locations,
                                      area=self.calculate_injury_coverage(),
                                      note=self.injury_note_entry.get())

            for body_map in self.staged_locations:
                self.body_maps_dict[body_map].add_injuries_deselect_body_map(self.injury_type_combobox.get())
            self.staged_injury_indices.clear()
            self.staged_locations.clear()
            self.set_staged_locations_label()
            self.set_injury_area_label()

            # TODO: add to injury display
            self.update_injury_display()

    def update_injury_display(self):
        # could delete all children from display and then re-add?
        for card in self.injury_display.winfo_children():
            card.destroy()
        # maybe update entire display based on what's in the injury record?
        for injury in self.record.injury_list:
            InjuryDisplayCard(master=self.injury_display, injury=injury).pack(padx=5, pady=5, fill=X, expand=False)

    def draw_injury(self, injury):
        # given a recorded injury, show it on the GUI
        pass

    # places the chosen body map
    def place_body_map(self, body_map_name):
        if self.current_body_map != self.body_maps_dict[body_map_name]:
            if self.current_body_map is not None:
                self.current_body_map.place_forget()
            self.body_maps_dict[body_map_name].place(relx=0, rely=0, relwidth=1, relheight=1)
            self.current_body_map = self.body_maps_dict[body_map_name]
