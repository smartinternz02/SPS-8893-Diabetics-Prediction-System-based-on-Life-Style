# -*- coding: utf-8 -*-
"""DiabeticsPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FJB82yHUyVRMkv-HRhCF_CYcCp8nE7bV

Importing **Libraries**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
import pickle

data = pd.read_csv('/content/diabetes.csv')

data.head()

data.shape

data.info()

data.describe()

data.Outcome.nunique()

data.Outcome.value_counts()

"""**Data Visualization**"""

features = ['Glucose', 'Outcome']
data[features].hist(figsize=(10, 4));

features = ['BloodPressure','Pregnancies']
data[features].hist(figsize=(10, 4));

features = ['Insulin']
data[features].hist(figsize=(10, 4));

sns.countplot(x='Pregnancies', hue='Outcome', data=data)

sns.countplot(x='Glucose', hue='Outcome', data=data)

sns.countplot(x='Age', hue='Outcome', data=data)

#Relation between Features

sns.jointplot(x='Glucose', y='Insulin', data=data, kind='scatter');

sns.jointplot(x='Glucose', y='Outcome', data=data, kind='scatter');

sns.jointplot(x='Glucose', y='DiabetesPedigreeFunction', data=data, kind='scatter');

sns.jointplot(x='Age', y='Outcome', data=data, kind='scatter');

#Correlation between Features
sns.heatmap(data.corr(), annot=True, fmt=".1f", linewidths=.5)

#the output variable is well correlated to the "Glucose" variable

"""**Missing Data**"""

data.isnull().sum()

data.info()

#We saw on data.head() that some features contain 0, it doesn't make sense here and this indicates missing value Below we replace 0 value by NaN :

data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)

data.info()

#we can see that we have some missing data in the next columns : Glucose , BloodPressure  ,  SkinThickness , Insulin , BMI .

#Missing values :
#Insulin = 374
#SkinThickness = 227
#BloodPressure = 35
#BMI = 11
#Glucose = 5

#To replace missing values, we'll use median by target (Outcome)

def median_target(var):   
    temp = data[data[var].notnull()]
    temp = temp[[var, 'Outcome']].groupby(['Outcome'])[[var]].median().reset_index()
    return temp

median_target('Insulin')

data.loc[(data['Outcome'] == 0 ) & (data['Insulin'].isnull()), 'Insulin'] = 102.5
data.loc[(data['Outcome'] == 1 ) & (data['Insulin'].isnull()), 'Insulin'] = 169.5

median_target('Glucose')

data.loc[(data['Outcome'] == 0 ) & (data['Glucose'].isnull()), 'Glucose'] = 107
data.loc[(data['Outcome'] == 1 ) & (data['Glucose'].isnull()), 'Glucose'] = 140

median_target('SkinThickness')

data.loc[(data['Outcome'] == 0 ) & (data['SkinThickness'].isnull()), 'SkinThickness'] = 27
data.loc[(data['Outcome'] == 1 ) & (data['SkinThickness'].isnull()), 'SkinThickness'] = 32

median_target('BloodPressure')

data.loc[(data['Outcome'] == 0 ) & (data['BloodPressure'].isnull()), 'BloodPressure'] = 70
data.loc[(data['Outcome'] == 1 ) & (data['BloodPressure'].isnull()), 'BloodPressure'] = 74.5

median_target('BMI')

data.loc[(data['Outcome'] == 0 ) & (data['BMI'].isnull()), 'BMI'] = 30.1
data.loc[(data['Outcome'] == 1 ) & (data['BMI'].isnull()), 'BMI'] = 34.3

"""**One Hot Encoding**"""

#we don't need to do one hot encoding since our data is all digital and our output variable is binary

"""**Feature Scaling**"""

min_max_scaler = preprocessing.MinMaxScaler(feature_range =(0, 1))

X = data.drop(['Outcome'],axis=1)
y = data.Outcome

X_sc = min_max_scaler.fit_transform(X)

"""**Splitting Data**"""

x_train, x_val,y_train,y_val = train_test_split(X_sc,y,test_size=0.2,random_state=42)

"""**Models**"""

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=100, bootstrap = True,max_features = 'sqrt',random_state=42)

rfc.fit(x_train,y_train)

y_pred = rfc.predict(x_val)

from sklearn.metrics import accuracy_score

accuracy_score(y_pred,y_val)

from sklearn.metrics import f1_score

f1_score(y_pred,y_val)

pickle.dump(rfc,open('model1.pkl','wb'))
model=pickle.load(open('model1.pkl','rb'))
