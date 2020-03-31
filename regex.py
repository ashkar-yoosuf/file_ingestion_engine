#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 09:29:34 2018

@author: ashkar
"""

REGEX_COMMON = {
        'start': r'^',
        'end': r'$',
        'start_paran': r'^(',
        'end_paran': r')$',
        'open_paran': r'(',
        'close_paran': r')',
        'or': r'|',
        'not_critical': r'?',
        'space': r' '
}

REGEX_NUMBER_COMPONENTS = {'currency_symbols': r'(\$|rs|usd|lkr)',
                           'percentage_symbol': r'%',
                           'negative': r'-',
                           'pre_decimal': r'(\d+,?)*\d*',
                           'pre_decimal_essential': r'(\d+,?)*\d+',
                           'digits_normal': r'(\d+)',\
                           'post_decimal': r'(\.(\d+|(\d+[eE][+\-]?\d+)))',
                           'num_paran_open': r'\(',
                           'num_paran_close': r'\)',
                           'zero_division': r'(#div/0!)'
}

CURRENCY_REGEX = REGEX_NUMBER_COMPONENTS['negative'] + REGEX_COMMON['not_critical'] + REGEX_COMMON['open_paran'] +\
                 REGEX_NUMBER_COMPONENTS['currency_symbols'] + REGEX_COMMON['not_critical'] + REGEX_NUMBER_COMPONENTS['pre_decimal'] + REGEX_NUMBER_COMPONENTS['post_decimal'] + REGEX_COMMON['or'] +\
                 REGEX_NUMBER_COMPONENTS['currency_symbols'] + REGEX_COMMON['not_critical'] + REGEX_NUMBER_COMPONENTS['pre_decimal_essential'] + REGEX_NUMBER_COMPONENTS['post_decimal'] + REGEX_COMMON['not_critical'] + REGEX_COMMON['or'] +\
                 REGEX_NUMBER_COMPONENTS['pre_decimal'] + REGEX_NUMBER_COMPONENTS['post_decimal'] + REGEX_NUMBER_COMPONENTS['currency_symbols'] + REGEX_COMMON['not_critical'] + REGEX_COMMON['or'] +\
                 REGEX_NUMBER_COMPONENTS['pre_decimal_essential'] + REGEX_NUMBER_COMPONENTS['post_decimal'] + REGEX_COMMON['not_critical'] + REGEX_NUMBER_COMPONENTS['currency_symbols'] + REGEX_COMMON['not_critical'] +\
                 REGEX_COMMON['close_paran']

PERCENTAGE_REGEX = REGEX_NUMBER_COMPONENTS['negative'] + REGEX_COMMON['not_critical'] + REGEX_NUMBER_COMPONENTS['digits_normal'] + REGEX_NUMBER_COMPONENTS['post_decimal'] + REGEX_COMMON['not_critical'] + REGEX_NUMBER_COMPONENTS['percentage_symbol']
                
NUMBER_REGEX = REGEX_COMMON['start_paran'] +\
               2 * REGEX_COMMON['open_paran'] + REGEX_NUMBER_COMPONENTS['num_paran_open'] +\
               CURRENCY_REGEX +\
               REGEX_NUMBER_COMPONENTS['num_paran_close'] + REGEX_COMMON['close_paran'] + REGEX_COMMON['or'] +\
               REGEX_COMMON['open_paran'] +\
               CURRENCY_REGEX +\
               2 * REGEX_COMMON['close_paran'] + REGEX_COMMON['or'] +\
               REGEX_COMMON['open_paran'] + REGEX_NUMBER_COMPONENTS['num_paran_open'] +\
               PERCENTAGE_REGEX +\
               REGEX_NUMBER_COMPONENTS['num_paran_close'] + REGEX_COMMON['close_paran'] + REGEX_COMMON['or'] +\
               REGEX_COMMON['open_paran'] +\
               PERCENTAGE_REGEX +\
               REGEX_COMMON['close_paran'] + REGEX_COMMON['or'] +\
               REGEX_NUMBER_COMPONENTS['zero_division'] +\
               REGEX_COMMON['end_paran']

REGEX_DATE_COMPONENTS = {
        'Y': r'(\d{2}|\d{4})',
        'MD': r'((((0?(1|3|5|7|8)|10|12)|jan|mar|may|jul|aug|oct|dec)(/|-| )([1-9]|[0-2][1-9]|3[0-1]|[1-2]0))|(((0?(4|6|9)|11)|apr|jun|sep|nov)(/|-| )([1-9]|[0-2][1-9]|30|[1-2]0))|(((0?2)|feb)(/|-| )([1-9]|[0-2][1-9]|[1-2]0)))',
        'DM': r'((([1-9]|[0-2][1-9]|3[0-1]|[1-2]0)(/|-| )((0?(1|3|5|7|8)|10|12)|jan|mar|may|jul|aug|oct|dec))|(([1-9]|[0-2][1-9]|30|[1-2]0)(/|-| )((0?(4|6|9)|11)|apr|jun|sep|nov))|(([1-9]|[0-2][1-9]|[1-2]0)(/|-| )((0?2)|feb)))',
        'separator': r'(/|-| )',
        'time_suffix': r'( (([0-9]|0[0-9]|1[0-2]):([0-5][0-9]) ?(am|pm)?)| (([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?))',
        'time': r'((([0-9]|0[1-9]|1[0-2]):([0-5][0-9]) (am|pm)?)|(([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]))',
        'time1': r'((0[1-9]|1[0-2]):([0-5][0-9]) (am|pm))',
        'time2': r'(([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])',
        'time3': r'([0-9]:[0-5][0-9]:[0-5][0-9])',
        'time4': r'(([0-1][0-9]|2[0-3]):[0-5][0-9])',
        'time5': r'([0-9]:[0-5][0-9])',
        'duration_or_time': r'(([0-9]|([0-1][0-9]|2[0-3])):[0-5][0-9])',
        'duration': r'(\d{1,3}:[0-5][0-9])',
        'duration1': r'(\d:[0-5][0-9])',
        'duration2': r'(\d{2}:[0-5][0-9])',
        'duration3': r'(\d{3}:[0-5][0-9])'
}

DATE_REGEX = REGEX_COMMON['start_paran'] + 3 * REGEX_COMMON['open_paran'] +\
             REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_COMMON['close_paran'] +\
             REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
             REGEX_DATE_COMPONENTS['DM'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['close_paran'] +\
             REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
             REGEX_DATE_COMPONENTS['MD'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['close_paran'] +\
             REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
             REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['DM'] +\
             2 * REGEX_COMMON['close_paran'] +  REGEX_DATE_COMPONENTS['time_suffix'] + REGEX_COMMON['not_critical'] + REGEX_COMMON['close_paran'] +\
             REGEX_COMMON['or'] + REGEX_DATE_COMPONENTS['duration'] +\
             REGEX_COMMON['or'] + REGEX_DATE_COMPONENTS['time'] + REGEX_COMMON['end_paran']
             
DATEONLY_REGEX = REGEX_COMMON['start_paran'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_COMMON['close_paran'] +\
                 REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['DM'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['close_paran'] +\
                 REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['MD'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['close_paran'] +\
                 REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['DM'] +\
                 REGEX_COMMON['close_paran'] + REGEX_COMMON['end_paran']
                 
DATEONLY_YDM_REGEX = REGEX_COMMON['start_paran'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['DM'] + REGEX_COMMON['end_paran']
DATEONLY_YMD_REGEX = REGEX_COMMON['start_paran'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_COMMON['end_paran']
DATEONLY_DMY_REGEX = REGEX_COMMON['start_paran'] + REGEX_DATE_COMPONENTS['DM'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['end_paran']
DATEONLY_MDY_REGEX = REGEX_COMMON['start_paran'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['end_paran']         
             
DATETIME_REGEX = REGEX_COMMON['start_paran'] + 2 * REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_COMMON['close_paran'] +\
                 REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['DM'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['close_paran'] +\
                 REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['MD'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['close_paran'] +\
                 REGEX_COMMON['or'] + REGEX_COMMON['open_paran'] +\
                 REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['DM'] +\
                 2 * REGEX_COMMON['close_paran'] +  REGEX_DATE_COMPONENTS['time_suffix'] +\
                 REGEX_COMMON['end_paran']

DATETIME_YDM_PREFIX_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['DM'] + REGEX_COMMON['space']
DATETIME_YMD_PREFIX_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_COMMON['space']
DATETIME_DMY_PREFIX_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['DM'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['space']
DATETIME_MDY_PREFIX_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['MD'] + REGEX_DATE_COMPONENTS['separator'] + REGEX_DATE_COMPONENTS['Y'] + REGEX_COMMON['space']

DATETIME_TIME1_SUFFIX_REGEX = REGEX_COMMON['space'] + REGEX_DATE_COMPONENTS['time1'] + REGEX_COMMON['end']
DATETIME_TIME2_SUFFIX_REGEX = REGEX_COMMON['space'] + REGEX_DATE_COMPONENTS['time2'] + REGEX_COMMON['end']
DATETIME_TIME3_SUFFIX_REGEX = REGEX_COMMON['space'] + REGEX_DATE_COMPONENTS['time3'] + REGEX_COMMON['end']
DATETIME_TIME4_SUFFIX_REGEX = REGEX_COMMON['space'] + REGEX_DATE_COMPONENTS['time4'] + REGEX_COMMON['end']
DATETIME_TIME5_SUFFIX_REGEX = REGEX_COMMON['space'] + REGEX_DATE_COMPONENTS['time5'] + REGEX_COMMON['end']

DATETIME_YDM1_REGEX = DATETIME_YDM_PREFIX_REGEX[:-1:] + DATETIME_TIME1_SUFFIX_REGEX
DATETIME_YDM2_REGEX = DATETIME_YDM_PREFIX_REGEX[:-1:] + DATETIME_TIME2_SUFFIX_REGEX
DATETIME_YDM3_REGEX = DATETIME_YDM_PREFIX_REGEX[:-1:] + DATETIME_TIME3_SUFFIX_REGEX
DATETIME_YDM4_REGEX = DATETIME_YDM_PREFIX_REGEX[:-1:] + DATETIME_TIME4_SUFFIX_REGEX
DATETIME_YDM5_REGEX = DATETIME_YDM_PREFIX_REGEX[:-1:] + DATETIME_TIME5_SUFFIX_REGEX
DATETIME_YMD1_REGEX = DATETIME_YMD_PREFIX_REGEX[:-1:] + DATETIME_TIME1_SUFFIX_REGEX
DATETIME_YMD2_REGEX = DATETIME_YMD_PREFIX_REGEX[:-1:] + DATETIME_TIME2_SUFFIX_REGEX
DATETIME_YMD3_REGEX = DATETIME_YMD_PREFIX_REGEX[:-1:] + DATETIME_TIME3_SUFFIX_REGEX
DATETIME_YMD4_REGEX = DATETIME_YMD_PREFIX_REGEX[:-1:] + DATETIME_TIME4_SUFFIX_REGEX
DATETIME_YMD5_REGEX = DATETIME_YMD_PREFIX_REGEX[:-1:] + DATETIME_TIME5_SUFFIX_REGEX
DATETIME_DMY1_REGEX = DATETIME_DMY_PREFIX_REGEX[:-1:] + DATETIME_TIME1_SUFFIX_REGEX
DATETIME_DMY2_REGEX = DATETIME_DMY_PREFIX_REGEX[:-1:] + DATETIME_TIME2_SUFFIX_REGEX
DATETIME_DMY3_REGEX = DATETIME_DMY_PREFIX_REGEX[:-1:] + DATETIME_TIME3_SUFFIX_REGEX
DATETIME_DMY4_REGEX = DATETIME_DMY_PREFIX_REGEX[:-1:] + DATETIME_TIME4_SUFFIX_REGEX
DATETIME_DMY5_REGEX = DATETIME_DMY_PREFIX_REGEX[:-1:] + DATETIME_TIME5_SUFFIX_REGEX
DATETIME_MDY1_REGEX = DATETIME_MDY_PREFIX_REGEX[:-1:] + DATETIME_TIME1_SUFFIX_REGEX
DATETIME_MDY2_REGEX = DATETIME_MDY_PREFIX_REGEX[:-1:] + DATETIME_TIME2_SUFFIX_REGEX
DATETIME_MDY3_REGEX = DATETIME_MDY_PREFIX_REGEX[:-1:] + DATETIME_TIME3_SUFFIX_REGEX
DATETIME_MDY4_REGEX = DATETIME_MDY_PREFIX_REGEX[:-1:] + DATETIME_TIME4_SUFFIX_REGEX
DATETIME_MDY5_REGEX = DATETIME_MDY_PREFIX_REGEX[:-1:] + DATETIME_TIME5_SUFFIX_REGEX

TIME_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['time'] + REGEX_COMMON['end']
TIME1_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['time1'] + REGEX_COMMON['end']
TIME2_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['time2'] + REGEX_COMMON['end']
TIME3_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['time3'] + REGEX_COMMON['end']
TIME4_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['time4'] + REGEX_COMMON['end']
TIME5_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['time5'] + REGEX_COMMON['end']

DURATION_OR_TIME_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['duration_or_time'] + REGEX_COMMON['end']

DURATION_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['duration'] + REGEX_COMMON['end']
DURATION1_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['duration1'] + REGEX_COMMON['end']
DURATION2_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['duration2'] + REGEX_COMMON['end']
DURATION3_REGEX = REGEX_COMMON['start'] + REGEX_DATE_COMPONENTS['duration3'] + REGEX_COMMON['end']