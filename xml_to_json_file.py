# -*- coding: utf-8 -*-
"""
This file transform the xml file into a json file(same name with '.json' 
in the end). And the program also store a list named 'data' containing 
all dictionaries corresponding to the jsons.
"""
import xml.etree.cElementTree as ET
import json
from process_util import *



XML_FILE = '../beijing_china.osm'
NODE_NAME_FILE = 'node_names'
WAY_NAME_FILE = 'way_names'
ABREVIATED_FILE = 'abreviated'
node_name_mapping = read_mapping(NODE_NAME_FILE)
way_name_mapping = read_mapping(WAY_NAME_FILE)
abreviated_mapping = read_mapping(ABREVIATED_FILE)

def xml_to_jason(file_in, pretty = False):
    '''
    This function takes a file as input and output a file with ".json" 
    attached to the name of input file. The output file contains all the 
    data as json format. The return of this function is a list containing 
    all the json objects as dictionaries.
    
    '''    
    file_out = "{0}.json".format(file_in)
    data = build_data_list(file_in)
    with codecs.open(file_out, "w") as fo:
        for el in data:
            if pretty:
                fo.write(json.dumps(el, indent=2)+"\n")
            else:
                fo.write(json.dumps(el) + "\n")
    return data


def build_data_list(filename):
    '''
    This function produce a list converted from the xml file.
    '''
    data = []    
    for _, element in ET.iterparse(filename):
        el = shape_element(element)
        if el:
            data.append(el)
    return data

def shape_element(element):
    '''
    This function shape single element in the xml file into a dictionary.
    '''
    if is_node(element):
        return shape_node(element)
    elif is_way(element):
        return shape_way(element)
    elif is_relation(element):
        return shape_relation(element)
    else:
        return None

def is_node(element):
    '''
    Test if it is a 'node' element
    '''
    return element.tag == 'node'

def is_way(element):
    '''
    Test if it is a 'way' element
    '''
    return element.tag == 'way'

def is_relation(element):
    '''
    Test if it is a 'relation' element
    '''    
    return element.tag == 'relation'

def shape_node(element):
    '''
    This is the workhorse function dealing with 'node' element in xml.
    Return of the function will be a dictionary.
    '''
    result = dict()
    result['type'] = 'node'
    result['changeset'] = element.attrib['changeset']
    result['id'] = element.attrib['id']
    result['pos'] = [float(element.attrib['lat']),float(element.attrib['lon'])]
    result['timestamp'] = element.attrib['timestamp']
    result['uid'] = element.attrib['uid']
    result['user'] = element.attrib['user']
    result['version'] = element.attrib['version']
    all_tags =  element.findall('tag')
    if all_tags!=[] and all_tags != None:
        result['tag'] = process_way_tags(all_tags)
    return result

def process_node_tags(all_tags):
    '''
    This function dealing with all the 'tag' within 'node' element in xml.
    Return of the function will be a dictionary.
    '''
    result = dict()
    for tag in all_tags:
        if tag.attrib['k'] == 'name':
            result['name'] = mapping_name(tag.attrib['v'], node_name_mapping)
        else:
            key = node_key_filters(tag.attrib['k'])
            value = node_value_filters(tag.attrib['v'])
            if is_match_reg(lower_reg, key):
                result[key] = value
            elif is_match_reg(colon_reg, key):
                key_splits = key.split(':')
                sub_key = key_splits[0] + '_other'
                if sub_key not in result:
                    result[sub_key] = dict()
                    result[sub_key][key_splits[1]] = value
                else:
                    result[sub_key][key_splits[1]] = value
            else:
                continue
    return result



def node_key_filters(string):
    '''
    This function filters the attribute 'k' in the 'tag' element within 
    'node' element.  
    '''
    result = string
    result = lower_filter(result)
    result = replace_hyphen_filter(result)
    result = mapping_name(result, abreviated_mapping)
    result = replace_second_colon_filter(result)
    return result

def node_value_filters(string):
    '''
    This function filters the attribute 'v' in the 'tag' element within 
    'node' element.  
    '''    
    result = string
    return result


