import data.colors
from data import colors
from injury_record import *
from components.body_maps import *
from components.injury_display import InjuryDisplayCard
from file_operations import *


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
        self.injury_depth = ["Superficial", "Moderate", "Severe"]

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
        self.injury_depth_label = CTkLabel(master=self.injury_edit_frame, text="Injury Depth: ")
        self.injury_depth_combobox = CTkComboBox(master=self.injury_edit_frame, values=self.injury_depth,
                                                state="readonly")
        self.injury_depth_combobox.set("Injury Depth")
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
        self.save_record_button = CTkButton(master=self.injury_display_frame,
                                            text="Save Record",
                                            state="disabled",
                                            command=self.save_record_callback)

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
        self.injury_area_label.grid(row=3, column=0)
        self.injury_depth_label.grid(row=2, column=0)
        self.injury_depth_combobox.grid(row=2, column=1)
        self.injury_type_combobox.grid(row=1, column=1)
        self.injury_note_entry.grid(row=3, column=1)
        self.unselect_all_button.grid(row=1, column=2)
        self.create_injury_button.grid(row=2, column=2)
        self.injury_error_label.grid(row=3, column=1)

        self.injury_display_frame.place(relx=0.65, rely=0, relwidth=0.35, relheight=1)
        self.injury_display.place(relx=0.05, rely=0.025, relwidth=0.9, relheight=0.89)
        self.save_record_button.place(relx=0.2, rely=0.93, relwidth=0.6, relheight=0.05)

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
        self.save_record_button.configure(state="normal")
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
                start_index = index_range[0]
                # retrieve the associated body map
                body_part = location
                body_frame: AbstractBodyFrame = self.body_maps_dict[body_part]
                # need to calculate what index in the body frame's list the button with assigned index "index" will be
                relative_index = index - start_index
                return body_frame.get_button(relative_index)

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
                                      note=self.injury_note_entry.get(), injury_depth=self.injury_depth_combobox.get())

            for body_map in self.staged_locations:
                self.body_maps_dict[body_map].add_injuries_deselect_body_map(self.injury_type_combobox.get())
            self.staged_injury_indices.clear()
            self.staged_locations.clear()
            self.set_staged_locations_label()
            self.set_injury_area_label()
            self.update_injury_display()

    def update_injury_display(self):
        # could delete all children from display and then re-add?
        for card in self.injury_display.winfo_children():
            card.destroy()
        # maybe update entire display based on what's in the injury record?
        for injury in self.record.injury_list:
            (InjuryDisplayCard(master=self.injury_display,
                               injury=injury,
                               delete_callback=self.delete_injury_card,
                               edit_callback=self.edit_injury)
             .pack(padx=5, pady=5, fill=X, expand=False))

    def delete_injury_card(self, injury_card: InjuryDisplayCard):

        # create confirmation popup
        popup = CTkToplevel(self)
        popup.title("Confirm Deletion")
        popup.geometry("300x125")
        popup.grab_set()  # Makes the popup modal (prevents interaction with main window)

        # Get main window position and size
        self.update_idletasks()  # Ensures accurate window size
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        # Calculate popup position
        popup_width = 300
        popup_height = 150
        x_position = main_x + (main_width // 2) - (popup_width // 2)
        y_position = main_y + (main_height // 2) - (popup_height // 2)

        # Set popup geometry with calculated position
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        # Label message
        label = CTkLabel(popup, text="Are you sure you want to\ndelete this injury?",
                         wraplength=250)
        label.pack(pady=20)

        # Button frame
        button_frame = CTkFrame(popup,
                                fg_color="transparent")
        button_frame.pack(pady=10)

        # Yes button
        def confirm_delete():
            popup.destroy()  # close popup

            # extract needed info from injury
            injury_to_delete: InjuryRecord.Injury = injury_card.injury
            injury_to_delete_id = injury_to_delete.id
            injury_to_delete_indices = injury_to_delete.indices
            injury_to_delete_type = injury_to_delete.type
            injury_to_delete_locations = injury_to_delete.primary_locations

            # for now, selecting indices to remove
            # deselect everything first

            self.staged_injury_indices.clear()
            self.staged_locations.clear()
            self.set_staged_locations_label()
            self.set_injury_area_label()

            # update indices and locations
            for index in injury_to_delete_indices:
                # need to retrieve the button to toggle select on it
                self.get_button(index).toggle_select()
                self.stage_injury(index)

            # delete injury from gui
            for body_map in self.staged_locations:
                self.body_maps_dict[body_map].remove_injuries_deselect_body_map(injury_to_delete_type)

            # extract id, delete injury from record
            self.record.remove_injury(injury_to_delete_id)

            # update display to reflect changes
            self.update_injury_display()
            self.staged_injury_indices.clear()
            self.staged_locations.clear()
            self.set_staged_locations_label()
            self.set_injury_area_label()

        yes_button = CTkButton(button_frame,
                               text="Yes",
                               fg_color=colors.GREEN,
                               hover_color=colors.DARK_GREEN,
                               width=125,
                               command=confirm_delete)
        yes_button.pack(side="left", padx=10)

        # No button
        no_button = CTkButton(button_frame,
                              text="No",
                              fg_color=colors.MAROON,
                              hover_color=colors.DARK_MAROON,
                              width=125,
                              command=popup.destroy)
        no_button.pack(side="right", padx=10)

    def edit_injury(self, injury_card: InjuryDisplayCard):
        # same logic as deletion, but select the boxes afterward
        injury_to_delete: InjuryRecord.Injury = injury_card.injury
        injury_to_delete_id = injury_to_delete.id
        injury_to_delete_indices = injury_to_delete.indices
        injury_to_delete_type = injury_to_delete.type
        injury_to_delete_locations = injury_to_delete.primary_locations

        # for now, selecting indices to remove
        # deselect everything first

        self.staged_injury_indices.clear()
        self.staged_locations.clear()
        self.set_staged_locations_label()
        self.set_injury_area_label()

        # update indices and locations
        for index in injury_to_delete_indices:
            # need to retrieve the button to toggle select on it
            self.get_button(index).toggle_select()
            self.stage_injury(index)

        # delete injury from gui
        for body_map in self.staged_locations:
            self.body_maps_dict[body_map].remove_injuries(injury_to_delete_type)

        # extract id, delete injury from record
        self.record.remove_injury(injury_to_delete_id)

        # update display to reflect changes
        self.set_staged_locations_label()
        self.set_injury_area_label()
        self.update_injury_display()

    # places the chosen body map
    def place_body_map(self, body_map_name):
        if self.current_body_map != self.body_maps_dict[body_map_name]:
            if self.current_body_map is not None:
                self.current_body_map.place_forget()
            self.body_maps_dict[body_map_name].place(relx=0, rely=0, relwidth=1, relheight=1)
            self.current_body_map = self.body_maps_dict[body_map_name]

    def save_record_callback(self):
        save_record(self.record)
        fg_color = self.save_record_button.cget("fg_color")
        hover_color = self.save_record_button.cget("hover_color")
        self.after(5000, lambda: self.save_record_button.configure(text="Save Record", fg_color=fg_color, hover_color=hover_color))
