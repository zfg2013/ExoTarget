import os
import sys
import argparse
import glob
import shutil
import re
from datetime import date



def combine_fasta(fasta_files):
    
    today = date.today().strftime("%m-%d-%y")
    combined_sequences = []
    
    for fasta_file in fasta_files:
        with open(fasta_file, 'r') as f:
            sequences = []
            for line in f:
                if line.startswith('>'):
                    continue
                else:
                    sequences.append(line.strip())
            combined_sequences.append('\n'.join(sequences))
    
    combined_file = "_".join([os.path.splitext(os.path.basename(file))[0] for file in fasta_files]) + '.fasta'
    
    with open(combined_file, 'w') as f:
        f.write(f'>{os.path.basename(combined_file)}\n')
        for i, sequence in enumerate(combined_sequences):
            if i ==0:
                f.write(sequence + ":")
            
            else:
                f.write(sequence)
    
    prot = os.path.basename(combined_file)[0:4]
    
    
    #porting over
    destination_directory = os.path.join(os.getcwd(), '..', 'Prepared', today, prot)
    os.makedirs(destination_directory, exist_ok=True)
    combined_file_path = os.path.join(os.getcwd(), combined_file)
    shutil.move(combined_file_path, destination_directory)
    
    
    
    #make the rest of the folders
    
    ###put try block later cause im lazy
    os.chdir('../..')
    script_dir = ('scripts/')
    
    folders = ['PNN','CF', 'CF','RFD', 'RFD', 'RFD', 'Amber', 'Amber']
    scripts = ['PNN.sh','CF_Prot.sh','CF_Complex.sh', 'CF_Screen.sh','RFD.sh', 'ProteinMPNN.sh', 'Amber.sh', 'video.sh']
    

    for folder, script in zip(folders, scripts):
        # Construct directory path for the new folder
        dir_path = os.path.join(destination_directory, folder)
    
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)
    
        # Construct source and destination script paths
        src_script_path = os.path.join(script_dir, script)
        dest_script_path = os.path.join(dir_path, script)
    
        # Copy the script file to the new directory
        shutil.copyfile(src_script_path, dest_script_path)
        
    #copy over peptide fasta to PNN and protein to CF
    peptide_file = f"{os.getcwd()}/Pipeline/Items/{fasta_files[0]}"
    protein_file =  f"{os.getcwd()}/Pipeline/Items/{fasta_files[1]}"
    shutil.copyfile(peptide_file, os.path.join(destination_directory, 'PNN', fasta_files[0]))
    shutil.copyfile(protein_file, os.path.join(destination_directory, 'CF', fasta_files[1]))
    
    #copy over the TopPep.py file over to RFD
    top_pep = f"{os.getcwd()}/TopPep.py"
    shutil.copyfile(top_pep, os.path.join(destination_directory, 'RFD', 'TopPep.py'))
    
    #copy over files to amber
    amber = f"{os.getcwd()}/AmberProtocol.py"
    shutil.copyfile(top_pep, os.path.join(destination_directory, 'Amber', 'AmberProtocol.py'))
    
    video = f"{os.getcwd()}/video.py"
    shutil.copyfile(top_pep, os.path.join(destination_directory, 'Amber', 'video.py'))
    
    print(f'Files and folders prepared for {prot} to apply the exosearch process')
    
   
                  

def main():
    parser = argparse.ArgumentParser(description='Combine two fasta files')
    parser.add_argument('--fasta_files', metavar='FASTA_FILE', nargs=2, help='input fasta files, first peptide then protein of interest')
    args = parser.parse_args()

    combine_fasta(args.fasta_files)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    