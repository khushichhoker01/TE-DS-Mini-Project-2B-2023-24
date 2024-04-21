# ASGI server implementation
import uvicorn

# Web framework for building APIs
from fastapi import FastAPI, Request

# Loading and saving scikit-learn models
import joblib

# Serving static files (e.g., CSS, JavaScript) in FastAPI
from fastapi.staticfiles import StaticFiles

# Templating engine for FastAPI
from fastapi.templating import Jinja2Templates

# Response type for returning HTML content
from fastapi.responses import HTMLResponse

# Numerical operations library
import numpy as np

# Natural Language Toolkit library
import nltk

# Collection of stop words for various languages
from nltk.corpus import stopwords

# Collection of punctuation characters
import string

# Stemmer for English words
from nltk.stem.porter import PorterStemmer

# Library for serializing and deserializing Python objects
import pickle


# Initialize Porter Stemmer
ps = PorterStemmer()

# Create FastAPI app instance
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load phishing model for website
phish_model = open('phishing.pkl', 'rb')
phish_model_ls = joblib.load(phish_model)

# Load TF-IDF vectorizer and model for sms
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Preprocessing function
def transform_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Tokenize text
    text = nltk.word_tokenize(text)
    
    # Filter out non-alphanumeric characters
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    
    # Remove stopwords and punctuation
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    
    # Apply stemming
    for i in text:
        y.append(ps.stem(i))
            
    return " ".join(y)


# Route for rendering spam.html template
@app.get('/spam/', response_class=HTMLResponse)
async def spam(request: Request):
    return templates.TemplateResponse(request=request, name='spam.html')

# Route for predicting if input text is a phishing SMS
@app.get('/spam/predict/{feature}')
async def spam_predict(request: Request, features):
    # Preprocess the input text
    trans = transform_text(features)
    # Vectorize the preprocessed text
    vect = tfidf.transform([trans])
    # Predict using the ML model
    prediction = model.predict(vect)[0]
    # Determine the result based on the prediction
    if prediction == 1:
        result = 'a Phishing SMS'
    else:
        result = 'not a Phishing SMS'
    # Render the result template with the prediction result and input feature
    return templates.TemplateResponse(request=request, name='res.html', context={'result': result, 'feature': features})

# Route for rendering web.html template
@app.get('/', response_class=HTMLResponse)
async def web(request: Request):
    # Render web.html template
    return templates.TemplateResponse(request=request, name='web.html')

# Route for rendering index.html template
@app.get('/index/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

# Route for predicting if input text is a phishing site
@app.get('/index/predict/{feature}')
# Route for predicting if input text is a phishing site
async def index_predict(request: Request, features):
    # Prepare the input data for prediction
    X_predict = []
    X_predict.append(str(features))
    # Predict using the phishing model
    y_Predict = phish_model_ls.predict(X_predict)
    # Determine the result based on the prediction
    if y_Predict == 'bad':
        result = "a Phishing Site"
    else:
        result = "not a Phishing Site"
    # Render the result template with the prediction result and input feature
    return templates.TemplateResponse(request=request, name='result.html', context={"result": result, "feature": features})

# Run the FastAPI app using Uvicorn server
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=33)