#!/bin/sh
#SBATCH --account=kgraim
#SBATCH --qos=kgraim-b
#SBATCH --job-name=ORCA
#SBATCH --ntasks=15
#SBATCH --nodes=1
#SBATCH --distribution=cyclic:cyclic
#SBATCH --mem-per-cpu=6000mb
#SBATCH --time=6:00:00
#SBATCH --array=1-1540
pwd; hostname; date


#For all files in the directory
file=$(ls *.inp | sed -n ${SLURM_ARRAY_TASK_ID}p)
name=${file:0:9}

#set OPENMPI paths here 
export PATH="/blue/kgraim/bryanjatkinson/ORCA_and_OpenMPI/bin:$PATH" 
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/blue/kgraim/bryanjatkinson/ORCA_and_OpenMPI/lib" 
export ORCA_DIR=//home/zfg2013/ORCA/
export PATH=$PATH:$ORCA_DIR
LaunchDir=$PWD


#Start ORCA
/blue/kgraim/bryanjatkinson/ORCA_and_OpenMPI/orca/orca $file 

exit 0
