import os
from config import config as cfg
import shutil
from enum import Enum

class Status(Enum):
    READY = 1
    NOTREADY = 2
    ERROR = 3

def isGCF(seq_id):
    seqtype = seq_id.split('_')[0]
    return (seqtype == 'GCF')
            
def check_status(seq_id):

    clean_result = cfg.MAXSEP_PATH + seq_id + "_maxsep.csv"

    if os.path.isfile(clean_result): # the result of CLEAN exists    
        shutil.copy(clean_result, cfg.WORK_DIR) # copy to copy_dist_path
        return Status.READY

    elif os.path.isfile(cfg.FASTA_PATH + seq_id + ".fasta"): # no result, but link exists
        print(seq_id + " is in the job queue!")
        return Status.NOTREADY

    elif os.path.isfile(cfg.NCBI_DATASET_DIR + seq_id + "/protein.faa"): # in the Bacteria, but not CLEAN/app/data
        print (seq_id + " link does not exist")
        return Status.NOTREADY

    else:    
        return Status.ERROR

