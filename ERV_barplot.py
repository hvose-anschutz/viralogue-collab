#!/usr/bin/env python3

"""Makes a barplot of ERV family and species."""

import re
import sys
import pandas as pd
import matplotlib.pyplot as plt

def find_erv(filename: str, mode: str|None=None, preformatted: bool=False) -> dict: 

    """Finds corresponding ERVs within a file. If the ERV groupings have
    been provided, the preformatted parameter can be adjusted to reflect 
    this, and no regex search will be performed."""

    my_erv_species = {}
    my_names = []

    if not preformatted:
        if mode == "LINE":
            my_regex = r"^L1"
            df_dict = {"Name":["LINE"]}
        elif mode == "ERV":
            my_regex = r"ERV(1\D|L|K)"
            df_dict = {"Name":["ERV"]}
        else:
            print("valid options are LINE or ERV when not preformatted.")
            sys.exit(1)

    with open(filename,"r",encoding="utf-8") as f:
        for my_values in f:
            line = my_values.strip().split("\t")
            if not preformatted:
                match_erv = re.search(my_regex,line[0])
                if match_erv is not None:
                    if line[0] not in my_erv_species:
                        my_erv_species[line[0]] = int(line[1])
                    else:
                        my_erv_species[line[0]] += int(line[1])
            else:
                my_erv_species[line[0]] = int(line[1])
                my_names.append(line[2])
    f.close()

    if preformatted:
        df_dict = {"Name":list(set(my_names))}

    total_ervs = sum(my_erv_species.values())

    for erv in my_erv_species:
        df_dict[erv] = my_erv_species[erv] / total_ervs


    return df_dict

###############################################################
# CHANGE THIS CODE

erv_list = "PRJNA1238225_allspecies_ERV.txt"
outfile = "my_stacked_barplot.svg"
subset = ["L1"]
save_figure = True
###############################################################

if __name__ == "__main__":

    my_df_dict = find_erv(erv_list,preformatted=True)

    read_df = pd.read_table(erv_list,names=["ERV","count","ERV Family"])

    print(read_df.head())

    df = pd.DataFrame(my_df_dict,)

    sub_df = df[df["Name"] == "L1"]

    df_pivot = sub_df.pivot_table(index="Name",values=my_df_dict.keys(),aggfunc=sum)

    print(df_pivot.head())

    my_plot = df_pivot.plot(kind="bar",stacked=True,grid=True)
    my_plot.set_axisbelow(True)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.title('ERV Species')
    plt.ylabel('Percentage of ERVs')
    plt.xticks(rotation=0)
    if save_figure:
        plt.savefig(outfile, bbox_inches='tight')
    plt.show()
