import pandas as pd
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

data=pd.read_csv('./fetal_data_cleaned.csv')

X = data.drop(['fetal_health'], axis=1)
y = data['fetal_health']

# Split into training and test set
X_train, X_test, y_train, y_test = train_test_split(
             X, y, test_size = 0.2, random_state=42)

def knn(X_test):
    knn = KNeighborsClassifier(n_neighbors=7)
    knn.fit(X_train, y_train)
    predicted_k1=knn.predict(X_test)
    return predicted_k1

