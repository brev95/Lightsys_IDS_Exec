import os, sys, csv

with open('outputData.txt', 'w') as output:
	with open('..\SampleData.txt', 'r') as sampleData:
		spamreader = csv.reader(sampleData, delimiter=' ')
		
		output.write("INSERT INTO dev1 VALUES\n")
		
		i = 0
		
		for line in spamreader:
			
			if(line[7] == 'From'):
				output.write("('" + str(line[0]) + "',") 			# Month	
				output.write("'" + str(line[2]) + "',")				# Day
				output.write("'" + str(line[3]) + "',")				# Timestamp
				output.write("'" + str(line[8]).strip(':') + "',")	# IP
				output.write("'" + str(line[9]) + "',")				# Run
				output.write("'" + str(line[11]) + "'),\n")			# Command
			
			elif(line[7] == 'exec'):
				output.write("('" + str(line[0]) + "',") 			# Month
				output.write("'" + str(line[2]) + "',")				# Day
				output.write("'" + str(line[3]) + "',")				# Timestamp
				output.write("'" + '' + "',")						# IP
				output.write("'" + str(line[7]) + "',")				# Run
				output.write("'" + str(line[9]) + "'),\n")			# Command
			
			elif(line[7] == 'chdir'):
				output.write("('" + str(line[0]) + "',") 			# Month
				output.write("'" + str(line[2]) + "',")				# Day
				output.write("'" + str(line[3]) + "',")				# Timestamp
				output.write("'" + '' + "',")						# IP
				output.write("'" + str(line[7]) + "',")				# Run
				output.write("'" + str(line[9]) + "'),\n")			# Command
				
			else:
				print 'New statement on line ' + i

			i += 1
			
		sampleData.close()
	output.close()

with open('outputData.txt', 'rb+') as output:
	output.seek(-3, os.SEEK_END)
	output.truncate()
	output.close
	
with open('outputData.txt', 'a') as output:
	output.write(";\n\n")