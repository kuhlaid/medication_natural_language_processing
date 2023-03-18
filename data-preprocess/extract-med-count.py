import csv
import argparse
import json
import pandas as pd
from collections import Counter

# this script counts the number of medications listed in the raw_data.csv and outputs the list of medications and counts to a JSON file
def parse_file(filename, medName, delim, header):
    medFile = pd.read_csv(filename, delimiter=delim)
    medCounter = Counter()
    # print('delim=',delim)
    # print('parse_file', filename)
    for index, row in medFile.iterrows():
        # print('row=', str(list(row)), ' and index=',medName)
        # print('parse_file row', row[medName.strip()].strip().lower())
        med = row[medName.strip()].lower()      # we need to make sure our column names do not begin or end with a space
        # print('len(row)=', len(row), " med=", row[medName.strip()])
        # # print('medCounter')
        medCounter[med] += 1
    return medCounter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input file")
    parser.add_argument("medName", type=str, help="what is the name of the medications column")
    parser.add_argument("-sep", type=int, default=1,
                        help="delimiter seperator")
    parser.add_argument('outfile', help="output file")
    parser.add_argument("-hdr", action='store_true')
    args = parser.parse_args()
    sepType = ","
    if args.sep == 2:
        sepType = "\t"
    medCounter = parse_file(args.infile, args.medName, sepType, args.hdr)
    with open(args.outfile, 'w') as outfile:
        json.dump(medCounter, outfile, indent=2)

if __name__ == "__main__":
    main()
