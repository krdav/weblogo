#!/usr/bin/env python

import sys, os, glob, csv, random, copy, time
from itertools import cycle
csv.field_size_limit(sys.maxsize)
from anarci import anarci
from collections import Counter
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
partis_path = '/fh/fast/matsen_e/kdavidse/partis'
sys.path.insert(1, partis_path + '/python')
import utils
import glutils
# Read default germline info
glfo = glutils.read_glfo(partis_path + '/data/germlines/human', locus='igh')


### Notice a gap is added as the 21th amino acid:
AA_LIST = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-']
AA_INDEX = {aa:i for i, aa in enumerate(AA_LIST)}

AHO_L = 149



## Read from three files
## Detect counts vs. frequency, if frequency convert to count with base 10,000
## Line by line make the logos and concatenate them
## Remove empty cols and mark FR/CDR boundaries by star (*)
## Output them as logo_1.eps, logo_2.eps, ..., logo_N.eps
## Clean up after the WebLogo outout
## Wrap as a multiple process to speed up things
## Detect plots with true shift in highest frequency AA in the enhanced profile. Print the index




def main():
    import argparse
    parser = argparse.ArgumentParser(description='Make a stacked logo plot from multiple profiles.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--glob_pat', type=str, required=False, default='*cluster-annotations.csv', help='Glob pattern to find the partis "cluster annotation" files.')
    parser.add_argument('--nsubs', type=int, required=False, default=200, help='How many subsampled profiles should be taken out?')
    parser.add_argument('--fsub', type=float, required=False, default=None, help='Fraction of sequences in the full profile to include in the subsample.')
    global args
    args = parser.parse_args()



if __name__ == '__main__':
    main()
