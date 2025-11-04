import re

title = 'SRR32782394_CodingRegionList.txt'
#making an output file for the coding region
with open('Mmus38_ERV_Coordinates.txt','r') as h, open(title,'w') as o:
    for lines in h.readlines():
        coordinates=lines.split('\t')
        #make sure it reads the file as a list and not a string so they can be indexed
        c = coordinates[1]
        #ERV chromosome number
        f = coordinates[2]
        #ERV first coordinate
        l = coordinates[3]
        #ERV last coordinate
        e = coordinates[0]
        #ERV name
        with open('SRR32782394.Strict.mapped_to_mm10Aligned.sam','r') as s:
            for reads in s:
                currentline = reads.split()
                #split strings to turn into a list
                if len(currentline) > 3:
                #we want to ignore the header lines which have a length of 2-3
                    rc = currentline[2]
                    #read chromosome number
                    rf = currentline[3]
                    #read first coordinate
                    rl = currentline[7]
                    #read last coordinate
                    if rc == c:
                    #needs to be on same chromosome
                        if int(rf) >= int(f):
                            #needs to be on or after the first coordinate
                            if int(rl) <= int(l):
                                #needs to be on or before the last coordinate
                                o.write(str(e) + '\t' + str(rc) + '\t' + str(rf) + '\t'+ str(rl) + '\t' + str(currentline[9]) + '\n')
                                #write ERV name tab chromosome number tab first coordinate tab last coordinate tab sequence
        s.close 
o.close
h.close