# -*- coding: utf-8 -*-
"""CWI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sELZNDfzRxPQP-Y0WtuNyzW9m9CX0x40
"""

from google.colab import drive
drive.mount('/content/drive')
path = '/content/drive/MyDrive/Colab/CleanedData/'
stoplemma_path = '/content/drive/MyDrive/Colab/CleanedData/stoplemmas.txt'

!pip install stanza
!pip install pyiwn
!pip install -q fasttext

import stanza
stanza.download('hi')
nlp = stanza.Pipeline('hi')

#Source: https://stackoverflow.com/questions/44474085/how-to-separate-a-only-hindi-script-from-a-file-containing-a-mixture-of-hindi-e
def is_hindi(token):
  for character in token:
    if character is None or character.strip() == '':
        return 0
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        pass
    else:
      return 0
  return 1

'''
import os
import shutil

def update_feature_values(dataset_path, feature_name, feature_values_path, common_feature_name):
  """
  Args:
  dataset_path (str): the path to the dataset to be updated
  feature_name (str): the feature whose values are to be updated
  feature_values_path (str): the file containing the new values of the feature
  common_feature_name (str): the feature that is common between the dataset and 
  the file in the feature_values_path, that can be used to select the required row
  """
  shutil.copyfile(dataset_path, "./")
  feature_values = pd.read_csv(feature_values_path)
  df = pd.read_csv(dataset_path)
  for row in df.iterrows():
    if(row[common_feature_name] in feature_values[common_feature_name].values()):
      row.loc[common_feature_name, feature_name] = feature_values[common_feature_name][feature_name]
  df.to_csv(dataset_path)
'''

"""## Stop Lemmas"""

stoplemmas = list()
with open(stoplemma_path, 'r', encoding = 'utf-8') as stoplemmas_file:
  for line in stoplemmas_file:
    stoplemmas.append(line.split(",")[0])

"""## Pre-Processing"""

def preprocess(sentence):
  #remove punctuations
  for symbol in string.punctuation:
    if symbol != ' ':
      sentence = sentence.replace(symbol, "")
  return sentence

# fetch values of lexical charactertistics
import pyiwn
import stanza

pyiwn.download()
iwn = pyiwn.IndoWordNet()

vowels_list = ['ऽ', 'ँ', 'ं', 'ः', 'ऺ', 'ऻ', '़', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॅ', 'ॆ', 'े', 'ै', 'ॉ', 'ॊ', 'ो', 'ौ',
         '्', 'ॎ', 'ॏ', '॑', '॒', '॓', '॔', 'ॕ', 'ॖ', 'ॗ', 'ॢ', 'ॣ', '॰', 'ॱ', '।', '॥','अ', 'आ','इ','ई','उ','ऊ',
         'ऋ','ए','ऐ','ओ','औ','अं','अः']
consonants_list = ['क','ख','ग','घ','ङ','च','छ','ज','झ','ञ','ट','ठ','ड','ढ','ण','त',
'थ','द','ध','न','प','फ','ब','भ','म','य','र','ल','व','श','ष','स','ह','क्ष','त्र','ज्ञ']

def get_length(word):
    word = word.strip()
    return len(word)

def get_root(word):
    """
    Return the root form of the specified word.
    Required argument:
	word (str): the word whose root form is to be retrieved
    """
    word = word.strip()
    doc = nlp(word)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma != None and word.lemma != '':
                return word.lemma
            return word

def get_synsets(word):
    word = word.strip()
    try:
      temp_synsets = iwn.synsets(word)
      return temp_synsets
    except:
      return ""
    

def get_number_of_synsets(word):
    #print(word)
    word = word.strip()
    return len(iwn.synsets(word))

def get_synonyms_in_synset(synset):
    synonyms = []
    #print("fetching synonyms in synset")
    lemma_list = synset.lemmas()
    for i in range(0, len(lemma_list)):
        if lemma_list[i].name() not in synonyms:
            synonyms.append(lemma_list[i].name())
    #print("returning synonyms")
    return synonyms

