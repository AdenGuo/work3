# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 21:30:07 2015

@author: adenguo
"""


import xml.etree.cElementTree as ET


filename = '../beijing_china.osm'

def get_root(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def count_child(element):
    result = dict()
    for sub_element in element:
        if sub_element.tag not in result:
            result[sub_element.tag] = 1
        else:
            result[sub_element.tag] = result[sub_element.tag] + 1
    return result

def count_child_element(element):
    return [sub_element for sub_element in element]


'''
root = get_root(filename)
type_counts = count_child(root)
'''