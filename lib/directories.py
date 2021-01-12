#!/usr/bin/env python3

"""
This python script creates several directories for the other python scripts to use.
Before creating the directories it checks if they already exist.
There is a directory for the preprocessing, a directory for the data and a directory for the results.
For the main function createAllDirs to be called, an output directory must be given as an argument.
"""

# METADATA VARIABLES
__author__ = "Joost Numan"
__status__ = "Development"
__date__ = "12-01-2021"
__version__ = "v0.2"

# IMPORTS
import os


# FUNCTIONS
def build_outputdir(outputdir):
    """
    Check if the output directory already exists, otherwise create it.
    """
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)


def extend_outputdir(outputdir):
    """
    Check if the preprocessing folder already exists, if this is not the
    case. Create this directory.
    Add timmed, aligned, sortedBam, addOrReplace, mergeSam and markDuplicates folders
    """
    if not os.path.exists(outputdir + "/Preprocessing/"):
        os.makedirs(outputdir + "/Preprocessing/")
        os.makedirs(outputdir + "/Preprocessing/trimmed")
        os.makedirs(outputdir + "/Preprocessing/aligned")
        os.makedirs(outputdir + "/Preprocessing/sortedBam")
        os.makedirs(outputdir + "/Preprocessing/addOrReplace")
        os.makedirs(outputdir + "/Preprocessing/mergeSam")
        os.makedirs(outputdir + "/Preprocessing/markDuplicates")
        os.makedirs(outputdir + "/Preprocessing/toolLogs")


def create_resultdir(outputdir):
    """
    Check if the results directory exists, otherwise create it.
    Add alignment, fastQC, multiQC and finalPDF folders.
    """
    if not os.path.exists(outputdir + "/Results/"):
        os.makedirs(outputdir + "/Results/")
        os.makedirs(outputdir + "/Results/alignment")
        os.makedirs(outputdir + "/Results/fastQC")
        os.makedirs(outputdir + "/Results/multiQC")
        os.makedirs(outputdir + "/Results/finalPDF")


def create_datadir(outputdir):
    """
    Check if the Data directory exists, otherwise create it.
    Add fastqfiles and counts folders.
    """
    if not os.path.exists(outputdir + "/Data/"):
        os.makedirs(outputdir + "/Data/")
        os.makedirs(outputdir + "/Data/fastqFiles")
        os.makedirs(outputdir + "/Data/counts")
        os.makedirs(outputdir + "/Data/genome")
        os.makedirs(outputdir + "/Data/genome/hisat2")


def create_alldirs(outputdir):
    """
    Main function to create all directories
    """
    build_outputdir(outputdir)
    extend_outputdir(outputdir)
    create_resultdir(outputdir)
    create_datadir(outputdir)


if __name__ == "__main__":
    DIRECTORY = "./"
    create_alldirs(DIRECTORY)