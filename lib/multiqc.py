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


class RunMultiQC:
    """"""
    def perform_multiqc(self):
        pass


# MAIN
def main():
    """Main function calling forth all tasks"""
    multiqc = RunMultiQC()
    multiqc.perform_multiqc()
    return 0


if __name__ == "__main__":
    sys.exit(main())
