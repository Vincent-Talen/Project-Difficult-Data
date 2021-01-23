#!/usr/bin/env python3

"""
This module creates several directories for the rest of the pipeline to use.
Before creating the directories it checks if they already exist and if they do it deletes all files.
There are directories for preprocessing, data and results.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "22-01-2021"
__version__ = "v0.3.1"

# IMPORTS
import os
import sys
from subprocess import run


class CreateDirs:
    """
    Class to create wanted directories, only takes an output directory
    where everything needs to be made as an argument
    """
    def __init__(self, output_dir):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

        if len(os.listdir(output_dir)) > 0:
            choice = input("The output directory is not empty, do you want to proceed and "
                           "delete everything from it? [Y/N]: ").upper()
            if choice == "Y":
                run(["rm", "-rf", f"{output_dir}/*"])
            else:
                sys.exit("You chose not to empty the given output directory "
                         "so the pipeline has been terminated")

        # Automatically create all directories
        self.create_dirs(self.all_dirs())

    @staticmethod
    def all_dirs():
        """Generates the dictionary with all the directories that need to be made"""
        preprocessing_dirs = ["trimmed", "aligned", "sortedBam", "addOrReplace",
                              "mergeSam", "markDuplicates", "toolLogs"]
        result_dirs = ["alignment", "fastQC", "multiQC", "finalPDF"]
        data_dirs = ["fastqFiles", "counts", "genome", "genome/hisat2"]

        dir_dict = {"Preprocessing": preprocessing_dirs, "Results": result_dirs, "Data": data_dirs}
        return dir_dict

    def create_dirs(self, dir_dict):
        """
        This method creates all the directories from a dictionary.

        :param dir_dict: A dictionary with pairs like main_dir: sub_dir_list
        """
        for main_dir, sub_dirs in dir_dict.items():
            for sub_dir in sub_dirs:
                os.makedirs(f"{self.output_dir}/{main_dir}/{sub_dir}")


# MAIN
def main():
    """Main function to test functionality of the module"""
    directory = "output"
    CreateDirs(directory)


if __name__ == "__main__":
    sys.exit(main())
