Fake News Detection : Udacity MLE Project
===============================================================

Data
----


The data was collected from Kaggle (https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset) and provided by Clément Bisaillon who further acknowledged the following sources:
* Ahmed H, Traore I, Saad S. “Detecting opinion spams and fake news using text classification”, Journal of Security and Privacy, Volume 1, Issue 1, Wiley, January/February 2018.
* Ahmed H, Traore I, Saad S. (2017) “Detection of Online Fake News Using N-Gram Analysis and Machine Learning Techniques. In: Traore I., Woungang I., Awad A. (eds) Intelligent, Secure, and Dependable Systems in Distributed and Cloud Environments. ISDDC 2017. Lecture Notes in Computer Science, vol 10618. Springer, Cham (pp. 127-138).

The data was initially split into two *filename.csv* files each containing respectively the data for 'True' news and 'Fake' news. We added a label column to each dataframe and merged the data into a single dataframe. The original dataset can be found in **./data/rawdata** and the merged data in **./data/cleandata**

Requirements
------------

```text
pandas==0.24.2
numpy==1.16.4
seaborn==0.8.1
matplotlib==3.0.3
sklearn==0.20.3
nltk==3.3
wordcloud==1.7.0
sagemaker==1.56.0
boto3==1.12.46
mxnet==1.6.0
```

Notebooks
---------

There are five IPython notebooks in which the key steps in the project are implemented:

* **01_DataStructureExploration** : Explore the structural aspect of the data. Indeed, the news articles come with metadata (for example the title, publication date...) and can present certain characteristics which are not 'word'-related (for example, twitter tokens such as #Udacity). We hence propose an approach to perform some feature engineering operations to exploit those characteristics. 

* **02_DataContentExploration** : In this notebook, we explore more specifically text-related cues: choice of vocabulary, presence of specific tokens and propose a transformation process to map a text to a list of tokens.

* **03_BenchmarkModels** : Here, we train and evaluate our Naive Bayes Benchmark model on the features engineered in the previous notebooks. We further save some training artifacts to compare results with our model.

* **04_LinearModel** : In this notebook, we have our final model which a simple logistic regression where we obtain highly satisfactory results. Further, we explore the weights obtained in training to interpret our results.

* **05_Discussion** : We provide an outlook and discuss the results obtained in the previous section by exploring an embedding of the data.

Folders
-------

Here, we provide a brief description of the content of the folders in this project:

* **data** : contains the rawdata and cleandata folders as well as well the benchmark artifacts.
* **images** : contains the plots featured in our project report.
* **model** : contains model artifacts used to interpret the fitted linear model.
* **project reports** : contains the project report. *NOTE : We will add the Capstone Proposal once it is validated by Udacity*.
* **utils** : contains a set of utils_*filename*.py files with functions used throughout the project.
* **website** : contains the html skeleton of a potential website for our project. Note the files here were adapted from a project in the Udacity MLE Course.

