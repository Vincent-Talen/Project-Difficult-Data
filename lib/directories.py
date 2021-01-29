#!/usr/bin/env python3

"""
This module creates several directories for the rest of the pipeline to use.
Before creating the directories it checks if they already exist and if they do it deletes all files.
There are directories for preprocessing, data and results.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen and Joost Numan"
__status__ = "Development"
__date__ = "28-01-2021"
__version__ = "v0.3.5"

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
        """
        Constructor for the CreateDirs class

        :param output_dir: The directory the user gave for all the output files to be saved in
        """
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

        self.keep_genome = self.check_empty()

    def check_empty(self):
        """

        :return: keep_genome; False or True if the user wants to keep genome files
        """
        if len(os.listdir(self.output_dir)) > 0:
            choice = input("The output directory is not empty, do you want to proceed and "
                           "delete everything from it? [Y/N]:\n").upper()
            if choice == "Y":
                remove_dirs = ["Preprocessing", "Results", "tool_logs",
                               "Data/fastqFiles", "Data/counts"]
                for directory in remove_dirs:
                    if os.path.exists(f"{self.output_dir}/{directory}"):
                        run(["rm", "-r", f"{self.output_dir}/{directory}"])

                if len(os.listdir(f"{self.output_dir}/Data/genome")) > 0:
                    choice = input("It appears you still have some genome reference files, "
                                   "do you want to download them again? "
                                   "(If you answer no, you should have ran this pipeline before "
                                   "and not changed anything in the /Data/genome directory) "
                                   "[Y/N]:\n").upper()  # TODO
                    if choice == "Y":
                        run(["rm", "-r", f"{self.output_dir}/Data/genome"])
                        return False
            else:
                sys.exit("You chose not to empty the given output directory "
                         "so the pipeline has been terminated")
        return True

    def create_dir_dict(self):
        """
        Generates the dictionary with all the directories that need to be made

        :return: A dictionary with all the dictionaries that need to be created
                 with main dirs as keys and sub dirs in a list as values
        """
        preprocessing_dirs = ["trimmed", "aligned", "sortedBam", "addOrReplace",
                              "mergeSam", "markDuplicates"]
        result_dirs = ["fastQC", "multiQC", "finalPDF"]
        data_dirs = ["fastqFiles", "counts"]
        if not os.path.isdir(f"{self.output_dir}/Data/genome"):
            data_dirs.append("genome")
        log_dirs = ["preprocessing", "genome_download", "qualitycheck"]

        dir_dict = {"Preprocessing": preprocessing_dirs, "Results": result_dirs,
                    "Data": data_dirs, "tool_logs": log_dirs}
        return dir_dict

    def create_all_dirs(self):
        """This method creates all the directories from a dictionary."""
        dir_dict = self.create_dir_dict()
        for main_dir, sub_dirs in dir_dict.items():
            for sub_dir in sub_dirs:
                os.makedirs(f"{self.output_dir}/{main_dir}/{sub_dir}")
        return self.keep_genome


# MAIN
def main():
    """Main function to test functionality of the module"""
    directory = "output"
    create_dirs = CreateDirs(directory)
    keep_genome = create_dirs.create_all_dirs()


if __name__ == "__main__":
    sys.exit(main())
