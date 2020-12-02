#!/usr/bin/env python3

"""
Ideas:
- Easy tool-install shell executable and some already-installed packages in the repository
- A configfile? So the user can easily define the wanted values and save them between runs easily.
    + If the intended use of this pipeline is with small setting changes (idk)
- Maybe create an object per file from a class (from a module)
- Dictionary returning all the genome info instead of all those functions in a module
- Directory per run with temp_files folder, settings_used.txt, results.pdf, processed_files folder
    + Used settings maybe in results.pdf?

Other:
- Paired end (In alignment with genomeHiSat2)
"""

# METADATA VARIABLES
__author__ = "M. Hagen, R. Meulenkamp, J. Numan, V. Talen and R. Visser"
__status__ = "Development"
__date__ = "02-12-2020"
__version__ = "v0.1"

# IMPORTS
import sys
import argparse
from math import ceil
from multiprocessing import cpu_count

from lib.alignment import Alignment
from lib.count_matrix import create_count_matrix
from lib.directories import CreateDirectories
from lib.end_report import EndReport
from lib.fasta_processing import FastaProcessor
from lib.genome_info import collect_genome_info
from lib.multiqc import RunMultiQC
from lib.preprocess import PreProcess
from lib.qualitycheck import QualityCheck
from lib.trimmer import Trimmer


# FUNCTIONS
def create_parser():
    """
    This function creates a parser for interaction with the command line interface.

    :return:    an object containing all arguments
    """
    # Create parser
    parser_desc = "Pipeline used for aligning and quality checking data." \
                  "Multiple reports will be generated about the quality including " \
                  "probable explanations if quality is bad."
    parser = argparse.ArgumentParser(description=parser_desc,
                                     epilog="Thanks for using our pipeline!")

    # Add arguments
    parser.add_argument("-f", "--files", required=True,
                        help="Directory with files or file name")
    parser.add_argument("-o", "--organism", required=True,
                        help="The organism whose genome needs to be aligned")
    parser.add_argument("-d", "--directory_out", required=True,
                        help="Directory where all the files need to be saved.")
    parser.add_argument("-p", "--paired", required=False, action='store_true',
                        help="Only use this when you want to use paired-end sequencing!"
                             "If you don't give this argument it will use single end")
    parser.add_argument("-t", "--trim", required=False,
                        help="Define the last bp to keep for trimming")
    parser.add_argument("-c", "--cores", required=False, default=ceil((2/3)*cpu_count()),
                        help="Define the number of cores to be used (optional)"
                             "(Defaults to two-thirds of the systems amount)")

    args = parser.parse_args()  # Collect the arguments/values
    return args


def collect_files(files):
    """"""
    return files


# MAIN
def main():
    """Main function calling forth all tasks"""
    args = create_parser()

    # Create needed directories to save (temporary) files
    CreateDirectories(args.directory_out)
    # Gather all the files the pipeline needs to be run on
    files = collect_files(args.files)
    # Collect the reference data related to the organism that was inputted
    collect_genome_info(args.organism)

    # Run FastQC tool on all files to create reports of quality
    QualityCheck(files)
    # Trim the data. (Adapter/primer)
    Trimmer(args.trim)
    # Picard fasta processing
    FastaProcessor()

    # Perform actual alignment to create BAM maps (with genomeHiSat2)
    Alignment(args.paired, args.cores)
    # Preprocessing all the mapped data
    PreProcess()

    # With the final sorted bam alignment and genome annotation create a matrix (featureCounts)
    #   - Creates a txt file with the gene counts
    create_count_matrix()
    # Run the MultiQC creating a HTML report with bam alignment and log files
    RunMultiQC()

    # Look for the bad qualities and create a PDF with
    #   the (possible) explanations why the quality is bad
    #   if all qualities are good say this too
    EndReport()

    print("Pipeline finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
