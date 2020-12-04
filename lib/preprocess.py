#!/usr/bin/env python3

"""
This module is now under development

The module is to be used between the
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Development"
__date__ = "04-12-2020"
__version__ = "v0.1"

# IMPORTS
import sys


class PreProcess:
    """"""
    def __init__(self):
        """Constructor for the PreProcess class"""
        pass

    def preprocess(self):
        # Picard SortSam (creates sorted bam alignment)
        # Picard AddOrReplaceReadGroups (processed bam alignment)
        # Picard FixMateInformation
        # Picard MergeSamFiles (merged bam alignment)
        # Picard MarkDuplicates (created duplicates log)
        # SamTools Sort (FINAL: Sorted bam alignment)
        pass


# MAIN
def main():
    """Main function calling forth all tasks"""
    pp = PreProcess()
    pp.preprocess()
    return 0


if __name__ == "__main__":
    sys.exit(main())
