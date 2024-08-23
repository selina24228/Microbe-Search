# This program does the following things.
# read from name_list, if a GenBank seq and a RefSeq seq have the same assembly, keep the RefSeq one.

import csv
from config import config as cfg
from check_status import isGCF

def preprocess():

    unique_ids = {}

    with open(cfg.NCBI_DATALIST, "r") as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        
        for row in reader:

            assembly = row['Assembly Name']
            seq_id = row['Assembly Accession']
            organism = row['Organism Name']
            strain = row['Organism Infraspecific Names Strain']
            
            if assembly not in unique_ids or isGCF(seq_id):
                unique_ids[assembly] = {'seq_id': seq_id, 'organism': organism, 'strain': strain}


    with open(cfg.NCBI_DATALIST_PURE, 'w', newline='') as csv_file:

        fieldnames = ['Assembly Accession', 'Assembly Name', 'Organism Name', 'Organism Infraspecific Names Strain']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for name, data in unique_ids.items():
            writer.writerow({'Assembly Accession': data['seq_id'], 'Assembly Name': name, 'Organism Name': data['organism'], 'Organism Infraspecific Names Strain': data['strain']})

    print("Finish preprocessing the name list")