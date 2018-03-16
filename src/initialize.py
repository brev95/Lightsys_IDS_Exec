import sys
import mysql.connector as sql
from collections import defaultdict

# If no arguments, errors and shoes usage statement
if(len(sys.argv) != 3):
        print("usage: python initialize.py <input_database> <output_database>")
        exit()

# Information about the database to be accessed
host='localhost'
user='root'
passwd='nosrebob'
db='grsecure_log'

# Make connection to database
conn = sql.connect(host=host, user=user, passwd=passwd, db=db)
conn.text_factory = str
cur = conn.cursor()

# Globals
INPUT_TABLE = str(sys.argv[1]) # Input to be read in -- initial table of training data
FREQUENCY_TABLE = str(sys.argv[2]) # Output table to insert frequencies/classifications of data into

ANOMALY_THRESHOLD = 1           # Positive integer indicating maximum frequency for classificatio of anomaly. Higher values indicate less sensitivity.

commandList = list()
commandFQ = defaultdict( int )
commandClass = dict()
commandProb = dict()

# Pull the list of commands from INPUT_TABLE and turn it into a list of commands
def getCommands():
        global commandList
        cur.execute("SELECT command FROM " + INPUT_TABLE)
        c = cur.fetchall()
        for item in c:
                item = item[0] 
                commandList.append(item)

# Get the frequencies of each command
def learnFrequencies():
        global commandList
        global commandFQ
        for cmd in commandList:
                commandFQ[cmd] += 1


# Label all commands which occur less than then number of times specified by ANOMALY_THRESHOLD as anomalies
def fetchAnomalies():
        global commandClass
        for cmd, freq in commandFQ.iteritems():
                if freq <= ANOMALY_THRESHOLD:
                        commandClass[cmd] = 'anomaly'
                else:
                        commandClass[cmd] = 'normal'

# Update the frequency table in the database with the values from the initial dataset
def updateFrequencyTable():
        for cmd in commandFQ.keys():
                cur.execute("INSERT INTO " + FREQUENCY_TABLE + " VALUE (\'" + cmd + "\', " + str(commandFQ[cmd]) + ", \'" + commandClass[cmd] + "\')")
                conn.commit()

# Read in data, learn and classify, and upload frquencies and classifications to server
getCommands()
learnFrequencies()
fetchAnomalies()
updateFrequencyTable()
