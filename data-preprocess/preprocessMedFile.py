"""
Preprocess the medication file by:
    - format the medication
    - each line has a single reason
    - cleans up some words
"""
import csv
import re
import json
import difflib
import sys
import time
import pandas as pd
sys.path.append("../data-preprocess")

import formatMed

def appendDrugs(drugName, drugCats, drugDict):
    if not drugDict.has_key(drugName):
        drugDict[drugName] = {"cat":drugCats, "type": "generic"}
    return drugDict


def format_med_string(drug):
    drug = drug.strip().lower()
    words = drug.split()
    word_list = set(words)
    drug = " ".join(sorted(word_list, key=words.index))
    return drug


def _return_drug(med, drugType):
    return {"type": 'D', "cat": drugType, "name": med}


def search_drug(med, medDict):
    medupdate, drugType = formatMed.get_med_approx(med, medDict)
    if drugType is not None:
        return _return_drug(med, drugType)
    medWords = med.split()
    if len(medWords) > 1:
        ## try the last word
        medupdate, drugType = formatMed.get_med_approx(medWords[-1], medDict)
        if drugType is not None:
            return _return_drug(med, drugType)
    medupdate, drugType = formatMed.get_med_approx(medWords[0], medDict)
    if drugType is not None:
            return _return_drug(med, drugType)
    return None
    

def main():
    header = pd.read_csv('raw_data.csv')
    print('reading raw_data.csv header=', str(list(header.head(0).columns)))
    # medFile = open('raw_data.csv', 'r')
    medReader = pd.read_csv('raw_data.csv', delimiter=",")
    outFile = open('med_processed_with_categories.csv', 'w', newline="\n")
    outWriter = csv.writer(outFile, delimiter=",")
    ## read and write the header and add a new column for revised symptoms

    tempRow = list(header.head(0).columns) + ['cat_v2', 'med_v2', 'med_class', 'help_v2']
    # s = '","'.join(str(x) for x in tempRow)
    # tempRow = "\""+s+"\""
    print("tempRow=",str(tempRow))
    outWriter.writerow(tempRow)
    MED_NAME_IDX = 'medication'      ## MED NAME COLUMN
    # MED_TYPE_IDX = 5        ## MEDICATION CLASSIFICATION (not being used)
    suppDict = json.load(open('../data-preprocess/data/rxlist-supp.json', 'r'))
    medDict = json.load(open('create_med_dict_file_OUTPUT.json', 'r')) 
    drugDict = {}
    for index, row in medReader.iterrows():
        print("medReader medication=",str(row.values.tolist()))
        if len(row) <= 0:
            continue
        med = format_med_string(row[MED_NAME_IDX])
        # print("simple med",med)
        # medType = row[MED_TYPE_IDX].lower()
        # print("medType=",medType)
        medHelp = ''
        if med == "":
            continue
        if med in drugDict:
            print("med in drugDict=",med)
            medInfo = drugDict[med]
            for medCat in medInfo['cat']:
                tempRow = row.values.tolist() + [medInfo['type'], medInfo['name'], medCat, medHelp]
                # s = '","'.join(str(x) for x in tempRow)
                # tempRow = "\""+s+"\""
                outWriter.writerow(tempRow)
            continue
        # print("Looking up:" + med)
        # see if it exists in the medication dictionary
        medInfo = search_drug(med, medDict)
        if medInfo is not None:
            drugDict[med] = medInfo
            for medCat in medInfo['cat']:
                tempRow = row.values.tolist() + [medInfo['type'], medInfo['name'], medCat, medHelp]
                # s = '","'.join(str(x) for x in tempRow)
                # tempRow = "\""+s+"\""
                outWriter.writerow(tempRow)
            continue 
        # next try the supplement dictionary
        drugType = formatMed.get_supp_approx(med, suppDict)
        if drugType is not None:
            drugDict[med] = {"type": 'S', "cat": drugType, "name": med}
            tempRow = row.values.tolist() + ['S', med, drugType, medHelp]
            # s = '","'.join(str(x) for x in tempRow)
            # tempRow = "\""+s+"\""
            outWriter.writerow(tempRow)
        else: 
            print("unable to resolve drug:" + med)
            print("output of row--" + str(row) + "-- end row")
            drugDict[med] = {"type": 'U', "cat": "unknown", "name": med}
            tempRow = row.values.tolist() + ['U', med, "unknown", medHelp]
            # s = '","'.join(str(x) for x in tempRow)
            # tempRow = "\""+s+"\""
            outWriter.writerow(tempRow)
    # medFile.close()
    outFile.close()
    
if __name__ == "__main__":
    main()
