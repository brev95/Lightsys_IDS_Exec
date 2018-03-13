import os, sys, csv

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

with open('unknown.txt', 'w') as unknown:
	with open('outputData.txt', 'w') as output:
		with open('..\delete\commands-20180311', 'r') as sampleData:
			spamreader = csv.reader(sampleData, delimiter=' ')
			
			#output.write("INSERT INTO dev1 VALUES\n")
			
			i = 0
			
			for line in spamreader:
				
				try:
					if("chroot" in line):
						output.write("('2018-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
						output.write("'" + str(line[8]).strip(':') + "',")																# IP
						output.write("'" + str(line[9]) + "',")																			# Run
						output.write("'" + str(line[11]) + "',")																		# Command
						
						index = 12
						concat = ""
						
						while(str(line[index]) != "by"):
							concat += str(line[index]) + " "
							index += 1
						
						output.write("'" + concat.lstrip('(').rstrip(" ") + "',")														# Parameters
						
						index += 2		# Increment past 'by'
						
						output.write("'" + str(line[index]) + "',")																		# Invoker
						
						index += 1		# Increment to UID/EUID
						
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# UID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# EUID
						
						index += 1		# Increment to GID/EGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# GID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")								# EGID
						
						index += 2		# Increment to parent process
						output.write("'" + str(line[index]) + "',")																		# Parent Process
						
						index += 1		# Increment to PUID/PEUID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PUID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# PEUID
						
						index += 1		# Increment to PGID/PEGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")								# PEGID
						
						
					elif(line[7] == 'From'):
						output.write("('2018-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
						output.write("'" + str(line[8]).strip(':') + "',")																# IP
						output.write("'" + str(line[9]) + "',")																			# Run
						output.write("'" + str(line[11]) + "',")																		# Command
						
						if(line[9] == 'exec'):											
							index = 12
							concat = ""
							
							while(str(line[index]) != ")"):
								concat += str(line[index]) + " "
								index += 1
						
							output.write("'" + concat.lstrip('(').rstrip(" ") + "',")													# Parameters
							
							index += 2		# Increment past 'by'
							
							output.write("'" + str(line[index]) + "',")																	# Invoker
							
							index += 1		# Increment to UID/EUID
							
							output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# UID
							output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")										# EUID
							
							index += 1		# Increment to GID/EGID
							output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# GID
							output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")							# EGID
							
							index += 2		# Increment to parent process
							output.write("'" + str(line[index]) + "',")																	# Parent Process
							
							index += 1		# Increment to PUID/PEUID
							output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# PUID
							output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")										# PEUID
							
							index += 1		# Increment to PGID/PEGID
							output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")										# PGID
							output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")							# PEGID
							
						if(line[9] == "chdir"):
							output.write("'',")																							# Parameters
							
							output.write("'" + str(line[13]) + "',")																	# Invoker
							output.write("'" + str(line[14]).split(":")[1].split("/")[0] + "',")										# UID
							output.write("'" + str(line[14]).split(":")[1].split("/")[1] + "',")										# EUID
							output.write("'" + str(line[15]).split(":")[1].split("/")[0] + "',")										# GID
							output.write("'" + str(line[15]).split(":")[1].split("/")[1].rstrip(",") + "',")							# EGID
							output.write("'" + str(line[17]) + "',")																	# Parent Process
							output.write("'" + str(line[18]).split(":")[1].split("/")[0] + "',")										# PUID
							output.write("'" + str(line[18]).split(":")[1].split("/")[1] + "',")										# PEUID
							output.write("'" + str(line[19]).split(":")[1].split("/")[0] + "',")										# PGID
							output.write("'" + str(line[19]).split(":")[1].split("/")[1].rstrip(",") + "'")								# PEGID
						
						output.write("),\n")
					
					elif(line[7] == 'exec'):
						output.write("('2018-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
						output.write("'" + '' + "',")																					# IP
						output.write("'" + str(line[7]) + "',")																			# Run
						output.write("'" + str(line[9]) + "',")																			# Command
						index = 10
						concat = ""
							
						while(str(line[index]) != "by"):																					# Parameters
							concat += str(line[index]) + " "
							index += 1
						
						output.write("'" + concat.lstrip('(').rstrip(" ").rstrip(")").rstrip(" ") + "',")
						
						index += 1		# Increment past 'by'
						output.write("'" + str(line[index]) + "',")																		# Invoker
						
						index += 1		# Increment to UID/EUID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# UID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# EUID
						
						index += 1		# Increment to GID/EGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# GID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")								# EGID
						
						index += 2		# Increment to parent process
						output.write("'" + str(line[index]) + "',")																		# Parent Process
						
						index += 1		# Increment to PUID/PEUID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PUID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# PEUID
						
						index += 1		# Increment to PGID/PEGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")								# PEGID
						
						output.write("),\n")
						
					
					elif(line[7] == 'chdir'):
						output.write("('2018-" + parseMonth(str(line[0])) + "-" + str(line[2]) + " " + str(line[3]) + "',") 			# DateTime
						output.write("'" + '' + "',")																					# IP
						output.write("'" + str(line[7]) + "',")																			# Run
						
						index = 9
						concat = ""
						while(str(line[index]) != "by"):
							concat += str(line[index]) + " "
							index += 1
						
						concat.strip(" ")
						output.write("'" + concat + "',")																				# Command
						output.write("'',")																								# Parameters
						
						index += 1
						output.write("'" + str(line[index]) + "',")																		# Invoker
						
						index += 1
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# UID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# EUID
						
						index += 1
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# GID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "',")								# EGID
						
						index += 2
						output.write("'" + str(line[index]) + "',")																		# Parent Process
						
						index += 1
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PUID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1] + "',")											# PEUID
						index += 1
						output.write("'" + str(line[index]).split(":")[1].split("/")[0] + "',")											# PGID
						output.write("'" + str(line[index]).split(":")[1].split("/")[1].rstrip(",") + "'")									# PEGID
						
						output.write("),\n")
					else:
						#print 'New statement on line ' + str(i)
						continue

					i += 1
				except IndexError:
					unknown.write(str(line) + "\n")
				
			sampleData.close()
		output.close()
	unknown.close()
		
with open('outputData.txt', 'rb+') as output:
	output.seek(-3, os.SEEK_END)
	output.truncate()
	output.close
	
with open('outputData.txt', 'a') as output:
	output.write(";")
	
	
	
#delete from dev1