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

#switch to the input directory
input_file=$(ls "../RFD"/*.fasta)

templates="AF_PROT/*_env/templates*/"
hit=$(ls "AF_PROT"/*_env/*.m8)

#purge all modules & load everything
module purge
ml conda
conda activate /blue/kgraim/zfg2013/localcolabfold/colabfold-conda
ml cuda/12.2.2 gcc/12.2.0 


#set paths
export PATH="/blue/kgraim/zfg2013/localcolabfold/colabfold-conda/bin:$PATH"
LaunchDir=$PWD


colabfold_batch --template --local-pdb-path ${templates} --pdb-hit-file ${hit} --num-models 3 --use-gpu-relax --num-recycle 15 --num-ensemble 3 --random-seed 1235892 --relax-max-iterations 4000 --amber --recycle-early-stop-tolerance 0 $input_file $LaunchDir/"AF_Screen"
