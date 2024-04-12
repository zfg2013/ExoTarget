#!/bin/sh
#SBATCH --account=kgraim
#SBATCH --qos=kgraim
#SBATCH --job-name=cfs
#SBATCH --nodes=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zfg2013@ufl.edu
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --distribution=cyclic:cyclic
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16gb
#SBATCH --time=24:00:00 
pwd; hostname; date

#modules
module purge
ml conda
conda activate SE3nv-cuda118
ml gcc/12.2.0

python video.py