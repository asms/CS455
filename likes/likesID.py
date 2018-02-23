import pandas as pd
import numpy as np
from sklearn import tree
from sklearn import metrics
from sklearn import svm
from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from sklearn.linear_model import PassiveAggressiveRegressor
import pickle

df1 = pd.read_csv('/Users/wildergarcia/Desktop/tcss455/training/profile/profile.csv', index_col=0)
df2 = pd.read_csv('/Users/wildergarcia/Desktop/tcss455/training/relation/relation.csv', index_col=0)

df2['like_id'] = df2['like_id'].astype(str)
# merged profile and relation files into one dataframe based in user id
df3 = pd.merge(df1,df2,how="outer",on='userid')
# add the df3 to fourth dataframe and groupby userid into a list
df4 = pd.DataFrame(df3.groupby('userid')['like_id'].apply(list))

# print(df4.head())
list = []
# convert the dataframe using the likeid column to string and add to list
for i in df4['like_id']:
    str = ' '.join(i)
    list.append(str)
# add list to df4 dataframe
df4['like_id'] = list #
# reset the index
df4 = df4.reset_index()

# #sort the dataframe base in useid in profile and relation
df1.sort_values(['userid'], ascending=True)
df4.sort_values('userid', ascending=True)
#combine base in userid
df5 = pd.merge(df1, df4, on=['userid'])
print(df5.columns)

# Splitting the data into 300 training instances and 104 test instances
n = 1500
all_Ids = np.arange(len(df5))
test_Ids = all_Ids[0:n]
train_Ids = all_Ids[n:]
data_test =df5.loc[test_Ids, :]
data_train = df5.loc[train_Ids, :]



# Training a Naive Bayes model
count_vect = CountVectorizer() # this mean a transformation in the training data
X_train = count_vect.fit_transform(data_train['like_id']) # replace transcript with like_id
y_train = data_train['gender']
clf = MultinomialNB() # this is the place where you can decrare decision tree
clf.fit(X_train, data_train['gender'])

# Testing the Naive Bayes model
newVec = CountVectorizer(vocabulary=count_vect.vocabulary_)
X_test = newVec.transform(data_test['like_id'])
y_test = data_test['gender']
y_predicted = clf.predict(X_test)

# Reporting on classification performance
print("Accuracy: %.2f" % accuracy_score(y_test,y_predicted))
# classes = ['Male','Female']
# cnf_matrix = confusion_matrix(y_test,y_predicted,labels=classes)
# print("Confusion matrix:")
# print(cnf_matrix)
with open("userlikes.pkl", "wb") as f:
    pickle.dump(clf, f, pickle.HIGHEST_PROTOCOL)

with open("likeVectors.pkl", "wb") as f:
    pickle.dump(newVec, f, pickle.HIGHEST_PROTOCOL)
