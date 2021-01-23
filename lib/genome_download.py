#!/usr/bin/env python3

"""
This module will check if the required genome data files are present in the output directory
and if they aren't it will download them.
The fasta file will also be
"""

# METADATA VARIABLES
__author__ = "Rob Meulenkamp and Vincent Talen"
__status__ = "Development"
__date__ = "15-01-2021"
__version__ = "v0.4.4"

# IMPORTS
import sys
import os
import subprocess as sub


# FUNCTIONS
def fix_output_dir(output_dir):
    """
    This is a small function that puts the output directory in the correct format

    :param output_dir: The output_dir the files need to be put in
    :result: The output directory that is in the correct format
    """
    if output_dir.startswith("/"):
        output_dir = output_dir[1:]

    # Add the suffix this module needs
    output_dir += "/genome/"
    return output_dir


def collect_hisat_index(output_dir):
    """
    This function downloads the HISAT index if it does not exist yet and removes compression.

    :param output_dir: The output directory where the file needs to be saved
    """
    hisat_dir = output_dir + 'hisat2'
    hisat_file_name = f"{hisat_dir}/grch38_genome.tar.gz"

    query = ["wget", "-c", "-O", "-",
             "https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz",
             "|", "tar", "-x", "-C", hisat_dir]
    if not os.path.isfile(hisat_file_name):
        sub.run(query)


def collect_human_genome_file(output_dir):
    """
    This function downloads the human genome fasta reference file and removes compression.

    :param output_dir: The output directory where the file needs to be saved
    """
    dir_fa_file = '{}Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz'.format(output_dir)

    query = ["wget", "ftp://ftp.ensembl.org/pub/release-84/fasta/homo_sapiens/dna/"
                     "Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz", "-P", output_dir]
    query_2 = ["gunzip", dir_fa_file]
    if not os.path.isfile(dir_fa_file):
        sub.run(query)
        sub.run(query_2)


def collect_genome_rtf(output_dir):
    """
    This function will check if the genome rtf file is existent and otherwise download it.

    :param output_dir: The output directory where the file needs to be saved
    """
    dir_gtf_file = f"{output_dir}Homo_sapiens.GRCh38.84.gtf.gz"

    query = ["wget", "ftp://ftp.ensembl.org/pub/release-84/gtf/homo_sapiens/"
                     "Homo_sapiens.GRCh38.84.gtf.gz", "-P", output_dir]
    query_2 = ["gunzip", dir_gtf_file]

    if not os.path.isfile(dir_gtf_file):
        sub.run(query)
        sub.run(query_2)


def fasta_processing(output_dir):
    """
    Creates the fasta dictionary and fai files with the Picard tool.

    :param output_dir: The output directory where the file needs to be saved
    """
    file_name_dict = "Homo_sapiens.GRCh38.dna.primary_assembly.dict"
    file_name_fai = "Homo_sapiens.GRCh38.dna.primary_assembly.fa.fai"
    dir_fa_file = f"{output_dir}Homo_sapiens.GRCh38.dna.primary_assembly.fa"
    picard_tool = "lib/Picard_2.23.9/picard.jar"

    query_dict = ["java", "-jar", picard_tool, "CreateSequenceDictionary",
                  f"R={dir_fa_file}", f"O={output_dir}{file_name_dict}"]
    query_fai = ["samtools", "faidx", dir_fa_file]

    # It is determined if the fasta.dict has been created already
    if not os.path.isfile(output_dir + file_name_dict):
        # If this is not the case, the file will be created
        sub.run(query_dict)

    # It is determined if the fasta.fa.fai has been created already
    if not os.path.isfile(output_dir + file_name_fai):
        # If this is not the case, the file will be created
        sub.run(query_fai)


def collect_all_genome_info(output_dir):
    """
    This function this is the function that can be called
    to collect all the genome data with other the other functions.

    :param output_dir: The output directory where the file needs to be saved
    :return: A list with the names of the three files
    """
    output_dir = fix_output_dir(output_dir)

    collect_hisat_index(output_dir)
    collect_genome_rtf(output_dir)
    collect_human_genome_file(output_dir)

    fasta_processing(output_dir)

    genome_hisat2 = "Data/genome/HiSat2/Homo_sapiens/GRCh38.92"
    gtf_file = "Data/genome/Homo_sapiens.GRCh38.92.gtf"
    genome_fasta = "Data/genome/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa"
    # Return the three variables in a list for further use.
    return [genome_hisat2, gtf_file, genome_fasta]


# MAIN
def main():
    """Main function to test functionality of the module"""
    output_dir = ''
    genome_hisat2, gtf_file, genome_fasta = collect_all_genome_info(output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
