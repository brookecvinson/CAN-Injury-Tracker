# need to figure out how to store this data
# makes sense to have individual records for each recording that can be written and retrieved in a common format for
# the GUI to process
# how should the injuries be stored?
import body_map_data


def find_location(index):
    for location, index_range in body_map_data.body_part_range_dict.items():
        if index_range[0] <= index <= index_range[1]:
            return location


# contains the data for a recording of all injuries on a client
class InjuryRecord:
    # contains the data for each individual injury

    def __init__(self, client, date, time, injury_list):
        self.client = client
        self.date = date
        self.time = time  # AM or PM
        self.injury_list = []
        self.next_injury_id = 1
        for injury in injury_list:
            pass  # use injury class to initialize an injury, depends on how data is stored in files
        self.location_dictionary = {}

        # FIXME: figure out way to import data from injury list into the location dictionary
        # will depend on how data is stored, so figure that out later I guess

    class Injury:
        def __init__(self, injury_id, injury_type, indices, locations, area, note):
            # identifies the injury
            self.id = injury_id
            # e.g., bruise, open wound, etc.
            self.type = injury_type
            self.indices = indices
            # locations of an injury: e.g., arms, head, etc.
            self.locations = locations
            self.area = area
            self.note = note
            if self.note == "":
                self.note = "None"

        def edit(self):
            pass

        def get_locations_string(self):
            locations_string = ""
            for location in self.locations:
                locations_string += f"{location}, "
            return locations_string[:-2]

        def print_injury(self):
            print(f"Injury {self.id}:")
            print(f"Location(s): {self.get_locations_string()}")
            print(f"Indices: {self.indices}")
            print(f"Area: {self.area}")
            print("*" * 30)

    # injury record methods

    def create_injury(self, injury_type, indices, locations, area, note):
        # create injury, append to list
        new_injury = self.Injury(self.next_injury_id, injury_type, indices, locations, area, note)
        new_injury.print_injury()
        self.injury_list.append(new_injury)
        # increment ID
        self.next_injury_id += 1
        # self.print_injuries()

    # for testing
    def print_injuries(self):
        for injury in self.injury_list:
            injury.print_injury()

    # use to retrieve a list of injuries for a specified region to send to the GUI
    # will this actually be used? idk
    def get_injuries(self, body_part):
        return_dict = {}
        for index in range(body_map_data.body_part_range_dict[body_part][0],
                           body_map_data.body_part_range_dict[body_part][1]):
            return_dict[index] = self.location_dictionary[index]

