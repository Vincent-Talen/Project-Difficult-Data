# Alignment pipeline for sequenced data
**Authors:** M. Hagen, R. Meulenkamp, J. Numan, V. Talen and R. Visser  
**Date:** 29 January 2021  
**Version:** v0.2

With this pipeline you can align and check the qualities of fastq.gz files.
The end product is a multiQC pdf file where a summary about the input files can be read.

## Installation
To use this pipeline a few things will have to be prepared before running it.  
The first thing to make sure is that Python3.7 or higher should be installed, you can check by typing this into the terminal
> $ python3 --version  

If you do not have python3.7 or higher install it, below is the official Python website.
> https://www.python.org/

There are also some tools and packages required to be able to use the pipeline.  
We have made them easy to install with 'setup.sh'.  
Make sure you have access to the root of your system and simply type the following in your terminal and everything should be set.  
> $ sh setup.sh  

## Usage
This pipeline is to be used in the Linux command line with the working directory as the directory of this repository.  
The pipeline has a parser with a help menu, to see this menu use:
> $ python3.7 pipeline.py -h  

Two examples of how the pipeline can be used:
> $ python3.7 pipeline.py -i input_directory -o output_directory -p -t 1-2 -c 8  

> $ python3.7 pipeline.py -i input_directory -o output_directory  


## Support
For questions, suggestions or other related things to this repository please contact this email:  
*v.k.talen@st.hanze.nl*