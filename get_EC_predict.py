import os
import subprocess
import shutil

from config import config as cfg

def check_file_for_J(seq_id):
    source = os.path.join( cfg.NCBI_DATASET_DIR, seq_id + "/protein.faa")
    with open(source, 'r') as file:
        for line in file:
            # Strip leading/trailing whitespace
            line = line.strip()
            
            # Check if the line does not begin with '>' and contains 'J'
            if not line.startswith('>') and 'J' in line:
                print("Found 'J' in a line that does not begin with '>'.")
                return True  # Early exit if condition is met
    
    print("No 'J' found in lines not beginning with '>'.")
    return False


def preprocess_seq(seq_id, method = 1):

    # mv protein.faa into protein.bak.faa
    source = os.path.join( cfg.NCBI_DATASET_DIR, seq_id + "/protein.faa")
    source_bak = os.path.join( cfg.NCBI_DATASET_DIR, seq_id + "/protein.bak.faa")
    os.rename(source, source_bak)

    with open(source_bak, "r") as origin, open(source, "w") as modif:
        title = None
        seq = None
        hasJ = False
        for line in origin:
            if line.startswith('>'): # title
                if title:
                    if not hasJ:
                        modif.write(title)
                        modif.write(seq)

                    elif(method == 1): # union
                        modif.write(title.replace('\n', '[I]\n'))
                        modif.write(seq.replace("J", "I"))
                        modif.write(title.replace('\n', '[L]\n'))
                        modif.write(seq.replace("J", "L"))
                    
                    else: # delete: do nothing.
                        pass

                title = line
                seq = None
                hasJ = False
            else: 
                if seq == None:
                    seq = line
                else:
                    seq += line
                if 'J' in line:
                    hasJ = True
        
        # handle the last line
        if not hasJ:
            modif.write(title)
            modif.write(seq)

        elif(method == 1): # union
            modif.write(title.replace('\n', '[I]\n'))
            modif.write(seq.replace("J", "I"))
            modif.write(title.replace('\n', '[L]\n'))
            modif.write(seq.replace("J", "L"))
        
        else: # delete: do nothing.
            pass



def create_link(seq_id):
    try:   
        source = os.path.join( cfg.NCBI_DATASET_DIR, seq_id + "/protein.faa")
        link_name = os.path.join(cfg.CLEAN_DIR, 'app/data/inputs/'+ seq_id + ".fasta")
        if not os.path.exists(link_name):
            os.symlink(source, link_name)
            print(f"Created symlink: {link_name} -> {source}")
        else:
            print(f"Symlink already exists: {link_name}")
    except OSError as e:
        print(f"Failed to create symlink {link_name} -> {source}: {e}")


def ececute_CLEAN(test_data):
    CLEAN_script = os.path.join(cfg.CLEAN_DIR, "app/CLEAN_infer_fasta.py")
    command = ["python", CLEAN_script, "--fasta_data", test_data]
    subprocess.run(command, cwd = os.path.join(cfg.CLEAN_DIR, "app"))
    

def get_EC_predict(seq_id):

    if check_file_for_J(seq_id):
        preprocess_seq(seq_id) # handle "J"

    create_link(seq_id)
    ececute_CLEAN(seq_id)

    clean_result = cfg.MAXSEP_PATH + seq_id + "_maxsep.csv"
    shutil.copy(clean_result, cfg.WORK_DIR) # copy to copy_dist_path