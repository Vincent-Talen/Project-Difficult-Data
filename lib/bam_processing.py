#!/usr/bin/env python3

"""
The is a module that contains a class performing all the processing of a bam file.
It takes the output directory as argument and collects aligned BAM files
and sorts, groups, fixes and marks duplicate reads.
Every file will be created into a process and multiple will run at the same time.
To use simply import the BamProcessing class and create an object with it with the output directory.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "15-12-2020"
__version__ = "v0.4.3"

# IMPORTS
import sys
from glob import glob
from pathlib import Path
from subprocess import run
from termcolor import colored
from concurrent.futures import ProcessPoolExecutor


class BamProcessing:
    def __init__(self, output_dir):
        """
        Constructor for the PreProcess class

        :param output_dir: The directory the user gave for all the output files to be saved in
        """
        self.working_dir = f"{output_dir}/Preprocessing"
        self.files = self.gather_files()
        self.preprocess_files()

    def gather_files(self):
        """
        This method gathers all the .BAM files in the given output directory.

        :return: A list with all the bam files found in the output directory
        """
        files = list()
        for aligned_file in glob(f"{self.working_dir}/aligned/*.bam"):
            files.append(Path(aligned_file).stem)  # Path.stem collects the name without extension
        return files

    def process_file(self, current_file):
        """
        This method takes a file and performs multiple steps creating output files per step.
        These output files will be saved in the output directory under Preprocessing.
        Per step/tool there will be a log file saved in toolLogs.

        :param current_file: The file all the processes need to be run on
        """
        call_picard = ["java", "-jar", "lib/Picard_2.23.9/picard.jar"]

        # Picard SortSam (creates sorted bam alignment)
        sort_sam = [*call_picard, "SortSam",
                    "-I", f"{self.working_dir}/aligned/{current_file}.bam",
                    "-O", f"{self.working_dir}/sortedBam/{current_file}.bam",
                    "-SO", "queryname"]
        self.run_tool(current_file, "SortSam", sort_sam)

        # Picard AddOrReplaceReadGroups (processed bam alignment)
        read_groups = [*call_picard, "AddOrReplaceReadGroups",
                       "-I", f"{self.working_dir}/sortedBam/{current_file}.bam",
                       "-O", f"{self.working_dir}/addOrReplace/{current_file}.bam",
                       "-LB", current_file, "-PU", current_file, "-SM", current_file,
                       "-PL", "illumina", "-CREATE_INDEX", "true"]
        self.run_tool(current_file, "AddOrReplaceReadGroups", read_groups)

        # Picard FixMateInformation
        fix_mate_info = [*call_picard, "FixMateInformation",
                         "-INPUT", f"{self.working_dir}/addOrReplace/{current_file}.bam"]
        self.run_tool(current_file, "FixMateInformation", fix_mate_info)

        # Picard MergeSamFiles (merged bam alignment)
        merge_sam = [*call_picard, "MergeSamFiles",
                     "-INPUT", f"{self.working_dir}/addOrReplace/{current_file}.bam",
                     "-OUTPUT", f"{self.working_dir}/mergeSam/{current_file}.bam",
                     "-CREATE_INDEX", "true", "-USE_THREADING", "true"]
        self.run_tool(current_file, "MergeSamFiles", merge_sam)

        # Picard MarkDuplicates (created duplicates log)
        mark_dupes = [*call_picard, "MarkDuplicates",
                      "-INPUT", f"{self.working_dir}/mergeSam/{current_file}.bam",
                      "-OUTPUT", f"{self.working_dir}/markDuplicates/{current_file}.bam",
                      "-CREATE_INDEX", "true", "-METRICS_FILE",
                      f"{self.working_dir}/markDuplicates/{current_file}.metrics.log"]
        self.run_tool(current_file, "MarkDuplicates", mark_dupes)

        # SamTools Sort (FINAL: Sorted bam alignment)
        final_sort = ["samtools", "sort",
                      "-n", f"{self.working_dir}/markDuplicates/{current_file}.bam",
                      "-o", f"{self.working_dir}/markDuplicates/{current_file}_sorted.bam"]
        self.run_tool(current_file, "SamtoolsSort", final_sort)

    def run_tool(self, current_file, tool_name, query):
        """
        This method can be used to run a tool/process, it calls it through the command line.

        :param current_file: The file this tool needs to be run on
        :param tool_name: The tool that needs to be executed
        :param query: The query used to execute the tool
        """
        print(colored(f"\t[{current_file}] {tool_name} started.", "cyan"))  # Say the tool started
        executed_process = run(query, capture_output=True, text=True)  # Run the tool

        save_tool_dir = f"{self.working_dir}/toolLogs/{current_file}"
        save_tool_log(executed_process, f"{save_tool_dir}_{tool_name}.txt")  # Save tool logs

        done_string = colored(f"[{current_file}] {tool_name} finished", "green")
        print(f"\t{done_string} Saved logfile {current_file}_{tool_name}.txt")  # Say tool finished

    def preprocess_files(self):
        """
        This method processes multiple files at once with multiprocessing.
        Every file gets preprocessed with the process_file method.
        """
        with ProcessPoolExecutor() as executor:
            executor.map(self.process_file, self.files)


def save_tool_log(finished_process, log_file_name):
    """
    Small function that saves the logs of a tool to a file.

    :param finished_process: The finished process we want to save the outputs/errors from
    :param log_file_name: The name of the file the output needs to be saved in (with directory)
    """
    with open(log_file_name, "w") as opened_log_file:
        opened_log_file.write(finished_process.stdout)
        opened_log_file.write(finished_process.stderr)


# MAIN
def main():
    """Main function calling forth all tasks"""
    print("Processing bam files...")
    BamProcessing("../output")
    print("Done processing all bam files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
