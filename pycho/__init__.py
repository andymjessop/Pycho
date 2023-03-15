from .Record import Record
from .RecordArray import RecordArray
#from .plotting.plotter import setPlotEngine


#define "load from folder" at the root level
def load(foldername):
    OutputRecords = RecordArray.loadFromFolder(foldername)
    return OutputRecords

#define root-level classes to simplify things
