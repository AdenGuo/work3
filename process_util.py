# -*- coding: utf-8 -*-
'''
This file containing utilities to assist in processing the xml file.
'''

import codecs
import re
import urllib
'''
Following is the regular expression match differenct kinds of strings.
'''

two_colons_reg = re.compile(r'^([a-z]|_|[0-9])*:([a-z]|_|[0-9])*:([a-z]|_|[0-9])*$')
lower_reg = re.compile(r'^([a-z]|_|[0-9])*$')
colon_reg = re.compile(r'^([a-z]|_|[0-9])*:([a-z]|_|[0-9])*$')

def download_file(url, file_out):
    '''
    This function download a file contained in a url to a local file
    '''
    urllib.urlretrieve (url, file_out)    

def read_mapping(filename):
    '''
    This function read a mapping file and output a corresponding dictionary.
    The input file contains a key value pair in each line. The key value pair 
    is separated by ':'. See file 'node_names' for example.
    '''
    f = codecs.open(filename, encoding='utf-8', mode='r')       
    result = dict()    
    for line in f:
        key = line.split(':')[0]
        value = line.split(':')[1].strip()
        result[key] = value
    f.close()
    return result

def lower_filter(string):
    '''
    This function transform a string into its lower case form.
    '''
    return string.lower()

def replace_hyphen_filter(string):
    '''
    This function replace hyphen(-) in a string with a underscore(_).
    '''
    if re.search('-',string):
        return re.sub('-', '_', string)
    else:
        return string

def replace_second_colon_filter(string):
    '''
    This function replace the second colon(:) with underscore(_) in a string.
    '''
    if re.search(two_colons_reg, string):
        string_list = list(string)
        string_list[[m.start() for m in re.finditer(r":",string)][1]] = '_'
        return ''.join(string_list)
    else:
        return string

def is_match_reg(regex, string):
    '''
    This function test if a string containing a given regular expression.
    '''
    if re.search(regex, string):
        return True
    else:
        return False

def mapping_name(string, name_mapping):
    '''
    This function transform a string to a new string. This tranform is defined 
    in a dictionary in which keys are original string and corresponding value 
    is the new string. If the string is not included in the dictionary. 
    Original string is returned. 
    '''
    if string in name_mapping:
        return name_mapping[string]
    else:
        return string