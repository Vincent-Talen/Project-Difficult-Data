#!/usr/bin/env python3

"""
Performs the alignment via the hisat tool and converts output to a bam file using samtools view.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen and Joost Numan"
__status__ = "Development"
__date__ = "27-01-2020"
__version__ = "v0.7.5"


# IMPORTS
import glob
import gzip
from sys import exit as sys_exit
from pathlib import Path
from subprocess import run
import lib.general_functions as gen_func


class Alignment:
    """
    The actual alignment is performed through this class.
    The trimmed reads are obtained from the trimmed folder in the given output directory.
    A log from the alignment is written to the tool_logs folder and the .bam file is created
    """
    def __init__(self, cores, paired, output_dir):
        """
        Constructor that assigns the parameters to the instance variables

        :param cores: The amount of cores the alignment needs to use
        :param output_dir: The path of the output directory
        :param paired: Determines if the data is single or paired
        """
        self.cores = cores
        self.paired = paired
        self.output_dir = output_dir

        self.threads = 1
        self.hisat_index = output_dir + "/Data/genome/grch38/genome"

        # Automatically perform the alignment
        self.perform_alignment()

    def perform_alignment(self):
        """
        Perform the alignment, it will check if the user wanted paired end and will run accordingly.
        It runs multiple processes simultaneously (multiprocessing).
        """
        file_dict = self.check_files()
        self.threads = gen_func.calculate_threads(self.cores, len(file_dict.keys()))

        if self.paired:
            pairs, single_ended = self.create_pairs(file_dict)
            gen_func.process_files(self.cores, self.align_pair, pairs)
            if single_ended:  # There might be left-over files that were not in pairs
                gen_func.process_files(self.cores, self.align_single, single_ended)
        else:
            files = file_dict.keys()
            gen_func.process_files(self.cores, self.align_single, files)

    def check_files(self):
        """
        This method will collect the first line from all files and check if they are not empty.
        If the file is not empty it will put it in a dictionary with the file name as key
        and the first line (header) as value.

        :return: A dictionary with filenames as keys and first lines/headers as values
        """
        files = glob.glob(f"{self.output_dir}/Preprocessing/trimmed/*.gz")
        file_line_dict = dict()

        # Gather header lines from files and put them in a dictionary bound to the file name
        for file in files:
            first_line = gzip.open(file).readline()
            if first_line:
                file_line_dict[file] = first_line.strip().decode('UTF-8')
        return file_line_dict

    def create_pairs(self, file_line_dict):
        """
        If files need to be paired this function will look for the pair identifier in the header
        of a file and look for the corresponding file to complete the pair.

        :param file_line_dict: A dictionary with filenames as keys and first lines/headers as values
        :return: pairs: A list containing lists with the names of the files from a pair
                 single_ended: A list containing all the filenames of single ended files
        """
        single_ended = list()
        pairs = list()
        for file_name, header in file_line_dict.items():
            header = header.split()
            # Look for the identifier that a file is a part of a pair
            if header[1].endswith("/1") or header[1].endswith("/2"):
                # Both files of a pair get added simultaneously so the file should not be added yet
                if not any(file_name in pair_list for pair_list in pairs):
                    # Get the paired file of the current file
                    found_paired_file, side = self._find_pair(file_line_dict, file_name, header[0])

                    # Add the pair in the correct order or if no pair could be made add to single
                    if side == "1":
                        pairs.append([found_paired_file, file_name])
                    elif side == "2":
                        pairs.append([file_name, found_paired_file])
                    else:
                        single_ended.append(file_name)
                        print(f"[INFO] File {file_name} was paired but the paired complementary "
                              f"file could not be found so it was aligned as singled ended")
            else:
                # If there isn't an identifier indicating the file is paired add it to single_ended
                single_ended.append(file_name)
        return pairs, single_ended

    def align_single(self, file):
        """
        Used to run a single ended alignment.

        :param file: The file the alignment needs to be performed on.
        """
        file_name = Path(file).stem
        new_name = Path(file_name).stem.replace("_trimmed", "_aligned") + ".bam"

        single_query = f"hisat2 -x {self.hisat_index} -U {file} -p {str(self.threads)} | " \
                       f"samtools view -b -o {self.output_dir}/Preprocessing/aligned/{new_name}"
        self.align(single_query, file_name)

    def align_pair(self, pair):
        """
        Used to run a paired ended alignment.

        :param pair: A list containing both filenames from a pair (in correct order)
        """
        # Create 1 filename from both files of the pair
        clean_pair = list()
        for input_file in pair:
            file_name = Path(input_file).stem
            clean_name = Path(file_name).stem.replace("_trimmed", "")
            clean_pair.append(clean_name)
        new_name = "_".join(clean_pair)

        # Create and run the query for paired ended
        pair_query = f"hisat2 -x {self.hisat_index} -1 {pair[0]} -2 {pair[1]} " \
                     f"-p {str(self.threads)} | samtools view -b " \
                     f"-o {self.output_dir}/Preprocessing/aligned/{new_name}.bam"
        self.align(pair_query, new_name)

    def align(self, query, log_name):
        """
        Performs the actual alignment using the given query and creates a logfile with given name.
        It will also convert the output file from the hisat tool to bam using samtools view.

        :param query: The complete query to run the alignment with in the form of a string
        :param log_name: The basename of the file that the alignment is getting done on
        """
        # Run the hisat too and samtools view query and save the log file after
        print(f"\t[{log_name}] Starting alignment process")
        executed_process = run(query, shell=True, capture_output=True, text=True)

        # Save all logs from stdout and stderr to a logfile
        tool_dir = f"{self.output_dir}/tool_logs/preprocessing"
        gen_func.save_tool_log(executed_process, f"{tool_dir}{log_name}_log.txt")  # Save tool log
        print(f"\t[{log_name}] Finished alignment process")

    @staticmethod
    def _find_pair(dictionary, mate_name, w_full_tag):
        """
        This method tries to find the complementary file from a pair
        using the other file from the pair.
        It goes through the given dictionary and tries to match the wanted tag with another file.
        If a file is found it will return the found file's name and the read direction.

        :param dictionary: The dictionary with all the filenames as keys and file headers as values
        :param mate_name: The file you want the paired complementary file of
        :param w_full_tag: Tag from the header of the 'mate_name' file

        :return: file_name: The name of the matched file (or None if not found)
                 paired_side: 1 or 2 indicating the side of the found file (or None if not found)
        """
        wanted_tag = w_full_tag.split(".")[0]

        for file_name, header in dictionary.items():
            full_tag = header.split()[0]  # Get only the tag from the header (first item)
            tag = full_tag.split(".")[0]  # Remove read number from the tag

            # We want a matched file (and that's not itself)
            if tag == wanted_tag and mate_name != file_name:
                paired_side = header.split()[1][-1]  # Collect the side of the file in the pair
                return file_name, paired_side
        return None, None


# MAIN
def main():
    """Main function to test module"""
    output_directory = "../../../students/2020-2021/Thema06/groepje3/temp"
    paired = True

    Alignment(32, paired, output_directory)
    return 0


if __name__ == "__main__":
    sys_exit(main())
