# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 03:02:59 2018

@author: chiran sachintha
"""


import t_data
import config
import f_load
import f_process

import collections
from scipy.stats import normaltest
import nltk
import math
from datetime import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import random
import numpy as np
import json
#import re

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

def sigmoid_output_to_derivative(output):
    return output*(1-output)

def clean_up_sentence(sentence,stemmer):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words,stemmer):
    sentence_words = clean_up_sentence(sentence,stemmer)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return(np.array(bag))
    
def think(sentence,words,synapse_0,synapse_1,stemmer):
    x = bow(sentence.lower(), words,stemmer)
    l0 = x
    l1 = sigmoid(np.dot(l0, synapse_0))
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2

def regDataType(str):
    if len(str) == 0:
        return 'BLANK'
    if f_process.re.match(r'^\d{1,2}([:.]?\d{1,2})?([ ]?[a|p]m)?$', str):
        return 'TIME'
    if f_process.re.match(r'(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})$', str):
        return 'month-year'
    if f_process.re.match(r'[\w\.-]+@[\w\.-]+$', str):
        return 'E-mail'
    return 'Categerical data'

def train(X, y,classes,words, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

    np.random.seed(1)

    last_mean_error = 1
    synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2*np.random.random((hidden_neurons, len(classes))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)
        
    for j in iter(range(epochs+1)):

        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
                
        if(dropout):
            layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))
            
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        layer_2_error = y - layer_2

        if (j% 10000) == 0 and j > 5000:
            
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                break
                
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        layer_1_error = layer_2_delta.dot(synapse_1.T)

        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
        
        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))
        
        if(j > 0):
            synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))        
        
        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update
        
        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    synapse = {config.fields['synapse0']: synapse_0.tolist(), config.fields['synapse1']: synapse_1.tolist(),
               config.fields['words']: words,
               config.fields['classes']: classes
              }
    synapse_file = config.fields['filename']

    with open(synapse_file, 'w') as outfile:
        json.dump(synapse, outfile, indent=4, sort_keys=True)


def domain_classification(sentence):
    synapse=[]
    stemmer = PorterStemmer()
    training_data=t_data.domain_training_data
    words = []
    classes = []
    documents = []
    ignore_words = ['?']

    for pattern in training_data:

        w = nltk.word_tokenize(pattern['sentence'])
        words.extend(w)
        documents.append((w, pattern['class']))
        if pattern['class'] not in classes:
            classes.append(pattern['class'])
        
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
    words = list(set(words))
    
    classes = list(set(classes))
    
    training = []
    output = []
    output_empty = [0] * len(classes)
    
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
    
        training.append(bag)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        output.append(output_row)

    i = 0
    w = documents[i][0]
    
    X = np.array(training)
    y = np.array(output)
    
   # train(X, y,classes,words, hidden_neurons=4, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2)
    

    synapse_file = 'synapses.json' 
    with open(synapse_file) as data_file: 
        synapse = json.load(data_file) 
        synapse_0 = np.asarray(synapse['synapse0']) 
        synapse_1 = np.asarray(synapse['synapse1'])
        
    results = think(sentence,words,synapse_0,synapse_1,stemmer)
    ERROR_THRESHOLD = 0.2
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
    results.sort(key=lambda x: x[1], reverse=True) 
    return_results =[[classes[r[0]],r[1]] for r in results]
    return return_results
       
def chechkMeta(fileName,db):
   dataset1 = db.datasets.find_one({'files.orgFileId': fileName})
   metaData = dataset1['metaData']

   list_of_headers = []
   for i in metaData:
       list_of_headers.append(i['name'])
   return list_of_headers

def sampleSize(no_of_rows):
    sample_size = 384/(1+(383/(no_of_rows+1)))
    return sample_size


def dev_group(data_set, no_of_groups):

    grouped_list = []

    division = int(len(data_set)/no_of_groups)
    for i in range(1, no_of_groups):
        grouped_list.append(data_set[(i-1)*division:i*division])

    grouped_list.append(data_set[division*i:])
    return grouped_list


def identify_numeric(group_list, no_of_sample):
    missing_value_list = ["?", "NA", "NULL", "#"]
    for i in range(no_of_sample):
        random.shuffle(group_list)
        sample = random.choice(group_list)

        try:
            for i in sample:
                float(i)
        except:
            if i in missing_value_list:
                continue
            else:
                return sample

        k = group_list.index(sample)
        group_list.pop(k)
    return "numeric"


def normal_distribution(data_list):
    try:
        stat, p = normaltest(data_list)
        alpha = 0.05
        if p > alpha:
            return 1
        else:
            return 0
    except:
        return 0

def char_equity(data_list):
    data_list = list(map(str, data_list))
    for i in range(len(data_list)-1):
        if len(data_list[i]) != len(data_list[i+1]):
            return 0
    else:
        return 1


def lead_0(data_list):
    data_list = list(map(str, data_list))
    for i in range(len(data_list)-1):
        if data_list[i][0] == '0':
            return 1
    else:
        return 0


def unique_values(data_list):
    counter = collections.Counter(data_list)
    return len(counter.keys())


def longestSubstringFinder(data_list):
    string1 = data_list[0]
    for i in range(1, len(data_list)):
        string2 = data_list[i]
        answer = ""
        len1, len2 = len(string1), len(string2)
        for i in range(len1):
            for j in range(len2):
                lcs_temp = 0
                match = ''
                while ((i+lcs_temp < len1) and (j+lcs_temp < len2) and string1[i+lcs_temp] == string2[j+lcs_temp]):
                    match += string2[j+lcs_temp]
                    lcs_temp += 1
                if (len(match) > len(answer)):
                    answer = match
        string1 = answer
    return answer


def num_id_type(data_list, char_equity):
    value = 0
    if char_equity:
        value = value+0.8
    if value > 0.5:
        return num_id_type


def str_id_type(data_list, char_equity, unique_values):
    value = 0
    if char_equity:
        value = value+0.3
    if len(data_list) == len(unique_values):
        value = value+0.8


def measure_data(normally_distributed, no_of_unique_values, char_equity, lead_0, data_type='FLOAT'):
    value = 0
    if data_type == config.data_types['integer']:
        value = value+0.8
    if data_type == config.data_types['float']:
        value = value+0.8
    if normally_distributed == 1:
        value = value+0.3
    if char_equity == 0:
        value = value+0.1
    if lead_0 == 0:
        value = value+0.1
    if value >= 1:
        return 1
    else:
        return 0


def cat_data(data_list):
    counter = collections.Counter(data_list)
    unique_values = len(counter.keys())
    try:
        if (unique_values*100/len(data_list)) < 30:
            return 1
        else:
            return 0
    except:
        return 1


def calculate_class_score_commonality(class_words, corpus_words, sentence, class_name, stemmer, show_details=True):
    score = 0
    for word in nltk.word_tokenize(sentence):
        if stemmer.stem(word.lower()) in class_words[class_name]:
            score += (1 / corpus_words[stemmer.stem(word.lower())])
    return score


def calculate_class_score_commonality_similar(class_words, corpus_words, sentence, class_name, stemmer, show_details=True):

    score = 0
    for word in nltk.word_tokenize(sentence):
        similar_word_list = similar(word)
        for sim_word in similar_word_list:
            if stemmer.stem(sim_word.lower()) in class_words[class_name]:
                score += (1 / corpus_words[stemmer.stem(sim_word.lower())])
    return score


def similar(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms


def classify(sentence, class_words, corpus_words, stemmer):
    sentence = sentence.split("_")
    sentence = " ".join(sentence)

    high_class = None
    high_score = 0
    for c in class_words.keys():
        score = calculate_class_score_commonality(class_words, corpus_words,
                                                  sentence, c, stemmer, show_details=False)
        if score > high_score:
            high_class = c
            high_score = score
    if high_class == None:
        for c in class_words.keys():
            score = calculate_class_score_commonality_similar(
                class_words, corpus_words, sentence, c, stemmer, show_details=False)
            if score > high_score:
                high_class = c
                high_score = score
        if high_class != None:
            return high_class
        else:
            return config.fields['unidentifiedkeyword']

    else:
        return high_class


def column_datatype(high_class):
    datatype = {'DATE': ["date"]}
    for data_types, header_list in datatype.items():
        if high_class in header_list:
            return data_types


def check_column_data(colum_data_type, no_of_rows, list2, weight=0.75):
    count = 0
    counter = collections.ounter(list2)
    for i in range(len(list2)):
        if list2[i] != colum_data_type:
            count = count+1
    if no_of_rows*weight > count:
        return colum_data_type
    elif max(counter.values()) >= no_of_rows*0.5:
        for key, value in counter.items():
            if value == max(counter.values()):
                return key
    else:
        return config.data_types['unidentifieddatatype']


def frequancy(data):
    counter = collections.Counter(data)
    return len(counter.keys())


def highest_value(data):
    counter_value = collections.Counter(data)
    maximum = max(counter_value.values())
    for key, value in counter_value.items():
        if value == maximum:
            return key


def get_headersList(fileName, db):
    dataset1 = db.datasets.find_one({config.fields['org_field']: fileName})
    metaData = dataset1[config.fields['meta_data']]
    listOfTypes = []
    for i in metaData:
        listOfTypes.append(i[config.fields['typeOfData']])
    return listOfTypes


def get_dataSet(fileName, db):
    dataset1 = db.datasets.find_one({config.fields['org_field']: fileName})
    return dataset1


def get_fileId(fileName, db):
    dataset1 = get_dataSet(fileName, db)
    files = dataset1[config.fields['files']]
    for i in files:
        if (i[config.fields['org_file_id']] == fileName):
            fileId = i[config.fields['file_id']]
            fileId = str(f_load.bson.objectid.ObjectId(fileId))
            return fileId


def column_data_records(fileName, db):
    column_data_records_1 = []
    dataset1 = get_dataSet(fileName, db)
    metadata = dataset1[config.fields['meta_data']]
    fileId = get_fileId(fileName, db)
    datarecord1 = list(db.datarecords.find({config.fields['file_id']: fileId}))
    for l in metadata:
        column_data = []
        i = str(l[config.fields['uniq_id']])
        column_data.append(i)
        column_data.append(l[config.fields['name']])
        for j in datarecord1:
            row_data = j[config.fields['row_data']]
            for k in row_data:
                 if i == k[config.fields['uniq_id']]:
                    if type(k[config.fields['value']]) == datetime:
                        column_data.append(str(k[config.fields['value']].date()))
                    elif k[config.fields['value']]!=None or k[config.fields['value']]!='' :
                        column_data.append(k[config.fields['value']])
        column_data_records_1.append(column_data)
    return column_data_records_1

def data_sense(fileName,db,data_sense_dict,data_records,class_words, corpus_words, stemmer):
    for data in data_records:
        new_dict = {config.fields['file_id']: None, config.fields['key_value']: None, config.fields['data_type']: None}
        field = data.pop(0)
        new_dict[config.fields['file_id']] = field
        header_name = data.pop(0)
        for k in range(0, 10):
            random.shuffle(data)
        if len(data)>100:
            sample_size = sampleSize(len(data))
            no_of_groups = math.ceil((len(data)/sample_size))
            group_list = dev_group(data, no_of_groups)
            value_1 = identify_numeric(group_list, no_of_groups)
        else:
            group_list=[data]
            value_1=identify_numeric(group_list, 1)
        high_class = classify(header_name, class_words, corpus_words, stemmer)
        new_dict[config.fields['key_value']] = high_class
        if column_datatype(high_class):
            new_dict[config.fields['data_type']] = column_datatype(high_class)
        else:
            if value_1 == config.data_types['numeric_data']:
                data_list = list(map(float, data))
                normal_distribution_1 = normal_distribution(data_list)
                unique_values_1 = unique_values(data)
                char_equity_1 = char_equity(data)
                lead_0_1 = lead_0(data)
                measure_data_1 = measure_data(
                    normal_distribution_1, unique_values_1, char_equity_1, lead_0_1)
                cat_data_1 = cat_data(data_list)
                if measure_data_1 == 0 and cat_data_1 == 1:
                    new_dict[config.fields['data_type']] = config.data_types['categorical_data']
                else:
                    new_dict[config.fields['data_type']] = config.data_types['measure_data']
            key_word_list = []
            if type(value_1) == list:
                for i in range(len(value_1)):
                    reg_data_type = regDataType(str(value_1[i]))
                    key_word_list.append(reg_data_type)
                key_word_type = highest_value(key_word_list)
                if key_word_type == "DATE":
                    new_dict[config.fields['data_type']] = config.data_types['date']
                else:
                    new_dict[config.fields['data_type']] = config.data_types['categorical_data']
            if value_1 == config.data_types['numeric_data']:
                data_list = list(map(float, data))
                normal_distribution_1 = normal_distribution(data_list)
                unique_values_1 = unique_values(data)
                char_equity_1 = char_equity(data)
                lead_0_1 = lead_0(data)
                measure_data_1 = measure_data(
                    normal_distribution_1, unique_values_1, char_equity_1, lead_0_1)
                cat_data_1 = cat_data(data_list)
                if measure_data_1 == 0 and cat_data_1 == 1:
                    new_dict[config.fields['data_type']] = config.data_types['categorical_data']
                else:
                    new_dict[config.fields['data_type']] = config.data_types['measure_data']
            key_word_list = []
            if type(value_1) == list:
                for i in range(len(value_1)):
                    reg_data_type = regDataType(str(value_1[i]))
                    key_word_list.append(reg_data_type)
                key_word_type = highest_value(key_word_list)
                if key_word_type == "date":
                    new_dict[config.fields['data_type']] = config.data_types['date']
                else:
                    new_dict[config.fields['data_type']] = config.data_types['categorical_data']
        #domain_name=domain_classification(headers)
        #print(str(domain_name))
#    domain[config.fields['domain_name']] = "val"
#    dic_1[config.fields['data_sense']].append(domain)
        data_sense_dict[config.fields['data_sense']]['columnInfo'].append(new_dict)
        #dic_1[config.fields['data_sense']].append(new_dict)
        #domain=domain_classification(headers)
        db.datasets.update_one({config.fields['org_field']: fileName}, {config.fields['$set']: data_sense_dict})
def classWords(training_data,class_words,corpus_words,stemmer):
    classes = list(set([a['class'] for a in training_data]))
    for c in classes:
        class_words[c] = []

    for data in training_data:
        for word in nltk.word_tokenize(data['sentence']):
            if word not in ["?", "'s"]:
                stemmed_word = stemmer.stem(word.lower())
                if stemmed_word not in corpus_words:
                    corpus_words[stemmed_word] = 1
                else:
                    corpus_words[stemmed_word] += 1
                class_words[data['class']].extend([stemmed_word])
def domain_identification(header_list):
    domain_name=domain_classification(" ".join(header_list))
    try:
        domain=domain_name[0][0]
        return domain
    except:
        domain=config.fields['unidentifieddomain']
        return domain
    
def dataSense(fileName):
    training_data = t_data.headers_training_data
    stemmer = PorterStemmer()
    corpus_words = {}
    class_words = {}
    classWords(training_data,class_words,corpus_words,stemmer)
    client = f_load.MongoClient(config.MONGO['client'])
    db = client.zeptoDB
    data_records = column_data_records(fileName, db)
    header_list= chechkMeta(fileName,db)
    domain_type= domain_identification(header_list)
    data_sense_dict={config.fields['data_sense']:{'domainName':domain_type,'columnInfo':[]}}
    data_sense(fileName,db,data_sense_dict,data_records,class_words, corpus_words, stemmer)