import re, os
import string
import nltk
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords

#nltk.download('wordnet')
#nltk.download('stopwords')

# URL_PATTERN taken from https://gist.github.com/gruber/249502
URL_PATTERN = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')


def replace_acronyms(text):
    # Regex to transform acronyms. Example : 'U.S.A' becomes 'USA'
    return re.sub(r'(?<!\w)([A-Z])\.',r'\1',text)

def clean_html(text):
    # bs4 and regex to remove any html tags
    text = BeautifulSoup(text,"lxml").get_text()
    return re.sub(r"<\w{1,10}>"," ",text)

def replace_url(text):
    # Regex to transform a URL to 'URL_TOKEN'
    return re.sub(URL_PATTERN,' URL_TOKEN ',text)

def replace_twitter(text):
    # Regex to replace #any_text by 'TWITTER_TOKEN'
    return re.sub('#([A-Za-z]+\w*)',' TWITTER_TOKEN ',text)

def replace_reference(text):
    # Regex to replace @any_text by 'REFERENCE_TOKEN'
    return re.sub('@([A-Za-z]+\w*)',' REFERENCE_TOKEN ',text)

def replace_compound(text):
    # Regex to transform compound words. Example 'full-course' becomes 'full course'
    return re.sub(r'(\w+)\-(\w+)',r'\1 \2',text)

def strip_punctuation(text):
    # Strips punctuation
    return re.sub(r"[^\w]",r" ",text)

def replace_numeric(text):
    # Regex to map digits to 'DIGIT_TOKEN'
    text = re.sub(r'(\d+) (\d+)',r'\1\2',text)
    return re.sub('\d+',' DIGIT_TOKEN ',text)

def lowercase(text):
    # lowercase the text
    return text.lower()

def tokenize(text):
    # split a text segment into token. ' ' is the separator
    return text.split()

def remove_stopwords(words):
    # remove stopwords from the tokens. Stopwords are taken from the default nltk list.
    return [w for w in words if w not in stopwords.words("english")]

def stem(words,active=False):
    # Stems the words from a list if active = True, otherwise simply returns the list of words. PorterStemmer from nltk.
    if active:
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in words]
    else:
        return words

def lemmatize(words,active=False):
    # Lemmatizes the words from a list if active = True, otherwise simply returns the list of words. WordNet from nltk.
    if active:
        wnl = WordNetLemmatizer()
        return [wnl.lemmatize(word) for word in words]
    else:
        return words
    
wnl = WordNetLemmatizer()
stemmer = PorterStemmer()

def transform(text,stem_bool=False,lemmatize_bool=True):
    """
    Wrapper that maps a text to a list of processed tokens.
    
    Inputs
    ------
    text (string) a text we wish to process
    stem_bool (bool) Stemming if True. Nothing Otherwise. Default is False
    lemmatize_bool (bool) Lemmatizing if True. Nothing otherwise. Default is True
    
    Output
    ------
    output (list) list of processed tokens. Each token must have a length superior to 1. 
    """
    text = replace_acronyms(text)
    text = replace_url(text)
    text = clean_html(text)
    text = replace_twitter(text)
    text = replace_reference(text)
    text = replace_compound(text)
    text = strip_punctuation(text)
    text = replace_numeric(text)
    text = lowercase(text)
    words = tokenize(text)
    words = remove_stopwords(words)
    words = lemmatize(words,lemmatize_bool)
    words = stem(words,stem_bool)
    output = [word for word in words if len(word)>1]
    return output