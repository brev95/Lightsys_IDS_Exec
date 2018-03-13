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
#training_data_X = list()
#training_data_y = list()


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
    
    #Add attribute that says whether a row is duplciated anywhere else in the dataframe
    dfNoDates = df.drop('date')
    dfNoDates['normal'] = dfNoDates.duplicated(keep=False)
    anomolies = dfNoDates[dfNoDates.normal == False]
    normal = dfNoDates[dfNoDates.normal == True]
    
    anomolies_y = anomolies['normal']
    anomolies_X = anomolies.drop('normal')
    
    normal_y = normal['normal']
    normal_X = normal.drop('normal')
    
    training_X = pd.concat(anomolies_X, normal_X)
    training_y = pd.concat(anomolies_y, normal_y)
    
    X_train = vec.fit_transform(training_X)
    y_train = np.asarray(training_y)
	
	clf.fit(X_train, y_train)
    
	#predict on the new values
	predictions = clf.predict(X_test)
	for i in range(len(predictions)):
		#send message if an anomoly is found
		if predictions[i] == False:
			msg = 'anomoly detected: ' + df.iloc[[i]]

			#feedback = get_feedback(msg) #TODO: implement get_feedback(msg)
			print predictions[i]
            
            
    '''
	#Fit data to test into an appropriate format
	new_training_data = df.to_dict(orient='records')	
	X_test = vec.transform(new_training_data).toarray() #Gives the array needed for testing the new values

    #train on the new data
    training_data_X = training_data_X + new_training_data
    training_data_y = training_data_y + predictions
    '''
            
#an initial query to get the starting training_data_X and training_data_y values
initial_query = "SELECT * FROM " + table
new_data(initial_query)












