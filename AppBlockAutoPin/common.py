import os
import random
import time

def random_digit():
    return random.choice("0123456789")

def generate_4_digit_code():
    return random_digit() + random_digit() + random_digit() + random_digit()

def generate_codes(count):
    return [generate_4_digit_code() for _ in range(0, count)]

def enter_code(code, coords_pin_buttons):
    if not 'ANDROID_SDK_ROOT' in os.environ.keys():
        raise RuntimeError("ANDROID_SDK_ROOT is not defined")

    sdk_root = os.environ['ANDROID_SDK_ROOT']
    for c in code:
        button_coords = coords_pin_buttons[c]
        command = sdk_root + "platform-tools/adb.exe shell input tap " + str(button_coords[0]) + " " + str(button_coords[1])
        os.system(command)
        time.sleep(0.5)
    time.sleep(1)

def generate_2_part_key(number_of_keys, part1_name, part2_name):
    codes      = generate_codes(number_of_keys)
    code_index = random.randint(0, number_of_keys - 1)

    with open(part1_name, "w") as key_part_1:
        for index, code in enumerate(codes):
            key_part_1.write(str(index) + " " + str(code) + "\n")
        key_part_1.close()

    with open(part2_name, "w") as key_part_2:
        key_part_2.write(str(code_index))    
        key_part_2.close()

    return codes[code_index]

def brutforce_unlock(start_number, pin_coords):
    assert len(start_number) == 4
    assert 'ANDROID_SDK_ROOT' in os.environ.keys()

    sdk_root = os.environ['ANDROID_SDK_ROOT']
    for number in range(int(start_number), 10000):
        number_str = str(number).zfill(4)
        print("Trying " + number_str + "...")

        for digit in number_str:
            button_coords = pin_coords[str(digit)]
            os.system(sdk_root + "/platform-tools/adb.exe shell input tap " + str(button_coords[0]) + " " + str(button_coords[1]))
            time.sleep(0.5)
        time.sleep(1)