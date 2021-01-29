#!/usr/bin/env python3

"""
This python module runs the multiQC tool, it requires the target output directory location.
MultiQC searches the entire output directory for all the results and uses them to create a summary.
The resulting reports will be written to the 'output_directory/Results/multiQC' directory.
"""


# METADATA VARIABLES
__author__ = "Joost Numan"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.3.3"


# IMPORTS
import sys
from subprocess import run
import lib.general_functions as gen_func


# FUNCTIONS
def perform_multiqc(output_dir):
    """
    This function creates a query for the multiQC tool and runs it through subprocess.run
    Any output meant for the command line is caught and put in a log file in directory 'tool_logs'.

    :param :output_dir is the directory that the user has given as parameter
    """
    query = ["multiqc", output_dir, "--pdf", "-o", f"{output_dir}/Results/multiQC",
             "-c", "lib/multiqc_config.yaml"]
    executed_process = run(query, capture_output=True, text=True)

    # Save all logs from stdout and stderr to a logfile
    gen_func.save_tool_log(executed_process, f"{output_dir}/tool_logs/multiQC.log")


# MAIN
def main():
    """Main function to test module"""
    perform_multiqc(".")


if __name__ == "__main__":
    sys.exit(main())
