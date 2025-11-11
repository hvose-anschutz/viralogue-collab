#!/usr/bin/env python3

"""A test of the multiprocessing library for speeding
up the reading of 33 million lines."""

import time
from multiprocessing import Pool, cpu_count

def process_line(line):
    currentline = line.split()
        # split strings to turn into a list
    if (len(currentline) > 3) and (currentline[0][0] != "@"):
            # we want to ignore the header lines which have a length of 2-3
        rc = currentline[2]
        # read chromosome number
        rf = currentline[3]
        # read first coordinate
        rl = currentline[7]
        # read last coordinate
        try:
            coordinate_list = ALL_COORDINATES[rc]
            for sub_list in coordinate_list:
                # needs to be on same chromosome
                if int(rf) >= sub_list[0]:
                    # needs to be on or after the first coordinate
                    if int(rl) <= sub_list[1]:
                        return sub_list[2] + "\t" + str(rc) + "\t" + str(rf) + "\t" + str(rl) + "\t" + str(currentline[9])
        except KeyError as e:
            return
    return

def process_file(filename:str, output_filename: str, start: float):
    results = []
    with open(filename, "r", encoding="utf-8") as foo:
        with Pool(cpu_count()) as pool:
            for result in pool.imap(process_line,foo,chunksize=1000):
                if result is not None:
                    results.append(result)
                if len(results) % 10000 == 0:
                    print(f"stored {len(results)} items at time {time.time()-start}")

    with open(output_filename, 'w', encoding='utf-8') as out:
        out.write('\n'.join(results))
    out.close()

if __name__ == "__main__":
    #initialize the hashtable
    ALL_COORDINATES = {}
    START_TIME = time.time()
    title = "SRR32782394_CodingRegionList.txt"

    with open("Mmus38_ERV_Coordinates.txt", "r") as h:
        for idx, lines in enumerate(h):
            coordinates = lines.split("\t")
            # make sure it reads the file as a list and not a string so they can be indexed
            c = "chr" + coordinates[1]
            # ERV chromosome number
            f = coordinates[2]
            # ERV first coordinate
            l = coordinates[3]
            # ERV last coordinate
            e = coordinates[0]
            # ERV name
            
            if c in ALL_COORDINATES:
                ALL_COORDINATES[c].append([int(f),int(l),e])
            else:
                ALL_COORDINATES[c] = [[int(f),int(l),e]]

    h.close()

    process_file("SRR32782394.Strict.mapped_to_mm10Aligned.sam",title,START_TIME)



