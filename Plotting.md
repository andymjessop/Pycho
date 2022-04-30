#Plotting Guide

##Basics
Echo Records or RecordArrays can be plotted using `plot()`.

The optional inputs that can be given to `plot()` fall into several categories
*Label Options*
    `legendLabels`:
    `colorLabels`:
    `lineStyleLabels`:
    `subplotLabels`:
*Figure and Axis Options*
    `figSize`:
    `fontSize`:
    `xLimits` and `yLimits`:
    `xLog` and `yLog`:
    `xGrid` and `yGrid`:

*Legend Options*
    `legendOn`:
    `legendLocation`:
    `legendFontSize`:

##Plot Engine
Right now, Pycho can use two popular Python plotting packages:
    - Matplotlib
    - Bokeh
The default plot engine can be changed using pycho.setPlotEngine(). 
Regardless of the engine used, the options used stay the same. The major differences are:
    - `figureSize` will change the individual subplots in Bokeh rather than the overall plot size. 