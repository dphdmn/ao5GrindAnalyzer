# ao5GrindAnalyzer

``python main.py --help``
```
usage: main.py [-h] [--file FILE] [--good GOOD] [--ok OK] [--minlucky MINLUCKY] [--overlap OVERLAP]

Analyze the best attempts at setting an average of 5 (ao5) score in speedsolving, primarily in Slidysim.

optional arguments:
  -h, --help           show this help message and exit
  --file FILE          Input file containing solves from oldest to latest. Format: "SOLVE_TIME{TAB}COMPLETED".
                       SOLVE_TIME is a float or a string for skipped scrambles. COMPLETED is a string TRUE or FALSE.
                       Separator is a TAB. Default file: "input.txt"
  --good GOOD          Threshold for a good solve to start a sequence (for example, solve less than your average).
                       Default: 0.4
  --ok OK              Threshold for an ok solve (solve that you think would be nice for an average). Default: 0.5
  --minlucky MINLUCKY  Minimum amount of solves in sequnce to print (from 0 to 4). Default: 1
  --overlap OVERLAP    1 to allow sequence overlapping, 0 to not allow (can help finding certain averages). Default: 1
```
