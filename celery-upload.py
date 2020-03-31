#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis
import subprocess
import sys
import fnmatch
import traceback

from celery import Celery
from celery import chain

from kombu import Exchange, Queue

####################
#importing methods from method files
import config
import f_process
import f_load
import f_sense

####################

app = Celery(config.CELERY_APP['name'], broker=config.CELERY_APP['broker'], backend=config.CELERY_APP['backend'])
app.conf.task_queues = (
    Queue(config.QUEUE['main'], Exchange(config.QUEUE['main'], delivery_mode=1), routing_key=config.QUEUE['main'], durable=False),
    Queue(config.QUEUE['temp'], Exchange(config.QUEUE['temp'], delivery_mode=1), routing_key=config.QUEUE['temp'], durable=False),
    Queue(config.QUEUE['q1'], Exchange(config.QUEUE['q1'], delivery_mode=1), routing_key=config.QUEUE['q1'], durable=False),
    Queue(config.QUEUE['q2'], Exchange(config.QUEUE['q2'], delivery_mode=1), routing_key=config.QUEUE['q2'], durable=False),
    Queue(config.QUEUE['q3'], Exchange(config.QUEUE['q3'], delivery_mode=1), routing_key=config.QUEUE['q3'], durable=False),
    Queue(config.QUEUE['q4'], Exchange(config.QUEUE['q4'], delivery_mode=1), routing_key=config.QUEUE['q4'], durable=False),
)

invoke_insights = config.INSIGHT['invoke_insights']

r = redis.StrictRedis(host=config.REDIS['host'], port=config.REDIS['port'], charset="utf-8", decode_responses=True)

def invokeInsigths(fileName):

    dataset1 = f_load.getDataSet(fileName)

    dataset_Id = dataset1['_id']

    body = {
        "dataSetId": str(f_load.bson.objectid.ObjectId(dataset_Id)),
        "rowCount" : int(dataset1['lastRowId'])
    }
    try :
        f_load.requests.post(invoke_insights, body)
    except Exception as e:
        print(e)
    print ("invoke")

@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def csv_function(path):

    fileName = path.split("/")[-1]
        
    user_correction_status = f_process.get_userCorrectionStatus(fileName)

    if user_correction_status != config.USER_CORRECTION_STATUS['pending']:
        return f_process.csv_transform(path, user_correction_status, fileName)
    else:#user_correction_status == config.USER_CORRECTION_STATUS['pending']
        f_process.useCheckMeta_Empty(fileName, config.DATABASE_STATES['process_fail'])
        return [path]
    
@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def xls_function(path):
    
    fileName = path.split("/")[-1]
        
    user_correction_status = f_process.get_userCorrectionStatus(fileName)

    if user_correction_status != config.USER_CORRECTION_STATUS['pending']:
        return f_process.xls_transform(path, user_correction_status, fileName)
    else:#user_correction_status == config.USER_CORRECTION_STATUS['pending']
        f_process.useCheckMeta_Empty(fileName, config.DATABASE_STATES['process_fail'])
        return [path]

@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def xlsx_function(path):

    fileName = path.split("/")[-1]
        
    user_correction_status = f_process.get_userCorrectionStatus(fileName)

    if user_correction_status != config.USER_CORRECTION_STATUS['pending']:
        return f_process.xlsx_transform(path, user_correction_status, fileName)
    else:#user_correction_status == config.USER_CORRECTION_STATUS['pending']
        f_process.useCheckMeta_Empty(fileName, config.DATABASE_STATES['process_fail'])
        return [path]

