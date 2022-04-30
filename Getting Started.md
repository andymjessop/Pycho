## Echo Basics
The primary class in Echo is the Record; an object containing:
    - The data for the record. Both an abscissa, an ordinate, and other datums can be stored (so long as they’re the same length as the original abscissa)
    - The units for the record. Currently, units are just a string needed for plotting, but more support is coming
    - A time stamp associated with the Record. Any time abscissa will associate this time as the 0 time for plotting on absolute scales.
    - The labels associated, which can be used for seeking records from a larger set.
    - The quantities, another term used in plotting (so you can note that a temperature is ‘Indoor Temperature’ or ‘Outdoor Temp’, for example)
    - The coordinates (not currently supported in Pycho, but supported in Echo)
   
Multiple Records are stored in a RecordArray, which allows for operations to be performed on groups of Records. A Pycho RecordArray, which must be instantiated independently of the Records themselves, functions similar to a normal array but also allows for pulling, pushing, and group operations.

Currently in Pycho, a Record must be instantiated by inputting a dictionary of datums to be used, for example:
`D = p.Record({‘x’:[1,2,3,4,5]})`
During instantiation, `Units`, `Labels`, `Quantity`, and `TimeStamp` are optional inputs:
    - `Units` and `Quantity` must be given as a dictionary of strings with keys matching the datums.
    - `TimeStamp` must be a datetime object.
    - `Labels` is a dictionary, with the keys containing the labels and the values as a string or number. If multiple values must be input under the same label, they can be an array or a set but they will automatically be added to a set (note that they cannot be arranged in any order as a set). See the “Developer Info” for how labels are formatted.
So, a sample Record formulation with all data is:
```
import pycho as p
import datetime as dt
D=p.Record({‘t’:[0,1,2,3,4],’x’:[1,2,3,4,5],
    Units={‘t’:’s’,’x’:’m’},
    TimeStamp=dt.datetime.today(),
    Labels={‘Location’:’Stairs’,’StepNames’:{‘A’,’B’,’C’}}
    )
```   
