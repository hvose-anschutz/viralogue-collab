#!/usr/bin/env python3

"""Make alignment (.sam) files against a genome for 
fastq files that are single end rather than paired end."""

import re
import subprocess
import sys

gDir = '/projects/apaine@xsede.org/Genomes/hg38'
#genome directory path
cOutput = '/scratch/alpine/apaine@xsede.org/SamFiles/Locus/'
#output directory path

arg=sys.argv[1]
#argv[0]=script, argv[1]=first argument (script name) in command line
id=int(sys.argv[2])-1
#task ID in command line, -1 because python indexes from 0 but we are counting from 1
total=int(sys.argv[3])
#task count in command line

print(id)
#this will tell us which id in case one fails and we need to troubleshoot
with open(arg,'r') as f:
#arg is file name given from command line (so we don't have to edit script every time)
    for idx,items in enumerate(f.readlines()):
        #for each SRR in the .txt files, read the lines and perform these commands:
        if idx%total==id:
            #this is how the computer assigns which sample is processed by which job (since we want to run all at the same time)
            print(items)
            #this will tell us which SRR# for troubleshooting purposes
            srr=re.search(r"SRR\d+",items)
            #search in items (list of SRRs) for SRR and any digits after it (just the SRR# without the .fastq)
            b=cOutput + srr.group(0)+'.Strict.mapped_to_hg38'
            sample='/scratch/alpine/apaine@xsede.org/sra/' + items.strip()
            A=['STAR','--runMode','alignReads','--runThreadN','16','--genomeDir',gDir,'--outFilterMultimapNmax','1','--readFilesIn',sample,'--outFileNamePrefix',b]
            #want the output file to be in the locus directory with the name of each SRR and Strict.mapped_to_hg38
            #python needs the commands to be in list format for the command line
            print(A)
            try: 
                result=subprocess.run(A,check=True,capture_output=True,text=True)
                #make sure command works and can output, output as a text string
            except subprocess.CalledProcessError as e:
            #tell me any errors (e) we run into
                print(f"star failed with error code {e.returncode}")
                print(e.stderr)
                #standard error
                print(e.stdout)
                #standard output
            except FileNotFoundError:
                print("star not found")
                #couldn't find STAR program to run (not installed)
f.close