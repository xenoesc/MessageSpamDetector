import numpy as np
import pandas as pd
data=pd.read_csv('spam.csv')
data.isna().sum()
data['Spam']=data['Category'].apply(lambda x:1 if x=='spam' else 0)
data.head(5)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(data.Message,data.Spam,test_size=1)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
clf=Pipeline([
    ('vectorizer',CountVectorizer()),
    ('nb',MultinomialNB())
])

def spamDetect(email):
    clf.fit(X_train,y_train)
    return(clf.predict(email))
