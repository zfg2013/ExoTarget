#!/bin/bash
#SBATCH --account=kgraim
#SBATCH --qos=kgraim
#SBATCH --job-name=HDOCK
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zfg2013@ufl.edu
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=2
#SBATCH --mem=48gb
#SBATCH --time=96:00:00
date;hostname;pwd

#modules
module purge 
module load intel/2019.1.144 openmpi/4.0.1 fftw/3.3.8

#paths
export PATH="/blue/kgraim/zfg2013/HDOCKlite-v1.1/:$PATH"
export PATH="/blue/kgraim/zfg2013/Input/HDOCK:$PATH"

# Sort files by name
receptors=$(ls *rec*.pdb | sort | sed -n "${SLURM_ARRAY_TASK_ID}p")
ligands=$(ls *lig*.pdb | sort | sed -n "${SLURM_ARRAY_TASK_ID}p")

# Extract name from receptor file path
name=${SLURM_ARRAY_TASK_ID}



# Run hdock with the obtained files
hdock "$receptors" "$ligands" -out "$name".out
createpl "$name".out "${name}_top1.pdb" -nmax 1 -complex -models
cp "model_1.pdb" "model_${SLURM_ARRAY_TASK_ID}.pdb"
mv "model_${SLURM_ARRAY_TASK_ID}.pdb" "Output/model_${SLURM_ARRAY_TASK_ID}.pdb"

exit 0