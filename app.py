from flask import Flask, render_template, request, redirect, jsonify
import pickle
import re
import nltk
import pandas as pd
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Load data
cols = ['kategori','berita']
pd.set_option("display.max_colwidth", 150)
df = pd.read_csv('E:/Tugas Akhir/500_berita_indonesia.csv', delimiter=";", usecols=cols)

# Load model and vectorizer
model_nb = pickle.load(open('models/model_nb.sav', 'rb'))
model_svc = pickle.load(open('models/model_svc.sav', 'rb'))
tfidfvect = pickle.load(open('models/tf_idf.sav', 'rb'))

factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    text = re.sub(r'@[^\s]+', '', text)
    # hapus hashtag
    text = re.sub(r'#[^\s]+', '', text)
    # hapus tanda baca
    text = re.sub(r'[^\w\s]', '', text) 
    # hapus angka
    text = re.sub(r'\d+', '', text)
    # remove spasi berlebih
    text = re.sub(r'\s+', ' ', text)
    # menghapus whitepace (karakter kosong)
    text = text.strip()
    # regex huruf yang berulang seperti haiiii (untuk fitur unigram)
    normal_regex = re.compile(r"(.)\1{1,}")
    # buang huruf yang berulang
    text = normal_regex.sub(r"\1\1", text)
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words
    words = [word for word in words if word not in stopwords]
    # Stem the words
    words = [stemmer.stem(word) for word in words]
    # Join the words back into a string
    text = ' '.join(words)

    return text

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/uji')
def uji():
    return render_template('uji.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    preprocessed_text = preprocess_text(text)
    X = tfidfvect.transform([preprocessed_text]).toarray()
    mnb_pred = model_nb.predict(X)
    mnb_prob = model_nb.predict_proba(X)
    mnbProba = np.amax(mnb_prob)
    mnbProba = format(mnbProba, ".2%")
    print(mnbProba)

    svc_pred = model_svc.predict(X)
    svc_prob = model_svc.predict_proba(X)
    svcProba = np.amax(svc_prob)
    svcProba = format(svcProba, ".2%")
    print(svcProba)
    return render_template('predict.html', text=text, predmnb=mnb_pred, probamnb=mnbProba, predsvc=svc_pred, probasvc=svcProba)

if __name__== '__main__':
    app.run(debug=True)