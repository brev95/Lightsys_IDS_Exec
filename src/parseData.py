import os, sys, csv
import mysql.connector as mysql

# Variables used to connect to database. Change as necessary
hostname = 'localhost'
username = 'root'
password = 'nosrebob'
database = 'grsecure_log'

# If no arguments, errors and shows usage statement
if(len(sys.argv) != 3):
	print("usage: python parseDataFix.py <database> <relative/path/to/file>")
	exit()

db = str(sys.argv[1]) # Database to insert into

insertLines = 100 # Number of lines to insert into database at a time

iFile = str(sys.argv[2]) # File to insert into database

year = iFile.split('-')[1][:4] # Parse the file name for the year

oFile = "outputData.txt"

f = open(oFile, 'w')

# Used to insert log entries into database 
def insertDB(filenm, conn):
	curr = conn.cursor()
	curr.execute(filenm.read())

# Self explanatory. Converts month to number format
def parseMonth(month):
	if(month == "Jan"):
		return '1';
	elif(month == "Feb"):
		return '2';
	elif(month == "Mar"):
		return '3';
	elif(month == "Apr"):
		return '4';
	elif(month == "May"):
		return '5';
	elif(month == "Jun"):
		return '6';
	elif(month == "Jul"):
		return '7';
	elif(month == "Aug"):
		return '8';
	elif(month == "Sep"):
		return '9';
	elif(month == "Oct"):
		return '10';
	elif(month == "Nov"):
		return '11';
	elif(month == "Dec"):
		return '12';

# Starts connection to database
connection = mysql.connect(host = hostname, user = username, passwd = password, db = database)

with open('unknown.txt', 'w') as unknown: # Unknown formatting of log file inserted into unknown.txt
	f = open(oFile, 'w')
	with open(iFile, 'r') as sampleData:
		# Open insert and output file and read in insert file as csv
		spamreader = csv.reader(sampleData, delimiter=' ')
		
		f.write("INSERT INTO " + db + " VALUES\n")
		
		i = 0
		
		for line in spamreader:
			
			try:
				if("chroot" in str(line)): # If "chroot" is in the line, output to unknown.txt instead of outputFile.txt
					unknown.write(str(line) + "\n")
				elif(str(line).count("parent") == 0):
					unknown.write(str(line) + "\n")
				elif(str(line).count("parent") > 1):
					unknown.write(str(line) + "\n")

				# Grabs input data and parses into insert statements in outputData.txt
				elif(line[7] == 'From'):
					
					f.write("('','" + year + "-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
					f.write("'" + str(line[8]).strip(':') + "',")																# IP
					f.write("'" + str(line[9]) + "',")																			# Run
					f.write("'" + str(line[11]) + "',")																		# Command
					
					if(line[9] == 'exec'):
						index = 12
						concat = ""
						
						while(str(line[index]) != ")"):
							concat += str(line[index]) + " "
							index += 1
					
						f.write("'" + concat.lstrip('(').rstrip(" ") + "',")													# Parameters
						
						index += 2		# Increment past 'by'
						
						f.write("'" + str(line[index]) + "',")																	# Invoker
						
						index += 1		# Increment to UID/EUID
						
						f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# UID
						f.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")										# EUID
						
						index += 1		# Increment to GID/EGID
						f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# GID
						f.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")							# EGID
						
						index += 2		# Increment to parent process
						f.write("'" + str(line[index]) + "',")																	# Parent Process
						
						index += 1		# Increment to PUID/PEUID
						f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# PUID
						f.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")										# PEUID
						
						index += 1		# Increment to PGID/PEGID
						f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# PGID
						f.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")							# PEGID
						
					if(line[9] == "chdir"):
						f.write("'',")																							# Parameters
						
						f.write("'" + str(line[13]) + "',")																	# Invoker
						f.write("'" + str(line[14]).split(":")[1].split("/")[0] + "',")										# UID
						f.write("'" + str(line[14]).split(":")[1].split("/")[1] + "',")										# EUID
						f.write("'" + str(line[15]).split(":")[1].split("/")[0] + "',")										# GID
						f.write("'" + str(line[15]).split(":")[1].split("/")[1].rstrip(",") + "',")							# EGID
						f.write("'" + str(line[17]) + "',")																	# Parent Process
						f.write("'" + str(line[18]).split(":")[1].split("/")[0] + "',")										# PUID
						f.write("'" + str(line[18]).split(":")[1].split("/")[1] + "',")										# PEUID
						f.write("'" + str(line[19]).split(":")[1].split("/")[0] + "',")										# PGID
						f.write("'" + str(line[19]).split(":")[1].split("/")[1].rstrip(",") + "'")								# PEGID
					
					f.write("),\n")
				
				elif(line[7] == 'exec'):
					f.write("('','" + year + "-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
					f.write("'Server',")																							# IP
					f.write("'" + str(line[7]) + "',")																			# Run
					f.write("'" + str(line[9]) + "',")																			# Command
				
					index = 10
					concat = ""
						
					while(str(line[index]) != "by"):																					# Parameters
						concat += str(line[index]) + " "
						index += 1
					
					f.write("'" + concat.lstrip('(').rstrip(" ").rstrip(")").rstrip(" ") + "',")
					
					index += 1		# Increment past 'by'
					f.write("'" + str(line[index]) + "',")																		# Invoker
					
					index += 1		# Increment to UID/EUID
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# UID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# EUID
					
					index += 1		# Increment to GID/EGID
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# GID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")								# EGID
					
					index += 2		# Increment to parent process
					f.write("'" + str(line[index]) + "',")																		# Parent Process
					
					index += 1		# Increment to PUID/PEUID
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PUID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# PEUID
					
					index += 1		# Increment to PGID/PEGID
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PGID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")								# PEGID
					
					f.write("),\n")
					
				
				elif(line[7] == 'chdir'):
					#print(f.mode)
						
					f.write("('','" + year + "-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
					f.write("'Server',")																					# IP
					f.write("'" + str(line[7]) + "',")																			# Run
					
					index = 9
					concat = ""
					while(str(line[index]) != "by"):
						concat += str(line[index]) + " "
						index += 1
					
					concat.strip(" ")
					f.write("'" + concat + "',")																				# Command
					f.write("'',")																								# Parameters
					
					index += 1
					f.write("'" + str(line[index]) + "',")																		# Invoker
					
					index += 1
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# UID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# EUID
					
					index += 1
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# GID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")								# EGID
					
					index += 2
					f.write("'" + str(line[index]) + "',")																		# Parent Process
					
					index += 1
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PUID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# PEUID
					index += 1
					f.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PGID
					f.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")								# PEGID
					
					f.write("),\n")
				else:
					continue
   				 
				i += 1	# Line count
    
				# When line numbers == the number of lines in the insert statement, inserts into the database
				if( i % insertLines == 0 or line is None):
					f.close()
					f = open(oFile, 'rb+')
					f.seek(-2, os.SEEK_END)
					f.truncate()
					f.close
	
					f = open(oFile, 'a')
					f.write(";\n")
					
					try:
						f = open(oFile, 'r')
						connection = mysql.connect(host = hostname, user = username, passwd = password, db = database)
						filenm = f
						insertDB(filenm, connection)
						connection.commit()
						connection.close()
					except (mysql.ProgrammingError, mysql.DataError):
						pass	
					f = open(oFile, 'w')
					f.write("INSERT INTO " + db + " VALUES\n")
    
			except IndexError:
				unknown.write(str(line) + "\n")
			
		sampleData.close()
	f.close()
	unknown.close()
