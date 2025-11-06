#!/usr/bin/env python3

"""Returns all valid family and species of
ERV based on a specified pattern."""

import re
import sys

def format_ERVs(ERV_list: dict,
                ERV_to_find: str,
                searched_ERV: str,
                my_species: str,
                count: int,
                include_groups: bool=True,
                print_others: bool=False,
                find_all: bool=False):
    
    """Takes in a file line and formats the ERV based on """
    
    my_match = re.search(REGEX_DICT[ERV_to_find],searched_ERV)

    match (include_groups,print_others,find_all):
        case (False, False, False): #we are only looking for the specified ERV_to_find
            if my_match is not None:
                if my_species not in ERV_list:
                    ERV_list[my_species] = count
                else:
                    ERV_list[my_species] += count

        case (True, False, False): #we want to print the groups, but we're only looking at ERV_to_find
            if my_species not in ERV_list:
                ERV_list[my_species] = [count, my_match.group(1)]
            else:
                ERV_list[my_species][0] += count

        case (True, True, False): #we want to have groups and group everything else in the file as "other"
            if my_match is not None:
                if my_species not in ERV_list:
                    ERV_list[my_species] = [count, my_match.group(1)]
                else:
                    ERV_list[my_species][0] += count
            else:
                if my_species not in ERV_list:
                    ERV_list[my_species] = [count, "other"]
                else:
                    ERV_list[my_species][0] += count

        case (True, True, True): #we want to find all patterns within REGEX_DICT, and label everything else as other
            for regex_match in REGEX_DICT:
                new_match = re.search(REGEX_DICT[regex_match],searched_ERV)
                if new_match is not None:
                    if my_species not in ERV_list:
                        #print("adding " + my_species + " to the dict with group " + new_match.group(1))
                        ERV_list[my_species] = [count, new_match.group(1)]
                        break
                    else:
                        #print("increasing " + my_species + " with group definition " + ERV_list[my_species][1])
                        ERV_list[my_species][0] += count
                        if ERV_list[my_species][1] != new_match.group(1):
                            ERV_list[my_species][1] = new_match.group(1)
                        break
                            #print("new group definition: " + ERV_list[my_species][1])
                else:
                    if my_species not in ERV_list:
                        #print("adding " + my_species + " to the dict with group other")
                        ERV_list[my_species] = [count, "other"]
                    else:
                        ERV_list[my_species][0] += count

        case (True, False, True): #we want to find all matches in REGEX_DICT but not print any others
            for regex_match in REGEX_DICT:
                new_match = re.search(REGEX_DICT[regex_match],searched_ERV)
                if new_match is not None:
                    if my_species not in ERV_list:
                        ERV_list[my_species] = [count, new_match.group(1)]
                        break
                    else:
                        ERV_list[my_species][0] += count
                        break
        
        case(False, False, True): #find all matches in REGEX_DICT but do not print groups or others
            for regex_match in REGEX_DICT:
                new_match = re.search(REGEX_DICT[regex_match],searched_ERV)
                if new_match is not None:
                    if my_species not in ERV_list:
                        ERV_list[my_species] = count
                        break
                    else:
                        ERV_list[my_species] += count
                        break

        case (False, True, True):
            print("just look at your original list, this would do the same thing.")

    return ERV_list


if __name__ == "__main__":
    filename = "PRJNA1238225_hashtable_min1.txt"
    output_filename = "PRJNA1238225_allspecies_ERV.txt"
    look_for = "LINE"

    include_groups = True
    print_others = False
    find_all = True
    REGEX_DICT = {"LINE":r"(L1)",
                "ERV":r"(ERV(?:K|L|1(?!\d)))"}

    ERV_list_d = {}

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            my_items = line.strip().split("\t")
            ERV = my_items[0]
            my_count = int(my_items[1])

            first_ERV = re.search(r"^[^ ]+",ERV).group(0)
            species = re.search(r"(.*?)\|",first_ERV).group(1)

            format_ERVs(ERV_list_d,look_for,first_ERV,species,my_count,
                        include_groups=True,
                        print_others=False,
                        find_all=True)

    f.close()

    with open(output_filename,"w",encoding="utf-8") as g:
        for keys,lists in ERV_list_d.items():
            if type(lists) != list:
                g.write(keys + "\t" + str(lists) + "\n")
            else:
                g.write(keys + "\t" + str(lists[0]) + "\t" + lists[1] + "\n") 
    g.close()
