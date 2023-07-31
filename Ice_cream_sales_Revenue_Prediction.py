import pandas as pd
icecream = pd.read_csv('https://github.com/ybifoundation/Dataset/raw/main/Ice%20Cream.csv')
icecream.columns
y = icecream['Revenue']
X = icecream[['Temperature']]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.7, random_state=2529)
# check shape of train and test sample
X_train.shape, X_test.shape, y_train.shape, y_test.shape
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train,y_train)
model.intercept_
model.coef_
y_pred = model.predict(X_test)
y_pred
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
mean_absolute_error(y_test,y_pred)
mean_absolute_percentage_error(y_test,y_pred)
mean_squared_error(y_test,y_pred)
