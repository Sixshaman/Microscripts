import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common

if __name__ == "__main__":
    assert len(sys.argv) > 1

    #Coordinates for the buttons on AppBlock pin enter screen for the particular phone model
    coords_pin_buttons = \
    {
        '0': (540, 2080),
        '1': (175, 1375),
        '2': (540, 1375),
        '3': (895, 1375),
        '4': (175, 1615),
        '5': (540, 1615),
        '6': (895, 1615),
        '7': (175, 1845),
        '8': (540, 1845),
        '9': (895, 1845),
    }

    common.brutforce_unlock(sys.argv[1], coords_pin_buttons)