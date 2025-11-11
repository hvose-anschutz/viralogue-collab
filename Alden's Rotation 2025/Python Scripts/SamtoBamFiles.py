import re
import subprocess
import sys

cOutput = '/scratch/alpine/apaine@xsede.org/SamFiles/Locus/TagDirectory/BamFiles/'
#output directory path

arg=sys.argv[1]
#argv[0]=script, argv[1]=first argument (file name) in command line
id=int(sys.argv[2])-1
#task ID in command line, -1 because python indexes from 0 but we are counting from 1
total=int(sys.argv[3])
#task count in command line

print(id)
#this will tell us which id in case one fails and we need to troubleshoot
with open(arg,'r') as f:
#arg is file name given from command line (so we don't have to edit script every time)
    for idx,items in enumerate(f.readlines()):
        #for each sam in the .txt files, read the lines and perform these commands:
        if idx%total==id:
            #this is how the computer assigns which sample is processed by which job (since we want to run all at the same time)
            print(items)
            #this will tell us which sam# for troubleshooting purposes
            sam=re.search(r"(.+)\.out\.sam",items)
            #search in items (list of sams) for characters before .out.sam
            #group0: whole .sam file name
            #group1: file name before .out.sam
            a=sam.group(0)
            b=cOutput + sam.group(1)+'.bam'
            A=['samtools','sort',a,'-o',b]
            #want the output file to be in the locus directory with the name of each SRR and Strict.mapped_to_mm10
            #python needs the commands to be in list format for the command line
            print(A)
            try: 
                result=subprocess.run(A,check=True,capture_output=True,text=True)
                #make sure command works and can output, output as a text string
            except subprocess.CalledProcessError as e:
            #tell me any errors (e) we run into
                print(f"samtools failed with error code {e.returncode}")
                print(e.stderr)
                #standard error
                print(e.stdout)
                #standard output
            except FileNotFoundError:
                print("samtools not found")
                #couldn't find samtools program to run (not installed)
f.close