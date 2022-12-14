#!/usr/bin/env python3

"""
This module contains multiple functions that can be used in other parts of the pipeline.
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "29-01-2021"
__version__ = "v0.2"

# IMPORTS
from math import floor
from concurrent.futures import ProcessPoolExecutor
from termcolor import colored


# FUNCTIONS
def save_tool_log(finished_process, log_file_name):
    """
    Small function that saves the logs of a tool to a file.

    :param finished_process: The finished subprocess process we want to save the outputs/errors from
    :param log_file_name: The name of the file the output needs to be saved in (with directory)
    """
    with open(log_file_name, "w") as opened_log_file:
        opened_log_file.write(finished_process.stdout)
        opened_log_file.write(finished_process.stderr)


def process_files(cores, function_name, input_list):
    """
    This method processes multiple files at once with ProcessPoolExecutor.
    Every file gets preprocessed with the process_file method.

    :param cores: The amount of wanted or available cores
    :param function_name: The name of the function you want to perform on the files
    :param input_list: The files in a list that the function needs to be run on
    """
    with ProcessPoolExecutor(max_workers=cores) as executor:
        executor.map(function_name, input_list)


def calculate_threads(cores, amt_of_files):
    """
    This function calculates the amount of threads/cores 1 file will need to be allocated.

    :param cores: The amount of wanted or available cores
    :param amt_of_files: The amount of files that the process needs to be performed on
    """
    threads = floor(cores / amt_of_files)
    if threads < 1:
        threads = 1

    return threads


def print_tool(file_name, start_finish, text):
    """
    With this function the status of what is happening to a file with a tool.

    :param file_name: The name of the file the tool is starting of has finished for
    :param start_finish: 's' for starting or 'f' for finished
    :param text: The text that needs to be printed (in color for starting and normal for finished)
    """
    if start_finish == "s":
        prefix = colored("Starting", "cyan")
    else:
        prefix = "Finished"
    print(f"\t[{file_name}]\t{prefix} {text}")
