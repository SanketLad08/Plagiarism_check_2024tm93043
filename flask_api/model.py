# flask_api/model.py
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from utils import calculate_cosine_similarity

def create_synthetic_dataset():
    data = [
        ("This is the original sentence.", "This is the original sentence.", 1),
        ("The sky is blue and beautiful.", "The sky is blue.", 1),
        ("Machine learning is fun.", "I like pizza.", 0),
        ("Python is a great language.", "I use Java for backend.", 0),
        ("The quick brown fox jumps over the lazy dog.","The quick brown fox jumps over the lazy dog.",1),
        ("Data science is interesting.", "I love studying data science.", 1),
        ("Python is cool.", "Java is another language.", 0),
        ("Weather is nice today.", "Apples are tasty.", 0)
    ]
    rows = []
    for original, submission, label in data:
        sim = calculate_cosine_similarity(original, submission)
        rows.append([sim, label])
    df = pd.DataFrame(rows, columns=["similarity", "label"])
    df.to_csv("plagiarism_dataset.csv", index=False)
    return df

def train_and_save_model():
    df = create_synthetic_dataset()
    X = df[["similarity"]]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, "plagiarism_model.pkl")
    print("Model trained and saved to plagiarism_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
