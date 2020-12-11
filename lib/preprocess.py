#!/usr/bin/env python3

"""
The module is to be used between the
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "10-12-2020"
__version__ = "v0.3.4"

# IMPORTS
import sys
from glob import glob
from pathlib import Path
from subprocess import run
from termcolor import colored


class PreProcess:
    def __init__(self, output_dir):
        """
        Constructor for the PreProcess class

        :param output_dir: The directory the user gave for all the output files to be saved in
        """
        self.working_dir = f"{output_dir}/Preprocessing"

    def _gather_files(self):
        """
        This method gathers all the .BAM files in the given output directory.

        :return: A list with all the bam files found in the output directory
        """
        files = list()
        for aligned_file in glob(f"{self.working_dir}/aligned/*.bam"):
            files.append(Path(aligned_file).stem)  # Path.stem collects the name without extension
        return files

    @staticmethod
    def save_tool_log(output, log_file_name):
        """
        Small method saving the log of a tool to a file.

        :param output: The output from the tool that needs to be saved
        :param log_file_name: The name of the file the output needs to be saved in
        """
        with open(log_file_name, "w") as opened_log_file:
            print(output, file=opened_log_file)

    def run_tool(self, current_file, tool_name, query):
        """
        This method can be used to run a tool/process, it calls it through the command line.

        :param current_file: The file this tool needs to be run on
        :param tool_name: The tool that needs to be executed
        :param query: The query used to execute the tool
        """
        print(colored(f"\tStarting {tool_name} for {current_file}", "cyan"))
        executed_process = run(query, capture_output=True, text=True)

        # TODO: Make the logfiles working (doesn't save the outputs yet)
        save_tool_dir = f"{self.working_dir}/toolLogs/{current_file}"
        self.save_tool_log(executed_process.stdout, f"{save_tool_dir}_{tool_name}.txt")
        done_string = colored(f"{tool_name} for {current_file} finished.", "green")
        print(f"\t{done_string} Saved logfile {current_file}_{tool_name}.txt")

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

    def preprocess_files(self):
        """This method is for processing multiple files at once, it uses the process_file method."""
        aligned_files = self._gather_files()

        # TODO: Make it use multithreading
        for file in aligned_files:
            self.process_file(file)


# MAIN
def main():
    """Main function calling forth all tasks"""
    print("Preprocessing files...")
    pp = PreProcess("../output")
    pp.preprocess_files()
    print("Done preprocessing all files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
