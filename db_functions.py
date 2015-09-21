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

def get_unique_time_sorted(collection):
    time_string_list = collection.distinct('timestamp')
    result = [datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ') for \
              date_string in time_string_list]
    result.sort()
    return result

def get_all_timestamp(collection):
    return [datetime.datetime.strptime(string['timestamp'], \
                   '%Y-%m-%dT%H:%M:%SZ') for string in \
                   list(collection.find({}, {'timestamp': 1, '_id':0}))]

def plot_timestamp_png(collection,png_filename):
    data = get_all_timestamp(collection)
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    mpl_data = mdates.date2num(data)
    fig, ax = plt.subplots(1,1)
    ax.hist(mpl_data, bins=20, color='lightblue')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y.%m'))
    fig.savefig(png_filename, dpi=1000)    

if __name__ == '__main__':
    all_collections = get_collections(DB_NAME)
    unique_times = get_unique_time_sorted(all_collections)
    plot_timestamp_png(all_collections,TIME_FREQUENCY_PNG)
