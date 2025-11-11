#!/bin/sh

#SBATCH --nodes=1
#SBATCH --qos=normal
#SBATCH --partition=amilan
#SBATCH --time=10:00:00
#SBATCH --mem=1G
#SBATCH --ntasks=1
#SBATCH --account=amc-general
#SBATCH --array=1-17
#SBATCH --job-name=SamtoBam
#SBATCH --output=SamtoBam_%J.out
#SBATCH --mail-user=alden.paine@cuanschutz.edu
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

module load samtools
module load python/3.10.2

python3 SamtoBamFiles.py /scratch/alpine/apaine@xsede.org/SamFiles/Locus/TagDirectory/MySamFiles.txt $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_COUNT