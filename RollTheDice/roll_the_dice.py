import random
import datetime
import time
import os
import sys

def decision_time():
    curr_time  = datetime.datetime.now()
    return curr_time + datetime.timedelta(seconds = 10)

def roll_the_dice(choices_filename):
    dtime = decision_time()
    ctime = datetime.datetime.now()

    ind = 0
    while ctime < dtime:
        time.sleep(0.05)
        os.system("cls")
        print(["/", "-", "\\", "|"][ind])
        ind = (ind + 1) % 4
        ctime = datetime.datetime.now()

    return fair_choice(choices_filename)

def all_choices(filename):
    choices = []
    with open(filename, "r") as f:
        choices = [line for line in f]            
    return choices

def last_7_choices():
    curr_date_time = datetime.datetime.now()

    prev_days_start = 1
    prev_days_end   = 8
    if curr_date_time.time().hour < 6: #The day starts at 6AM
        prev_days_start = 2
        prev_days_end   = 9

    last_day_files = [daily_file(curr_date_time.date() - datetime.timedelta(days = i)) for i in range(prev_days_start, prev_days_end)]
    return [choice_from_file(f) for f in last_day_files if os.path.exists(f)]

def fair_choice(choices_filename):
    choices      = all_choices(choices_filename)
    last_choices = last_7_choices()

    last_choices_by_days_ago = dict()
    for days_ago, last_choice in enumerate(last_choices):
        if last_choice in choices: #Forbid selecting something that has been deleted recently
            last_choices_by_days_ago[days_ago] = last_choice

    chance_non_recent  = 0.85
    chance_last_day    = 0.1
    chance_last_2_days = 0.01

    if len(last_choices_by_days_ago.keys()) > 0:
        non_last_choices = [choice for choice in choices if not choice in last_choices_by_days_ago.values()]

        #The probability to select something from > a week ago is 85%
        chances         = []
        choices_ordered = []
        for i in range(0, len(non_last_choices)):
            chances.append((i + 1) * chance_non_recent / len(non_last_choices))
            choices_ordered.append(non_last_choices[i])

        remaining_chance = 1.0 - chance_non_recent * (len(non_last_choices) > 0)
        remaining_start  = 1.0 - remaining_chance

        if 0 in last_choices_by_days_ago: #If the last choice hasn't been deleted recently
            yesterday_choice      = last_choices_by_days_ago[0]
            non_yesterday_choices = [choice for choice in last_choices_by_days_ago.values() if choice != yesterday_choice]

            non_yesterday_choices = list(set(non_yesterday_choices))

            yesterday_choice_quota = remaining_chance * chance_last_day
            if 1 in last_choices_by_days_ago and last_choices_by_days_ago[1] == yesterday_choice:
                yesterday_choice_quota = remaining_chance * chance_last_2_days
        
            remaining_chance = remaining_chance - yesterday_choice_quota
            for i, choice in enumerate(non_yesterday_choices):
                chances.append(remaining_start + (i + 1) * remaining_chance / len(non_yesterday_choices))
                choices_ordered.append(choice)

            chances.append(1.0)
            choices_ordered.append(yesterday_choice)

        else:
            last_non_deleted_choices = list(set(last_choices_by_days_ago.values()))

            for i, choice in enumerate(last_non_deleted_choices):
                chances.append(remaining_start + (i + 1) * remaining_chance / len(last_non_deleted_choices))
                choices_ordered.append(choice)

        final_choice = random.choice(choices_ordered) #First naive choice in the case something goes wrong
        diceroll = random.uniform(0.0, 1.0)
        for chance, choice in zip(chances, choices_ordered):
            if diceroll <= chance:
                final_choice = choice
                break

        return final_choice

    else:
        return random.choice(choices)

def choice_from_file(file):
    with open(file, 'r', encoding="utf-8-sig") as fstr:
        return fstr.readline()

def save_choice(choice):
    tfile = today_file()
    with open(tfile, 'w', encoding="utf-8-sig") as fstr:
        fstr.write(choice)

def daily_file(day):
    return os.path.dirname(os.path.realpath(__file__)) + "/Data/RollTheDice/" + str(day) + ".txt"

def today_file():
    curr_date_time = datetime.datetime.now()
    curr_date      = curr_date_time.date()
    curr_time      = curr_date_time.time()  

    #I don't want to use timezones, never use fixed timezones for this
    if curr_time.hour < 6:
        curr_date = curr_date - datetime.timedelta(1)

    return daily_file(curr_date)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the file with choices")
    else:
        choices_filename = sys.argv[1]
        curr_file = today_file()
        
        if not os.path.exists(curr_file):
            today_choice = roll_the_dice(choices_filename)
            print(today_choice)
            save_choice(today_choice)
        else:
            print(choice_from_file(curr_file))