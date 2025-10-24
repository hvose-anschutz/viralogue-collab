ERVlist = []
#empty ERV list

with open('Hsap38_ERV.gtf','r') as g:
    #open gtf file and read as g
    for items in g.readlines():
        info = items.strip().split('\t')
        #need to split at the tab (because there are spaces) splitting adds a new line character at the end so we want to strip that
        n = info[15]
        #ERV name
        c = info[1]
        #chromosome
        f = info[2]
        #first coordinate
        l = info[3]
        #last coordinate
        ERVlist.append(str(n) + '\t' + str(c) + '\t' + str(f) + '\t' + str(l) + '\n')
        #add the name, chromosome, and coordinates to the list
g.close()

file = 'Hsap38_ERV_Coordinates.txt'
#make a new file for the info
with open(file, 'w') as h:
    for coordinates in ERVlist:
        h.write(coordinates)
        #add everything in the list to our new file
h.close()