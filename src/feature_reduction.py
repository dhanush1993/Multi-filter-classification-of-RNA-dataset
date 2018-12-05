import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import pandas as pd
import KR 
import pdb
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
inputFile = '../res/RNA_matrix'
df = pd.DataFrame()
for i in range(1):
	df = df.append(pd.read_csv(inputFile+'-'+str(i)+'.csv'),ignore_index=True)
df = df.dropna(axis=0)
file_id = df.pop('file_id')
labels = df.pop('label')
X = df.copy()
Y = labels
for i in range(10):
	print("Running KMeans - "+str(i))
	X = KR.kmeans_reduce(X)

clf = LinearDiscriminantAnalysis()
clf.fit(X,Y)
Z = clf.transform(X)
print('After Kmeans feature reduction and LDA we have the number of features reduced from '+str(X.shape[1])+' to '+str(Z.shape[1]))
clf = LinearDiscriminantAnalysis()
clf.fit(df.values,Y)
lda = clf.transform(df.values)

#########################################################################################################
def train(X, Y):
	models = {'SVC': SVC()}
	tuned_parameters = {'SVC': {'kernel': ['rbf'], 'C': [1, 10], 'gamma': [0.001, 0.0001]}}
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
	clf = GridSearchCV(models['SVC'], tuned_parameters['SVC'], scoring=None,  refit=True, cv=10)
	clf.fit(X_train, y_train)
	y_test_predict = clf.predict(X_test)
	precision = precision_score(y_test, y_test_predict,average='macro')
	accuracy = accuracy_score(y_test, y_test_predict)
	f1 = f1_score(y_test, y_test_predict,average='macro')
	recall = recall_score(y_test, y_test_predict,average='macro')
	scores = {"accuracy":accuracy*100, "precision":precision*100, "f1":f1*100, "recall":recall*100}
	return scores
scores = {}
print("*************Proposed Model(Kmeans and LDA)*************")
scores["kmeans_lda"] = train(Z,Y)
print("Accuracy: "+str(scores["kmeans_lda"]["accuracy"]))
print("Precision: "+str(scores["kmeans_lda"]["precision"]))
print("F1 score: "+str(scores["kmeans_lda"]["f1"]))
print("recall: "+str(scores["kmeans_lda"]["recall"]))
print(' ')
print("***************************LDA***************************")
scores["lda"] = train(lda,Y)
print("Accuracy: "+str(scores["lda"]["accuracy"]))
print("Precision: "+str(scores["lda"]["precision"]))
print("F1 score: "+str(scores["lda"]["f1"]))
print("recall: "+str(scores["lda"]["recall"]))
labels = ['accuracy', 'precision', 'f1', 'recall']
plt.subplot(1, 2, 1)
plt.bar(range(len(scores['kmeans_lda'])), list(scores['kmeans_lda'].values()), color=('b','r','g','y'),align='center')
plt.xticks(range(len(scores['kmeans_lda'])),list(scores['kmeans_lda'].keys()),rotation='vertical')
plt.title("Kmeans and LDA")
plt.subplot(1, 2, 2)
plt.bar(range(len(scores['lda'])), list(scores['lda'].values()), color=('b','r','g','y'),align='center')
plt.xticks(range(len(scores['lda'])),list(scores['kmeans_lda'].keys()),rotation='vertical')
plt.title("LDA")
plt.show()
