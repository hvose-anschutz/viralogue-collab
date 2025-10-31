experimentlist={}
#saying that experiment list is going to be a dictionary (filled with keys and values) for later

ERVlist=[]
#making an empty ERV list

with open('PRJNA1181856_CountTableCopy.txt','r') as g:
    #open tab delimited count table as g and read
    for items in g.readlines():
        #for each item in g, read and do the following:
        ERV = items.strip().split('\t')
        #defining ERV as stripping the end of line new line characters and splitting at the tabs so everything in the file is in a comma separated list
        if float(ERV[81]) > 1:
            #this index is the average column, we only want ERVs included in the count if their average expression score across the experiment is above whatever float we indicate
            ERVlist.append(ERV[0])
            #the 0 index is the ERV Reference column, we want to append the ERVlist to include just the ERVs (ERV[0])

for p in ERVlist:
    if p in experimentlist.keys():
        #making experimentlist the dictionary of ERVs (keys) and count (values) in that experiment
        experimentlist[p]+=1
        #if a ERV is already in experimentlist dictionary, add 1 to whatever number is in there
    else:
        experimentlist[p]=1
        #if ERV isn't in experimentlist dictionary already, make a new key value pairing
title = 'PRJNA1181856_ERVcount_min1.txt'
#making a new txt file that includes the ERVs and how many times they showed up
with open(title,'w') as f:
    for keys,values in experimentlist.items():
        #open the file we just made and write in it
        f.write(keys + '\t' + str(values) +'\n')
        #write keys (ERV) space the counts (numbers need to be listed as a string because you can't add strings and ints)

