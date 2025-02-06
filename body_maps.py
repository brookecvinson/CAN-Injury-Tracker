from customtkinter import *
from abc import ABC, abstractmethod

from injury_button import InjuryButton, CustomInjuryButton


# contains data and functions necessary for all maps, base for inheritance
class AbstractBodyMap(CTkFrame):
    def __init__(self, master, body_map_interface):
        super().__init__(master=master, fg_color="transparent")

        self.body_map_interface = body_map_interface
        self.button_list = []

        # called in order to push a queued injury to the GUI and backend

    def update_buttons(self):
        for button in self.button_list:
            if button.selected:
                pass

    def add_injury(self):
        for button in self.button_list:
            if button.selected:
                pass

    # use to deselect all buttons
    def deselect_buttons(self):
        for button in self.button_list:
            if button.selected:
                button.toggle_select()

    def add_injury_and_deselect_buttons(self, injury_type):
        for button in self.button_list:
            if button.selected:
                button.add_injury(injury_type)
                button.toggle_select()

    def remove_injury_buttons(self, injury_type):
        for button in self.button_list:
            if button.selected:
                button.remove_injury(injury_type)
                button.toggle_select()
        # TODO: make this work with however deleting injuries ends up being handled

    def place_buttons(self, width, height):
        for button in self.button_list:
            button.place(relx=button.col / width, rely=button.row / height, relwidth=1 / width,
                         relheight=1 / height)

    def get_selected_area(self, button_size):
        area = 0
        for button in self.button_list:
            if button.selected:
                area += button_size
        return area


class BodyMap(AbstractBodyMap):
    def __init__(self, master, starting_index, button_data_list, max_width, body_map_interface):
        super().__init__(master=master, body_map_interface=body_map_interface)

        current_index = starting_index
        current_row = 0
        current_column = 0
        for row in button_data_list:
            for button in range(row[1]):
                self.button_list.append(InjuryButton(self, current_index, current_row,
                                                     current_column + row[0], body_map_interface))
                current_column += 1
                current_index += 1

            current_column = 0

            if len(row) > 2:
                for button in range(row[3]):
                    self.button_list.append(InjuryButton(self, current_index, current_row,
                                                         current_column + row[2], body_map_interface))
                    current_column += 1
                    current_index += 1

            current_column = 0
            current_row += 1

        self.place_buttons(max_width, len(button_data_list))


class MirroredBodyMap(AbstractBodyMap):
    def __init__(self, master, starting_index, button_data_list, max_width, body_map_interface):
        super().__init__(master=master, body_map_interface=body_map_interface)

        current_index = starting_index
        current_row = 0
        current_column = 0
        for row in button_data_list:
            for box in range(row[1]):
                self.button_list.append(InjuryButton(self, current_index, current_row,
                                                     current_column + (max_width - (row[0] + row[1])),
                                                     body_map_interface))
                current_column += 1
                current_index += 1

            current_column = 0

            if len(row) > 2:
                for box in range(row[3]):
                    self.button_list.append(InjuryButton(self, current_index, current_row,
                                                         current_column + (max_width - (row[2] + row[3])),
                                                         body_map_interface))
                    current_column += 1
                    current_index += 1

            current_column = 0
            current_row += 1

        self.place_buttons(max_width, len(button_data_list))


# used for the head maps, where buttons must have locations, indices, and sizes uniquely specified
class CustomBodyMap(AbstractBodyMap):
    def __init__(self, master, button_data_list, max_width, max_height, body_map_interface):
        super().__init__(master=master, body_map_interface=body_map_interface)

        self.max_width = max_width
        self.max_height = max_height

        for tuple in button_data_list:
            self.button_list.append(CustomInjuryButton(self, tuple[0], tuple[1], tuple[2], tuple[3],
                                                       tuple[4], tuple[5], body_map_interface))

        for button in self.button_list:
            button.place(relx=button.row / self.max_width, rely=button.col / self.max_height,
                         relwidth=button.width / self.max_width,
                         relheight=button.height / self.max_height)

    def get_selected_area(self, button_size):
        area = 0
        for button in self.button_list:
            if button.selected:
                area += button_size * button.area
        return area


# body frames contain body maps, titles, and other information needed to be grouped together
class AbstractBodyFrame(CTkFrame):
    def __init__(self, master, body_map_interface):
        super().__init__(master=master, fg_color="transparent")

        self.record = body_map_interface

    @abstractmethod
    def deselect_body_map_buttons(self):
        pass

    @abstractmethod
    def add_injuries_deselect_body_map(self, injury_type):
        pass

    @abstractmethod
    def get_map_selected_area(self, button_size):
        pass


