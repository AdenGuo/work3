# -*- coding: utf-8 -*-
"""
This file contains many functions to audit the data.
"""

import xml.etree.cElementTree as ET
import re
import codecs


filename = '../beijing_china.osm'
colon_reg = re.compile(r'^([a-z]|_|[0-9])*:([a-z]|_|[0-9])*$')
two_colons_reg = re.compile(r'^([a-z]|_|[0-9])*:([a-z]|_|[0-9])*:([a-z]|_|[0-9])*$')

def get_root(filename):
    '''
    Get the root of a xml file. 
    '''
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def get_node_tags_key(element):
    '''
    This function return a dictionary including all the 'k' attributes in 'tag's 
    element within node element.
    '''
    result = dict()
    for node in element.iter('node'):
        for tag in node.iter('tag'):
            key =  tag.attrib['k']
            if key not in result:
                result[key] = 1
            else:
                result[key] =  result[key] + 1
    return result
    
def is_unicode(string):
    '''
    Test if a string is a unicode string.
    '''
    return type(string) == unicode

def find_unicode_list(string_list):
    '''
    This function return a list of unicode strings in a list.
    '''
    return [string for string in string_list if is_unicode(string)]

def find_hyphen_list(string_list):
    '''
    This function return a list of strings containing hyphen("-") in a list.
    '''    
    result = []
    for string in string_list:
        if re.search('-',string):
            result.append(string)
    return result

def find_uppercase_list(string_list):
    '''
    This function return a list of strings containing uppercase letters in a list.
    '''    
    result = []
    for string in string_list:
        if re.search(r'[A-Z]+',string):
            result.append(string)
    return result

def find_single_colon(string_list):
    '''
    This function return a list of strings containing a single colon in a list.
    '''    
    result = []
    for string in string_list:
        if re.search(colon_reg,string):
            result.append(string)
    return result

def find_double_colon(string_list):
    '''
    This function return a list of strings containing double colons in a list.
    '''    
    result = []
    for string in string_list:
        if re.search(two_colons_reg,string):
            result.append(string)
    return result

def get_node_tags_key_value(element):
    '''
    This function return a list of tuples containing 'name' and value 
    in a list.
    '''        
    result = []
    for node in element.iter('node'):
        for tag in node.iter('tag'):
            if (tag.attrib['k'], tag.attrib['v']) not in result \
               and tag.attrib['k'] == 'name':              
                result.append((tag.attrib['k'], tag.attrib['v']))
    return result

if __name__ == '__main__':
    filename = '../beijing_china.osm'
    root = get_root(filename)
    print '\n'
    print '***********************************************************'   
    print 'Problem 1: inconsistency in keys' 
    node_tag_key_count = get_node_tags_key(root)
    sort_key = sorted(node_tag_key_count, key=node_tag_key_count.get)
    unicode_keys = find_unicode_list(sort_key)
    print 'Unicode keys in the "tag" element are:'
    print unicode_keys
    print '-----------------------------------------------------------' 
    hyphen_keys = find_hyphen_list(sort_key)
    print 'Strings containing hyphen are:'
    print hyphen_keys
    print '-----------------------------------------------------------'   
    upper_keys = find_uppercase_list(sort_key)
    print 'Strings containing uppercase letters or abbreviated words are:'
    print upper_keys
    print '***********************************************************'
    print '\n'
    print '\n'
    print '***********************************************************'   
    print 'Problem 2: colon(s) in keys' 
    colon_keys = find_single_colon(sort_key)
    print 'Strings containing single colon:'
    print colon_keys
    print '-----------------------------------------------------------' 
    double_colon_keys = find_double_colon(sort_key)
    print 'Strings containing duoble colons:'
    print double_colon_keys
    print '***********************************************************'    
    print '\n'
    print '\n'    
    print '***********************************************************'
    print 'Problem 3: pinyin as names' 
    colon_keys = find_single_colon(sort_key)
    print 'First 100 tag element containing names:'
    node_keys = get_node_tags_key_value(root)
    print node_keys[:20]
    print '***********************************************************'
    print '\n'        