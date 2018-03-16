# Lightsys_IDS_Exec

This project uses a Bayesian method to calculate anomalies from data given in grsec execution data logs.

## Getting Started

### Creating Databases
Create databases using the statements in *createTables.txt*

### Parsing Data
*usage: python parseData.py <'database'> <'relative/path/to/file'>*

### Calculate Anomalies

Setup databases

Initial Training:

Use the parseData.py to fill in dev1 table using chosen past log files

Repeat above for as many log files as necessary in order to gurantee accurate initial training data

Use initalize.py that pulls information from dev1 to make analysis as to what is and isn't anomalous.


Live anomaly detection:

Use parseData.py to fill dev2 with single log file that contains the logs to officially test
Use learn.py to calucate any anomalies in the chosen log file
The contents will be outputted to anomalies.txt

Then run the command: 

```sql
source moveData.sql //
```





## Authors

* **Kyle Hansen** - Bayesian anomaly calculation
* **John Wolfe** - Database creation
* **Breven Hettinger** - Parsing data

## Possible Improvements
* 
