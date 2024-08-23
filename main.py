import csv
import os 
import pandas as pd

from config import config as cfg
from preprocess_fasta import preprocess
from check_status import check_status, Status 
from get_EC_predict import get_EC_predict
from collect_ec_csv import gen_vectors_from_dir, gen_vectors_from_list
from faiss_test import faiss_test, Metric


# num_expected_instances = 0
# num_exist_instances = 0
# num_GCF = 0

def main():
    
    preprocess()

    with open(cfg.NCBI_DATALIST_PURE, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            seq_id = row['Assembly Accession']

            if check_status(seq_id) == Status.ERROR:
                print(f"{seq_id} is not in the database!")
            elif (cfg.REPREDICT_EC == True) or (check_status(seq_id) != Status.READY):
                get_EC_predict(seq_id)

    # all the result should be put at cfg.WORK_DIR now
    xb_path = os.path.join(cfg.WORK_DIR, "faiss/xb.csv")
    xb = gen_vectors_from_dir(cfg.WORK_DIR, output = xb_path, J = 'union')
    
    xq = pd.read_csv( xb_path, index_col=0 ).loc[["GCF_030758275.1_maxsep.csv"]]
    xq.to_csv(os.path.join(cfg.WORK_DIR, "faiss/xq.csv"))
    
    # the following code is incorrect since the dim while be different
    # xq = gen_vectors_from_list([cbm588], output = os.path.join(cfg.WORK_DIR, "faiss/xq.csv")) # GCF_030758275.1 is the RefSeq of CBM588
    D, I = faiss_test(xb, xq, metric = Metric.COSINE_SIM, save_file = True, dataset = cfg.NCBI_DATALIST_PURE, outputfile = cfg.FAISS_OUT_CSV)
    
    # plot_faiss(I, D)


if __name__ == '__main__':
    main()