import re

title = 'SRR13479241_DistPlot.txt'
#making an output file for the distributionplot
with open('Hsap38_ERV_Coordinates.txt','r') as h, open(title,'w') as o:
    for lines in h.readlines():
        coordinates=lines.split('\t')
        #print(coordinates[1])
        #make sure it reads the file as a list and not a string so they can be indexed
        c = coordinates[1]
        #ERV chromosome number
        #if re.search('chr\d',lines) is not None:
            #print(str(c) + str(coordinates))
        #x = re.search("chr([\d+|X|Y])",c).group(1)
        f = coordinates[2]
        #ERV first coordinate
        l = coordinates[3]
        #ERV last coordinate
        e = coordinates[0]
        #ERV name
        with open('SRR13479241.Strict.mapped_to_hg38Aligned.out.sam','r') as s:
            for reads in s:
                # print(c)
                # print(f)
                # print(l)
                currentline = reads.split()
                #split strings to turn into a list
                if len(currentline) > 3:
                    #print(currentline)
                #we want to ignore the header lines which have a length of 2-3
                    rc = currentline[2]
                    #read chromosome number
                    rf = currentline[3]
                    #read first coordinate
                    rl = currentline[7]
                    #read last coordinate
                    #print(c + '\t' + rc)
                    if rc == c:
                    #needs to be on same chromosome
                        #print(c+'\t'+rc+lines)
                        if int(rf) >= int(f):
                            #needs to be on or after the first coordinate
                            #print(f+'\t'+rf+lines)
                            if int(rl) <= int(l):
                                #needs to be on or before the last coordinate
                                print(l+'\t'+rl+lines)
                                o.write(str(e) + '\t' + str(rc) + '\t' + str(rf) + '\t'+ str(rl) + '\t' + str(currentline[9]) + '\n')
                                #write ERV name tab chromosome number tab first coordinate tab last coordinate tab sequence
        s.close 
o.close
h.close