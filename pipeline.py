#!/usr/bin/env python3

"""
Use this script to run the pipeline.
From here all the modules will be used in correct order to form the pipeline and create results.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.4.2"

# IMPORTS
import sys
import argparse
from math import ceil
from datetime import datetime
from multiprocessing import cpu_count
from termcolor import colored

from lib.alignment import Alignment
from lib.bam_processing import BamProcessing
from lib.count_matrix import run_feature_counts
from lib.directories import CreateDirs
from lib.genome_download import DownloadGenomeInfo
from lib.multiqc import perform_multiqc
from lib.qualitycheck import QualityCheck
from lib.trimmer import Trimmer


# FUNCTIONS
def create_parser():
    """
    This function creates a parser for interaction with the command line interface.

    :return:    an object containing all arguments
    """
    # Create parser
    parser_desc = "Pipeline used for aligning and quality checking data. " \
                  "Multiple reports will be generated about the quality."
    parser = argparse.ArgumentParser(description=parser_desc,
                                     epilog="Thanks for using our pipeline!")

    # Add arguments
    parser.add_argument("-i", "--input_directory", required=True,
                        help="Directory with the files the pipeline needs to run on")
    parser.add_argument("-o", "--output_directory", required=True,
                        help="Directory where all the files need to be saved.")
    parser.add_argument("-p", "--paired", required=False, action="store_true",
                        help="Only use this when you want to use paired-end sequencing. "
                             "If you don't give this argument it will process as single ended")
    parser.add_argument("-t", "--trim", required=False,
                        help="Define values to trim sequence ends with. "
                             "If you want to only trim the 3' end only give 1 integer and for"
                             "trimming both ends give 'int-int'."
                             "If you don't want to trim simply don't use this argument")
    parser.add_argument("-c", "--cores", required=False,
                        help="Define the number of cores to be used (optional) "
                             "(Defaults to three-quarters of the systems total amount)")

    args = parser.parse_args()  # Collect the arguments/values
    return args


def fix_core_count(cores):
    """Small function checking given (or not given -> default) core count against system info"""
    cores = int(cores)
    if cores:
        if not cores <= cpu_count():
            if not cpu_count() == 1:
                cores = cpu_count() - 1
            else:
                cores = cpu_count()
    else:
        cores = ceil(0.75 * cpu_count())  # Default for pipeline
    return cores


def print_status(color, text):
    """
    Function to print the status of a process so the user can see where the pipeline is at.
    It includes the time so the user can see how long the processes take.

    :param color: 'c' (cyan), 'g' (green) or something else for no color
    :param text: The text that needs to be printed in color after the time
    """
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    if color == "c":
        string = colored(text, "cyan")
    elif color == "g":
        string = colored(f"{text}\n", "green")
    else:
        string = text
    print(f"[{time}] {string}")


# MAIN
def main():
    """Main function calling forth all tasks"""
    args = create_parser()

    # Preparing multiple things for pipeline functionality
    if args.output_directory.endswith("/"):
        output_dir = args.output_directory[:-1]
    else:
        output_dir = args.output_directory

    if not args.input_directory.endswith("/"):
        input_dir = args.input_directory + "/"
    else:
        input_dir = args.input_directory

    # Create all the directories we'll be using
    print_status("c", "Preparing everything for pipeline usage and emptying + creating directories")
    create_dirs = CreateDirs(output_dir)
    download_genome = create_dirs.create_all_dirs()
    cores = fix_core_count(args.cores)  # Determine the to be used core count

    # Download all the needed files from the internet
    # If files were already found only download the user doesn't want to keep the existing ones
    if download_genome:
        print_status("c", "Starting downloads of all required genome files")
        genome_info = DownloadGenomeInfo(output_dir)
        genome_info.collect_all_genome_info()
        print_status("g", "Finished downloading all files")

    # Run FastQC tool on all files to create reports of quality
    print_status("c", "Starting Quality Check")
    quality_check = QualityCheck(input_dir, output_dir)
    quality_check.run_qualitycheck(cores)
    print_status("g", "Finished Quality Check")

    # Trim the data. (Adapter/primer)
    print_status("c", "Starting Trimmer")
    trimmer = Trimmer(args.trim, input_dir, output_dir)
    trimmer.run_trimmer(cores)
    print_status("g", "Finished Trimmer")

    # Perform actual alignment to create BAM maps (with genomeHiSat2)
    print_status("c", "Starting Alignment")
    align = Alignment(args.paired, output_dir)
    align.perform_alignment(cores)
    print_status("g", "Finished Alignment")

    # Preprocess all the mapped data
    print_status("c", "Preprocessing bam files")
    bam_pro = BamProcessing(output_dir)
    bam_pro.perform_preprocessing(cores)
    print_status("g", "Finished preprocessing bam files")

    # With the final sorted bam alignment and genome annotation create a matrix (featureCounts)
    print_status("c", "Starting featureCounts to create count matrix")
    run_feature_counts(cores, output_dir)
    print_status("g", "Finished creating count matrix")

    # Run the MultiQC creating a HTML report with bam alignment and log files
    print_status("c", "Starting MultiQC to create summary report")
    perform_multiqc(output_dir)
    print_status("g", "Finished summary report")

    finished = colored("Pipeline finished!", "green")
    print(f"{finished} Output created in '{output_dir}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
