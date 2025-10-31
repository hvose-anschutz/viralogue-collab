import re

specieslist={}
#saying that specieslist is going to be a dictionary (filled with keys and values) for later

with open('SRR32782394_ERVcount_min1.txt','r') as g:
    #open tab delimited hash table as g and read
    for items in g.readlines():
        #for each item in g, read and do the following:
        ERV = items.split('\t')
        #make sure it reads the file as a list and not a string so they can be indexed
        name = ERV[0]
        #0 index is name of ERV
        count = int(ERV[1])
        #1 index is integer of count of ERV
        family = re.search(r"(.*?)\|",name)
        #search in name for just the family, we want everything after the | and before a space or new line character
        if family.group(1) in specieslist.keys():
            #making familylist the dictionary of ERVs (keys) and count (values) in that experiment
            specieslist[family.group(1)] += count
            #group 1 is just the family, if family name is already in familylist dictionary, add new count to existing count
        else:
            specieslist[family.group(1)] = count
            #if family name isn't in specieslist dictionary already, make a new key value pairing with its count

title = 'SRR32782394_speciescount.txt'
#making a new txt file that includes the ERV families and how many times they showed up
with open(title,'w') as f:
    for keys,values in specieslist.items():
        #open the file we just made and write in it
        f.write(keys + '\t' + str(values) +'\n')
        #write keys (ERV species) space the counts (numbers need to be listed as a string because you can't add strings and ints)

