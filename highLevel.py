import pandas as pd  # import pandas library

data = pd.read_csv('spam.csv')  # read a CSV file into a pandas dataframe called 'data'
data.isna().sum()  # calculate the number of missing values in each column of the dataframe
data['Spam'] = data['Category'].apply(lambda x: 1 if x == 'spam' else 0)  # create a new column named 'Spam' with a binary value indicating if a message is spam or not
data.head(5)  # display the first 5 rows of the dataframe

from sklearn.model_selection import train_test_split  # import the train_test_split function from scikit-learn
X_train, X_test, y_train, y_test = train_test_split(data.Message, data.Spam, test_size=1)  # split the data into training and testing sets

from sklearn.feature_extraction.text import CountVectorizer  # import the CountVectorizer class from scikit-learn
from sklearn.naive_bayes import MultinomialNB  # import the MultinomialNB class from scikit-learn
from sklearn.pipeline import Pipeline  # import the Pipeline class from scikit-learn

clf = Pipeline([('vectorizer', CountVectorizer()), ('nb', MultinomialNB())])  # create a pipeline for text classification

def spamDetect(email):  # define a function to detect spam emails
    clf.fit(X_train, y_train)  # train the classifier on the training data
    return clf.predict(email)  # make a prediction on the input email
