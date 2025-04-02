from customtkinter import CTkButton
from components.injury_priority_multiset import InjuryPriorityMultiset
from data import colors


# basic injury button: location determined by body map tuple, size and color are constant
class InjuryButton(CTkButton):
    def __init__(self, parent, index, row, col, body_map_interface):
        super().__init__(master=parent,
                         text="",
                         corner_radius=0,
                         fg_color=colors.BLUE,
                         hover_color=colors.LIGHT_BLUE,
                         command=self.button_function)
        self.body_map_interface = body_map_interface
        self.index = index
        self.row = row
        self.col = col
        self.unselected_fg_color = colors.BUTTON_COLOR_DICT["unselected"][1]
        self.unselected_hover_color = colors.BUTTON_COLOR_DICT["unselected"][0]
        self.selected_fg_color = colors.BUTTON_COLOR_DICT["selected"][1]
        self.selected_hover_color = colors.BUTTON_COLOR_DICT["selected"][1]
        self.selected = False
        self.injury_set = InjuryPriorityMultiset()

        self.bind("<B1-Motion>", self.paint_select)



    # update state of button
    def toggle_select(self):
        # selecting
        if not self.selected:
            self.configure(fg_color=self.selected_fg_color, hover_color=self.selected_hover_color)
            self.selected = True
        # unselecting
        else:
            self.configure(fg_color=self.unselected_fg_color, hover_color=self.unselected_hover_color)
            self.selected = False

    def paint_select(self, event=None):
        if not self.selected:
            self.configure(fg_color=self.selected_fg_color, hover_color=self.selected_hover_color)
            self.selected = True
            self.body_map_interface.stage_injury(self.index)

    # handles front and back end parts of button functionality
    def button_function(self):
        self.toggle_select()
        self.body_map_interface.stage_injury(self.index)

    def add_injury(self, injury_type):
        self.injury_set.add(injury_type)
        self.set_color(self.injury_set.get_highest_priority())

    def remove_injury(self, injury_type):
        self.injury_set.remove(injury_type)
        self.set_color(self.injury_set.get_highest_priority())

    def set_color(self, injury_type):
        if injury_type is None:
            self.unselected_hover_color = colors.BUTTON_COLOR_DICT["unselected"][0]
            self.unselected_fg_color = colors.BUTTON_COLOR_DICT["unselected"][1]
        else:
            self.unselected_hover_color = colors.BUTTON_COLOR_DICT[injury_type][0]
            self.unselected_fg_color = colors.BUTTON_COLOR_DICT[injury_type][1]


class CustomInjuryButton(InjuryButton):
    def __init__(self, parent, index, row, col, width, height, color_bit, body_map_interface):
        super().__init__(parent=parent,
                         index=index,
                         row=row,
                         col=col,
                         body_map_interface=body_map_interface)
        self.width = width
        self.height = height
        self.area = float(width) * float(height)
        self.color_bit = color_bit
        if color_bit == 1:
            self.configure(fg_color=colors.DARK_BLUE)
            self.unselected_fg_color = colors.DARK_BLUE
            self.selected_fg_color = colors.DARK_GREEN

    def set_color(self, injury_type):
        if injury_type is None:
            self.unselected_hover_color = colors.BUTTON_COLOR_DICT["unselected"][0]
            if self.color_bit == 0:
                self.unselected_fg_color = colors.BUTTON_COLOR_DICT["unselected"][1]
            else:
                self.unselected_fg_color = colors.BUTTON_COLOR_DICT["unselected"][2]
            # self.unselected_fg_color = colors.BLUE
        else:
            self.unselected_hover_color = colors.BUTTON_COLOR_DICT[injury_type][0]
            if self.color_bit == 0:
                self.unselected_fg_color = colors.BUTTON_COLOR_DICT[injury_type][1]
            else:
                self.unselected_fg_color = colors.BUTTON_COLOR_DICT[injury_type][2]


