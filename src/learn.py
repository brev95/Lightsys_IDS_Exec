import sys
import mysql.connector as sql
from collections import defaultdict
#Information about the database to be accessed
host='localhost'
user='root'
passwd='nosrebob'
db='grsecure_log'

# If no arguments, errors and shoes usage statement
if(len(sys.argv) != 3):
        print("usage: python learn.py <input_database> <output_database>")
        exit()

# Make connection to database
conn = sql.connect(host=host, user=user, passwd=passwd, db=db)
conn.text_factory = str
cur = conn.cursor()

# Globals
INPUT_TABLE = str(sys.argv[1])	# Table of new input data
FREQUENCY_TABLE = str(sys.argv[2])	# Table of frequency/classification values

newCommands = list()		
commandFQ = defaultdict( int )	# { <command> : <frequency> }
commandClass = dict()		# { <command> : <class> } 
classFQ = defaultdict( int )	# { <class> : <frequency> }
conditionalFQ = defaultdict(lambda: defaultdict(int)) # { <class> : { <command> : <frequency> } }
total = 0


#first query to fill dicitonaries from first dataset
def getNewCommands():
	global newCommands
	cur.execute("SELECT command FROM " + INPUT_TABLE)	
	c = cur.fetchall()
	for item in c:
		item = item[0] #item[0] turns tuple of single string into a string
		newCommands.append(item)
	

#Get the frequency table and store in memory as appropriate
def getFrequencyTable():
	global total
	cur.execute("SELECT * FROM " + FREQUENCY_TABLE)
	c = cur.fetchall()
	for items in c:
		cmd = items[0]
		freq = int(items[1])
		cls = items[2]
		
		total = total + freq
		commandFQ[cmd] = freq
		commandClass[cmd] = cls
		classFQ[cls] = classFQ[cls] + freq
		conditionalFQ[cls][cmd] = freq

# Classify new data according to bayesian classification and write lines of anomalous data to "anomalies.txt"
def bayesianClassifier():
	with open('anomalies.txt', 'w') as output:
		for cmd in set(newCommands):
			argmax = 'anomaly'
			maxVal = 0.0
			for cls in ['normal', 'anomaly']:
				clsProb = float(classFQ[cls])/total 		# P(cls) : the probability that the class is the given class
				
				# If adding more features than just commands, this will be the product of probability of all those features
				#	(i.e. Product(x_i | cls) where 'x_i' is the given feature.  
				#	For now, only x_i value is frequency of commands.
				
				cmdProb = float(conditionalFQ[cls][cmd])/classFQ[cls]	# P(x_i | cls) : the probability that the command is this one, given the current class
				
				posteriori = cmdProb*clsProb			# Poseriori = P(cls) * Product( P(x_i | cls) )

				# Find the class value that maximizes the posteriori
				if posteriori > maxVal:
					argmax = cls
					maxVal = posteriori
			
			# Set the class of the command to the class that maximizes the posteriori and if anomalous, write to output file
			commandClass[cmd] = argmax
			if argmax == 'anomaly':
				cur.execute("SELECT * FROM " + INPUT_TABLE + " WHERE command = \'" + cmd + "\'")
				lines = cur.fetchall()
				for line in lines:
					outputLine = ''
					for word in line:
						outputLine = outputLine + str(word) + ', '
					output.write(outputLine + '\b\b\n')

# Update the command frequencies from the new data
def learnFromNew():
	for cmd in newCommands:
		commandFQ[cmd] = commandFQ[cmd] + 1
		

# Update the frequency table on the server
def updateFrequencyTable():
	cur.execute("DELETE FROM " + FREQUENCY_TABLE)
	for cmd in commandFQ.keys():
		cur.execute("INSERT INTO " + FREQUENCY_TABLE + " VALUE (\'" + cmd + "\', " + str(commandFQ[cmd]) + ", \'" + commandClass[cmd]  + "\')")
		conn.commit()


# Get the new commands, and the current frequency table, then run the classifier and update frequency table
getNewCommands()
getFrequencyTable()
bayesianClassifier()
learnFromNew()
updateFrequencyTable()



