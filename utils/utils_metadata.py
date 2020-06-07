import re
import pandas as pd
import numpy as np
from collections import Counter

from .utils_date import extract_date

def caption_ratio(text,epsilon=10e-6):
    # Returns the "normalized" count of uppercase letters and the "normalized" count of lowercase letters
    count_u = 0
    count_l = 0
    for c in text:
        count_u += (c.isupper())*1
        count_l += (c.islower())*1
    return count_u/(len(text)+epsilon),count_l/(len(text)+epsilon)

def replace_acronyms(text):
    # Removes acronyms
    pattern = r'(?<!\w)([A-Z])\.'
    return re.sub(pattern, r'\1', text)

def average_sentence_length(text):
    # Computes the mean length of a sentence within a document by splitting according to '.'
    temp = replace_acronyms(text)
    return np.mean([len(sentence) for sentence in temp.split('.')])

def uppercase_count(text):
    # Returns the number of uppercase words
    text = replace_acronyms(text)
    if ' ' in text:
        words = text.split()
        return sum([w.isupper() for w in words])
    else:
        return text.isupper()*1
    
def metadata_engineering(data):
    data = data.copy()
    # Convert date
    data['processed_date'] = data['date'].apply(lambda x : extract_date(x))
    
    # Title features
    data['title_length'] = data['title'].apply(lambda x : len(x))
    data['title_uppercase'] = data['title'].apply(lambda x : caption_ratio(x)[0])
    data['title_lowercase'] = data['title'].apply(lambda x : caption_ratio(x)[1])
    data['title_uppercase_count'] = data['title'].apply(lambda x : uppercase_count(x))
    
    # Text features
    data['text_length'] = data['text'].apply(lambda x : len(x))
    data['text_uppercase'] = data['text'].apply(lambda x : caption_ratio(x)[0])
    data['text_lowercase'] = data['text'].apply(lambda x : caption_ratio(x)[1])
    data['avg_sent_length'] = data['text'].apply(lambda x : average_sentence_length(x))
    data['text_uppercase_count'] = data['text'].apply(lambda x : uppercase_count(x))
    
    return data

DEFAULT_CHARACTERS = [str(i) for i in range(10)] + ['!','?','<','>','-','#','@']

def distributionCharacters(text,enlist=True):
    count = Counter(text.lower())
    special = {}
    for char in DEFAULT_CHARACTERS:
        if enlist:
            special[char]=[count[char]]
        else:
            special[char]=count[char]
    return special

def update(old,new):
    if list(old.keys()) == list(new.keys()):
        for key in old.keys():
            old[key]+=new[key]
    else:
        for key in new:
            old[key]=new[key]
    return old

def process_row(row,keys = None):
    elements = []
    count = distributionCharacters(row['text'],enlist=False)
    if keys == None:
        keys = count.keys()
    for key in keys:
        elements.append([key,count[key],row['label']])
    return elements

def structure_engineering(data):
    data = data.copy()

    # Title features
    data['title_length'] = data['title'].apply(lambda x : len(x))
    data['title_uppercase'] = data['title'].apply(lambda x : caption_ratio(x)[0])
    data['title_lowercase'] = data['title'].apply(lambda x : caption_ratio(x)[1])
    data['title_uppercase_count'] = data['title'].apply(lambda x : uppercase_count(x))
    
    # Text features
    data['text_length'] = data['text'].apply(lambda x : len(x))
    data['text_uppercase'] = data['text'].apply(lambda x : caption_ratio(x)[0])
    data['text_lowercase'] = data['text'].apply(lambda x : caption_ratio(x)[1])
    data['avg_sent_length'] = data['text'].apply(lambda x : average_sentence_length(x))
    data['text_uppercase_count'] = data['text'].apply(lambda x : uppercase_count(x))
    
    # Special Characters
    for char in DEFAULT_CHARACTERS:
        data['count_({})'.format(char)] = data['text'].apply(lambda x : distributionCharacters(x,enlist=False)[char])
    
    return data

DEFAULT_SELECTION = ['?','!','#','@','-']

def get_structure(data):
    
    data = data.copy()
    data['title_length'] = data['title'].apply(lambda x : len(x))
    data['title_uppercase'] = data['title'].apply(lambda x : caption_ratio(x)[0])
    data['text_lowercase'] = data['text'].apply(lambda x : caption_ratio(x)[1])
    data['avg_sent_length'] = data['text'].apply(lambda x : average_sentence_length(x))
    data['text_uppercase_count'] = data['text'].apply(lambda x : uppercase_count(x))
    for char in DEFAULT_SELECTION:
        data['count_({})'.format(char)] = data['text'].apply(lambda x : distributionCharacters(x,enlist=False)[char])
    
    del data['date']
    del data['subject']
    
    return data
    
def text_transform(title,text):
    features = [len(title),caption_ratio(title)[0],caption_ratio(text)[1],average_sentence_length(text),uppercase_count(text)]
    for char in DEFAULT_SELECTION:
        features.append(distributionCharacters(text,enlist=False)[char])
    return np.array(features)