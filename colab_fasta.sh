#!/bin/sh
#SBATCH --account=kgraim
#SBATCH --qos=kgraim
#SBATCH --job-name=colab_fold
#SBATCH --nodes=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zfg2013@ufl.edu
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --distribution=cyclic:cyclic
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=2
#SBATCH --mem=48gb
#SBATCH --time=24:00:00 
pwd; hostname; date


#switch to the input directory
cd "Input"
input_file="*.fasta"


#for fasta files
file=$(ls *.fasta | sed -n ${SLURM_ARRAY_TASK_ID}p)
name=${file:0:9}


#purge all modules & load everything
module purge
module load cuda/11.4.3
module load gcc/12.2.0
pip3 install tensorflow --upgrade

#set paths
export PATH="//blue/kgraim/zfg2013/localcolabfold/colabfold-conda/bin:$PATH"
export PATH="//blue/kgraim/zfg2013/Input:$PATH"
LaunchDir=$PWD

#make an outfiles directory
COLABFOLD_DIR="//blue/kgraim/"$USER"/COLAB_OUTFILES"
mkdir -p "$COLABFOLD_DIR"

colabfold_batch --templates --num-models=3 --use-gpu-relax --num-recycle=15 --amber $file $COLABFOLD_DIR/$name/