@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def load_function(chaindata):
    
    f_load.connect(config.MONGO['connect'])

    fileName = (chaindata[0].split("/"))[-1]

    if (f_load.get_mergeStatus(fileName) == config.DATABASE_STATES['process_success']):

        header_list = chaindata[1]
        type_list = chaindata[2]
        data_list = chaindata[3]
        sub_types = chaindata[4]
        format_types = chaindata[5]

        var = f_load.checkMeta_Empty(fileName)
        #cheking the metaData field of the dataset is empty or not.
        #if empty metadeta will be added. If not check for any available missmatching of the datatypes of the columns. 
        #then is there is no miss match with the current metaData list dta records will be added to the database. Else an error msg will be sent to the socket serve
        try:    
            if (var == True):
                f_load.update_dataSetStatus(fileName, 'status', config.DATABASE_STATES['load_start'])
                print(1)
                # db.datasets.update_one({'files.orgFileId' : fileName}, {'$set': {'status': config.DATABASE_STATES['load_start']}})
                f_load.post_result(fileName)
                print(2)
                f_load.update_mergeStatus(fileName,config.DATABASE_STATES['load_start'])
                # post_mergeStatus(fileName)
                #updating the metaDeta
                print(3)
                f_load.update_dataSetStatus(fileName, 'lastRowId', len(data_list))
                #db.datasets.update_one({'files.orgFileId': fileName}, {'$set': {"lastRowId": len(data_list)}})
                print(4)
                list_of_values = f_load.list_dataset(f_load.getDataSet(fileName),header_list, type_list,sub_types, format_types)
                print(5)
                f_load.update_dataSetStatus(fileName, 'metaData', list_of_values[0])
                # db.datasets.update({'files.orgFileId': fileName},  {'$set': { "metaData": list_of_values[0]} })
                print(6)
                #updating the dataRecords collection
                f_load.createDataRecords(data_list,fileName, type_list, list_of_values, format_types, sub_types, f_load.getFileId(fileName))
                print(7)
            #meta data llist is not empty
            else:
                #checking for the equality of the data types of the column
                if (f_load.chechkMeta(fileName, type_list)[0] == True):
                    #updating the rowCount 
                    last_rowId = f_load.get_rowCount(fileName)
                    new_rowCount = len(data_list) + last_rowId
    
                    f_load.update_dataSetStatus(fileName, 'lastRowId', new_rowCount)
                    #updating the dataRecords collection if and only if metaDeta is matcching.
                    list_of_values = f_load.list_dataset(f_load.getDataSet(fileName),header_list, type_list,sub_types, format_types)
    
                    f_load.createDataRecords(data_list,fileName, type_list, list_of_values, format_types, sub_types, f_load.getFileId(fileName))
    
                elif (f_load.chechkMeta(fileName, type_list)[0] == False):
                    #posting the error msg to the socket serve
                    f_load.post_errMerge(fileName,type_list)
                    f_load.update_mergeStatus(fileName, config.DATABASE_STATES['load_fail'])
                    f_load.post_mergeStatus(fileName)
        
        except Exception as e:
            f_load.update_fileErrorStatus(fileName, 'errorInfo', str(type(e)) + str(e))
            print (e)
        
        if (var == True):
            
            if (f_load.getCount(f_load.getFileId(fileName)) == len(data_list)):
    
                f_load.update_dataSetStatus(fileName, 'status', config.DATABASE_STATES['load_success'])
                # db.datasets.update_one({'files.orgFileId' : fileName}, {'$set': {'status': config.DATABASE_STATES['load_success']}})
                f_load.post_result(fileName)
                f_load.update_mergeStatus(fileName, config.DATABASE_STATES['load_success'])
                # post_mergeStatus(fileName)
                invokeInsigths(fileName)
                    
            else:

                f_load.update_dataSetStatus(fileName, 'status', config.DATABASE_STATES['load_fail'])
                # db.datasets.update_one({'files.orgFileId' : fileName}, {'$set': {'status': config.DATABASE_STATES['load_fail']}})
                f_load.post_result(fileName)
                f_load.update_mergeStatus(fileName, config.DATABASE_STATES['load_fail'])
                # post_mergeStatus(fileName)
                f_process.sendemail(fileName, "Load Failed")
                
        elif (var == False):

            if (f_load.getCount(f_load.getFileId(fileName)) == len(data_list)):

                f_load.update_mergeStatus(fileName, config.DATABASE_STATES['load_success'])
                # db.datasets.update_one({'files.orgFileId' : fileName}, {'$set': {'status': 'LOAD_SUCCESS'}})
                f_load.post_mergeStatus(fileName)
                
                invokeInsigths(fileName)
            else:
                #db.datasets.update_one({'files.orgFileId' : fileName}, {'$set': {'status': 'LOAD_FAIL'}})
                f_load.update_mergeStatus(fileName, config.DATABASE_STATES['load_fail'])
                #posting the merge status to socket serve
                f_load.post_mergeStatus(fileName)
                f_process.sendemail(fileName, "Load Failed")
    # delete of file instead of clean function
    if f_process.os.path.exists(chaindata[0]):
        f_process.os.remove(chaindata[0])

    return chaindata

