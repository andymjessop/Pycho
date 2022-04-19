from .Record import Record
from .RecordArray import RecordArray
#from .plotting.plotter import setPlotEngine


def load(foldername):
    OutputRecords = RecordArray.loadFromFolder(foldername)
    return OutputRecords
