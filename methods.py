# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 04:38:25 2018

@author: chiran sachintha
"""
import re
def regDataType(str):
    str = str.strip()
    if len(str) == 0:
        return 'BLANK'

#    if re.match(r'True$|^False$|^0$|^1$', str):
#        return 'BIT'
#    if re.match(r'([-+]\s*)?\d+[lL]?$', str):
#        return 'INT'
#    if re.match(r'([-+]\s*)?[1-9][0-9]*\.?[0-9]*([Ee][+-]?[0-9]+)?$', str):
#        return 'FLOAT'
#    if re.match(r'([-+]\s*)?[0-9]*\.?[0-9][0-9]*([Ee][+-]?[0-9]+)?$', str):
#        return 'FLOAT'
#    if re.match(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$', str):
#        return 'PHONE_NO'
#    if re.match(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$', str):
#        return 'PHONE_NO'
#    if re.match(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})', str):
#        return 'DATE'
#    if re.match(r'[\d]{1,2}/[\d]{1,2}/[\d]{4}', str):
#        return 'DATE'
    if re.match(r'^\d{1,2}([:.]?\d{1,2})?([ ]?[a|p]m)?$', str):
        return 'TIME'
    if re.match(r'(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})$', str):
        return 'month-year'
#    if re.match(r'[\w\.-]+@[\w\.-]+$', str):
#        return 'E-mail'
#    if re.match(r'\b((mon|tues|wed(nes)?|thur(s)?|fri|sat(ur)?|sun)(day)?)\b$', str):
#        return 'Days_of_week'
#    if re.match(r'^\d{1,3}(?:[,]\d{3})*$', str):
#        return 'number'
#    if re.match(r'((?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?))$', str):
#        return 'DATE'

    return 'Categerical data'