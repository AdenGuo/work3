# -*- coding: utf-8 -*-
"""
This file contains many functions to audit the data.
"""

import xml.etree.cElementTree as ET
import re
import codecs


filename = '../beijing_china.osm'

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
    This function return a unicode string in a list.
    '''
    return [string for string in string_list if is_unicode(string)]

filename = '../beijing_china.osm'
root = get_root(filename)

print 'Problem 1: unicode keys(chinese character as keys' 
node_tag_key_count = get_node_tags_key(root)
sort_key = sorted(node_tag_key_count, key=node_tag_key_count.get)
unicode_keys = find_unicode_list(sort_key)
print '