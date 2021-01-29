#!/usr/bin/env python3

"""
This module will download all the required genome reference and data files and unpack them.
From the fasta reference file a dictionary and an index file about it will also be made.
"""

# METADATA VARIABLES
__author__ = "Rob Meulenkamp and Vincent Talen"
__status__ = "Development"
__date__ = "28-01-2021"
__version__ = "v0.5.4"

# IMPORTS
import os
import sys
from subprocess import run
import lib.general_functions as gen_func


class DownloadGenomeInfo:
    def __init__(self, output_dir):
        """
        Constructor for the DownloadGenomeInfo class

        :param output_dir: The directory the user gave for all the output files to be saved in
        """
        self.output_dir = output_dir
        if self.output_dir.startswith("/"):
            self.output_dir = self.output_dir[1:]
        self.genome_dir = f"{self.output_dir}/Data/genome"
        self.tool_dir = f"{self.output_dir}/tool_logs/genome_download"

    def collect_hisat_index(self):
        """
        This function downloads the HISAT index if it does not exist yet and removes compression.
        """
        hisat_query = ["wget", "-c", "-O", "-",
                       "https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz"]
        exe_hisat = run(hisat_query, capture_output=True)

        unzip_query = ["tar", "-xz", "-C", self.genome_dir]
        run(unzip_query, input=exe_hisat.stdout)

        with open(f"{self.tool_dir}/hisat_download_log.txt", "w") as opened_log_file:
            opened_log_file.write(exe_hisat.stderr.decode('UTF-8'))

    def download_and_unzip(self, link, filename, log_name):
        """
        This function will check if the genome rtf file is existent and otherwise download it.
        """
        dir_gtf_file = f"{self.genome_dir}/{filename}"

        download_query = ["wget", link, "-P", self.genome_dir]
        exe_down = run(download_query, capture_output=True, text=True)

        unzip_query = ["gunzip", dir_gtf_file]
        exe_unzip = run(unzip_query, capture_output=True, text=True)

        with open(f"{self.tool_dir}/{log_name}_log.txt", "w") as opened_log_file:
            opened_log_file.writelines([exe_down.stdout, exe_down.stderr,
                                        exe_unzip.stdout, exe_unzip.stderr])

    def process_fasta(self):
        """
        Creates the fasta dictionary and fai files with the Picard tool.
        """
        picard_tool = "lib/Picard_2.23.9/picard.jar"
        dict_file_name = "Homo_sapiens.GRCh38.dna.primary_assembly.dict"
        fa_file_name = f"{self.genome_dir}/Homo_sapiens.GRCh38.dna.primary_assembly.fa"

        query_dict = ["java", "-jar", picard_tool, "CreateSequenceDictionary",
                      "-R", fa_file_name, "-O", f"{self.genome_dir}/{dict_file_name}"]
        exe_dict = run(query_dict, capture_output=True, text=True)
        gen_func.save_tool_log(exe_dict, f"{self.tool_dir}/dict_log.txt")

        query_fai = ["samtools", "faidx", fa_file_name]
        exe_fai = run(query_fai, capture_output=True, text=True)
        gen_func.save_tool_log(exe_fai, f"{self.tool_dir}/fai_log.txt")

    def collect_all_genome_info(self, keep_genome):
        """
        This function this is the function that can be called
        to collect all the genome data with other the other functions.

        :param keep_genome: False or True, decides if all the genome files need to be downloaded
        """
        if not keep_genome:
            print("\tNow downloading the Hisat genome index")
            self.collect_hisat_index()

            print("\tFinished downloading the Hisat genome index. Now downloading annotation file")
            self.download_and_unzip("ftp://ftp.ensembl.org/pub/release-84/gtf/homo_sapiens/"
                                    "Homo_sapiens.GRCh38.84.gtf.gz", "Homo_sapiens.GRCh38.84.gtf.gz",
                                    "gtf_download")

            print("\tFinished downloading annotation file. Now downloading human reference file")
            self.download_and_unzip("ftp://ftp.ensembl.org/pub/release-84/fasta/homo_sapiens/"
                                    "dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz",
                                    "Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz",
                                    "reference_download")

            print("\tFinished downloading human reference file. Creating fasta dictionary now.")
            self.process_fasta()

            print("Done with downloading and processing all genome files.")


# MAIN
def main():
    """Main function to test functionality of the module"""
    output_dir = "../../../students/2020-2021/Thema06/groepje3/temp"
    DownloadGenomeInfo(output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
