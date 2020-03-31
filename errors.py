#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:35:36 2018

@author: ashkar
"""


PROCESS_ERRORS = {
    'empty_header': 'Error! Empty Header(s)',
    'duplicate_header': 'Error! Duplicate Header(s)',
    'empty_and_duplicate_header': 'Error! Duplicate and Empty Header(s)',
    'multiple_visible_sheets': 'Error! More than one visible sheet',
    'column_limit_exceeded': 'Error! More than 100 columns found',
    'mismatching_data&header_index': 'Error! Element under non-existent header',
    'only headers': 'Error! No data',
    'empty_file': 'Error! Empty file'
}

MAIL_MSG = {
    'too_large': 'File too large',
    '20sec_timeout': 'Process Failed after 20 seconds of waiting',
    'load_fail': 'Load Failed'
}