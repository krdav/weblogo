#!/usr/bin/env python

import sys, os, glob, csv, random, copy, time, re
from itertools import cycle
from collections import Counter

### Notice a gap is added as the 21th amino acid:
AA_LIST = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-']
AA_INDEX = {aa:i for i, aa in enumerate(AA_LIST)}

AHO_L = 149
WEBLOGO_EXE = '/Users/krdav/Dropbox/seattle_master/weblogo/weblogo'


## Read from three files
## Detect counts vs. frequency, if frequency convert to count with base 10,000
## Line by line make the logos and concatenate them
## Remove empty cols and mark FR/CDR boundaries by star (*)
## Output them as logo_1.eps, logo_2.eps, ..., logo_N.eps
## Clean up after the WebLogo outout
## Wrap as a multiple process to speed up things
## Detect plots with true shift in highest frequency AA in the enhanced profile. Print the index







def line2counts(line, counts=True, base=10000):
    profile = list(map(float, line.strip().split(',')))
    assert(len(profile) == (AHO_L*len(AA_LIST)))
    if counts is True:
        return list(map(int, profile))

    Cprofile = list()
    for p in range(AHO_L):
        aho = profile[(p*21):((p+1)*21)]  # Extract the aho positions
        # If negative values move the profile up:
        if min(aho) < 0:
            min_aho = min(aho)
            aho = [x+abs(min_aho) for x in aho]
        # Normalize to sum=1:
        sum_aho = sum(aho)
        aho = [x/sum_aho for x in aho]
        # Stupid way of converting to integers but keeping the total sum=base:
        aho_count = [x*base for x in aho]
        aho_int_count = [int(x) for x in aho_count]
        aho_left = [x-y for x,y in zip(aho_count, aho_int_count)]
        left = base - sum(aho_int_count)
        aho_left_idx = sorted(range(len(aho_left)), key=lambda k: aho_left[k])[0:left]
        aho_int_count = [x if idx not in aho_left_idx else x+1 for idx, x in enumerate(aho_int_count)]
        assert(sum(aho_int_count) == base)

        # Add aho position to the count list:
        Cprofile.extend(aho_int_count)

    return Cprofile


def count_AAswitch(pi, pe, pf=None):
    wrong_switch = 0
    correct_switch = 0
    for p in range(AHO_L):
        aho = profile[(p*21):((p+1)*21)]  # Extract the aho positions

    return num



'''
../weblogo < sub_profiles_2.aho --weight 0 --units probability --stacks-per-line 149 --errorbars False --fineprint '' --alphabet ACDEFGHIKLMNPQRSTVWY > ggg.eps
'''

def make_logo(pi, pe, index, pf=None):
    ll = ['i', 'e', 'f'] if pf is not None else ['i', 'e']
    var = [pi, pe, pf] if pf is not None else [pi, pe]
    logos = list()
    for v, l in zip(var, ll):
        profile = 'p{}_{}.aho'.format(l, index)
        with open(profile, 'w') as fh_out:
            fh_out.write(','.join(map(str, v)))
        logoname = 'logo_p{}_{}.eps'.format(l, index)
        logos.append(logoname)
        cmd = '{} < {} --weight 0 --units probability --stacks-per-line 149 --errorbars False --fineprint "" --alphabet ACDEFGHIKLMNPQRSTVWY > {}'.format(WEBLOGO_EXE, profile, logoname)
        os.system(cmd)
    #logoname = 'logo_stacked_{}.eps'.format(index)  # merged logo
    # Start with a copy of the input profile:
    #cmd = 'cp {} {}'.format('logo_pi_{}.eps'.format(index), logoname)
    #os.system(cmd)
    with open(logos[0]) as fh:
        first = fh.readlines()
    logolines = list()
    with open(logos[1]) as fh:
        flag = 0
        for line in fh:
            if line.startswith('StartLine'):
                logolines.append(line)
                flag = 1
            elif line.startswith('EndLine'):
                logolines.append(line)
                break
            elif flag == 1:
                logolines.append(line)

    if pf is not None:
        with open(logos[2]) as fh:
            flag = 0
            for line in fh:
                if line.startswith('StartLine'):
                    logolines.append(line)
                    flag = 1
                elif line.startswith('EndLine'):
                    logolines.append(line)
                    break
                elif flag == 1:
                    logolines.append(line)

    stacked_logo = list()
    for line in first:
        if line.startswith('%%BoundingBox:'):
            t = line.split()
            t[-1] = str(len(ll) * int(t[-1]))
            line = '  '.join(t) + '\n'
        elif line.startswith('/logo_height'):
            t = line.split()
            t[-2] = str(len(ll) * int(t[-2]))
            line = '  '.join(t) + '\n'

        stacked_logo.append(line)
        if line.startswith('EndLine'):
            stacked_logo.extend(logolines)

    # Print the stacked logo:
    logoname = 'logo_stacked_{}.eps'.format(index)  # merged logo
    with open(logoname, 'w') as fh_out:
        for line in stacked_logo:
            fh_out.write(line)
    cmd = 'epstopdf {}'.format(logoname)
    os.system(cmd)






#m = re.search('BoundingBox:\s+\d+\s+\d+\s+\d+\s+\d+\s+$', s)
# template = re.sub(r'', '</html>', template)

#'BoundingBox:\s+\d+\s+\d+\s+'




def stack_logos(pi, pe, pf=None):
    if pf is not None:
        pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Make a stacked logo plot from multiple profiles.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='Input profile e.g. a sub-sampled profile.')
    parser.add_argument('enhanced', type=str, help='Enhanced profile. Output of enhancement on the input profile.')
    parser.add_argument('--full_profile', type=str, required=False, default=None, help='If the "true" profile is known plot this as a reference point.')
    parser.add_argument('--counts', type=bool, required=False, default=False, help='Is the input profiles counts? If false defaults on frequency.')
#    parser.add_argument('--nsubs', type=int, required=False, default=200, help='How many subsampled profiles should be taken out?')
#    parser.add_argument('--fsub', type=float, required=False, default=None, help='Fraction of sequences in the full profile to include in the subsample.')
    global args
    args = parser.parse_args()

    # Read lists into memory and assert that they have equal length:
    with open(args.input) as fh:
        pi_list = fh.readlines()
    with open(args.enhanced) as fh:
        pe_list = fh.readlines()
    assert(len(pi_list) == len(pe_list))
    if args.full_profile is not None:
        with open(args.full_profile) as fh:
            pf_list = fh.readlines()
        assert(len(pi_list) == len(pf_list))
    else:
        pf_list = None

    for i in range(len(pi_list)):
        # Split the line intp flat aho positions and convet frequencies to counts:
        pi = line2counts(pi_list[i], args.counts)
        pe = line2counts(pe_list[i], args.counts)
        if pf_list is not None:
            pf = line2counts(pf_list[i], args.counts)
        else:
            pf = None

        make_logo(pi, pe, i, pf=pf)
        # sys.exit()









if __name__ == '__main__':
    main()
