#!/usr/bin/env python3

"""
downloads the genome fasta and gtf file and the indexes for the Hisat2 tool.

"""

__author__ = "Rob Meulenkamp"
__status__ = "Development"
__date__ = "06-01-2021"
__version__ = "v0.3"

import sys
import os
import subprocess as sub


def hisat_index(dir_hisat):
    """downloads the hisat indexes"""
    # Dowloanden gaat op basis in welke directory je staat.
    # De indexes voor de hisat tool wordt in een mapje gestopt genaamd 'grch38'.
    # Directory moet bestaan anders breekt hij de pipeline af.
    dir_hisat_file = '{}grch38_genome.tar.gz'.format(dir_hisat)
    in_query = "wget", "-c", "https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz", "-O", "-"
    out_query = "tar", "-xz", "-C", dir_hisat
    if not os.path.isfile(dir_hisat_file):
        try:
            hisat2 = sub.Popen(in_query,
                               stdout=sub.PIPE)
            sub.check_output(out_query, stdin=hisat2.stdout)
            hisat2.wait()
        except sub.CalledProcessError as e:
            print("Oeps, there went something wrong! Check if the directory exists.\n{}".format(e))
    else:
        print("Indexes for the hisat tool are already in the directory")
    return 0


def human_genome_file(dir_fa_gtf):
    """downloads fasta file and unzipped the file"""
    dir_fa_file = '{}Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz'.format(dir_fa_gtf)
    query = ["wget", "ftp://ftp.ensembl.org/pub/release-84/fasta/"
                     "homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz", "-P", dir_fa_gtf]
    query_2 = ["gunzip", dir_fa_file]
    if not os.path.isfile(dir_fa_file):
        try:
            sub.run(query)
            sub.run(query_2)
        except sub.CalledProcessError as e:
            print("Oeps, there went something wrong! Check if the directory exists.\n{}".format(e))
    else:
        print('the fasta file is already in your given directory.')

    return 0


def genome_rtf(dir_fa_gtf):
    """downloads gtf file and unzipped the file"""
    dir_gtf_file = '{}Homo_sapiens.GRCh38.84.gtf.gz'.format(dir_fa_gtf)
    query = ["wget", "ftp://ftp.ensembl.org/pub/release-84/gtf/homo_sapiens/Homo_sapiens.GRCh38.84.gtf.gz",
             "-P", dir_fa_gtf]
    query_2 = ["gunzip", dir_gtf_file]
    if not os.path.isfile(dir_gtf_file):
        try:
            sub.run(query)
            sub.run(query_2)
        except sub.CalledProcessError as e:
            print("Oeps, there went something wrong! Check if the directory exists.\n{}".format(e))
    else:
        print('The gtf file is already in your given directory.')
    return 0


def fastaprocessing(dir_fa_gtf):
    """create indexed reference genomes"""
    file_name_dict = "Homo_sapiens.GRCh38.dna.primary_assembly.dict"
    file_name_fai = "Homo_sapiens.GRCh38.dna.primary_assembly.fa.fai"
    dir_fa_file = '{}Homo_sapiens.GRCh38.dna.primary_assembly.fa'.format(dir_fa_gtf)
    picard_tool = "lib/Picard_2.23.9/picard.jar"
    query_dict = ["java", "-jar", picard_tool, "CreateSequenceDictionary", "R=" + dir_fa_file,
                  "O=" + dir_fa_gtf + file_name_dict]
    query_fai = ["samtools", "faidx", dir_fa_file]
    # It is determined if the fasta.dict has been created already
    if not os.path.isfile(dir_fa_gtf + file_name_dict):
        # If this is not the case, the file will be created
        sub.run(query_dict)

    else:
        print('The dict file is already in your given directory.')
    # It is determined if the fasta.fa.fai has been created already
    if not os.path.isfile(dir_fa_gtf + file_name_fai):
        # If this is not the case, the file will be created
        sub.run(query_fai)
    else:
        print('The fa.fai file is already in your given directory.')

        return 0


def execute(outputDir):
    """execute multiple functions"""
    dir_hisat = outputDir + '/genome/hisat2/'
    dir_fa_gtf = outputDir + '/genome/'
    hisat_index(dir_hisat)
    genome_rtf(dir_fa_gtf)
    human_genome_file(dir_fa_gtf)
    fastaprocessing(dir_fa_gtf)


def main():
    """main function"""
    outputDir = ''
    execute(outputDir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
