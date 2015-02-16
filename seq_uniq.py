#!/usr/bin/python

import argparse
import os.path
import sys
import re

from run_blast import Blastn
from run_blast import At_least_part_seq_aligned
from split_fasta import split_fasta_files_on_seq_ids

def check_file_exists(filename):
    if not os.path.isfile(filename):
        print "cannot find file " + filename
        sys.exit(1)

def add_prefix_to_file(prefix, filename):
    """ for a given filename creates new filename
        e.g. /usr/bin/smth.dat 
        would create /usr/bin/FOX_smth.dat if prefix is FOX_
    """
    if re.search(r"\s", prefix):
        raise ValueError("Only prefixes without space are allowed.")
    basename = os.path.basename(filename)
    folder = os.path.abspath(os.path.dirname(filename))
    w_prefix = os.path.join(folder, prefix + basename)
    return w_prefix

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        'Unique and shared sequences for each of the two FASTA files.')
    parser.add_argument('fasta_files', nargs=2, help='2 fasta files for comparison')

    args = parser.parse_args()
    unique_seq_fasta = {}
    shared_seq_fasta = {}

    for seq_fasta in args.fasta_files:
        check_file_exists(seq_fasta)
        unique = add_prefix_to_file("unique_", seq_fasta)
        shared = add_prefix_to_file("shared_", seq_fasta)
        unique_seq_fasta[seq_fasta] = unique
        shared_seq_fasta[seq_fasta] = shared
        print "For FASTA file: " + seq_fasta
        print "unique sequences will be written to: " + unique
        print "shared sequences will be written to: " + shared
        print

    blastn = Blastn(args.fasta_files[0], args.fasta_files[1])
    percentage = 50.0
    similarity = At_least_part_seq_aligned(percentage)
    similar_seq_ids = blastn.find_similar_seq_ids(similarity)
    split_fasta_files_on_seq_ids(
        similar_seq_ids, args.fasta_files, 
        shared_seq_fasta, unique_seq_fasta)

