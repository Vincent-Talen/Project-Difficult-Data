#!/usr/bin/env python3

"""
This module contains the create_count_matrix function that can be used to create a count matrix for
one or more bam files.
"""


# METADATA VARIABLES
__author__ = "Joost Numan and Vincent Talen"
__status__ = "Development"
__date__ = "14-01-2021"
__version__ = "v0.3.2"


# IMPORTS
import sys
import glob
from subprocess import run


# FUNCTIONS
def create_count_matrix(output_dir):
    """
    This function creates and runs a query that calls forth the Feature Counts tool
    from the Subread package.

    :param output_dir: is the directory where this script needs to be run
    """
    if output_dir.startswith("/"):
        output_dir = output_dir[1:]

    files = glob.glob(f"{output_dir}/Preprocessing/markDuplicates/*_sorted.bam")
    anno_file = f"{output_dir}/Data/genome/Homo_sapiens.GRCh38.84.gtf"

    query = ["lib/Subread-2.0.1/bin/featureCounts", "-a", anno_file,
             "-o", f"{output_dir}/RawData/counts/counts.txt", *files]
    run(query)


# MAIN
def main():
    """Main function to test the module"""
    create_count_matrix("/output")
    return 0


if __name__ == "__main__":
    sys.exit(main())