@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def sense_function(chaindata):

    if config.ENABLE['sense']:
    
        fileName = (chaindata[0].split("/"))[-1]
        try:
            if f_load.get_mergeStatus(fileName) == config.DATABASE_STATES['load_success']:
                f_sense.dataSense(fileName)
            else:
                print('error in else no load_success')
        except Exception as e:
            print('error in exception', e)
            traceback.print_exc()
            f_process.sendemail(fileName, str(type(e)) + str(e))


def startTasks(filelist):
    for i in filelist:
        if (i[-4:] == ".csv"):
            bestQueue=getQueueState()
            if (f_process.os.path.getsize(i) < 110000000):
                chain(csv_function.s(i).set(queue=bestQueue), load_function.s().set(queue=bestQueue), sense_function.s().set(queue=bestQueue)).apply_async(queue=bestQueue)
            else:
                f_load.update_dataSetStatus(i.split("/")[-1], 'status', config.DATABASE_STATES['process_fail'])
                f_process.sendemail(i.split("/")[-1], "File too large")
                
        elif (i[-4:] == ".xls"):
            bestQueue=getQueueState()
            if (f_process.os.path.getsize(i) < 110000000):
                chain(xls_function.s(i).set(queue=bestQueue), load_function.s().set(queue=bestQueue), sense_function.s().set(queue=bestQueue)).apply_async(queue=bestQueue)
            else:
                f_load.update_dataSetStatus(i.split("/")[-1], 'status', config.DATABASE_STATES['process_fail'])
                f_process.sendemail(i.split("/")[-1], "File too large")
                
        elif (i[-5:] == ".xlsx"):
            bestQueue=getQueueState()
            if (f_process.os.path.getsize(i) < 110000000):
                chain(xlsx_function.s(i).set(queue=bestQueue), load_function.s().set(queue=bestQueue), sense_function.s().set(queue=bestQueue)).apply_async(queue=bestQueue)
            else:
                f_load.update_dataSetStatus(i.split("/")[-1], 'status', config.DATABASE_STATES['process_fail'])
                f_process.sendemail(i.split("/")[-1], "File too large")


def startTempTasks(filelist):
    removelist = []
    print ("in startTempasks........")
    for i in filelist:
        user_correction_status = f_process.get_userCorrectionStatus(i[0].split("/")[-1])
        print ("iteration number" + str(i), user_correction_status)
        if user_correction_status == config.USER_CORRECTION_STATUS['success']:
            # shutil.move(temp_path_to_watch+i[0].split("/")[-1], path_to_watch)
            f_process.shutil.copy2(config.WATCH_PATHS['temp']+i[0].split("/")[-1], config.WATCH_PATHS['main']+i[0].split("/")[-1])
            print("second copy: "+i[0].split("/")[-1])
            f_process.os.remove(config.WATCH_PATHS['temp']+i[0].split("/")[-1])
            removelist.append(i)
        elif (user_correction_status == config.USER_CORRECTION_STATUS['pending']):
            if (i[1] > 6):
                # shutil.move(temp_path_to_watch+i[0].split("/")[-1], path_to_watch)
                f_process.shutil.copy2(config.WATCH_PATHS['temp']+i[0].split("/")[-1], config.WATCH_PATHS['main']+i[0].split("/")[-1])
                print("second copy: "+i[0].split("/")[-1])
                f_process.os.remove(config.WATCH_PATHS['temp']+i[0].split("/")[-1])
                removelist.append(i)
        elif (user_correction_status) == '':
            f_process.os.remove(config.WATCH_PATHS['temp']+i[0].split("/")[-1])
            removelist.append(i)
        else:
            if (i[1] > 6):
                f_process.shutil.copy2(config.WATCH_PATHS['temp']+i[0].split("/")[-1], config.WATCH_PATHS['main']+i[0].split("/")[-1])
                print("second copy: "+i[0].split("/")[-1])
                f_process.os.remove(config.WATCH_PATHS['temp']+i[0].split("/")[-1])
                removelist.append(i)
    return removelist

