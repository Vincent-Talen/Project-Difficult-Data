# Alignment pipeline for sequenced data
**Authors:** M. Hagen, R. Meulenkamp, J. Numan, V. Talen and R. Visser  
**Date:** 02 december 2020  
**Version:** v0.1

## Installation
To use this pipeline a few things will have to be prepared before running it, 
there are some tools and files required to be installed on the system the pipeline will be run on.

#### List of tools:
TODO: Delete the ones that don't have to be installed?
* FastQC
* Fastx_trimmer
* TrimGalore
* Picard
* GenomeHiSat2
* SAMTools
* FeatureCounts
* MultiQC

## Usage
This pipeline is to be used in the command line, it has a parser with a help.  
A standard usecase would look like:
> python3 align_data.py -s data

You have multiple arguments where you can choose the desired values like 
the organism, trim intensity,

## Support
For questions, suggestions or other support related things please contact this email:  
*v.k.talen@st.hanze.nl*