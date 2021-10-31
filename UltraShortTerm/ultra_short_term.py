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

def print_objective(objective, dot_count):
    print(objective + "." * (dot_count - len(objective)))

def print_united_objectives(objectives, dot_count):
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
        print_objective(objective, dot_count)

        if len(objectives[objective_type]) == 0:
            objectives.pop(objective_type)

        last_objective_type = objective_type


def print_split_objectives(objectives, dot_count):
    for objective_type in objectives.keys():
        for objective in objectives[objective_type]:
            print_objective(objective, dot_count)

        print("")

def print_split_objectives_with_remove(flat_objectives, type_to_remove, dot_count):
    for objective in flat_objectives:
        if objective[0] == type_to_remove:
            continue

        print_objective(objective[1], dot_count)

def print_united_objectives_with_extract(flat_objectives, type_to_extract, dot_count):
    for objective in flat_objectives:
        if objective[0] == type_to_extract:
            print_objective(objective[1], dot_count)

    for objective in flat_objectives:
        if objective[0] != type_to_extract:
            print_objective(objective[1], dot_count)


def parse_cmd_args(cmd_args):
    args_count = len(cmd_args)
    if args_count < 2:
        raise ValueError("Filename is not provided!")

    use_dots   = False
    mode       = Mode.UNITE
    type_param = ""

    filename = cmd_args[1]

    arg_index = 2
    while arg_index < args_count:
        if cmd_args[arg_index] == "--dots":
            use_dots = True
            arg_index += 1
            continue

        elif cmd_args[arg_index] == "--unite":
            mode = Mode.UNITE
            arg_index += 1

        elif cmd_args[arg_index] == "--split":
            mode = Mode.SPLIT
            arg_index += 1

        elif cmd_args[arg_index] == "--remove" or cmd_args[arg_index] == "--extract":
            if sys.argv[arg_index] == "--remove":
                mode = Mode.REMOVE

            if sys.argv[arg_index] == "--extract":
                mode = Mode.EXTRACT

            if args_count > (arg_index + 1):
                type_param = sys.argv[arg_index + 1]
                arg_index += 1

            arg_index += 1

    return filename, mode, type_param, use_dots


if __name__ == "__main__":
    filename, mode, type_param, use_dots = parse_cmd_args(sys.argv)

    objectives = {}
    flat_objectives = []
    max_objective_len = 0
    with open(filename, 'r', encoding='utf-8', errors='ignore') as ff:
        for line in ff:
            found_groups = re.search(r"\[(.*)\].*", line)
            if found_groups:
                objective_type = found_groups[1]
                objective      = found_groups[0]
                
                if not objective_type in objectives.keys():
                    objectives[objective_type] = [objective]
                else:
                    objectives[objective_type].append(objective)

                flat_objectives.append((objective_type, objective))

                if use_dots:
                    max_objective_len = max(max_objective_len, len(objective))

    dot_count = 0
    if use_dots:
        dot_count = max(dot_count, max_objective_len + 3)

    #Select a random type if none provided
    if len(type_param) == 0:
        type_param = random.choice(list(objectives.keys()))

    if mode == Mode.UNITE:
        print_united_objectives(objectives, dot_count)

    elif mode == Mode.SPLIT:
        print_split_objectives(objectives, dot_count)

    elif mode == Mode.REMOVE:
        print_split_objectives_with_remove(flat_objectives, type_param, dot_count)

    elif mode == Mode.EXTRACT:
        print_united_objectives_with_extract(flat_objectives, type_param, dot_count)