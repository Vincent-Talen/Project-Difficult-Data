#!/usr/bin/env python3

"""
Module
"""

# METADATA VARIABLES
__author__ = "Vincent Talen"
__status__ = "Template"
__date__ = "02-12-2020"
__version__ = "v0.1"

# IMPORTS
import sys


class PreProcess:
    """"""
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
