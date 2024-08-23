import numpy as np
import pandas as pd
import faiss
from enum import Enum

from config import config as cfg

class Metric(Enum):
    L2_NORM = 1    
    COSINE_SIM = 2

def normalize_L2(matrix):
    for vector in matrix:
        norm = np.linalg.norm(vector)
        if norm != 0:
            vector /= norm
    return matrix

def faiss_test(df_d, df_q, metric = Metric.COSINE_SIM, save_file = False, dataset = None, outputfile = None):
    # xb xd are Dataframes
    index_list = df_d.index.tolist()
    index_list = [index.split('_')[0] + '_' + index.split('_')[1] for index in index_list]

    d = df_q.shape[1]   # 2476
    nb = df_d.shape[0]  # 194
    nq = df_q.shape[0]  # 2
    xd = df_d.to_numpy()
    xq = df_q.to_numpy()

    if metric == Metric.COSINE_SIM:
        normalized_xd = normalize_L2(xd.astype('float32'))
        normalized_xq = normalize_L2(xq.astype('float32'))
    else:
        normalized_xd = xd
        normalized_xq = xq
    
    ngpus = faiss.get_num_gpus()
    if ngpus != 4:
        print("number of GPUs:", ngpus)
        cpu_index = faiss.IndexFlatIP(d) if metric == Metric.COSINE_SIM else faiss.IndexFlatL2(d)
        index = faiss.index_cpu_to_all_gpus(  # build the index
            cpu_index
        )

    else: 
        index = faiss.IndexFlatIP(d) if metric == Metric.COSINE_SIM else faiss.IndexFlatL2(d)

        index.add(normalized_xd)

    k = nb
    # D, I = index.search(normalized_xd[:5], k) # sanity check
    # print(I)
    # print(D)
    D, I = index.search(normalized_xq, k)     # actual search
    print(I)                   # neighbors of the 5 first queries
    print(D)                   # neighbors of the 5 first queries
    print(f'cfg.LIMIT_PRECISION = {cfg.LIMIT_PRECISION}')
    if cfg.LIMIT_PRECISION is True:
        D_round = [round(d, 6) for d in D]
        print(D_round)
        sorted_pairs = sorted(zip(D_round, I))
        D, I = zip(*sorted_pairs)
        D = list(D)
        I = list(I)

    if save_file is True:
        save_faiss_test(I, D, index_list,
            dataset = cfg.NCBI_DATALIST_PURE if dataset == None else dataset,
            outputfile = cfg.FAISS_OUT_CSV if outputfile == None else outputfile
        )
    return D, I   

def save_faiss_test(I, D, index_list, dataset, outputfile):

    for query in range(I.shape[0]):
        sorted_list = []

        for i in I[query]:
            sorted_list.append(index_list[i])

        # output 
        df_faiss = pd.DataFrame({
            'Assembly Accession': sorted_list,
            'dist': D[query]  # Flatten the NumPy array to a 1D array
        })
        df_dataset = pd.read_csv( dataset )
        print(df_dataset)
        df_out = pd.merge(df_faiss, df_dataset, on='Assembly Accession')

        df_out = df_out.sort_values(by='dist', ascending=False)
        df_out.to_csv(f'{outputfile}_{query}.csv', index=True)