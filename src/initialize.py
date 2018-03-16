import sys
import mysql.connector as sql
from collections import defaultdict

if(len(sys.argv) != 3):
        print("usage: python initialize.py <input_database> <output_database>")
        exit()


#Information about the database to be accessed
host='localhost'
user='root'
passwd='nosrebob'
db='grsecure_log'


#Connect to sql database
conn = sql.connect(host=host, user=user, passwd=passwd, db=db)
conn.text_factory = str
cur = conn.cursor()

#globals
INPUT_TABLE = str(sys.argv[1])  # Input to be read in--initial table of training data
OUTPUT_TABLE = str(sys.argv[2])	# Output table to insert frequencies/classifications of data into

commandList = list()
commandFQ = defaultdict( int )
commandClass = dict()
commandProb = dict()
ANOMALY_THRESHOLD = 0.0

#pull the list of commands from the database and turn it into a list of string
def getCommands():
	global commandList
	cur.execute("SELECT command FROM " + INPUT_TABLE)	
	c = cur.fetchall()
	for item in c:
		item = item[0] #item[0] turns tuple of single string into a string
		commandList.append(item)

#get the frequencies of each command
def initialLearn():
	global commandList
	global commandFQ
	global commandProb
	global ANOMALY_THRESHOLD
	total = 0
 
	for cmd in commandList:
		commandFQ[cmd] = commandFQ[cmd] + 1
		
	for cmd in commandList:
		total = total + commandFQ[cmd]

	for cmd, freq in commandFQ.iteritems():
		commandProb[cmd] = float(freq)/total

	ANOMALY_THRESHOLD = 1.0/total


#decide which commands are anomolies based on the probability of the command and the set threshold
def fetchAnomalies():
	global commandClass
	for k,v in commandProb.iteritems():
		if v <= ANOMALY_THRESHOLD:
			commandClass[k] = 'anomaly'
		else:
			commandClass[k] = 'normal'

#update the frequency table in the database with the "learned" values from the initial dataset
def updateDictTable():
	for cmd in commandFQ.keys():
		cur.execute("INSERT INTO " + OUTPUT_TABLE + " VALUE (\'" + cmd + "\', " + str(commandFQ[cmd]) + ", \'" + commandClass[cmd] + "\')")
		conn.commit()

#read in data, learn and classify, and upload frquencies and classifications to server
getCommands()
initialLearn()
fetchAnomalies()
updateDictTable()


