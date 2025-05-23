# need to figure out how to store this data
# makes sense to have individual records for each recording that can be written and retrieved in a common format for
# the GUI to process
# how should the injuries be stored?
from data import body_map_data


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
        print(self.time)
        self.injury_list = []
        self.next_injury_id = 1
        for injury in injury_list:
            pass  # use injury class to initialize an injury, depends on how data is stored in files
        self.location_dictionary = {}

    class Injury:
        def __init__(self, injury_id, injury_type, indices, locations, area, note, injury_depth):
            self.id = injury_id
            self.type = injury_type
            self.indices = set(indices)  # Ensure it's a set
            self.primary_locations = list(locations)  # Ensure it's a list copy
            self.secondary_location = None
            self.depth = injury_depth
            self.side = None
            self.area = area
            self.note = note if note else "None"

            # Debug prints
            print(f"Created Injury {self.id}:")
            print(f"  Locations: {self.primary_locations}")
            print(f"  Indices: {self.indices}")

        def print_injury(self):
            print(f"Injury {self.id}:")
            print(f"Location(s): {self.get_locations_string()}")
            print(f"Indices: {self.indices}")
            print(f"Area: {self.area}")
            print("*" * 30)

        def get_locations_string(self):
            return ", ".join(self.primary_locations) if self.primary_locations else "None"

    # injury record methods

    def create_injury(self, injury_type, indices, locations, area, note, injury_depth):
        # create injury, append to list
        new_injury = self.Injury(self.next_injury_id, injury_type, indices, locations, area, note, injury_depth)
        new_injury.print_injury()
        self.injury_list.append(new_injury)
        # increment ID
        self.next_injury_id += 1
        # self.print_injuries()

    def remove_injury(self, injury_id):
        """Removes an injury by ID and confirms if successful."""
        initial_length = len(self.injury_list)
        self.injury_list = [injury for injury in self.injury_list if injury.id != injury_id]

        if len(self.injury_list) < initial_length:
            print(f"Injury {injury_id} removed.")
        else:
            print(f"No injury found with ID {injury_id}.")

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

    def get_total_injury_area(self):
        total_area = 0
        for injury in self.injury_list:
            total_area += injury.area
        return total_area

    def get_avg_injury_area(self):
        if len(self.injury_list) == 0:
            return 0
        return self.get_total_injury_area() / self.get_num_injuries()

    def get_num_injuries(self):
        return len(self.injury_list)

    def safe_date_format(self) -> str:
        return self.date.replace("/", "-")

    def safe_time_format(self) -> str:
        return self.time.replace(".", "")

    def get_injury_type_dict(self):
        injury_type_dict = {
            "Bruise": 0,
            "Open Wound": 0,
            "Closed Wound": 0,
            "Redness": 0,
            "Other": 0
        }
        for injury in self.injury_list:
            injury: InjuryRecord.Injury
            injury_type_dict[injury.type] += 1
        return injury_type_dict

    def get_date(self):
        return self.date

    def get_largest_injury_size(self):
        largest_size = 0
        for injury in self.injury_list:
            injury: InjuryRecord.Injury
            if injury.area > largest_size:
                largest_size = injury.area
        return largest_size

