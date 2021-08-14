import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common

if __name__ == "__main__":
    number_of_codes = 16 #Default number of codes
    if sys.argv >= 2:
        number_of_codes = int(sys.argv[1])

    #Save the 2-part key
    code = common.generate_2_part_key(number_of_codes, "KeyPart1.txt", "KeyPart2.txt")

    #Coordinates for the buttons on AppBlock pin enter screen for the particular phone model
    coords_pin_buttons = \
    {
        '0': (540, 1750),
        '1': (220, 1000),
        '2': (540, 1000),
        '3': (760, 1000),
        '4': (220, 1250),
        '5': (540, 1250),
        '6': (760, 1250),
        '7': (220, 1500),
        '8': (540, 1500),
        '9': (760, 1500),
    }

    #Enter the pin and block the phone
    common.enter_code(code, coords_pin_buttons)
    common.enter_code(code, coords_pin_buttons)