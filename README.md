# Pycho

*A (barely-functional) method for data analysis and plotting*

### Description

Pycho is a Python-based implementation of [Echo](https://github.com/lanl/EchoDemo), a MATLAB-based software package developed by Los Alamos National Laboratory (LANL) for data analysis and plotting.  Pycho is developed entirely as a hobbyist project and is not affiliated with LANL, the DOE, or NNSA.

For the time being, all Echo can do is read MATLAB-derived Echo files and plot them. But check out "To-Do" for the roadmap of what should be coming.

### Features

- Reads Echo-formatted HDF5 files into Python

- Performs (basic) pull and purge commands to select subsets of data

- Plots using the Bokeh package for interactive plots

### To-Do

There's a lot to be done to match feature parity with Echo; I make no claim to ever match all the functionality. But a few things on the roadmap include:

- Defining subclasses of Record for common data types (Time histories, PSDs, SRS are top on the list)

- Preserving operation history

- Support for unit conversion and cross-unit calculation

- Supporting additional plotting architectures (certainly matplotlib, maybe plotly?)







### 