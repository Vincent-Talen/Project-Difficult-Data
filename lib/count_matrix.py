#!/usr/bin/env python3

"""
This python module runs the featureCounts tool to create a count matrix file.
It requires the output directory and the amount of cores for multiprocessing
"""


# METADATA VARIABLES
__author__ = "Joost Numan and Vincent Talen"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.4"


# IMPORTS
import sys
import glob
from subprocess import run
import lib.general_functions as gen_func


# FUNCTIONS
def run_feature_counts(cores, output_dir):
    """
    This method runs the feature counts tool and captures the output

    :param cores: The amount of cores the feature counts tool needs to use
    :param output_dir: The path of the output directory
    """
    feature_count_loc = "lib/Subread-2.0.1/bin/featureCounts"
    anno_file = f"{output_dir}/Data/genome/Homo_sapiens.GRCh38.84.gtf"
    files = glob.glob(f"{output_dir}/Preprocessing/markDuplicates/*_sorted.bam")

    query = [feature_count_loc, "-a", anno_file, "-T", str(cores),
             "-o", f"{output_dir}/Data/counts/geneCounts.txt", *files]
    executed_process = run(query, capture_output=True, text=True)

    # Save all logs from stdout and stderr to a logfile
    log_dir = f"{output_dir}/tool_logs"
    gen_func.save_tool_log(executed_process, f"{log_dir}/feature_counts.log")


# MAIN
def main():
    """Main function calling forth all tasks"""
    run_feature_counts(32, "../../../students/2020-2021/Thema06/groepje3/temp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
