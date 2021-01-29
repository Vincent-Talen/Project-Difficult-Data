#!/usr/bin/env python3

"""
This python module runs the multiQC tool, it requires the target output directory location.
This module searches the entire output directory for other tool results
and uses them to create an html result file.
The results will be written to the outputdirectory/Results/multiQC directory
"""


# METADATA VARIABLES
__author__ = "Joost Numan"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.3.2"


# IMPORTS
import sys
from subprocess import run
import lib.general_functions as gen_func


# FUNCTIONS
def perform_multiqc(output_dir):
    """
    this function creates a query for running the multiQC tool
    the query is run in the terminal by using the library subprocess
    the log from the multiQC tool is captured

    :param :output_dir is the directory for the output
    """
    print("Starting MultiQC")
    query = ["multiqc", output_dir, "--pdf", "-o", f"{output_dir}/Results/multiQC"]
    executed_process = run(query, capture_output=True, text=True)

    # Save all logs from stdout and stderr to a logfile
    gen_func.save_tool_log(executed_process, f"{output_dir}/tool_logs/multiQC_log.txt")
    print("Finished MultiQC")


# MAIN
def main():
    """Main function to test module"""
    perform_multiqc(".")


if __name__ == "__main__":
    sys.exit(main())
