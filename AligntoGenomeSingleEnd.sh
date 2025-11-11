#!/bin/sh

#SBATCH --nodes=1
#SBATCH --qos=normal
#SBATCH --partition=amilan
#SBATCH --time=06:00:00
#SBATCH --mem=48G
#SBATCH --ntasks=16
#SBATCH --account=amc-general
#SBATCH --array=1-31
#SBATCH --job-name=SingleEndAlignToGenome
#SBATCH --output=SingleEndAlignToGenome_%J.out
#SBATCH --mail-user=alden.paine@cuanschutz.edu
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

echo "Loading Apps:"
module load star/2.7.10b
module load python/3.10.2

python3 SingleEndAlignment.py /scratch/alpine/apaine@xsede.org/sra/HumanSingleEndDRIPc.txt $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_COUNT