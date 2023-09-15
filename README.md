# Welcome to ExoSearch
ExoSearch is a consensus peptide modelling program used to find peptides-specific ligands for protein targeting and modification. Particularly, peptides obtained in this pipeline are used to modify the surface of extracellular vesicles, enabling precision drug delivery. ExoSearch uses Colabfold & HDOCK to initially predict the peptide-protein pose, then AMBER is applied to dynamically refine the binding energetics and investigate the expected peptide folding interactions. 

## Installing ExoSearch
ExoSearch is developed through SLURM on the University of Florida's cluster (HPG). To install ExoSearch, clone this repository, then follow the next step to install colabfold into the directory. 

## Local colabfold installation on HiperGator
1. Download `install_colabbatch_linux.sh` from this repository:<pre>$ wget https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/install_colabbatch_linux.sh</pre> and run it in the directory where you want to install:<pre>$ bash install_colabbatch_linux.sh</pre>About 5 minutes later, `colabfold_batch` directory will be created. Do not move this directory after the installation.
2. Rename colabfold_batch to to localcolabfold

## Applying ExoSearch
1. Open Peptide_Pipeline.ipynb
2. Modify the input files as necessary
3. Run the notebook
4. Your predictions will be in Output
