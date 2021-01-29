#!/usr/bin/env python3

"""
This python module runs the featureCounts tool to create a count matrix file.
It requires the output directory and the amount of cores for multiprocessing
"""


# METADATA VARIABLES
__author__ = "Joost Numan and Vincent Talen"
__status__ = "Development"
__date__ = "28-01-2021"
__version__ = "v0.3.4"


# IMPORTS
import sys
import glob
from subprocess import run
import lib.general_functions as gen_func


# FUNCTIONS
class CountMatrix:
    """
    The CountMatrix class runs the feature counts tool to create a count matrix file
    """
    def __init__(self, cores, output_dir):
        """
        Constructor that assigns the parameters to the instance variables

        :param cores: The amount of cores the feature counts tool needs to use
        :param output_dir: The path of the output directory
        """
        self.cores = cores
        self.output_dir = output_dir

        self.anno_file = output_dir + "/Data/genome/Homo_sapiens.GRCh38.84.gtf"

        # Automatically run the feature counts tool
        self.run_feature_counts()

    def run_feature_counts(self):
        """This method runs the feature counts tool and captures the output"""
        print(f"Starting Feature Counts")
        feature_count_loc = "lib/Subread-2.0.1/bin/featureCounts"
        files = glob.glob(f"{self.output_dir}/Preprocessing/markDuplicates/*_sorted.bam")

        query = [feature_count_loc, "-a", self.anno_file,  "-T", str(self.cores),
                 "-o", f"{self.output_dir}/Data/counts/geneCounts.txt", *files]
        executed_process = run(query, capture_output=True, text=True)

        # Save all logs from stdout and stderr to a logfile
        gen_func.save_tool_log(executed_process,
                               f"{self.output_dir}/tool_logs/feature_counts_log.txt")
        print(f"Finished Feature Counts")


# MAIN
def main():
    """Main function calling forth all tasks"""
    CountMatrix(20, "../../../students/2020-2021/Thema06/groepje3/temp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
