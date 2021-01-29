#!/usr/bin/env python3

"""
Execute quality check for every fastq.gz file from the input directory.
Put the reports into the given output directory.
Containing a zip and html file.
"""


__author__ = "Rob Meulenkamp and Vincent Talen"
__status__ = "Development"
__date__ = "28-01-2021"
__version__ = "v0.2.4"


import sys
import glob
from pathlib import Path
from subprocess import run
import lib.general_functions as gen_func


class QualityCheck:
    """
    The fastqc quality check is performed through this class.
    """
    def __init__(self, cores, input_dir, output_dir):
        """
        Constructor that assigns the parameters to the instance variables

        :param cores: The amount of cores the quality check needs to use
        :param input_dir: Path to the input directory with the files that need to be quality checked
        :param output_dir: The path of the output directory
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.cores = cores

        # Automatically perform the quality check
        self.run_qualitycheck()

    def run_qualitycheck(self):
        """Calls the fastqc tool for all the fastq.gz files in the given input directory."""
        files = glob.glob(f"{self.input_dir}*fastq.gz")
        gen_func.process_files(self.cores, self.perform_fastqc, files)
        print("Finished all quality checks")

    def perform_fastqc(self, file):
        """
        This method runs the fastqc tool on a file.

        :param file: The file the fastqc process needs to be run on
        """
        file_path = Path(file)
        print(f"\t[{file_path.name}] Starting quality check")

        query = ["fastqc", file, "-o", f"{self.output_dir}/Results/fastQC/"]
        exe_fastqc = run(query, capture_output=True, text=True)

        log_dir = f"{self.output_dir}/tool_logs/qualitycheck"
        gen_func.save_tool_log(exe_fastqc, f"{log_dir}/{file_path.stem}_log.txt")
        print(f"\t[{file_path.name}] Finished quality check")


def main():
    """Main function to test module functionality"""
    cores = 20
    in_dir = "../../../students/2020-2021/Thema06/RawFiles/"
    out_dir = "../../../students/2020-2021/Thema06/groepje3/temp"
    QualityCheck(cores, in_dir, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
