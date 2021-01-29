#!/usr/bin/env python3

"""
This is a module that contains a class performing all the processing of a bam file.
It takes the output directory as argument and collects aligned BAM files
and sorts, groups, fixes and marks duplicate reads for all of the files.
Every file will be created into a process and multiple will run at the same time.
To use simply import the BamProcessing class and create an object from it with the output directory.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "29-12-2020"
__version__ = "v0.5"

# IMPORTS
import sys
from glob import glob
from pathlib import Path
from subprocess import run
import lib.general_functions as gen_func


class BamProcessing:
    """
    Class for processing bam files with multiple tools from packages like picard and samtools.
    """
    def __init__(self, output_dir):
        """
        Constructor for the BamProcessing class

        :param output_dir: The directory the user gave for all the output files to be saved in
        """
        self.output_dir = output_dir
        self.working_dir = f"{output_dir}/Preprocessing"

    def perform_preprocessing(self, cores):
        """
        This function will collect all the files and run the tools on them.

        :param cores: The amount of cores the processes needs to use
        """
        files = self.gather_files()

        gen_func.process_files(cores, self.process_file, files)

    def gather_files(self):
        """
        This method gathers all the .BAM files in the given working directory.

        :return: A list with all the bam files found in the working directory
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
        log_name = current_file.replace("_aligned", "")

        # run Picard SortSam (creates sorted bam alignment)
        sort_sam = [*call_picard, "SortSam",
                    "-I", f"{self.working_dir}/aligned/{current_file}.bam",
                    "-O", f"{self.working_dir}/sortedBam/{current_file}.bam",
                    "-SO", "queryname"]
        self.run_tool(log_name, "SortSam", sort_sam)

        # run Picard AddOrReplaceReadGroups (processed bam alignment)
        read_groups = [*call_picard, "AddOrReplaceReadGroups",
                       "-I", f"{self.working_dir}/sortedBam/{current_file}.bam",
                       "-O", f"{self.working_dir}/addOrReplace/{current_file}.bam",
                       "-LB", current_file, "-PU", current_file, "-SM", current_file,
                       "-PL", "illumina", "-CREATE_INDEX", "true"]
        self.run_tool(log_name, "AddOrReplaceReadGroups", read_groups)

        # run Picard FixMateInformation
        fix_mate_info = [*call_picard, "FixMateInformation",
                         "-INPUT", f"{self.working_dir}/addOrReplace/{current_file}.bam"]
        self.run_tool(log_name, "FixMateInformation", fix_mate_info)

        # run Picard MergeSamFiles (merged bam alignment)
        merge_sam = [*call_picard, "MergeSamFiles",
                     "-INPUT", f"{self.working_dir}/addOrReplace/{current_file}.bam",
                     "-OUTPUT", f"{self.working_dir}/mergeSam/{current_file}.bam",
                     "-CREATE_INDEX", "true", "-USE_THREADING", "true"]
        self.run_tool(log_name, "MergeSamFiles", merge_sam)

        # run Picard MarkDuplicates (created duplicates log)
        mark_dupes = [*call_picard, "MarkDuplicates",
                      "-INPUT", f"{self.working_dir}/mergeSam/{current_file}.bam",
                      "-OUTPUT", f"{self.working_dir}/markDuplicates/{current_file}.bam",
                      "-CREATE_INDEX", "true", "-METRICS_FILE",
                      f"{self.working_dir}/markDuplicates/{current_file}.metrics.log"]
        self.run_tool(log_name, "MarkDuplicates", mark_dupes)

        # run SamTools Sort (FINAL: Sorted bam alignment)
        final_sort = ["samtools", "sort",
                      "-n", f"{self.working_dir}/markDuplicates/{current_file}.bam",
                      "-o", f"{self.working_dir}/markDuplicates/{current_file}_sorted.bam"]
        self.run_tool(log_name, "SamtoolsSort", final_sort)

    def run_tool(self, log_name, tool_name, query):
        """
        This method can be used to run a tool/process, it calls it through the command line.

        :param log_name: The name of the file without extensions and '_aligned'
        :param tool_name: The tool that needs to be executed
        :param query: The query used to execute the tool
        """
        gen_func.print_tool(log_name, "s", tool_name)

        executed_process = run(query, capture_output=True, text=True)  # Run the tool

        save_tool_dir = f"{self.output_dir}/tool_logs/preprocessing/{log_name}"
        gen_func.save_tool_log(executed_process, f"{save_tool_dir}_{tool_name}.log")

        gen_func.print_tool(log_name, "f", tool_name)


# MAIN
def main():
    """Main function calling forth all tasks"""
    print("Processing bam files...")
    bam_pro = BamProcessing("../output")
    bam_pro.perform_preprocessing(32)
    print("Done processing all bam files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
