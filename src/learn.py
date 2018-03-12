import pandas as pd
import mysql.connector as sql
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.feature_extraction import DictVectorizer as DV
import numpy as np

#Information about the database to be accessed
host='localhost'
user='root'
passwd='nosrebob'
db='grsecure_log'
tablename='dev1'

#Connect to sql database and read table into a pandas dataframe
db_connection = sql.connect(host=host, user=user, passwd=passwd, db=db)
df = pd.read_sql('SELECT * FROM '+tablename, con=db_connection, parse_dates=['date'])

#turn pandas dataframe into dictionary usable by sklearn
dfDict = df.to_dict()

#select all data from the month of February as training data
trainingData = df.query(df.time.to_datetime().month = 2)
tdDict = trainingData.to_dict()

#TODO 
#insert training values into 'y' as an array of values (i.e. 0 and 1, 0 for 'anomoly', 1 for 'normal')
y_train = np.asarray(categorize(trainingData))

#Make training data usable by sklearn
vec = DV()
X_train = [tdDict]
X_train = vec.fit_transform(X_train).toarray()

#Make a classifier to train
clf = MNB()

#Train classifier
training = clf.fit(X_train, y_train)

#Make prediction data usable by sklearn
X_predict = [dfDict]
X_predict = vec.fit_transform(X_predict).toarray()

#Predict classifications of all data
predictions = clf.predict(X_predict)

print predictions



