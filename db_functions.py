# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:13:41 2015

@author: adenguo
"""
import json
import codecs

JSON_FILE = '../beijing_china.osm.json'
DB_NAME = 'examples'

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
    pipeline = [{'$match':{'country':'India', 'lon':{'$gte':75}, 'lon':{'$lte': 80}}},
                {'$unwind':'$isPartOf'},
                {'$group':{'_id':'$isPartOf',
                           'count':{'$sum':1}}},
                {'$sort':{'count':-1}},
                {'$limit':1}
                ]
    return pipeline

def aggregate(db, pipeline):
    result = db.cities.aggregate(pipeline)
    return result




def insert_maps(infile, db_name):
    db = get_db(db_name)
    data = process_file(infile)
    db.beijing_maps.insert_many(data)

def process_file(filename):
    result = []
    with codecs.open(filename, "r") as fo:
        for line in fo:
            result.append(json.loads(line.strip()))
    return result

