import pickle
import nltk
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pyresparser import ResumeParser


with open('models/NaiveBayes.pickle', 'rb') as efile:
    clf=pickle.load(efile)
with open('models/TFIDFVectorizer.pickle', 'rb') as efile:
    word_vectorizer=pickle.load(efile)
with open('models/LabelEncoder.pickle', 'rb') as efile:
    le=pickle.load(efile)


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) #creating a set of stop words


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    word_tokens = word_tokenize(resumeText) #Tokenize words
    filtered_sentence = [w for w in word_tokens if not w in stop_words] #Contains words other than stop words
    filtered_sentence = map(lambda x: lemmatizer.lemmatize(x), filtered_sentence)
    resumeText=' '.join(filtered_sentence)
    return resumeText

def largest_indices(ary, n):
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return indices

def test(sent):
    sent=cleanResume(sent)
    WordFeatures = word_vectorizer.transform([sent])
    x=largest_indices(clf.predict_proba(WordFeatures), 3)
    recommendation=le.inverse_transform(x)
    return recommendation

def resume_test(path):
    data = ResumeParser(path).get_extracted_data()
    sentences=" "
    omit=["name", "email", "mobile_number", "no_of_pages", "total_experience"]
    for key, value in data.items():
          if value !=None and key not in omit: 
            if type(value)==list:
                  sentences= sentences +" "+ key + " " + " ".join(value)
            else:
                  sentences= sentences +" "+ key + " " + value
    professions= test(sentences)
    return (professions,data)

