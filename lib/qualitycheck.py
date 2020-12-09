#!/usr/bin/env python3

"""
Execute quality check for every fastq.gz file from the input directory.
Put the reports into the given output directory.
Containing a zip and html file.

Fastqc function needs 3 parameters:
fastq_dir = Input directory with the raw data.
fastqc_dir = Output directory for the reports.
threads = The number of files to process.
"""


__author__ = "Rob Meulenkamp"
__status__ = "Development"
__date__ = "02-12-2020"
__version__ = "v0.2"


import subprocess
import sys


def fastqc(fastq_dir, fastqc_dir, threads):
    """Performs the fastqc tool for all the fastq.gz files."""

    query = 'fastqc --casava {}*fastq.gz -o={} -t {}'.format(fastq_dir, fastqc_dir, threads)

    subprocess.run(query, shell=True)

    return 0


def main():
    """execute the programm"""
    #Temporary variables
    fastq_dir = ""
    fastqc_dir = ""
    threads = ""
    fastqc(fastq_dir, fastqc_dir, threads)

    return 0


if __name__ == "__main__":
    sys.exit(main())
