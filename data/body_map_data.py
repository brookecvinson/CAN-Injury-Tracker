from data.body_map_index_lists import *

BODY_MAP_INIT_DICT = {
    "front head": (FRONT_HEAD_LIST, 12, 15),
    "back head": (BACK_HEAD_LIST, 10, 15),
    "front torso": (2051, FRONT_TORSO_LIST, 30),
    "back torso": (3257, BACK_TORSO_LIST, 30),
    "front left arm": (279, ARMS_LIST, 24),
    "front right arm": (722, ARMS_LIST, 24),
    "back left arm": (1165, ARMS_LIST, 24),
    "back right arm": (1608, ARMS_LIST, 24),
    "front right hand": (4628, HANDS_FR_BL_LIST, 26),
    "front left hand": (5051, HANDS_FL_BR_LIST, 26),
    "back right hand": (5470, HANDS_FL_BR_LIST, 26),
    "back left hand": (5892, HANDS_FR_BL_LIST, 26),
    "front legs": (6312, FRONT_LEGS_LIST, 20),
    "back legs": (7071, BACK_LEGS_LIST, 19)
}

body_part_range_dict = {  # "all": (1, 7850),
    "Front Head": (1, 136),
    "Back Head": (137, 278),
    "Front Arms": (279, 1164),
    "Back Arms": (1165, 2050),
    "Front Torso": (2051, 3256),
    "Back Torso": (3257, 4627),
    "Front Hands": (4628, 5469),
    "Back Hands": (5470, 6311),
    "Front Legs": (6312, 7070),
    "Back Legs": (7071, 7850)}

body_part_area_dict = {
    "Front Head": 2.25,
    "Back Head": 2.25,
    "Front Arms": 1.44,
    "Back Arms": 1.44,
    "Front Torso": 1.44,
    "Back Torso": 1.44,
    "Front Hands": 0.3025,
    "Back Hands": 0.3025,
    "Front Legs": 4.6,
    "Back Legs": 4.6}

