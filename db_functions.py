# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:13:41 2015

@author: adenguo
"""
import json
import codecs
import re
import datetime

JSON_FILE = '../beijing_china.osm.json'
DB_NAME = 'examples'
TIME_FREQUENCY_PNG = 'figures/updating_frequency.png'
USER_UPDATING_PNG = 'figures/user_updating_frequency.png'
LOW_FREQUENCY_PNG = 'figures/low_frequency.png'
HIGH_FREQUENCY_PNG = 'figures/high_frequency.png'

time_reg = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')


def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


def get_collections(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db.beijing_maps    

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{'$group':{'_id':'$timestamp',
                           'count':{'$sum':1}}},
                {'$sort':{'count':-1}},
                {'$limit':1}
                ]
    return pipeline

def aggregate(collection, pipeline):
    result = collection.aggregate(pipeline)
    return result

def insert_maps(infile, db_name):
    data = process_file(infile)
    all_collection = get_collections(db_name)
    all_collection.remove({})
    all_collection.insert_many(data)

def process_file(filename):
    result = []
    with codecs.open(filename, "r") as fo:
        for line in fo:
            result.append(json.loads(line.strip()))
    return result

def convert_stringdate_datetime(datetime_string_list):
    return [datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ') for \
              date_string in datetime_string_list]

def get_unique_time_sorted(collection):
    time_string_list = collection.distinct('timestamp')
    result = convert_stringdate_datetime(time_string_list)
    result.sort()
    return result

def get_all_timestamp_string_list(collection):    
    return [string['timestamp'] for string in \
            list(collection.find({}, {'timestamp': 1, '_id':0}))]

def plot_datetime_hist_png(datetime_list,png_filename, labels):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    data = convert_stringdate_datetime(datetime_list)    
    mpl_data = mdates.date2num(data)
    fig, ax = plt.subplots(1,1)
    ax.hist(mpl_data, bins=20, color='lightblue')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y.%m'))
    ax.set_xlabel(labels[0],size = 'x-large')
    ax.set_ylabel(labels[1],size = 'x-large')
    fig.savefig(png_filename, dpi=1000)      


def plot_timestamp_png(collection,png_filename):
    date_string_list = get_all_timestamp_string_list(collection)
    plot_datetime_hist_png(date_string_list, png_filename, ['Date', 'Frequency of Total Updating Counts'])




'''
if __name__ == '__main__':
    all_collections = get_collections(DB_NAME)
    unique_times = get_unique_time_sorted(all_collections)
    plot_timestamp_png(all_collections,TIME_FREQUENCY_PNG)
    pipeline = [{'$group':{'_id':'$user',
                       'count':{'$sum':1}}},
                {'$match':{'count':{'$lt':200}}} 
               ]
    count_list = [item['count'] for item in \
                  list(aggregate(all_collections, pipeline))]
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1,1)
    ax.hist(count_list, bins=50, color='red')
    ax.set_xlabel('Updating Count',size = 'x-large')
    ax.set_ylabel('Frequency',size = 'x-large')
    fig.savefig(USER_UPDATING_PNG, dpi=1000)
    
    pipeline = [{'$group':{'_id':'$user',
                           'count':{'$sum':1},
                           'timestamp':{'$push':'$timestamp'}}},
                {'$match':{'count':{'$lt':100}}},
                { '$unwind' : "$timestamp" }
               ]
    low_frequency_timestamp = [item['timestamp'] for item in \
              list(aggregate(all_collections, pipeline))]
    plot_datetime_hist_png(low_frequency_timestamp,LOW_FREQUENCY_PNG, \
                           ['Date', 'Frequency of Lower Updating Counts'])
    
    pipeline = [{'$group':{'_id':'$user',
                       'count':{'$sum':1},
                       'timestamp':{'$push':'$timestamp'}}},
            {'$match':{'count':{'$gt':100}}},
            { '$unwind' : "$timestamp" }
           ]
    high_frequency_timestamp = [item['timestamp'] for item in \
              list(aggregate(all_collections, pipeline))]
    plot_datetime_hist_png(high_frequency_timestamp,HIGH_FREQUENCY_PNG, \
                           ['Date', 'Frequency of Higher Updating Counts'])
    
    pipeline = [{'$match':{'type':'way'}},
                {'$unwind' : '$nodes'},
                {'$group' : {'_id':'$nodes'}}           
           ]
    print len(list(aggregate(all_collections, pipeline)))
    print all_collections.find({'type':'node'}).count()
    
    from process_util import *
    result = read_word_list(NODE_NAME_FILE)
    print len(result)
    print count_map(pinyin_reg, result)
    
    result = read_word_list(WAY_NAME_FILE)
    print len(result)
    print count_map(pinyin_reg, result)    
'''