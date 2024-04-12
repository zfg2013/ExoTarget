#!/bin/sh
#SBATCH --account=kgraim
#SBATCH --qos=kgraim
#SBATCH --job-name=test
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zfg2013@ufl.edu
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:4
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=4
#SBATCH --mem=80gb
#SBATCH --time=00:30:00
pwd; hostname; date

module purge
ml conda
conda activate SE3nv-cuda118


#LOOK IN THE DESIGN FOLDER
design=$(ls "design"/*.pdb)


mkdir -p ${PWD}/"fastas/"
output=${PWD}/"fastas/"

python ../../../../../RFdiffusion/pipeline_prot.py --pdb ${design} --directory ${output)

exit 0
