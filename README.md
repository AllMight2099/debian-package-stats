# Debian Package Statistics: pkg-stats

## Problem Statement


Debian uses *deb packages to deploy and upgrade software. The packages
are stored in repositories and each repository contains the so called "Contents
index". The format of that file is well described here
https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices


Your task is to develop a python command line tool that takes the
architecture (amd64, arm64, mips etc.) as an argument and downloads the
compressed Contents file associated with it from a Debian mirror. The program should parse the file and output the statistics of the top 10
packages that have the most files associated with them.
An example output could be:


```bash 
./package_statistics.py amd64

1. <package name 1> <number of files>
2. <package name 2> <number of files>
......
10. <package name 10> <number of files>
```

You can use the following Debian mirror
http://ftp.uk.debian.org/debian/dists/stable/main/. Please try to
follow Python's best practices in your solution. Hint: there are tools
that can help you verify your code is compliant.

## Installation

1. To install the pkg locally, first create a virtual environment and install dependencies using pip

2. Run `python setup.py develop` to install `pkg-stats` locally

## Usage
```
pkg-stats [-h] [-m MIRROR] [-i] [-a] [-n NUMBER] arch

Displays stats for debian packages of a particular architecture

positional arguments:
  arch                  Input system architecture. Eg: arm, amd64, etc

optional arguments:
  -h, --help            show this help message and exit
  -m MIRROR, --mirror MIRROR
                        Mirror link to fetch package information from. Defaults to debian's mirror
  -i, --include-udeb    Flag to include stats of udeb packages of the procided architecture
  -a, --all             Finds package stats for all distributions
  -n NUMBER, --number NUMBER
                        Input to display the top 'n' packages
```
