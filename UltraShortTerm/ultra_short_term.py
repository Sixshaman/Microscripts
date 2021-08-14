from os import linesep
import sys
import re
import random
from enum import Enum

class Mode(Enum):
    SPLIT   = 0
    UNITE   = 1
    REMOVE  = 2
    EXTRACT = 3

def print_united_objectives(objectives):
    last_objective_type = ''
    while len(objectives.keys()) > 0:
        total_objective_count = sum([len(objective_list) for objective_list in objectives.values()])

        #Dynamically make the probabilities
        objective_count_sum = 0
        objective_weights = {}
        for objective_type in objectives.keys():
            objective_count = len(objectives[objective_type])

            minimum_prob = objective_count_sum / total_objective_count
            maximum_prob = (objective_count_sum + objective_count) / total_objective_count

            objective_weights[objective_type] = (minimum_prob, maximum_prob)
            objective_count_sum += objective_count

        objective_roll = random.uniform(0.0, 1.0)
        selected_objective_type = ''
        for objective_type in objective_weights.keys():
            objective_weight = objective_weights[objective_type]
            
            if objective_roll >= objective_weight[0] and objective_roll <= objective_weight[1]:
                selected_objective_type = objective_type
                break

        #75% chance to reroll if the last one was the same
        #Yes, that's just copy-pasted code
        if objective_type == last_objective_type and random.uniform(0.0, 1.0) >= 0.25:
            objective_roll = random.uniform(0.0, 1.0)
            selected_objective_type = ''
            for objective_type in objective_weights.keys():
                objective_weight = objective_weights[objective_type]
                
                if objective_roll >= objective_weight[0] and objective_roll <= objective_weight[1]:
                    selected_objective_type = objective_type
                    break
        
        objective = objectives[selected_objective_type].pop(0)
        print(objective)

        if len(objectives[objective_type]) == 0:
            objectives.pop(objective_type)

        last_objective_type = objective_type


def print_split_objectives(objectives):
    for objective_type in objectives.keys():
        for objective in objectives[objective_type]:
            print(objective)

        print("")

def print_split_objectives_with_remove(flat_objectives, type_to_remove):
    for objective in flat_objectives:
        if objective[0] == type_to_remove:
            continue

        print(objective)

def print_united_objectives_with_extract(objectives, type_to_extract):
    if type_to_extract in objectives.keys():
        for objective in objectives[type_to_extract]:
            print(objective)

        objectives.pop(type_to_extract)

    print_united_objectives(objectives)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ENTER FILENAME!")
    else:
        mode       = Mode.UNITE
        type_param = ""
        if len(sys.argv) > 2:
            if sys.argv[2] == "--unite":
                mode = Mode.UNITE
            elif sys.argv[2] == "--split":
                mode = Mode.SPLIT
            elif sys.argv[2] == "--remove" or sys.argv[2] == "--extract":
                if len(sys.argv) < 4:
                    raise ValueError("Please provide objective type")
                else:
                    type_param = sys.argv[3]

                    if sys.argv[2] == "--remove":
                        mode = Mode.REMOVE

                    if sys.argv[2] == "--extract":
                        mode = Mode.EXTRACT

        filename = sys.argv[1]

        objectives = {}
        flat_objectives = []
        with open(filename, 'r', encoding='utf-8', errors='ignore') as ff:
            for line in ff:
                found_groups = re.search(r"\[(.*)\].*", line)
                if found_groups:
                    objective_type = found_groups[1]
                    
                    if not objective_type in objectives.keys():
                        objectives[objective_type] = [found_groups[0]]
                    else:
                        objectives[objective_type].append(found_groups[0])

                    flat_objectives.append((objective_type, found_groups[0]))

        if mode == Mode.UNITE:
            print_united_objectives(objectives)

        elif mode == Mode.SPLIT:
            print_split_objectives(objectives)

        elif mode == Mode.REMOVE:
            print_split_objectives_with_remove(flat_objectives, type_param)

        elif mode == Mode.EXTRACT:
            print_united_objectives_with_extract(objectives, type_param)