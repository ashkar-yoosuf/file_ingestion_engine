#defining the app serve end point
ZEPTO_SOCKET_SERVER = "http://10.0.0.35:3007"
CONSTANT_DATA_SENSE_SERVER_URL = "http://10.0.1.232:5000"

DATABASE_CONNECTION = {
    'zeptoDB' : 'zeptoDB'
}

AWS_SERVERS = {
    'app_server': '10.0.0.207',
    'db_server': '10.0.1.137',
    'upload_server': '10.0.1.187'
}

REDIS = {
    'host': 'localhost',
    'port': 6379
}

MONGO = {
    'connect': 'mongodb://10.0.1.187:27017/zeptoDB',
    'client': 'mongodb://10.0.1.187:27017/'
}

WATCH_PATHS = {
    'main': '/home/ubuntu/watch/',
    'temp': '/home/ubuntu/tempwatch/'
}

ENABLE = {
    'sense': True,
    'clean': True,
    'load': True,
    'process': True,
    'csv_process': True,
    'xls_process': True,
    'xlsx_process': True
}

DATABASE_STATES = {
    'upload_success': 'UPLOAD_SUCCESS',
    'process_start': 'PROCESS_START',
    'process_fail': 'PROCESS_FAIL',
    'process_success': 'PROCESS_SUCCESS',
    'load_start': 'LOAD_START',
    'load_fail': 'LOAD_FAIL',
    'load_success': 'LOAD_SUCCESS'
}

USER_CORRECTION_STATUS = {
    'none': None,
    'success': 'SUCCESS',
    'pending': 'PENDING'        
}

CELERY_APP = {
    'name': 'celery-upload',
    'broker': 'amqp://zepto:zepto123@localhost/',
    'backend': 'redis://localhost:6379/0'
}

CELERY_RETRY = {
    'delay': 60,
    'number_of_times': 1
}

QUEUE = {
    'main': 'nfs',
    'temp': 'tempnfs',
    'q1': 'q1',
    'q2': 'q2',
    'q3': 'q3',
    'q4': 'q4'
}

SOCKET = {
    'upload_response': ZEPTO_SOCKET_SERVER+'/push_status',
    'upload_errMerge': ZEPTO_SOCKET_SERVER+'/push_errMerge',
    'upload_mergeResponse': ZEPTO_SOCKET_SERVER+'/push_mergeStatus',
    'upload_correction': ZEPTO_SOCKET_SERVER+'/push_errorCorrection'
}

INSIGHT = {
    'invoke_insights': CONSTANT_DATA_SENSE_SERVER_URL+'/auth/api/generate/insight'
}

MONTH_DICT = {
        '1':"January",
        '2':"February",
        '3':"March",
        '4':"April",
        '5':"May",
        '6':"June",
        '7':"July",
        '8':"August",
        '9':"September",
        '10':"October",
        '11':"November",
        '12':"December"
}

#chiran
data_types = {
    'categorical_data': 'categoricalData',
    'measure_data': 'measureData',
    'date': 'date',
    'numeric_data': 'numeric',
    'integer':'INT',
    'float':'FLOAT',
    'unidentifieddatatype':"data_type_error",
    


}
fields = {
    'file_id': 'fileId',
    'field_id': 'fieldId',
    'key_value': 'keyValue',
    'data_type': 'dataType',
    'meta_data': 'metaData',
    'type_of_data': 'typeOfData',
    'files': 'files',
    'org_file_id':'orgFileId',
    'org_field': 'files.orgFileId',
    '$set':'$set',
    'uniq_id': 'uniqId',
    'name': 'name',
    'row_data': 'rowData',
    'value': 'value',
    'data_sense': 'dataSense',
    'domain_name':'domainName',
    'synapse0':'synapse0',
    'synapse1':'synapse1',
    'words':'words',
    'classes':'classes',
    'filename':"synapses.json",
    'unidentifiedkeyword':'xxx',
    'unidentifieddomain':'None',
    
    }