#!/usr/bin/env python3

"""Sort SRA files by PRJNA."""

import requests
import re
#re=regular expression

URL_search="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
URL_summary="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
experimentlist={}
#saying that experiment list is going to be a dictionary (filled with keys and values) for later

with open("HumanDRIPcSeqConfirmedSRRs.txt","r") as f:
    #r=read file
    for items in f.readlines():
    #instructions for each SRR in the read text file
        params={
        "api_key": "4099ac173f7c8032db1c0397a98781295c08",
        "db":"sra",
        #db=database, using sra database to pull samples
        "term":items.strip()}
        #items=SRR numbers in list, stripping the new line character at the end of each line

        response=requests.get(URL_search,params)
        #using esearch based on parameters (uuIDs for SRAs we are looking for)
        #esearch will use the SRR# and only output uuID
        a=str(response.content)
        #content for each SRR# will be given as a string rather than bytes
        uuId=re.search(r"<Id>(\d+)",a)
        #uuId=ID associated with each SRR#
        #search SRR content for all numbers following <Id> which will be the uuID and output as a string

        params_search={
        "api_key": "4099ac173f7c8032db1c0397a98781295c08",
        "db":"sra",
        "id":uuId.group(1)}
        #group(0)=<Id>#####, group 1=##### (just the uuID without the <Id> before it)

        response=requests.get(URL_summary,params_search)
        #using esummary based on parameters (PRJNAs for SRAs we are looking for)
        #esummary used uuID to find all the info about an experiment (name, PRJNA, protocol, etc.)
        b=str(response.content)
        #content for each uuID will be given as a string
        PRJNA=re.search(r"PRJNA\d+",b)
        #searching for PRJNA followed by numbers and outputting as a string
        
        p=PRJNA.group(0)
        if p in experimentlist.keys():
            #making experimentlist the dictionary of PRJNAs (keys) and SRRs (values) in that experiment
            experimentlist[p].append(items)
            #if a PRJNA is already in experimentlist dictionary (all SRRs after first SRR for that PRJNA), add SRR to the value list rather than overwriting the one(s) already in there
        else:
            experimentlist[p]=[items]
            #if PRJNA isn't in experimentlist dictionary already (first time an SRR matches a PRJNA), make a new key value pairing
            #list items in value (SRR numbers) as a [list]
    for keys,values in experimentlist.items():
        #print(keys+": "+str(values)+"\n")
        title=keys+".txt"
        #.txt file name with list of SRRs in that experiment will be PRJNA###(key).txt
        with open(title,"w") as g:
            #open PRJNA###.txt file we just made
            #"w"=write (write over anything that is in .txt file which in this case is blank)
            for SRRs in values:
                g.write(SRRs.strip()+" \\"+"\n")
                #for each SRR#, write the SRR number without the new line character and add a space + \ (so the shell script can read them separately) + new line
                #have to do two \\ because \ is an escape key but we want a literal \ so it needs to escape itself
        g.close()
f.close()