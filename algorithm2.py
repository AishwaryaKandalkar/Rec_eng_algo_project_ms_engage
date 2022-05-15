# -*- coding: utf-8 -*-
"""algorithm2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ceIHG_XUn6_h7ZK6LVInztZWQH0w8F4Y
"""

# Give the location of the dataset
path_dataset ="/content/movie2.zip" 
  
import pandas as pd
data = pd.read_csv(path_dataset)
data.head()

len(data)

import numpy as np
np.unique(data['Origin/Ethnicity'])

len(data.loc[data['Origin/Ethnicity']=='American'])

len(data.loc[data['Origin/Ethnicity']=='British'])

# Concatenating American and British movies
df1 = pd.DataFrame(data.loc[data['Origin/Ethnicity']=='American'])
df2 = pd.DataFrame(data.loc[data['Origin/Ethnicity']=='British'])
data = pd.concat([df1, df2], ignore_index = True)
  
len(data)
  
finaldata = data[["Title", "Plot"]]          # Required columns - Title and movie plot
finaldata = finaldata.set_index('Title')    # Setting the movie title as index
  
finaldata.head(10)
finaldata["Plot"][0]

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
  
  
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
  
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
  
VERB_CODES = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}

def preprocess_sentences(text):
  text = text.lower()
  temp_sent =[]
  words = nltk.word_tokenize(text)
  tags = nltk.pos_tag(words)
  for i, word in enumerate(words):
      if tags[i][1] in VERB_CODES: 
          lemmatized = lemmatizer.lemmatize(word, 'v')
      else:
          lemmatized = lemmatizer.lemmatize(word)
      if lemmatized not in stop_words and lemmatized.isalpha():
          temp_sent.append(lemmatized)
          
  finalsent = ' '.join(temp_sent)
  finalsent = finalsent.replace("n't", " not")
  finalsent = finalsent.replace("'m", " am")
  finalsent = finalsent.replace("'s", " is")
  finalsent = finalsent.replace("'re", " are")
  finalsent = finalsent.replace("'ll", " will")
  finalsent = finalsent.replace("'ve", " have")
  finalsent = finalsent.replace("'d", " would")
  return finalsent
  
finaldata["plot_processed"]= finaldata["Plot"].apply(preprocess_sentences)
finaldata.head()

from sklearn.feature_extraction.text import TfidfVectorizer
  
# Vectorizing pre-processed movie plots using TF-IDF
tfidfvec = TfidfVectorizer()
tfidf_movieid = tfidfvec.fit_transform((finaldata["plot_processed"]))
  
# Finding cosine similarity between vectors
from sklearn.metrics.pairwise import cosine_similarity
cos_sim = cosine_similarity(tfidf_movieid, tfidf_movieid)

# Storing indices of the data
indices = pd.Series(finaldata.index)
  
def recommendations(title, cosine_sim = cos_sim):
    recommended_movies = []
    index = indices[indices == title].index[0]
    similarity_scores = pd.Series(cosine_sim[index]).sort_values(ascending = False)
    top_10_movies = list(similarity_scores.iloc[1:11].index)
    for i in top_10_movies:
        recommended_movies.append(list(finaldata.index)[i])
    return recommended_movies

recommendations("Harry Potter and the Chamber of Secrets")

recommendations("Ice Age")

recommendations("Blackmail")

