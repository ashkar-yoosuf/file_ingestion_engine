#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 17:36:12 2018

@author: ashkar
"""
from pymodm import connect, fields, MongoModel
from pymongo import MongoClient
from datetime import datetime

import bson
import requests
import uuid

import config
import datatypes

connect(config.MONGO['connect'])

database_Name = config.DATABASE_CONNECTION['zeptoDB']

#connecting using pymongo
client = MongoClient(config.MONGO['client'])
db = client[database_Name]

class datarecords(MongoModel):
    fileId = fields.CharField()
    dataSetId = fields.CharField()
    rowData = fields.ListField()
    id = fields.IntegerField()

def getDataSet(fileName):

    client = MongoClient(config.MONGO['client'])
    db = client[database_Name]

    dataset1 = db.datasets.find_one({'files.orgFileId': fileName})
    return dataset1

def getStatus(fileName):

    dataset1 = getDataSet(fileName)
    status = dataset1['status']
    return status

def getFileId(fileName):

    dataset1 = getDataSet(fileName)
    files = dataset1['files']
    for i in files:
        if (i['orgFileId'] == fileName):
            fileId = i['fileId']
            return fileId

def getCount(fileId):

    client = MongoClient(config.MONGO['client'])
    db = client[database_Name]

    fileId = str(fileId)
    count = db.datarecords.find({'fileId': fileId}).count()
    return count


#########################################################################################################
def get_rowCount(fileName):

    dataset1 = getDataSet(fileName)
    rowCount = dataset1['lastRowId']

    return rowCount


def checkMeta_Empty(fileName):

    dataset1 = getDataSet(fileName)
    metaData = dataset1['metaData']

    if (metaData == []):
        return True
    else:
        return False

def chechkMeta(fileName, type_list):

    dataset1 =getDataSet(fileName)
    metaData = dataset1['metaData']

    if (len(type_list) == len(metaData)):
        listOfTypes = []
        for i in metaData:
            listOfTypes.append(i['typeOfData'])
        # print(listOfTypes)
        for i in range(len(listOfTypes)):
            if (listOfTypes[i] != type_list[i]):
                msg = ("column "+ str(i+1) + " is having the data type of " + listOfTypes[i] + ". But the original datasheet contains it as a " + type_list[i] + 
                ". Please check the data sheet and try uploading again.")
                return [False, msg]
        return [True]
    else:
        msg = 'Number of Headers are not equal'
        return [False,msg]


 #method to update the merge status of the files array
def update_mergeStatus(fileName,status):

    client = MongoClient(config.MONGO['client'])
    db = client[database_Name]

    dataset1 = getDataSet(fileName)
    files = dataset1['files']
    
    for i in files:
        if  (i['orgFileId'] == fileName):
            i['mergeStatus'] = status
         
    db.datasets.update_one({'files.orgFileId' : fileName}, {'$set': {'files': files}})

def get_mergeStatus(fileName):

    dataset1 = getDataSet(fileName)
    files = dataset1['files']

    for i in files:
        if (i['orgFileId'] == fileName):
            return (i['mergeStatus'])

############################################################################################################

def get_uniqIdList(fileName):

    dataset1 = getDataSet(fileName)
    metaData = dataset1['metaData']
    uniqueId_list = []
    for i in metaData:
        uniq_Id = i['uniqId']
        uniqueId_list.append(uniq_Id)

    return uniqueId_list

def createDataRecords(data_list,fileName,type_list,list_of_values,format_types,sub_types,funct):
    data_records = []
    print(6.1)
    dataset = getDataSet(fileName)
    print(6.2)
    fileId = funct
    print(6.3, fileId)
    print(6.4, len(data_list))
    uniqueId_list = get_uniqIdList(fileName)
    print(6.5)
    for i in range(len(data_list)):
        x = datarecords(
            fileId,
            dataset['_id'],
            list_new(data_list[i], type_list,list_of_values,format_types,sub_types,fileName,uniqueId_list),
            i
        )
        data_records.append(x)
    print(6.6)
    datarecords.objects.bulk_create(data_records)

def list_new(l,type_list,list_of_values,format_types,sub_types,fileName,uniqueId_list):
    newList = []
    rowdata_List = []
    uniqueId_list = uniqueId_list

    new_list = ['fieldId', 'autoId', 'value', 'uniqId']

    for i in range(len(l)):

        unique_ID = uniqueId_list[i]
        newList = [i, i, l[i], unique_ID]
        dic_new = dict(zip(new_list, newList))
        typeOfValue = type_list[i]
        sub_type = sub_types[i]

        if (typeOfValue == datatypes.HEADER_TYPES['date']):
            
            if (dic_new['value'] == ''):
                dic_new['value'] = None

            else:
                if (sub_type == datatypes.DATE_SUBTYPES['dateonly']):

                    format_str = datatypes.PY_DATE_FORMATS[format_types[i]]
                    p = datetime.strptime(dic_new['value'], format_str)
                    date = p.date()
                    dic_new['value'] = p

                    m = date.month
                    d = date.day
                    y = date.year
                    # q = (m-1)//3 + 1

                    w = date.weekday()

                    aggregationVals = {'year_quarter': None, 'quarter': None, 'monthly':None, 'weekly': None, 'day_of_month': None, 'year': None, 'year_month': None, 'year_month_date': None}

                    if(m <= 3):
                        aggregationVals['year_quarter'] =  str(y) + "-Q1"
                        aggregationVals['quarter'] = "Q1"
                    elif(m <= 6):
                        aggregationVals['year_quarter'] = str(y) +  "-Q2"
                        aggregationVals['quarter'] = "Q2"
                    elif(m <= 9):
                        aggregationVals['year_quarter'] = str(y) + "-Q3"
                        aggregationVals['quarter'] = "Q3"
                    elif(m <= 12):
                        aggregationVals['year_quarter'] = str(y) + "-Q4"
                        aggregationVals['quarter'] = "Q4"

                    aggregationVals['monthly'] = config.MONTH_DICT[str(m)]
                    aggregationVals['weekly'] = w + 1
                    aggregationVals['day_of_month'] = d
                    aggregationVals['year'] = y
                    aggregationVals['year_month'] = str(y) + '-' + str(m)
                    aggregationVals['year_month_date'] = str(date)

                    dic_new['aggregationVals'] = aggregationVals

                elif (sub_type == datatypes.DATE_SUBTYPES['datetime']):
                    
                    format_str = datatypes.PY_DATETIME_FORMATS[format_types[i]]
                    p = datetime.strptime(dic_new['value'], format_str)
                    date = p.date()
                    time = p.time()
                    # q = date.isocalendar()
                    dic_new['value'] = p

                    m = date.month
                    d = date.day
                    y = date.year
                    # q = (m-1)//3 + 1

                    w = date.weekday()

                    aggregationVals = {'year_quarter': None, 'quarter': None, 'monthly':None, 'weekly': None, 'day_of_month': None, 'year': None, 'year_month': None, 'year_month_date': None, 'hour_day': None, 'hour_min': None, 'minute_hour': None }

                    if(m <= 3):
                        aggregationVals['year_quarter'] =  str(y) + "-Q1"
                        aggregationVals['quarter'] = "Q1"
                    elif(m <= 6):
                        aggregationVals['year_quarter'] = str(y) +  "-Q2"
                        aggregationVals['quarter'] = "Q2"
                    elif(m <= 9):
                        aggregationVals['year_quarter'] = str(y) + "-Q3"
                        aggregationVals['quarter'] = "Q3"
                    elif(m <= 12):
                        aggregationVals['year_quarter'] = str(y) + "-Q4"
                        aggregationVals['quarter'] = "Q4"

                    aggregationVals['monthly'] = config.MONTH_DICT[str(m)]
                    aggregationVals['weekly'] = w + 1
                    aggregationVals['day_of_month'] = d
                    aggregationVals['year'] = y
                    aggregationVals['year_month'] = str(y) + '-' + str(m)
                    aggregationVals['year_month_date'] = str(date)
                    aggregationVals['hour_day'] = time.hour
                    aggregationVals['hour_min'] = str(time)
                    aggregationVals['minute_hour'] = time.minute

                    dic_new['aggregationVals'] = aggregationVals
                    
                elif(sub_type == datatypes.DATE_SUBTYPES['time']):

                    format_str = datatypes.PY_TIME_FORMATS[format_types[i]]
                    date = datetime.strptime(dic_new['value'], format_str)
                    time = date.time()
                    dic_new ['value'] = date

                    aggregationVals = {'hour_day': None, 'hour_min': None, 'minute_hour': None, 'totalMilliSeconds': None}
                    aggregationVals['hour_day'] = time.hour
                    aggregationVals['hour_min'] = str(time)
                    aggregationVals['minute_hour'] = time.minute
                    milsec = (time.hour * 60 * 60 * 1000) + (time.minute * 60 * 1000)
                    aggregationVals['totalMilliSeconds'] = milsec

                    dic_new['aggregationVals'] = aggregationVals
                    
                elif (sub_type == datatypes.DATE_SUBTYPES['duration']):

                    aggregationVals = {'hour_min': None,'totalMilliSeconds': None}
                    aggregationVals ['hour_min'] = dic_new['value']
                    dic_new['value'] = dic_new['value']
                    time_str = dic_new['value']
                    min = int(time_str[-2:])
                    hour = int(time_str[:-3])
                    milsec = (hour * 60 * 60 *1000) + (min * 60 * 1000)
                    aggregationVals['totalMilliSeconds'] = milsec

                    dic_new['aggregationVals'] = aggregationVals
   
        elif (typeOfValue == datatypes.HEADER_TYPES['number']):
            if (dic_new['value'] == ''):
                dic_new['value'] = None
            else:
                dic_new['value'] = float(dic_new['value'])
        else:
            if (dic_new['value'] == ''):
                dic_new['value'] = None
            else: 
                dic_new['value'] = dic_new['value']

        rowdata_List.append(dic_new)
    return rowdata_List

def list_dataset(funct,header_list,type_list, sub_types, format_types):

    dataset = funct
    metaDataList = dataset['metaData']
    uniqueId_list = []

    for i in range(len(header_list)):
        if (type_list[i] == datatypes.HEADER_TYPES['string']):

            new_dict = {'typeOfData': None, 'orderId': None , 'id': None, 'name': None, 'uniqId': None}
            new_dict ['typeOfData'] = type_list[i]
            new_dict ['orderId'] = i
            new_dict ['id'] = i
            new_dict ['name'] = header_list[i]
            new_dict ['uniqId'] = str(uuid.uuid4())
            uniqueId_list.append(new_dict['uniqId'])

        elif(type_list[i] == datatypes.HEADER_TYPES['number']):
            new_dict = {'typeOfData': None, 'orderId': None ,'id': None,'subTypeOfData': None,  'id': None,'name': None, 'uniqId': None}
            new_dict ['typeOfData'] = type_list[i]

            if (sub_types[i] == datatypes.NUMBER_SUBTYPES['currency']):
                new_dict['subTypeOfData'] = 'Currency'
                new_dict['formatType'] = format_types[i]

            elif(sub_types[i] == datatypes.NUMBER_SUBTYPES['normal']):
                new_dict['subTypeOfData'] = 'Number'
                new_dict['formatType'] = 'null'

            elif(sub_types[i] == datatypes.NUMBER_SUBTYPES['percentage']):
                new_dict['subTypeOfData'] = 'Percentage'
                new_dict['formatType'] = 'null'

            new_dict ['orderId'] = i
            new_dict ['id'] = i
            new_dict ['name'] = header_list[i]
            new_dict ['uniqId'] = str(uuid.uuid4())
            uniqueId_list.append(new_dict['uniqId'])

        elif (type_list[i] == datatypes.HEADER_TYPES['date']):
            new_dict = {'typeOfData': None, 'orderId': None , 'id': None,'subTypeOfData': None, 'dataFormat': [],  'isDuration': False ,  'name': None, 'uniqId': None,}
            new_dict ['typeOfData'] = type_list[i]
            if (sub_types[i] == datatypes.DATE_SUBTYPES['duration']):
                new_dict ['isDuration'] = True
            new_dict ['subTypeOfData'] = sub_types[i]
            new_dict ['orderId'] = i
            new_dict ['id'] = i
            new_dict ['dataFormat'].append(format_types[i])
            new_dict ['name'] = header_list[i]
            new_dict ['uniqId'] = str(uuid.uuid4())
            uniqueId_list.append(new_dict['uniqId'])

        metaDataList.append(new_dict)

    return_values = [metaDataList, uniqueId_list]

    return return_values



#######################getting the information of the corrected headers

def get_fileName(fileName):

    dataset1 = getDataSet(fileName)
    files = dataset1['files']

    for i in files:
        if  (i['orgFileId'] == fileName):
            file_name = i['fileName']
            
            return file_name

#Update status on the file of the dataset
def update_fileErrorStatus(fileName, key, status):

    client = MongoClient(config.MONGO['client'])
    db = client[database_Name]

    dataset1 = getDataSet(fileName)
    files = dataset1['files']

    for i in files:
        if  (i['orgFileId'] == fileName):
            i[key] = status

    db.datasets.update_one({'files.orgFileId' : fileName}, {'$set' : { 'files' : files } })
    post_errorMsg(fileName, status)

#update the status in the dataset

#name should be changed to update_dataSetValues
def update_dataSetStatus(fileName, key, status):

    client = MongoClient(config.MONGO['client'])
    db = client[database_Name]
    
    db.datasets.update_one({'files.orgFileId' : fileName}, {'$set' : { key : status } })


def post_result(fileName):
    
    dataset1 = getDataSet(fileName)

    dataset_Id = dataset1['_id']

    body = {
        "userId": dataset1['userId'],
        "componentId" : "dataSetCom",
        "status" : dataset1['status'],
        "dataSetId": str(bson.objectid.ObjectId(dataset_Id)),
    }

    requests.post(config.SOCKET['upload_response'], body)

def post_errorMsg(fileName, errorMsg):

    dataset1 = getDataSet(fileName)

    dataset_Id = dataset1['_id']

    body = {
        "userId": dataset1['userId'],
        "componentId" : "errorMsgCom",
        "msg" : errorMsg,
        "dataSetId": str(bson.objectid.ObjectId(dataset_Id)),
        "fileId" : getFileId(fileName)
    }

    requests.post(config.SOCKET['upload_errMerge'], body)

def post_mergeStatus(fileName):

    dataset1 = getDataSet(fileName)

    dataset_Id = dataset1['_id']

    body = {
        "userId": dataset1['userId'],
        "componentId" : "dataSetComMerge",
        "mergeStatus" : get_mergeStatus(fileName),
        "dataSetId": str(bson.objectid.ObjectId(dataset_Id)),
        "fileId" : getFileId(fileName)
    }
    requests.post(config.SOCKET['upload_mergeResponse'], body)

def post_errMerge(fileName,type_list):

    dataset1 = getDataSet(fileName)
    
    dataset_Id = dataset1['_id']

    body = {
        "userId": dataset1['userId'],
        "componentId" : "errorMsgCom",
        "msg" : chechkMeta(fileName, type_list)[1],
        "dataSetId": str(bson.objectid.ObjectId(dataset_Id)),
        "fileId" : getFileId(fileName)
    }

    requests.post(config.SOCKET['upload_errMerge'], body)