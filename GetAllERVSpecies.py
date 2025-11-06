#!/usr/bin/env python3

"""Returns all valid family and species of
ERV based on a specified pattern."""

import re
import sys

filename = "PRJNA1238225_hashtable_min1.txt"
output_filename = "PRJNA1238225_allspecies_ERV.txt"
look_for = "ERV"

regex_dict = {"LINE":r"(L1)",
              "ERV":r"(ERV[1LK])[^\d]"}

include_groups = True
print_others = False

ERV_list = {}

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        my_items = line.strip().split("\t")
        ERV = my_items[0]
        count = int(my_items[1])

        first_ERV = re.search(r"^[^ ]+",ERV).group(0)

        try:
            my_match = re.search(regex_dict[look_for],first_ERV)
            if my_match is not None:
                my_species = re.search(r"(.*?)\|",first_ERV)
                if my_species.group(1) not in ERV_list:
                    if include_groups:
                        ERV_list[my_species.group(1)] = [count, my_match.group(1)]
                    else:
                        ERV_list[my_species.group(1)] = count
                else:
                    if include_groups:
                        ERV_list[my_species.group(1)][0] += count
                    else:
                        ERV_list[my_species.group(1)] += count
        except KeyError as e:
            print("Valid options are LINE or ERV for look_for parameter.")
            sys.exit(1)
f.close()

with open(output_filename,"w",encoding="utf-8") as g:
    for keys,list in ERV_list.items():
        g.write(keys + "\t" + str(list[0]) + "\t" + list[1] + "\n")
g.close()


