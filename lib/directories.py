#!/usr/bin/env python3

"""
This module creates several directories for the rest of the pipeline to use.
Before creating the directories it checks if they already exist and if they do it deletes all files.
There are directories for preprocessing, data and results.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen and Joost Numan"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.3.6"

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

        self.download_genome = self.check_empty()

    def check_empty(self):
        """
        Checks if there already files in the genome directory and if there are ask the user
        if they want to download them again.

        :return: download_genome; Returns True by default or False if files have been found
                                  and user wants to use the existing ones
        """
        if len(os.listdir(self.output_dir)) > 0:
            choice = input("\tThe output directory is not empty, do you want to proceed and "
                           "delete everything from it?\n\t[Y/N]: ").upper()
            if choice == "Y":
                remove_dirs = ["Preprocessing", "Results", "tool_logs",
                               "Data/fastqFiles", "Data/counts"]
                for directory in remove_dirs:
                    if os.path.exists(f"{self.output_dir}/{directory}"):
                        run(["rm", "-r", f"{self.output_dir}/{directory}"])

                if len(os.listdir(f"{self.output_dir}/Data/genome")) > 0:
                    choice = input("\tIt appears you still have some genome reference files, "
                                   "do you want to keep the existing ones?\n\t"
                                   "(If you don't want to download them (again) make sure that the "
                                   "pipeline has been run before and you have not changed anything "
                                   "in the Data/genome directory.\n\t[Y/N]: ").upper()
                    if choice == "Y":
                        return False
                    else:
                        run(["rm", "-r", f"{self.output_dir}/Data/genome"])
                        print()
                        return True
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
        result_dirs = ["fastQC", "multiQC"]
        data_dirs = ["counts"]
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
        return self.download_genome


# MAIN
def main():
    """Main function to test functionality of the module"""
    directory = "output"
    create_dirs = CreateDirs(directory)
    create_dirs.create_all_dirs()


if __name__ == "__main__":
    sys.exit(main())
