import os
import re
import csv
import json
import pandas as pd
from collections import defaultdict

from config import config as cfg
from get_all_ec import get_all_EC

def get_EC_list():
    if not os.path.exists(cfg.WHOLE_EC_LIST):
        get_all_EC()

    with open(cfg.WHOLE_EC_LIST, 'r') as f:
        EC_list = json.load(f)
        print(EC_list)

    value_mapping = {}
    # Convert the JSON data to a dictionary mapping occurrences of certain values to a key.
    for group in EC_list:
        for value in group:
            value_mapping[value] = group[0]
    
    return value_mapping

def count_occurrence(filename, value_mapping, J = 'union'):
    
    with open(filename, "r") as f:
        count_dict = defaultdict(int)
        ECs = set()
        for row in f:

            values = re.findall(r"\d+\.\d+\.\d+\.n?\d+", row)
            for value in values:
                mapped_value = value_mapping[value]
                ECs.add(mapped_value)
            
            if '[I]' in row:
                pass
            elif J == 'delete' and '[L]' in row:
                ECs.clear()
            else:
                for ec in ECs:
                    count_dict[ec] += 1
                ECs.clear()

        return count_dict


def gen_vectors_from_dir(dir_path, output = None, J = 'union'):
    value_mapping = get_EC_list()

    # Get all the maxsep.csv files and process each file, counting the occurrences of each key, while aggregating values as specified.
    maxsep_csvfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    counts = []
    for csvfile in maxsep_csvfiles:
        file_count = count_occurrence(os.path.join(dir_path, csvfile), value_mapping, J)
        counts.append(file_count)
    
    df = pd.DataFrame(counts, index=maxsep_csvfiles).fillna(0).astype(int)
    print(df)

    if output is None:
        output = os.path.join(dir_path, 'faiss/dir_out.csv')
    df.to_csv(output)
    
    return df


def gen_vectors_from_list(input_list, output = None, J = 'union'):
    value_mapping = get_EC_list()
    counts = []
    
    for file in input_list:
        file_count = count_occurrence(file, value_mapping, J)
        counts.append(file_count)
    
    # Construct a DataFrame to display the results.
    df = pd.DataFrame(counts, index=input_list).fillna(0).astype(int)
    print(df)
    
    if output is None:
        output = '../faiss/list_out.csv'
    df.to_csv(output)
    
    return df