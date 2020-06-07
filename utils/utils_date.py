import re, datetime
import numpy as np

# Default date dictionary : maps month in string format to int number 
date_dictionary = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,
                   'october':10,'november':11,'december':12}

def update_date_dictionary(dic):
    # Update the date dictionary by taking first three letters of the month in the string format to map to int.
    new = {}
    for key in dic:
        new[key] = dic[key]
        new[key[:3]] = dic[key]
    return new

date_dictionary = update_date_dictionary(date_dictionary)

def get_month(text):
    # extract month value
    pattern_month = re.compile(r"[A-Za-z]+")
    try:
        return date_dictionary[pattern_month.findall(text)[0].lower()]
    except:
        return -1

def process_year(year):
    # transform year value to have same format everywhere
    if len(year)==2:
        return int('20'+year)
    elif len(year)==4:
        return int(year)
    else:
        return -1
    
def get_day(text):
    # extract the day for the date
    pattern = re.compile(r"(\d+)([^\d]+)(\d+)")
    try:
        return int(pattern.search(text).group(1))
    except:
        return -1

def get_year(text):
    # extract the year
    pattern = re.compile(r"(\d+)([^\d]+)(\d+)")
    try:
        return process_year(pattern.search(text).group(3))
    except:
        return -1   

def extract_date(text,string = True):
    # wrapper of previous function to extract the full date in datetime format
    day = get_day(text)
    month = get_month(text)
    year = get_year(text)
    try:
        if not string:
            return datetime.date(year, month, day)
        else:
            return str(datetime.date(year, month, day))
    except:
        return np.nan