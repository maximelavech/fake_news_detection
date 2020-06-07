import os, re, random
import pandas as pd
from IPython.display import Markdown, display

def load_data(filepath):
    # loads the original files provided by Clement Bisaillon and returns a merged dataframe of 'True' and 'Fake' news
    pattern = re.compile('(\w*)\.(\w*)')
    files = [(os.path.join(filepath,file),pattern.search(file).group(1)) for file in os.listdir(filepath)]
    dataframes = []
    for (f,label) in files:
        df = pd.read_csv(f)
        df['label'] = label
        dataframes.append(df)
    return pd.concat(dataframes,axis = 0).reset_index(drop=True)

def printmd(string):
    # display string in MarkDown format
    display(Markdown(string))

def process_label(label=str):
    # Checks the label is in the correct format and returns it. If not, or If None, returns randomly 'True' or 'Fake'
    if label == None:
        return random.choice(['True','Fake'])
    elif label not in ['True','Fake']:
        return random.choice(['True','Fake'])
    else:
        return label

def display_random_article(data,label=None,max_characters=1000):
    """
    Formats the data for manual inspection of the samples.
    
    Inputs
    ------
    data : (pandas.Dataframe) dataframe with at least columns label, title, text
    label : (string) True or Fake label. If None, see output of process_label
    max_characters (int) the max number of characters to display
    
    Outputs
    -------
    Prints a randomly chosen article of label = label with at most max_characters characters
    
    
    """
    label = process_label(label)
    subdata = data.loc[data['label']==label]
    index = random.choice(subdata.index)
    printmd(r'**Title:** {}'.format(subdata.loc[index,'title']))
    try:
        printmd(r'**Date:** {}; **Subject:** {} ; **Label:** {}'.format(subdata.loc[index,'date'],
                                                                       subdata.loc[index,'subject'],
                                                                       subdata.loc[index,'label']))
    except:
        printmd(r'**Label:** {}'.format(subdata.loc[index,'label']))
    text = subdata.loc[index,'text']
    if len(text) < max_characters:
        printmd(r'**Text:** {}'.format(subdata.loc[index,'text']))
    else:
        printmd(r'**Text:** {}'.format(subdata.loc[index,'text'][:max_characters]+ '... (*max_characters* = {})'.format(max_characters)))