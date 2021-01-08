#!/usr/bin/env python3

"""
this python module runs the featureCounts tool
it requires the output directory and an annotation file
the result is a txt file
"""


# METADATA VARIABLES
__author__ = "Joost Numan"
__status__ = "Development"
__date__ = "8-01-2021"
__version__ = "v0.2"


# IMPORTS
import sys
import subprocess


# FUNCTIONS
def create_count_matrix(outputdir, anno_file, bam_file):
    """
    this function creates a query to be run with subprocess to run the Feature Counts tool
    the input for this function is outputdir and anno_file
    outputdir is the directory where this script needs to be run
    anno_file is the annotation file in GTF format
    bam_file is the Bam file required as input for the tool
    """
    query = "{}/featureCounts/bin/featureCounts -a {} -o {}/RawData/counts/geneCounts.txt {}/Preprocessing/markDuplicates/{}"
    query = query.format(outputdir, anno_file, outputdir, outputdir, bam_file)
    subprocess.run(query.split())


# MAIN
def main():
    """Main function calling forth all tasks"""
    create_count_matrix(".", "Homo_sapiens.GRCh38.84.gtf")
    return 0


if __name__ == "__main__":
    sys.exit(main())
