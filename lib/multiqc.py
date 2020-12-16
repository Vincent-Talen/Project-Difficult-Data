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
__date__ = "09-12-2020"
__version__ = "v0.2.1"


# IMPORTS
import sys
import subprocess


# FUNCTIONS
def perform_multiqc(outputdir):
    """
    this function creates a query for running the multiQC tool
    the query is run in the terminal by using subprocess.run()
    """
    query = "multiqc {} -o {}/Results/multiQC".format(outputdir, outputdir)
    subprocess.run(query.split())


# MAIN
def main():
    """Main function calling forth all tasks"""
    perform_multiqc(".")


if __name__ == "__main__":
    sys.exit(main())