def shape_way(element):
    '''
    This is the workhorse function dealing with 'way' element in xml.
    Return of the function will be a dictionary.
    '''    
    result = dict()
    result['type'] = 'way'
    result['changeset'] = element.attrib['changeset']
    result['id'] = element.attrib['id']
    result['timestamp'] = element.attrib['timestamp']
    result['uid'] = element.attrib['uid']
    result['user'] = element.attrib['user']
    result['version'] = element.attrib['version']
    all_nds = element.findall('nd')
    if all_nds!= [] and all_nds != None:
        result['nodes'] = process_way_nds(all_nds)
    all_tags =  element.findall('tag')
    if all_tags!=[] and all_tags != None:
        result['tag'] = process_way_tags(all_tags)
    return result

def process_way_nds(all_nds):
    '''
    This function dealing with all the 'nd' within 'way' element in xml.
    Return of the function will be a list.
    '''    
    result = []
    for node in all_nds:
        result.append(node.attrib['ref'])
    return result

def process_way_tags(all_tags):
    '''
    This function dealing with all the 'tag' within 'way' element in xml.
    Return of the function will be a dictionary.
    '''    
    result = dict()
    for tag in all_tags:
        if tag.attrib['k'] == 'name':
            result['name'] = mapping_name(tag.attrib['v'], way_name_mapping)
        else:
            key = way_key_filters(tag.attrib['k'])
            value = way_value_filters(tag.attrib['v'])
            if is_match_reg(lower_reg, key):
                result[key] = value
            elif is_match_reg(colon_reg, key):
                key_splits = key.split(':')
                sub_key = key_splits[0] + '_other'
                if sub_key not in result:
                    result[sub_key] = dict()
                    result[sub_key][key_splits[1]] = value
                else:
                    result[sub_key][key_splits[1]] = value
            else:
                continue
    return result

def way_key_filters(string):
    '''
    This function filters the attribute 'k' in the 'tag' element within 
    'way' element.  
    '''    
    result = string
    result = lower_filter(result)
    result = replace_hyphen_filter(result)
    result = mapping_name(result, abreviated_mapping)
    result = replace_second_colon_filter(result)
    return result

def way_value_filters(string):
    '''
    This function filters the attribute 'v' in the 'tag' element within 
    'way' element.  
    '''        
    result = string
    return result


def shape_relation(element):
    '''
    This is the workhorse function dealing with 'relation' element in xml.
    Return of the function will be a dictionary.
    '''       
    result = dict()
    result['type'] = 'way'
    result['changeset'] = element.attrib['changeset']
    result['id'] = element.attrib['id']
    result['timestamp'] = element.attrib['timestamp']
    result['uid'] = element.attrib['uid']
    result['user'] = element.attrib['user']
    result['version'] = element.attrib['version']
    all_members = element.findall('member')
    if all_members!= [] and all_members != None:
        result['members'] = process_relation_members(all_members)
    all_tags =  element.findall('tag')
    if all_tags!=[] and all_tags != None:
        result['tag'] = process_relation_tags(all_tags)
    return result

def process_relation_members(all_members):
    '''
    This function dealing with all the 'member' within 'relation' element in xml.
    Return of the function will be a list.
    '''        
    result = []
    for member in all_members:
        result.append({'ref':member.attrib['ref'], \
                       'role':member.attrib['role'], 'type': member.attrib['type']})
    return result

def process_relation_tags(all_tags):
    '''
    This function dealing with all the 'tag' within 'relation' element in xml.
    Return of the function will be a dictionary.
    '''        
    result = dict()
    for tag in all_tags:
        key = relation_key_filters(tag.attrib['k'])
        value = relation_value_filters(tag.attrib['v'])
        if is_match_reg(lower_reg, key):
            result[key] = value
        elif is_match_reg(colon_reg, key):
            key_splits = key.split(':')
            sub_key = key_splits[0] + '_other'
            if sub_key not in result:
                result[sub_key] = dict()
                result[sub_key][key_splits[1]] = value
            else:
                result[sub_key][key_splits[1]] = value
        else:
            continue
    return result

def relation_key_filters(string):
    '''
    This function filters the attribute 'k' in the 'tag' element within 
    'relation' element.  
    '''    
    result = string
    result = lower_filter(result)
    result = replace_hyphen_filter(result)
    result = mapping_name(result, abreviated_mapping)
    result = replace_second_colon_filter(result)
    return result

def relation_value_filters(string):
    '''
    This function filters the attribute 'v' in the 'tag' element within 
    'relation' element.  
    '''      
    result = string
    return result

if __name__ == '__main__':
    data = xml_to_jason(XML_FILE, pretty = False)    