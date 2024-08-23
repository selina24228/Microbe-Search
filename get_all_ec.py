import re
import json
import wget

from config import config as cfg

def get_all_EC():

    EC_list = []
    working_EC = []
    former_EC_found = []
    counter = 0

    # if ./enzyme.dat doesn't exist, wget
    if not os.path.exists(cfg.EC_LIST_SOURCE):
        url = "https://ftp.expasy.org/databases/enzyme/enzyme.dat"
        wget.download(url, out = cfg.EC_LIST_SOURCE.replace("enzyme.dat", ""))
    
    # read from "./enzyme.dat"
    with open(cfg.EC_LIST_SOURCE) as fp: 
        for line in fp:
            new_ec_match = re.search(r"ID   (?:\d+\.\d+\.\d+\.n?\d+)", line)
            if new_ec_match: # get a new EC
                new_ec = re.findall(r"\d+\.\d+\.\d+\.n?\d+", new_ec_match.group(0))
                
                if working_EC:
                    EC_list.append(working_EC) # append working_EC to EC_list
                    working_EC = [] # clear working_EC
                working_EC.append(new_ec[0])

            else: # try to find formerly or Transferred
                match_formerly = re.search(r"Formerly EC ((?:\d+\.\d+\.\d+\.n?\d+)(?:, EC \d+\.\d+\.\d+\.n?\d+)*(?: and EC \d+\.\d+\.\d+\.n?\d+)?)", line)
                match_transferred = re.search(r"Transferred entry:", line)

                if match_transferred: # drop working_EC
                    working_EC = []

                elif match_formerly:
                    former = re.findall(r"\d+\.\d+\.\d+\.n?\d+", match_formerly.group(1))
                    working_EC.extend(former)
                    for ec in former:
                        if ec in former_EC_found:
                            print(f"Duplicate EC: {ec}")
                            counter += 1
                        else:
                            former_EC_found.append(ec)

        EC_list.append(working_EC)

        print(EC_list)
        print(f"total EC: {len(EC_list)}")
        print(f"{counter} duplicate")

    # write the result to json file
    with open(cfg.WHOLE_EC_LIST, 'w') as f:
        # indent=2 is not needed but makes the file human-readable 
        # if the data is nested
        json.dump(EC_list, f, indent=2) 
