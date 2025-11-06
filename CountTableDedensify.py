#!/usr/bin/env python3

"""A test of the multiprocessing library for speeding
up the reading of 33 million lines."""

import time
from multiprocessing import Pool, cpu_count
from functools import partial

def process_line(coords: dict, line: str):
    currentline = line.split()
        # split strings to turn into a list
    rc = currentline[1]
    # read chromosome number
    rf = currentline[2]
    # read first coordinate
    rl = currentline[3]
    # read last coordinate
    try:
        coordinate_list = coords[rc]
        for sub_list in coordinate_list:
            # needs to be on same chromosome
            if int(rf) >= sub_list[0]:
                # needs to be on or after the first coordinate
                if int(rl) <= sub_list[1]:
                    my_key = rc + ":" + str(sub_list[0]) + "-" + str(sub_list[1])
                    return [my_key, sub_list[2]]
    except KeyError as e:
        return
    return

def process_file(filename:str, output_filename: str, start: float, worker: partial):
    results = {}
    with open(filename, "r", encoding="utf-8") as foo:
        with Pool(cpu_count()) as pool:
            for result in pool.imap(worker,foo,chunksize=1000):
                if (result is not None) and (result[1] > 0):
                    results[result[0]] = result[1]
                if len(results) % 10000 == 0:
                    print(f"stored {len(results)} items at time {time.time()-start}")
    
    with open ("PRJNA1238225_CountTable.txt", "r") as f, open(title, "w") as o:
        for lines in f:
            countline = lines.split("\t")
            checkkey = countline[2] + ":" + countline[3] + "-" + countline[4]
            if checkkey in results:
                o.write(lines)
    f.close
    o.close


if __name__ == "__main__":
    #initialize the hashtable
    ALL_COORDINATES = {}
    START_TIME = time.time()
    title = "SRR32782394_CodingCountTable.txt"

    with open("PRJNA1238225_CountTable.txt", "r") as h:
        for idx, lines in enumerate(h):
            coordinates = lines.split("\t")
            # make sure it reads the file as a list and not a string so they can be indexed
            c = coordinates[2]
            # ERV chromosome number
            f = coordinates[3]
            # ERV first coordinate
            l = coordinates[4]
            # ERV last coordinate
            e = coordinates[9]
            # expression level of sample
            
            if c in ALL_COORDINATES:
                ALL_COORDINATES[c].append([int(f),int(l),float(e)])
            else:
                ALL_COORDINATES[c] = [[int(f),int(l),float(e)]]

    h.close()

    worker_function = partial(process_line, ALL_COORDINATES)

    process_file("SRR32782394_CodingRegionList.txt",title,START_TIME, worker_function)



