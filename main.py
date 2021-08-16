# -*- coding: utf-8 -*-
"""main.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g-uhai-pJMYSb3OON4w_mtQHy3thWu5J
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('IMDB-Movie-Data.csv')

cleaned = dataset.set_index('Rank').Genre.str.split(',', expand=True).stack()
cleaned = pd.get_dummies(cleaned).groupby(level=0).sum()
cleaned

dataset_new=dataset.iloc[:, [7,8,9,11]]

data = []
data.insert(0, {'Runtime (Minutes)':0, 'Rating':0, 'Votes':0, 'Metascore':0})

ds=pd.concat([pd.DataFrame(data), dataset_new], ignore_index=True)
horizontal_stack = pd.concat([cleaned, ds], axis=1)

horizontal_stack.drop(index=horizontal_stack.index[0], 
        axis=0, 
        inplace=True)


X = np.array(horizontal_stack)
y=dataset.iloc[:,10].values


from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.NaN, strategy='most_frequent', verbose=1)
imputer.fit(X[:, 20:])
X[:, 20:] = imputer.transform(X[:, 20:])

y = y.reshape(len(y),1)

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.NaN, strategy='mean')
imputer.fit(y)
y = imputer.transform(y)

"""#One Hot Encoding"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

"""#Splitting the dataset into the test set and training set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
type(y_train)

"""#Feature Scaling"""

# from sklearn.preprocessing import StandardScaler
# sc = StandardScaler()
# X_train[:, 20:] = sc.fit_transform(X_train[:, 20:])
# X_test[:, 20:] = sc.transform(X_test[:, 20:])


"""#XGBOOST"""

from xgboost import XGBRegressor
regressor = XGBRegressor(learning_rate=0.25,n_estimators=20)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
r2_score(y_test, y_pred)

"""#Training the MLR model on the training set and predicting the test set results."""

from sklearn.linear_model import LinearRegression
regressor2 = LinearRegression()
regressor2.fit(X_train, y_train)

y_pred2 = regressor2.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred2.reshape(len(y_pred2),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
r2_score(y_test, y_pred2)

"""#Training the Decision tree model on the training set and predicting the test set results."""

from sklearn.tree import DecisionTreeRegressor
regressor3 = DecisionTreeRegressor(random_state = 0)
regressor3.fit(X_train, y_train)

y_pred3 = regressor3.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred3.reshape(len(y_pred3),1), y_test.reshape(len(y_test),1)),1))

regressor3.score(X_test,y_test)

from sklearn.metrics import r2_score
r2_score(y_test,y_pred3)

"""#Training the Random Forest model on the training set and predicting the test set results."""

from sklearn.ensemble import RandomForestRegressor
regressor4 = RandomForestRegressor(n_estimators = 232, random_state = 0, n_jobs=2, min_samples_split=12)
regressor4.fit(X_train, y_train)

y_pred4 = regressor4.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred4.reshape(len(y_pred4),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
r2_score(y_test, y_pred4)

"""#Training the Polynomial Regression model on the Training set and predicting the test set results."""

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
poly_reg = PolynomialFeatures(degree = 3)
X_poly = poly_reg.fit_transform(X_train)
regressor5 = LinearRegression()
regressor5.fit(X_poly, y_train)

y_pred5 = regressor5.predict(poly_reg.transform(X_test))
np.set_printoptions(precision=2)
print(np.concatenate((y_pred5.reshape(len(y_pred5),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
r2_score(y_test,y_pred5)

"""#Training the SVR model on the Training set and predicting the test set results."""

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
sc_y = StandardScaler()
X_train = sc_X.fit_transform(X_train)
y_train = sc_y.fit_transform(y_train)

from sklearn.svm import SVR
regressor6 = SVR(kernel = 'rbf', gamma='auto', tol=0.001, C=2.4, 
                 epsilon=0.36, shrinking=True, verbose=False, max_iter=-1)
regressor6.fit(X_train, y_train)

y_pred6 = sc_y.inverse_transform(regressor6.predict(sc_X.transform(X_test)))
np.set_printoptions(precision=2)
print(np.concatenate((y_pred6.reshape(len(y_pred6),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
r2_score(y_test, y_pred6)

print(regressor.coef_)
print(regressor.intercept_)

##predicting a single prediction
# print(regressor.predict([[120,7.1,240,77]]))