def findFiles(watch_path):
  matches = []
  for root, dirnames, filenames in f_process.os.walk(watch_path):
    for filename in fnmatch.filter(filenames, '*.csv'):
      matches.append(f_process.os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, '*.xls'):
      matches.append(f_process.os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, '*.xlsx'):
      matches.append(f_process.os.path.join(root, filename))
  return matches

def getQueueState():
    result = subprocess.check_output(['sudo', 'rabbitmqctl', 'list_queues'])
    A = []
    try:
        A.append(getValues(result, config.QUEUE['q1']))
    except Exception as e:
        A.append([0, config.QUEUE['q1']])
    try:
        A.append(getValues(result, config.QUEUE['q2']))
    except Exception as e:
        A.append([0, config.QUEUE['q2']])
    try:
        A.append(getValues(result, config.QUEUE['q3']))
    except Exception as e:
        A.append([0, config.QUEUE['q3']])
    try:
        A.append(getValues(result, config.QUEUE['q4']))
    except Exception as e:
        A.append([0, config.QUEUE['q4']])

    A.sort(key=lambda x: x[0])
    #print(A)
    bestQueue = A[0][1]
    #print(bestQueue)
    return bestQueue

def out(str):
  #print (str)
  sys.stdout.flush()

def getValues(a,q):
    a=a.decode("utf-8")
    a=a.split()
    value=a.index(q)
    return [int(a[value+1]),q]

@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def main():
    after = {}
    added = []
    start = dict ((f, f_process.os.path.getmtime(f)) for f in findFiles(config.WATCH_PATHS['main']))
    starttime = f_process.time.time()
    
    ##
    fileslist = [f for f in findFiles(config.WATCH_PATHS['temp'])]
    for i in fileslist:
        f_process.os.remove(i)

    while 1:
        before = dict ((f, f_process.os.path.getmtime(f)) for f in findFiles(config.WATCH_PATHS['main']))
        count = 0
        nowtime = f_process.time.time()
        removelist = []
        if nowtime - starttime > 10:
            for filee in start:
                count += 1
                if count < 3:
                    f_process.shutil.copy2(config.WATCH_PATHS['main']+ filee.split("/")[-1], config.WATCH_PATHS['temp']+filee.split("/")[-1])
                    f_process.os.remove(filee)
                    removelist.append(filee)
                else:
                    break
            for item in removelist:
                del start[item]
            starttime = f_process.time.time()
        f_process.time.sleep(1)
        if added:
            out("Added: " + ", ".join (added))
        if (added):
            startTasks(added)
        after = dict((f, f_process.os.path.getmtime(f)) for f in findFiles(config.WATCH_PATHS['main']))
        added = [f for f in after.keys() if not f in before.keys()]

@app.task(autoretry_for=(Exception,), default_retry_delay=config.CELERY_RETRY['delay'], retry_kwargs={'max_retries': config.CELERY_RETRY['number_of_times']})
def tempmain():
    tempafter = {}
    templist = []
    tempset = set()

    while 1:
        removelist = []
        tempafter = dict ((f, f_process.os.path.getmtime(f)) for f in findFiles(config.WATCH_PATHS['temp']))
        templist += [[f,0] for f in tempafter.keys() if f not in tempset]
        print ("tempafter", tempafter, "templist", templist, "tempset", tempset)
        for i in tempafter.keys():
            tempset.add(i)
        if (templist):
            for x in templist:
                x[1] += 1
            print (templist)
            removelist = startTempTasks(templist)
        for i in removelist:
            tempset.remove(i[0])
            del templist[templist.index(i)]
        f_process.time.sleep(10)

if __name__ == '__main__':
    main.apply_async(queue=config.QUEUE['main'])
    tempmain.apply_async(queue=config.QUEUE['temp'])
