import os
import time
from dotenv import load_dotenv

load_dotenv()

class Config:
    # variable for CLEAN
    NCBI_DATALIST = os.getenv('NCBI_DATALIST')
    NCBI_DATALIST_PURE = os.getenv('NCBI_DATALIST_PURE', NCBI_DATALIST.split('\\.')[0] + "_pure.csv")
    NCBI_DATASET_DIR = os.getenv('NCBI_DATASET_DIR')

    CLEAN_DIR = os.getenv('CLEAN_DIR')
    MAXSEP_PATH = os.getenv('MAXSEP_PATH', os.path.join(CLEAN_DIR, "app/results/inputs/"))
    FASTA_PATH = os.getenv('FASTA_PATH', os.path.join(CLEAN_DIR, "app/data/inputs/"))

    WORK_DIR = os.getenv('WORKING_DIR')
    
    EC_LIST_SOURCE = os.getenv('EC_LIST_SOURCE')
    WHOLE_EC_LIST = os.getenv('WHOLE_EC_LIST')

    # XB_CSV = os.getenv('XB_CSV', os.path.join(WORK_DIR, 'faiss/xb_out.csv'))
    # XQ_CSV = os.getenv('XQ_CSV', os.path.join(WORK_DIR, 'faiss/xq_out.csv'))
    FAISS_OUT_CSV = os.getenv('FAISS_OUT_CSV', os.path.join(WORK_DIR, f'faiss/{time.strftime("%m%d%H%M")}_faiss_out'))

    REPREDICT_EC = os.getenv("REPREDICT_EC", False)
    LIMIT_PRECISION = os.getenv("LIMIT_PRECISION", False)

config = Config()
