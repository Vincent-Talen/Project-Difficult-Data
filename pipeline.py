#!/usr/bin/env python3

"""
Ideas:
- Easy tool-install shell executable and some already-installed packages in the repository
- Dictionary returning all the genome info instead of all those functions in a module
- Used settings maybe in results.pdf?
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "22-01-2021"
__version__ = "v0.3.6"

# IMPORTS
import sys
import argparse
from math import ceil
from multiprocessing import cpu_count

from lib.alignment import Alignment  # TODO
from lib.bam_processing import BamProcessing
from lib.count_matrix import create_count_matrix
from lib.directories import CreateDirs
from lib.end_report import EndReport  # TODO
from lib.genome_download import collect_all_genome_info
from lib.multiqc import perform_multiqc  # TODO
from lib.qualitycheck import perform_fastqc  # TODO
from lib.trimmer import Trimmer  # TODO


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
    parser.add_argument("-i", "--input", required=True,
                        help="Directory with files or file name")
    parser.add_argument("-o", "--organism", required=True,
                        help="The organism whose genome needs to be aligned")
    parser.add_argument("-d", "--directory_out", required=True,
                        help="Directory where all the files need to be saved.")
    parser.add_argument("-p", "--paired", required=False, action="store_true",
                        help="Only use this when you want to use paired-end sequencing! "
                             "If you don't give this argument it will use single end")
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


def calculate_threads(cores):
    threads = 1
    return threads


# MAIN
def main():
    """Main function calling forth all tasks"""
    args = create_parser()

    # Preparing multiple things for pipeline functionality
    if args.directory_out.endswith("/"):
        output_dir = args.directory_out[:-1]
    else:
        output_dir = args.directory_out

    CreateDirs(output_dir)  # Create all the directories we'll be using
    cores = fix_core_count(args.cores)  # Determine the to be used core count
    genome_hisat2, gtf_file, genome_fasta = collect_all_genome_info(args.directory_out)

    # Run FastQC tool on all files to create reports of quality
    perform_fastqc(args.input, output_dir, calculate_threads(cores))
    # Trim the data. (Adapter/primer)
    Trimmer(output_dir, args.trim)

    # Perform actual alignment to create BAM maps (with genomeHiSat2)
    align_obj = Alignment(output_dir, genome_hisat2, calculate_threads(cores), args.paired)
    align_obj.perform_alignment()
    # Preprocess all the mapped data
    BamProcessing(output_dir)

    # With the final sorted bam alignment and genome annotation create a matrix (featureCounts)
    #   - Creates a txt file with the gene counts
    create_count_matrix(args.directory_out)
    # Run the MultiQC creating a HTML report with bam alignment and log files
    perform_multiqc(args.directory_out)

    # Look for the bad qualities and create a PDF with
    #   the (possible) explanations why the quality is bad
    #   if all qualities are good say this too
    EndReport(args.directory_out)

    print(f"Pipeline finished, output created in '{args.directory_out}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
