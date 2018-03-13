import pandas as pd
import mysql.connector as sql 
from sklearn.naive_bayes import MultinomialNB as MNB 
from sklearn.feature_extraction import DictVectorizer as DV
import numpy as np


#Make a classifier to train
clf = MNB()

#Make a vector that will transform all data into a usable format
vec = DV()

#A list to contain all the dictionaries of training data
training_data_X = list()
training_data_y = list()

#run predictions and train algorithm on new data
def new_data(query):
	#TODO make this secure
	#Information about the database to be accessed
	host='localhost'
	user='root'
	passwd='nosrebob'
	db='grsecure_log'
	table='dev1'

	#Connect to sql database and read table into a pandas dataframe
	db_connection = sql.connect(host=host, user=user, passwd=passwd, db=db)
	df = pd.read_sql(query, con=db_connection, parse_dates=['date'])

	#Fit data to test into an appropriate format
	new_training_data = df.to_dict(orient='records')	
	X_test = vec.transform(new_training_data).toarray() #Gives the array needed for testing the new values

	#predict on the new values
	predictions = clf.predict(X_test)
	for i in range(len(predictions)):
		#send message if an anomoly is found
		if predictions[i] == 0:
			msg = 'anomoly detected: ' + df.iloc[[i]]

			feedback = get_feedback(msg) #TODO: implement get_feedback(msg)
			predictions[i] = feedback

	#train on the new data
	training_data_X = training_data_X + new_training_data
	training_data_y = training_data_y + predictions

	X_train = vec.fit_transform(training_data_X).to_array() #Fits the vector to include the new data within the testing values
	y_train = np.asarray(training_data_y)#TODO: find a way to get the initial training values
	
	clf.fit(X_train, y_train)

#an initial query to get the starting training_data_X and training_data_y values
initial_query = "SELECT * FROM " + table + " WHERE date <= '2018-02-28 23:59:59' AND date >= '2018-02-01 00:00:00'"













