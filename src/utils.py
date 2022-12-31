from matplotlib.colors import to_rgba
import argparse

def arg_parser():
    parser = argparse.ArgumentParser(description="MagicCubeMPL")
    parser.add_argument("-n", dest="n", type=int, required=False, default=DEFAULT_N, help="cube size (2 or 3)")
    parser.add_argument("-r", dest="r", type=int, required=False, default=DEFAULT_RANDOM_ROTATIONS, help="amount of random rotations when initializing")
    return parser

WHITE   = "#ffffff"
GREEN   = "#009b48"
RED     = "#b71234"
YELLOW  = "#ffd500"
BLUE    = "#0046ad"
ORANGE  = "#ff5800"

DEFAULT_COLORS = {
    "U": to_rgba(WHITE),
    "L": to_rgba(GREEN),
    "F": to_rgba(RED),
    "D": to_rgba(YELLOW),
    "R": to_rgba(BLUE),
    "B": to_rgba(ORANGE)
}

DEFAULT_VIEW_SETTINGS = {
    "gridspec": "24",
    "views": [
        {"elev": 30, "azim": -60, "disable_mouse_rotation": True, "face_ids": ["U", "F", "R"]},
        {"elev": 30, "azim": 30, "disable_mouse_rotation": True, "face_ids": ["U", "R", "B"]},
        {"elev": 30, "azim": 120, "disable_mouse_rotation": True, "face_ids": ["U", "B", "L"]},
        {"elev": 30, "azim": 210, "disable_mouse_rotation": True, "face_ids": ["U", "L", "F"]},
        {"elev": 210, "azim": -30, "disable_mouse_rotation": True, "face_ids": ["D", "L", "B"]},
        {"elev": 210, "azim": 60, "disable_mouse_rotation": True, "face_ids": ["D", "F", "L"]},
        {"elev": 210, "azim": 150, "disable_mouse_rotation": True, "face_ids": ["D", "R", "F"]},
        {"elev": 210, "azim": 240, "disable_mouse_rotation": True, "face_ids": ["D", "B", "R"]}
    ]
}

DEFAULT_FIGSIZE = (20, 10)
DEFAULT_N = 3
DEFAULT_RANDOM_ROTATIONS = 50
