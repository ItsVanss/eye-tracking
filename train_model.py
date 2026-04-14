import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import joblib

# Load dataset
data = pd.read_csv('eye_dataset.csv', header=None)
X = data.iloc[:, 0:2]
y = data.iloc[:, 2]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Pilih model
model = KNeighborsClassifier(n_neighbors=3)
# model = SVC(kernel='linear')

# Training
model.fit(X_train, y_train)

# Akurasi
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Simpan model
joblib.dump(model, 'eye_model.pkl')