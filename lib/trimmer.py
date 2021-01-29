#!/usr/bin/env python3

"""
This module contains a class Trimmer that can be used to trim files.
When calling the class it will automatically perform the trimming with the given parameters.
"""

# METADATA VARIABLES
__author__ = "Michael Hagen, Vincent Talen and Joost Numan"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.7"

# IMPORTS
import sys
import glob
import re
from pathlib import Path
from subprocess import run
from termcolor import colored
import lib.general_functions as gen_func


class Trimmer:
    """The Trimmer class is a package to trim files with. It uses multiprocessing."""
    def __init__(self, trim_values, input_dir, output_dir):
        """
        Constructor for the Trimmer class

        :param trim_values: None or string with "\"3-5\" (start and end) or \"3\" (end only)"
        :param input_dir: The directory with all the files you want you use the trimmer on
        :param output_dir: The directory where all the output files need to be saved in
        """
        self.input_files = [file for file in glob.glob(input_dir + "*.gz")]
        self.output_dir = output_dir

        self.trim_values = trim_values
        self.value_type = self.check_trim_values()

    def run_trimmer(self, cores):
        """
        This method actually runs the trimmer

        :param cores: The amount of cores the trimmer needs to use
        """
        gen_func.process_files(cores, self.trim_file, self.input_files)

    def check_trim_values(self):
        """
        This method checks if the given trim values are in the correct format.
        If they are it will say in what format (no trimming, only 3' end or both end trimming)
        by returning a value_type parameter.

        :return: A variable that is 1, 2 or 3 corresponding with the order mentioned above.
        """
        if self.trim_values is None:
            # If there are no values given continue without trimming off ends
            value_type = 1
        elif re.match(r"^\d+-\d+$", self.trim_values):
            # Check if it has both start and end values and use them if they are correct
            value_type = 2
        elif re.search(r"\D+", self.trim_values) is None:
            # Checks if there are no non-digit chars and uses the value that's left as the end value
            value_type = 3
        else:
            # If the trim values given were not correct
            # ask user if they want to stop or continue without trimming
            warning = colored("WARNING", "yellow")
            print(f"\t[{warning}] Trim values incorrect, make sure the input is like "
                  "\"3-5\" (start and end) or \"3\" (end only)")

            choice = input("\tDo you want to continue pipeline without hard trimming file ends?\n\t"
                           "(If you don't say yes the pipeline will stop)\n\t[Y/N]: ").upper()
            if choice == "Y":
                value_type = 1
                info = colored("INFO", "cyan")
                print(f"\t[{info}] Continuing without hard trimming file ends!")
            else:
                terminated = colored("terminated", "red")
                print(f"You chose not to continue without trimming the files "
                      f"so the pipeline has been {terminated}")
                sys.exit(1)
        return value_type

    def trim_file(self, file):
        """
        This method performs the trimming on a file, based on the user specified trim values
        it uses different parameters for the trimming tool.

        :param file: Name of the file you want to trim with directories.
        """
        file_path = Path(file).stem
        clean_name = Path(file_path).stem
        gen_func.print_tool(clean_name, "s", "trimming process")
        trimmed_dir = f"{self.output_dir}/Preprocessing/trimmed/"
        galore_loc = "lib/TrimGalore-0.6.6/trim_galore"

        if self.value_type == 1:  # Don't trim ends
            galore_query = [galore_loc, file, "-o", trimmed_dir]

        elif self.value_type == 2:  # Both 3'- and 5' end
            trim_list = self.trim_values.split("-")
            galore_query = [galore_loc, file, "-o", trimmed_dir,
                            "--clip_R1", trim_list[0], "--three_prime_clip_R1", trim_list[1]]

        elif self.value_type == 3:  # Only 3' end
            galore_query = [galore_loc, file, "-o", trimmed_dir,
                            "--three_prime_clip_R1", self.trim_values]

        executed_process = run(galore_query, capture_output=True, text=True)

        save_tool_dir = f"{self.output_dir}/tool_logs/preprocessing"
        gen_func.save_tool_log(executed_process, f"{save_tool_dir}/{clean_name}_trimmed.log")
        gen_func.print_tool(clean_name, "f", "trimming process")


def main():
    """Main function to test the module"""
    in_dir = "../../../students/2020-2021/Thema06/RawFiles/"
    out_dir = "../../../students/2020-2021/Thema06/groepje3/temp"
    trimmer = Trimmer("4-5a", in_dir, out_dir)
    trimmer.run_trimmer(32)
    return 0


if __name__ == "__main__":
    sys.exit(main())
