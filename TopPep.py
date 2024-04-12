#libaries
import os
import sys
import glob
import pandas as pd
import numpy as np
from datetime import date
import shutil
import json
import re



#first task, delete everything that is not the top rank within the folder

#change into folder based on today's date
today = date.today().strftime("%m-%d-%y")

#os.chdir(f'Input/{today}/files/AF_{today}')
os.chdir(f'Input/04-11-24/files/AF_04-11-24')

         
#next, find all the junk files
junk_folders = (
    glob.glob(os.path.join(os.getcwd(), '*_env'))
    + glob.glob(os.path.join(os.getcwd(), '*_pairgreedy'))
    + glob.glob(os.path.join(os.getcwd(), '*.a3m'))
    + glob.glob(os.path.join(os.getcwd(), '*.done.txt'))
    + glob.glob(os.path.join(os.getcwd(), '*_predicted_aligned_error_v1.json'))
    + glob.glob(os.path.join(os.getcwd(), '*_rank_002_*.pdb'))
    + glob.glob(os.path.join(os.getcwd(), '*_rank_002_*.json'))
    + glob.glob(os.path.join(os.getcwd(), '*_rank_003_*.pdb'))
    + glob.glob(os.path.join(os.getcwd(), '*_rank_003_*.json'))
)


# Delete each folder
for folder_path in junk_folders:
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)  # Delete directory
    elif os.path.isfile(folder_path):
        os.remove(folder_path)      # Delete file
    else:
        print(f"Skipping {folder_path}: neither a file nor a directory")

    
#next look at all the json files 
pep_json = glob.glob(os.path.join(os.getcwd(), '*_scores_rank_001_*.json'))

metrics = pd.DataFrame(columns=['name', 'plddt', 'ptm', 'iptm'])

# Iterate through each JSON file path
for index, pep_file_path in enumerate(pep_json):
    # Open the JSON file
    with open(pep_file_path, 'r') as pep_data_file:
        # Load JSON data
        pep_data = json.load(pep_data_file)
        
        #get the name using regex
        basename = os.path.basename(pep_file_path)
        pep_string = re.search(r'^([^_]*_[^_]*)', basename)
        if pep_string:
            pep_name = pep_string.group(1)
        else:
            pep_name = ''

        #average plddt
        plddt = np.mean(pep_data['plddt'], axis=0)
        ptm = pep_data['ptm']
        iptm = pep_data['iptm']
        metrics=pd.concat([metrics, 
                           pd.DataFrame({'name': [pep_name], 'plddt': [plddt], 'ptm': [ptm], 'iptm' : [iptm]})], 
                          ignore_index=True
                         )
        
#process
metric_sort = metrics.sort_values(by=['plddt','iptm']) #resort by plddt then by ptm 

metric_sort.to_csv('xpan_rfd.csv')

#set cutoff
cutoff = 87
TopPep= 20

#grab the useless peps and remove the junk
metric_below_cut = metric_sort[metric_sort['plddt'] < cutoff]

for index, row in metric_below_cut.iterrows():
    
    jplist = glob.glob(os.path.join(os.getcwd(), f"{pep_name}_*"))
    
    if jplist:
        for file in jplist:
            if os.path.isfile(file):
                os.remove(file)
        else:
            print(f"Skipping {file}: not a file")
    else:
        print(f"No files found for {pep_name}")    
    
print("junk remove complete")


#here are the most useful peptides
metric_above_cut = metric_sort[metric_sort['plddt'] > cutoff].sort_values(by=['plddt','iptm'], ascending=False)[:TopPep]
print(metric_above_cut)

directory = os.path.join(os.getcwd(),'imp_peps')

#now move to them to a new folder
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Folder '{directory}' created successfully.")
else:
    print(f"Folder '{directory}' already exists.")

    
    
pep_imp = metric_above_cut['name']

for index, peptides in enumerate(pep_imp):
    af_files = glob.glob(os.path.join(os.getcwd(), f'{peptides}_*'))
    fasta_files = glob.glob(os.path.join(os.getcwd(), f'../{peptides}.fasta'))
    
    for file in af_files + fasta_files:
        if os.path.exists(file):
            shutil.move(file, directory)
        else:
            print(f"No files found for {file}")
            
print("completed")    