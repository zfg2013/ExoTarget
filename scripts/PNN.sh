#!/bin/sh
#SBATCH --account=kgraim
#SBATCH --qos=kgraim
#SBATCH --job-name=colabfold
#SBATCH --nodes=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zfg2013@ufl.edu
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --distribution=cyclic:cyclic
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=2
#SBATCH --mem=15gb
#SBATCH --time=24:00:00 
pwd; hostname; date

conda activate pepnn

#get the protein of interest in the prepared folder
prot=$(ls "../"*.pdb)

#get the peptide of interest 
fasta=$(ls *.fasta)

python ../../../../../pepnn/pepnn_struct/scripts/predict_binding_site.py -prot ${prot} -pep ${fasta} -c A