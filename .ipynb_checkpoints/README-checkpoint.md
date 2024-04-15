# Welcome to ExoTarget
ExoTarget is an automated platform used to find peptides-specific ligands for protein targeting and modification. Particularly, peptides obtained in this pipeline are used to modify the surface of extracellular vesicles, enabling precision drug delivery. When given a peptide protein pair, ExoTarget will search for targetable domains with ColabFold & PepNN, design new peptides using RFD & ProteinMPNN, then validate paired interactions with 10 nanosecond MD simulations using OpenMM. We cross-validate the predicted protein target with HDOCK (more to come) using the ExoTarget Class API.   


# Graphical Summary 



# Installing ExoTarget
ExoTarget is developed through SLURM on the University of Florida's cluster (HPG). To install ExoTarget, clone this repository, then follow the next steps to install ExoTarget onto your cluster.

## Install the kernels

## Colabfold installation 
1. Download `install_colabbatch_linux.sh` from this repository:<pre>$ wget https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/install_colabbatch_linux.sh</pre> and run it in the directory where you want to install:<pre>$ bash install_colabbatch_linux.sh</pre>About 5 minutes later, `colabfold_batch` directory will be created. Do not move this directory after the installation.

2. Rename colabfold_batch to to localcolabfold


## PepNN installation
1. Inside of the ExoTarget repo, type the following code: <pre>$ git clone https://gitlab.com/oabdin/pepnn.git </pre>
2. change directories by typing <pre> cd pepnn </pre>. then run git lfs pull 
3. After, type <pre> pip install. </pre>


## RFD installation
1. Inside of the ExoTarget repo, type the following code: <pre>$ git clone https://github.com/RosettaCommons/RFdiffusion.git </pre>
2. Next, download the weights by typing <pre> cd RFdiffusion </pre> then <pre> mkdir models && cd models </pre> then the following block:
<pre>
wget http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/60f09a193fb5e5ccdc4980417708dbab/Complex_Fold_base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/74f51cfb8b440f50d70878e05361d8f0/InpaintSeq_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/76d00716416567174cdb7ca96e208296/InpaintSeq_Fold_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/5532d2e1f3a4738decd58b19d633b3c3/ActiveSite_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/12fc204edeae5b57713c5ad7dcb97d39/Base_epoch8_ckpt.pt
</pre>

3. After, activate the SE3nv-cuda118 kernel. Then, go into RFdiffusion/env/SE3transformer
4. Move the SE3nv.yml from the ExoTarget repo into this folder. Overwrite. 
5. type the following <pre> pip install --no-cache-dir -r requirements.txt </pre>
6. then type <pre> python setup.py install </pre>
7. go back to the root of the RFdiffusion repo and type <pre> pip install -e . </pre>
8. Move RFDenovo 

## ProteinMPNN installation
1. Inside of the ExoTarget repo, type the following code: <pre> https://github.com/sokrypton/ColabDesign/tree/main </pre>
2. Next, activate the SE3nv-cuda118 kernel. Type <pre> python setup.py install </pre>


## Unit test
needs a unit test / deployment script. 

# How to use

The following sections detail how to use the ExoTarget platform

## Input requirements

ExoTarget will only need two fasta files, an input protein and peptide pair. These files should be in fasta format, and placed within Pipeline/Items. The user will type <pre> python preparer.py --fasta_files {peptide} {protein} </pre>. See python preparer.py -h for more info.

## Automated design

The master scripts will be pulled into each protein-peptide pair within Pipeline/Prepared/(today's day)/, sorted by the peptide's first 3 characters. In each folder, users will need to edit their SLURM config in the master scripts folder appropriately (1 gpu requirement) before using sbatch. 

## Recommended workflow
After providing the peptide-protein pair, the recommended workflow is as follows:

1. cd into /CF/ ; then execute CF_Prot.sh to generate a predicted PDB structure. Move the top ranked PDB structure into the directory <pre> cp $(ls "CF/AF_PROT/*_rank_001_"*.pdb) ../$(ls "CF/AF_PROT/*_rank_001_"*.pdb) </pre>

2. cd into /PNN/ ; then execute PNN.sh

3. Next go inside /CF/ and execute CF_Complex.sh

4. Check the results of PNN and CF_Complex to see if they agree with each other before moving onto generating peptides by RFD

6. go inside /RFD/ and edit the RFD.sh file appropriately including length of protein, hotspots, and number of designs requested.

7. After executing, go inside Outputs/designs and move/delete all other designs than the target one. ONLY 1 PDB file should exist in this directory. 

8. Go back to /RFD/ and execute ProteinMPNN.sh

9. Afterward, execute CF_Screen.sh

10. After completion, execute TopPep.py 

11. Move the top 20 pdb structures to the amber folder to complete the AMBER analysis (TO:DO automate this later).