def get_number_of_synonyms_in_synset(synset):
    synonyms = []
    lemma_list = synset.lemmas()
    for i in range(0, len(lemma_list)):
        if lemma_list[i].name() not in synonyms:
            synonyms.append(lemma_list[i].name())
    return len(synonyms)

def get_number_of_hypernyms(word):
  n_hypernyms=0
  #for v in iwn.all_synsets():
  #  print("totalling number of hypernyms for ", v)
  synsets = get_synsets(word)
  for synset in synsets:
      n_hypernyms += len(iwn.synset_relation(synset, pyiwn.SynsetRelations.HYPONYMY))
  #print("calculated total")
  return n_hypernyms

def get_number_of_hyponyms(word):
  n_hyponyms=0
  synsets = get_synsets(word)
  for synset in synsets:
    n_hyponyms += len(iwn.synset_relation(synset, pyiwn.SynsetRelations.HYPERNYMY))
  return n_hyponyms


def get_synset_id(synset):
    return synset.synset_id()

def get_synset_gloss(synset):
    return synset.gloss()

def get_word_gloss(word):
    word = word.strip()
    synsets = get_synsets(word)
    gloss_list = []
    for synset in synsets:
        gloss_list.append(synset.gloss())
    return gloss_list

def get_synset_examples(synset):
    return synset.examples()

def get_ontology_nodes(synset):
    #print(synset.ontology_nodes())
    return synset.ontology_nodes()

def is_person(synset):
    """ Return true if all the nodes are person nodes. """
    person = True
    ontology_list = get_ontology_nodes(synset)
    for item in ontology_list:
        if item.find('PRSN') == -1:
            person = False
    return person

def is_place(synset):
    """ Return true if all the nodes are physical place nodes. """
    place = True
    ontology_list = get_ontology_nodes(synset)
    for item in ontology_list:
        if item.find('PHSCL') == -1:
            place = False
    return place

def get_number_of_consonants(word):
    word = word.strip()
    consonants = 0
    charList = list(word)
    for character in charList:
        if character in consonants_list:
            consonants = consonants + 1
    return consonants

def get_number_of_vowels(word):
    word = word.strip()
    vowels = 0
    charList = list(word)
    for character in charList:
        if character in vowels_list:
            vowels = vowels + 1
    return vowels

def get_number_of_consonant_conjuncts(word):
    word = word.strip()
    conjuncts = 0
    charList = list(word)
    for character in charList:
        if character == '्':
            conjuncts = conjuncts + 1
    return conjuncts

def get_syllable_count(word):
    syllables = 0
    consonants = 1
    consonant_flag = 0
    charList = list(word)
    prev = -1
    index = 1
    syllables = 1
    #print(charList)
    #find the second consonant
    for i in range(1, len(charList)):
        character = charList[i]
        #print(character)
        if character in consonants_list:
            consonants = consonants + 1
            if consonants == 2:
                break
        index = index + 1
    beg = index
    #print("BEG: ", beg)
    #print(syllables)
    for i in range(index, len(charList)):
        character = charList[i]
        #print(character)
        #character_count = character_count + 1
        #if character_count == 1:
        #    syllables = 1
        #elif character in Words.consonants_list:
        #    consonants = 1
        #    consonant_flag = 1
        #print("PREV: ", prev)
        if character in consonants_list and syllables > 0 and i != len(charList)-1:# and i != prev + 1:
            if (i+1 < len(charList) and charList[i+1] != '़'):
                #print("Charlist i + 1: ", charList[i+1])
                prev = i
                syllables = syllables + 1
                consonant_flag = consonant_flag + 1
        elif ((character == 'य' and charList[i-1] in vowels_list) or character == 'त्र' or (character == 'र' and charList[i-1] == '्') or character == 'ज्ञ')and i == len(charList) - 1:
            syllables = syllables + 1
            continue
        elif character in vowels_list and character != '़' and  character != '्' and i == len(charList)-1 and i != prev + 1:
            if consonant_flag > 0:
                syllables = syllables - 1
            syllables = syllables + 1
            prev = i
        elif character in vowels_list and character != '़' and  character != '्' and i < len(charList)-1 and i != prev + 1 and charList[i-1] == '़':
            syllables = syllables + 1
            prev = i
        if character == '्':
            syllables = syllables - 1
        if character == '़' and i != len(charList)-1 and i-1 != beg and i-1 == prev:
            syllables = syllables - 1
        if character in vowels_list and character != '़' and  character != '्' and i == len(charList)-1 and charList[i-2] in consonants_list and charList[i-1] not in vowels_list:
            syllables = syllables - 1
        #if character == '्' and i == len(charList)-2:
        #    syllables = syllables + 1
        #elif character in Words.vowels_list and syllables > 0 and consonants > 0 and consonant_flag == 1:
         #   if character != '्':
         #       syllables = syllables + 1
          #      consonant_flag = 0
        index = index + 1
        #print(syllables)
    return syllables

