import joblib, pandas as pd


loaded_model = joblib.load(open("models/model.sav", "rb"))
tfidf_vectorizer = joblib.load(open("models/vectorizer.sav", "rb"))

def predict(text):
    text_vector = tfidf_vectorizer.transform([text.replace('\n',"")])
    proba = loaded_model._predict_proba_lr(text_vector)[0]
    tresh = 0.55
    result = loaded_model.predict(text_vector)

    if proba[0] - proba[1] < tresh and proba[0]>0.5:
        if proba[0] - proba[1] <= tresh/2:
            return "REAL", 80 if round(100*proba[1]) < 80 else round(100*proba[1])
        else:
            return "UNIDENTIFIED", ""
    else:
        if result[0].upper() == "REAL":
            score = 80 if round(100*proba[1]) < 80 else round(100*proba[1])
        else:
            score = round(100 * proba[0])
        return result[0], score