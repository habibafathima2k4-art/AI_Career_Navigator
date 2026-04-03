import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
import pickle

# Load dataset
data = pd.read_csv('dataset/career_data.csv')
data = shuffle(data)

# 🔥 Encode categorical columns
data['interest'] = data['interest'].map({
    'tech': 0,
    'design': 1,
    'business': 2
})

# Features
columns = [
    'python','java','sql','excel','communication','design',
    'marketing','statistics','networking','cloud','interest','education'
]

X = data[columns]
y = data['career']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = LogisticRegression(max_iter=300)
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Save model
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

# ----------- TEST INPUT -----------

test_input = pd.DataFrame([[
    1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0
]], columns=columns)

prediction = model.predict(test_input)

print("Test Prediction:", prediction[0])
