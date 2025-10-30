import re

familylist={}
#saying that experiment list is going to be a dictionary (filled with keys and values) for later

with open('PRJNA1238225_hashtable_min1.txt','r') as g:
    #open tab delimited count table as g and read
    for items in g.readlines():
        #for each item in g, read and do the following:
        ERV = items.split('\t')
        #make sure it reads the file as a list and not a string so they can be indexed
        name = ERV[0]
        #0 index is name of ERV
        print(name)
        count = int(ERV[1])
        #1 index is count of ERV
        family = re.search(r"\|([^ |\n]+)",name)
        #searching for just the family
        if family.group(1) in familylist.keys():
            #making experimentlist the dictionary of ERVs (keys) and count (values) in that experiment
            familylist[family.group(1)] += count
            #if a ERV is already in experimentlist dictionary, add 1 to whatever number is in there
        else:
            familylist[family.group(1)] = count
            #if ERV isn't in experimentlist dictionary already, make a new key value pairing

for keys,values in familylist.items():
    print(keys + '\t' + str(values) +'\n')

# title = 'PRJNA1238225_familycount.txt'
# #making a new txt file that includes the ERVs and how many times they showed up
# with open(title,'w') as f:
#     for keys,values in experimentlist.items():
#         #open the file we just made and write in it
#         f.write(keys + '\t' + str(values) +'\n')
#         #write keys (ERV) space the counts (numbers need to be listed as a string because you can't add strings and ints)

