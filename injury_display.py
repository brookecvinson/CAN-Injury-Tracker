from customtkinter import *

import colors
from colors import *


class InjuryDisplayCard(CTkFrame):
    def __init__(self, master, injury):
        super().__init__(master=master, height=100)

        print(injury.get_locations_string())
        print(injury.locations)
        print(injury.area)

        # inner frames
        self.frame1 = CTkFrame(master=self, fg_color="transparent", height=32)
        self.frame2 = CTkFrame(master=self, fg_color="transparent", height=32)

        self.id_label = CTkLabel(master=self.frame1,
                                 text=f"ID: {injury.id}")
        self.topography_label = CTkLabel(master=self.frame1, text=f"Topography: {injury.type}")
        self.area_label = CTkLabel(master=self,
                                   text=f"Area: {injury.area} cm²")
        self.locations_label = CTkLabel(master=self,
                                        text=f"Location(s): {injury.get_locations_string()}")
        self.edit_button = CTkButton(master=self.frame2,
                                     text="Edit Injury",
                                     fg_color=colors.GREEN,
                                     hover_color=colors.DARK_GREEN,
                                     command=self.edit_button_callback)
        self.delete_button = CTkButton(master=self.frame2,
                                       text="Delete Injury",
                                       fg_color=colors.MAROON,
                                       hover_color=colors.DARK_MAROON,
                                       command=self.delete_button_callback)

        # placing widgets

        self.frame1.pack_propagate(False)
        self.frame2.pack_propagate(False)

        self.frame1.pack(pady=5, fill=X, expand=False)
        self.id_label.place(relx=0.1)
        self.topography_label.place(relx=0.3)

        self.locations_label.pack()
        # self.area_label.pack()

        self.frame2.pack(pady=5, fill=X, expand=False)
        self.edit_button.place(relx=0.05, relwidth=0.40)
        self.delete_button.place(relx=0.55, relwidth=0.40)

    def edit_button_callback(self):
        pass

    def delete_button_callback(self):
        pass







