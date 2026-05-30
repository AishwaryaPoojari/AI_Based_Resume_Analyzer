import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Load dataset
data = pd.read_csv("dataset/UpdatedResumeDataSet.csv")

# Input and Output
X = data["Resume"]
y = data["Category"]

# Convert text into numerical vectors
vectorizer = TfidfVectorizer(stop_words='english')

X_vectorized = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = MultinomialNB()

model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("models/model.pkl", "wb"))

# Save vectorizer
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("Model Trained Successfully")