def get_frequency(word):
    lemmas_path='/content/drive/MyDrive/Colab/CleanedData/lemmas_new.txt'
    df = pd.read_csv(lemmas_path)
    #print(df.head())
    #df.set_index('word', inplace = True)
    #print(df.columns)
    #print(df['word'] == word)
    try:
      #print(word, df['frequency'].to_numpy()[df['word'] == word].item())
      return df['frequency'].to_numpy()[df['word'] == word].item()
    except:
      return 0

# function to normalise
from sklearn import preprocessing
import numpy as np

def normalise(values):
  reshaped_list = np.array(values).reshape(-1,1)
  scaler = preprocessing.MinMaxScaler()
  normalised_list = scaler.fit_transform(reshaped_list)
  return normalised_list

def get_all_synonyms(word):
    synonyms = list()
    #print("fetching synsets")
    synsets = get_synsets(word)
    for synset in synsets:
      synonyms.extend(get_synonyms_in_synset(synset))
    #print("returning all synonyms")
    return synonyms

def get_freq_lexical_properties(word):
    props = dict()
    props['word'] = word
    props['length'] = get_length(word)
    props['n_synsets'] = get_number_of_synsets(word)
    props['n_synonyms'] = len(get_all_synonyms(word))
    #print("fetching n_consonants")
    props['n_consonants'] = get_number_of_consonants(word)
    #print("fetching n_vowels")
    props['n_vowels'] = get_number_of_vowels(word)
    #print("fetching n_hypernyms")
    props['n_hypernyms'] = get_number_of_hypernyms(word)
    #print("fetching n_hyponyms")
    props['n_hyponyms'] = get_number_of_hyponyms(word)
    #print("fetching n_consonant conjuncts")
    props['n_consonantconjuncts'] = get_number_of_consonant_conjuncts(word)
    #print("fetching n_syllables")
    props['n_syllables'] = get_syllable_count(word)
    #print("fetching frequency")
    props['frequency'] = get_frequency(word)
    #print("returning raw values of all features")
    return props

def create_wordgroup(word):
    reduce_synonyms = 0
    wordgroup = list()
    word = get_root(word)
    #print(word)
    synonyms = set()
    synonyms.update(word)
    #print("fetching all synonyms")
    synonyms.update(get_all_synonyms(word))
    for token in synonyms:
      if token in vowels_list or token in consonants_list:
        reduce_synonyms += 1
        continue
      props = get_freq_lexical_properties(token)
      props['n_synonyms'] -= reduce_synonyms
      # props contains raw un-normalised values
      wordgroup.append(props)
    #[{'word':word, 'length':length, ....}, {'word':word, 'length':length, ....}, ...]
    return wordgroup

