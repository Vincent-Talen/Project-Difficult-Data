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
__status__ = "Template"
__date__ = "02-12-2020"
__version__ = "v0.1"

# IMPORTS
import sys
import argparse

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
    # Create parser and add arguments
    parser = argparse.ArgumentParser(description="Align data, check if the data is of quality",
                                     epilog="Thanks for using our pipeline!")
    parser.add_argument('-f', '--files', help='Directory with files or file name')
    # TODO: Add all necessary arguments

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
    CreateDirectories()
    # Gather all the files the pipeline needs to be run on
    files = collect_files(args.files)
    # Collect the reference data related to the organism that was inputted
    collect_genome_info()

    # Run FastQC tool on all files to create reports of quality
    QualityCheck()
    # Trim the data. (Adapter/primer)
    Trimmer()
    # Picard fasta processing
    FastaProcessor()

    # Perform actual alignment to create BAM maps (with genomeHiSat2)
    Alignment()
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
