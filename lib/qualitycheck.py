#!/usr/bin/env python3

"""
Execute quality check for every fastq.gz file from the input directory.
Put the reports into the given output directory.
Containing a zip and html file.
"""


__author__ = "Rob Meulenkamp and Vincent Talen"
__status__ = "Development"
__date__ = "22-01-2021"
__version__ = "v0.2.3"


import sys
from subprocess import run


def perform_fastqc(input_dir, output_dir, threads):
    """Performs the fastqc tool for all the fastq.gz files in the given input directory.

    :param input_dir: Input directory with the raw data.
    :param output_dir: Output directory for the reports.
    :param threads: The number of files to process.
    """
    if not input_dir.endswith("/"):
        input_dir += "/"
    fastqc_out = f"{output_dir}/Results/fastQC/"

    query = ["fastqc", f"{input_dir}*fastq.gz", f"-o={fastqc_out}/" "-t", threads]
    run(query)


def main():
    """Main function to test module functionality"""
    input_dir, output_dir, threads = "" * 3
    perform_fastqc(input_dir, output_dir, threads)
    return 0


if __name__ == "__main__":
    sys.exit(main())
