# Lightsys_IDS_Exec

This project uses a Bayesian method to calculate anomalies from data given in grsec execution data logs.

## Getting Started

### Creating Databases
Create databases using 
```sql
source createTables.sql
```
in mysql

### Parsing Data
*usage: python parseData.py <'database'> <'relative/path/to/file'>*

ex: `python parseData.py dev1 testFile`

### Calculate Anomalies

Setup databases

Initial Training:

Use `parseData.py` to fill in dev1 table using chosen past log files

Repeat above for as many log files as necessary in order to gurantee accurate initial training data

Use `initalize.py` that pulls information from dev1 to make analysis as to what is and isn't anomalous.

ex: `python initialize.py dev1 master_val`


Live anomaly detection:

Use parseData.py to fill dev2 with single log file that contains the logs to officially test

ex: `python parseData.py dev2 testFile2

Use learn.py to calucate any anomalies in the chosen log file

ex: `python learn.py dev2 master_val`

The contents will be outputted to anomalies.txt

Then run the command: 

```sql
source moveData.sql
```
in mysql




## Authors

* **Kyle Hansen** - Bayesian anomaly calculation
* **John Wolfe** - Database creation
* **Breven Hettinger** - Parsing data

## Possible Improvements
* Adding more attributes on learning algorithm
* Including 'chroot' in parser
