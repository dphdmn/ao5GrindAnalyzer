# ao5GrindAnalyzer

``python main.py --help``
```
usage: main.py [-h] [--file FILE] [--good GOOD] [--ok OK] [--minlucky MINLUCKY]

Classify sequences of solves.

optional arguments:
  -h, --help           show this help message and exit
  --file FILE          Input file containing solves from oldest to latest. Format: "SOLVE_TIME{TAB}COMPLETED".
                       SOLVE_TIME is a float or a string for skipped scrambles. COMPLETED is a string TRUE or FALSE.
                       Separator is a TAB.
  --good GOOD          Threshold for a good solve to start a sequence (for example, solve less than your average).
  --ok OK              Threshold for an ok solve (solve that you think would be nice for an average).
  --minlucky MINLUCKY  Minimum amount of solves in sequnce to print (from 0 to 4)
```
