import pandas as pd
import mysql.connector as sql 
from sklearn.naive_bayes import MultinomialNB as MNB 
from sklearn.feature_extraction import DictVectorizer as DV
import numpy as np
from sklearn.externals import joblib


#A list to contain all the dictionaries of training data
#training_data_X = list()
#training_data_y = list()

#TODO make this secure
#Information about the database to be accessed
host='localhost'
user='root'
passwd='nosrebob'
db='grsecure_log'
table='dev1'

typicalIPs = ['10.254.254.0/24', '10.254.253.0/24', '204.238.168.224/27', '71.39.55.48/29', '10.5.0.0/17', '10.5.128.0/24']

#run predictions and train algorithm on new data
def train_on_data(query):
    #Make or read a classifier to train
    try:
        clf = joblib.load('clf.pkl')
    except: 
        clf = MNB()
    
    '''
    #Make or read in a vector to train
    try:
        vec = joblib.load('vec.pkl')
    except: 
        vec = DV()
        
    #Make or get values of other X values to keep training consistent
    
    try:
        old_training_X = pd.read_pickle('training_X.pkl')
    except:
        old_training_X = pd.DataFrame()
    '''
    
    #Connect to sql database and read table into a pandas dataframe
    db_connection = sql.connect(host=host, user=user, passwd=passwd, db=db)
    df = pd.read_sql(query, con=db_connection, parse_dates=['date'])
    
    #Add attribute that says whether a row is duplciated anywhere else in the dataframe
    dfNoDates = df.drop(columns='date')
    dfNoDates['normal'] = dfNoDates.duplicated(keep=False)
    
    #Make those rows with activity from accepted IPs 'normal'
    normalRows = list()
    for index, row in dfNoDates.iterrows():
        if row['ipaddr'] in typicalIPs:
            normalRows.append(index)
    
    for index in normalRows:
        dfNoDates.at[index, 'normal'] = True
    
    #Separate anomalies and normal
    for index, row in dfNoDates.iterrows():
        if row['normal']:
            dfNoDates.at[index, 'normal'] = 1
        else:
            dfNoDates.at[index, 'normal'] = 0
    
    training_X = dfNoDates.drop(columns='normal')
    training_y = dfNoDates[['normal']]
    
    #add new values to training set
    #all_vec_X = pd.concat([training_X, old_training_X])
    
    #vec.fit(all_vec_X.to_dict(orient='records'))
    
    #X_train = vec.transform(all_vec_X.to_dict(orient='records')).toarray()
    #X_train = vec.transform(training_X.to_dict(orient='records')).toarray()
    X_train = training_X.as_matrix()
    y_train = training_y.as_matrix()
	
    #train the classifier
    clf.fit(X_train, y_train)
     

    
    #all_vec_X.to_pickle('training_X.pkl')    
    joblib.dump(clf, 'clf.pkl')
    #joblib.dump(vec, 'vec.pkl')
    
    
def predict(query):
    try:
        clf = joblib.load('clf.pkl')
    except: 
        print 'classifier does not exist'
    
    #Connect to sql database and read table into a pandas dataframe
    db_connection = sql.connect(host=host, user=user, passwd=passwd, db=db)
    df = pd.read_sql(query, con=db_connection, parse_dates=['date'])
    
    #Add attribute that says whether a row is duplciated anywhere else in the dataframe
    dfNoDates = df.drop('date')
    X_test = dfNoDates.to_dict(orient='records')
    
    #predict on the new values
    predictions = clf.predict(X_test)
    for i in range(len(predictions)):
        #send message if an anomoly is found
        if predictions[i] == 0:
            msg = 'anomoly detected: ' + df.iloc[[i]]
            print msg
            
    train_on_data(query)
    
#An initiial test
train_on_data('SELECT * FROM dev1 LIMIT 10')
predict('SELECT * FROM dev1 LIMIT 30')


        
#an initial query to get the starting training_data_X and training_data_y values
'''
dates = [['2018-01-01', '2018-01-21'], ['2018-01-08', '2018-01-28'], ['2018-01-15', '2018-02-04']]

for date in dates:
    start = date[0]
    end = date[1]
    train_on_data('SELECT * FROM ' + table + ' WHERE date >= ' + start + ' AND date <= ' + end)
'''

#TODO: make queries that run prediction testing on data
#predict(query)














