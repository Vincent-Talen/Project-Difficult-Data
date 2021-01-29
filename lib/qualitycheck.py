#!/usr/bin/env python3

"""
This module contains a class for the quality check,
  the quality check will be done for every fastq.gz file in the input directory.
"""


__author__ = "Rob Meulenkamp and Vincent Talen"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.3"


import sys
import glob
from pathlib import Path
from subprocess import run
import lib.general_functions as gen_func


class QualityCheck:
    """
    The fastqc quality check can be performed through this class.
    """
    def __init__(self, input_dir, output_dir):
        """
        Constructor that assigns the parameters to the instance variables

        :param input_dir: Path to the input directory with the files that need to be quality checked
        :param output_dir: The path of the output directory
        """
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run_qualitycheck(self, cores):
        """
        Calls the fastqc tool for all the fastq.gz files in the given input directory.

        :param cores: The amount of cores the quality check needs to use
        """
        files = glob.glob(f"{self.input_dir}*fastq.gz")
        gen_func.process_files(cores, self.perform_fastqc, files)

    def perform_fastqc(self, file):
        """
        This method runs the fastqc tool on a file.

        :param file: The file the fastqc process needs to be run on
        """
        file_path = Path(file).stem
        file_name = Path(file_path).stem
        gen_func.print_tool(file_name, "s", "quality check")

        query = ["fastqc", file, "-o", f"{self.output_dir}/Results/fastQC/"]
        exe_fastqc = run(query, capture_output=True, text=True)

        log_dir = f"{self.output_dir}/tool_logs/qualitycheck"
        gen_func.save_tool_log(exe_fastqc, f"{log_dir}/{file_name}_qualitycheck.log")
        gen_func.print_tool(file_name, "f", "quality check")


def main():
    """Main function to test module functionality"""
    in_dir = "../../../students/2020-2021/Thema06/RawFiles/"
    out_dir = "../../../students/2020-2021/Thema06/groepje3/temp"
    qual_check = QualityCheck(in_dir, out_dir)
    qual_check.run_qualitycheck(32)
    return 0


if __name__ == "__main__":
    sys.exit(main())