# WILL NEED TO INITIALIZE MAPS WITHIN THEIR PARENT FRAMES
class SimpleBodyFrame(AbstractBodyFrame):
    def __init__(self, master, body_map_interface, body_map_tuple):
        super().__init__(master=master, body_map_interface=body_map_interface)

        self.body_map = BodyMap(master=self, starting_index=body_map_tuple[0], button_data_list=body_map_tuple[1],
                                max_width=body_map_tuple[2], body_map_interface=body_map_interface)
        self.body_map.place(relx=0.3, rely=0.02, relwidth=0.4, relheight=0.96)

    def deselect_body_map_buttons(self):
        self.body_map.deselect_buttons()

    def add_injuries_deselect_body_map(self, injury_type):
        self.body_map.add_injury_and_deselect_buttons(injury_type)

    def get_map_selected_area(self, button_size):
        return self.body_map.get_selected_area(button_size)


class DoubleBodyFrame(AbstractBodyFrame):
    def __init__(self, master, body_map_interface, left_body_map_tuple, right_body_map_tuple):
        super().__init__(master=master, body_map_interface=body_map_interface)

        self.left_body_map = BodyMap(master=self, starting_index=left_body_map_tuple[0],
                                     button_data_list=left_body_map_tuple[1],
                                     max_width=left_body_map_tuple[2], body_map_interface=body_map_interface)
        self.left_body_map.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.96)

        self.right_body_map = BodyMap(master=self, starting_index=right_body_map_tuple[0],
                                      button_data_list=right_body_map_tuple[1],
                                      max_width=right_body_map_tuple[2], body_map_interface=body_map_interface)
        self.right_body_map.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.96)

    def deselect_body_map_buttons(self):
        self.left_body_map.deselect_buttons()
        self.right_body_map.deselect_buttons()

    def add_injuries_deselect_body_map(self, injury_type):
        self.left_body_map.add_injury_and_deselect_buttons(injury_type)
        self.right_body_map.add_injury_and_deselect_buttons(injury_type)

    def get_map_selected_area(self, button_size):
        return self.left_body_map.get_selected_area(button_size) + self.right_body_map.get_selected_area(button_size)


# same as DoubleBodyFrame but the right body frame is mirrored
class MirroredDoubleBodyFrame(AbstractBodyFrame):
    def __init__(self, master, body_map_interface, left_body_map_tuple, right_body_map_tuple):
        super().__init__(master=master, body_map_interface=body_map_interface)

        self.left_body_map = BodyMap(master=self, starting_index=left_body_map_tuple[0],
                                     button_data_list=left_body_map_tuple[1],
                                     max_width=left_body_map_tuple[2], body_map_interface=body_map_interface)
        self.left_body_map.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.96)

        self.right_body_map = MirroredBodyMap(master=self, starting_index=right_body_map_tuple[0],
                                              button_data_list=right_body_map_tuple[1],
                                              max_width=right_body_map_tuple[2], body_map_interface=body_map_interface)
        self.right_body_map.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.96)

    def deselect_body_map_buttons(self):
        self.left_body_map.deselect_buttons()
        self.right_body_map.deselect_buttons()

    def add_injuries_deselect_body_map(self, injury_type):
        self.left_body_map.add_injury_and_deselect_buttons(injury_type)
        self.right_body_map.add_injury_and_deselect_buttons(injury_type)

    def get_map_selected_area(self, button_size):
        return self.left_body_map.get_selected_area(button_size) + self.right_body_map.get_selected_area(button_size)


class CustomBodyFrame(AbstractBodyFrame):
    def __init__(self, master, body_map_interface, body_map_tuple):
        super().__init__(master=master, body_map_interface=body_map_interface)

        self.body_map = CustomBodyMap(self, body_map_tuple[0], body_map_tuple[1], body_map_tuple[2], body_map_interface)
        self.body_map.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)

    def deselect_body_map_buttons(self):
        self.body_map.deselect_buttons()

    def add_injuries_deselect_body_map(self, injury_type):
        self.body_map.add_injury_and_deselect_buttons(injury_type)

    def get_map_selected_area(self, button_size):
        return self.body_map.get_selected_area(button_size)
