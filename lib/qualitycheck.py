#!/usr/bin/env python3

"""
execute quality check for every fastq.gz file in the directory.
"""

__author__ = "Rob Meulenkamp"
__status__ = "template"
__date__ = "02-12-2020"
__version__ = "v1"


import os
import sys
import argparse


def fastqc(fastq_dir, fastqc_dir):
    """prepared the data for the fastqc tool."""

    query = 'fastqc --casava {}*fastq.gz -o={}'.format(fastq_dir, fastqc_dir)
                                                            # 'fastq_dir' directory waar de *fastq.gz staan.
    os.system(query)                                        # '-o=' plek van output directory.

    return 0


def main(args):
    """execute the programm"""
    parser = argparse.ArgumentParser()
    parser.add_argument("fastq", help="Give the directory to the fastq.gz files.")
    parser.add_argument("fastqc", help="Give the output directory to the fastqc report(s).")
    arg = parser.parse_args()
    fastq_dir = arg.fastq
    fastqc_dir = arg.fastqc
    fastqc(fastq_dir, fastqc_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