def normalise_wordgroup(wordgroup):
    import pandas as pd
    props = ['word', 'length', 'n_synsets', 'n_synonyms', 'n_consonants', 'n_vowels', 
             'n_hypernyms', 'n_hyponyms', 'n_consonantconjuncts', 'n_syllables', 'frequency']
    feature_dict = dict()
    #print(pd.DataFrame.from_dict(wordgroup))
    for word_dict in wordgroup:
      for key, value in word_dict.items():
        key = key.strip()
        #print("key: ", key)
        if key not in feature_dict.keys():
          feature_dict[key] = list()
        feature_dict[key].append(value)
    #print("feature dict: ", pd.DataFrame.from_dict(feature_dict))
    normalised_feature_dict = dict()
    for key, value in feature_dict.items():
      if key != 'word':
        normalised_feature_dict[key] = normalise(feature_dict[key])
        if key == 'frequency':
           print('word: ', feature_dict['word'], ' old: ', feature_dict[key], ' new: ', normalised_feature_dict[key])
      else:
         normalised_feature_dict[key] = feature_dict[key]
         #print("word: ", feature_dict[key])
    #print(normalised_feature_dict)
    for key, value_list in normalised_feature_dict.items():
      if key != 'word':
        #normalised_feature_dict[key] = [element for innerList in value for element in innerList]
        normalised_feature_dict[key] = list()
        for value in value_list:
          normalised_feature_dict[key].append(value[0])
      #print("value: ", value)
    #print("NORMALISED: ", normalised_feature_dict)
    #df = pd.DataFrame.from_dict(normalised_feature_dict)
    df = pd.DataFrame.from_dict(normalised_feature_dict)
    #df = df.reset_index()
    #print(df)
    return df

#normalise_wordgroup(create_wordgroup('बोलता'))

# function to fetch embeddings
#from google.colab import drive
import fasttext

drive.mount('/content/drive')
file = '/content/drive/MyDrive/Colab/AI4Bharat/indicnlp.v1.hi.bin'

model = fasttext.load_model(file)

def vectorise(key):
    try:
        return model.get_word_vector(key)
    except:
	      return [0]*300 #dimensions

"""##Predict"""

import string

stoplemmas = list()


import pickle
import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion

def get_lemma(word):
    """
    Return the root form of the specified word.
    Args:
	    word (str): the word whose root form is to be retrieved
    """
    word = word.strip()
    doc = nlp(word)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma != None and word.lemma != '':
                return word.lemma
            return word

def create_record(word_lemma):
  vector = vectorise(word_lemma)
  df = pd.DataFrame()

  #fasttext vector of the word
  df['vector'] = vector
  X_vector = pd.DataFrame(df['vector'].values.tolist())
  scaler = preprocessing.MinMaxScaler().fit(X_vector)
  X_vector =  pd.DataFrame(scaler.transform(X_vector))
  df.index = X_vector.index
  X_vector = X_vector.transpose()

  #normalised wordgroup
  columns = ['length', 'n_synsets', 'n_synonyms', 'n_consonants', 'n_vowels', 'n_hypernyms', 'n_hyponyms', 'n_consonantconjuncts', 'n_syllables', 'frequency']
  wordgroup = create_wordgroup(word_lemma)
  normalised_wordgroup = normalise_wordgroup(wordgroup)

  #append lexical feature values to the record with embeddings
  for column in columns:
    X_vector[column] = normalised_wordgroup.loc[normalised_wordgroup['word'] == word_lemma][column].values[0]
  return X_vector

def predict(path, word_df):
  #load the model
  model = pickle.load(open(path + 'model', 'rb'))
  #print(word_df.columns)
  return model.predict(word_df)[0]
  #model.transform(word_df)


def process_input(sentence):
  global entry
  global stoplemmas
  predictions = dict()

  sentence = preprocess(sentence)
   
  for word in sentence.split(" "):
    if word not in predictions.keys():
      if word != "\n" and word != "\r\n" and word.strip() != "" :
        #ignore numbers
        if not any(chr.isdigit() for chr in word):
          #fetch the lemma
          word_lemma = get_lemma(word)
          #process the lemma if it is not in stop lemmas
          if word_lemma not in stoplemmas:
            #check if word exists in the wordnet
            if get_synsets(word_lemma) == "":
              predictions[word] = 0
            else:
              record = create_record(word_lemma)
              predictions[word] = predict(path, record)
  print(predictions)

process_input(input("Enter a sentence"))