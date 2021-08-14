import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common

if __name__ == "__main__":
    number_of_codes = 16 #Default number of codes
    if len(sys.argv) >= 2:
        number_of_codes = int(sys.argv[1])

    #Save the 2-part key
    code = common.generate_2_part_key(number_of_codes, "KeyPart1.txt", "KeyPart2.txt")

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

    #Enter the pin and block the phone
    common.enter_code(code, coords_pin_buttons)
    common.enter_code(code, coords_pin_buttons)