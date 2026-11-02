import xml.etree.ElementTree as ET
from pymongo import MongoClient
import os
import re
from datetime import datetime
import gdelt
import time
from dateutil.parser import ParserError
import numpy as np
import pandas as pd

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'gdelt_data'
COLLECTION_NAME_PARTICIPATORS = 'participation'
COLLECTION_NAME_DATA = 'data'
COLLECTION_NAME_ACTOR_GEO = 'actor_geography'
COLLECTION_NAME_EVENTS = 'events'
COLLECTION_NAME_ACTORS = 'actors'

SHOULD_RESET_TABLES = True

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
participation = db[COLLECTION_NAME_PARTICIPATORS]
data = db[COLLECTION_NAME_DATA]
actor_geography = db[COLLECTION_NAME_ACTOR_GEO]
events = db[COLLECTION_NAME_EVENTS]
actors = db[COLLECTION_NAME_ACTORS]
                
def load_data_management(results, collection):
    batch = []
    
    for row in results.iterrows():
        event_id = row[1]['GLOBALEVENTID']
        date_added = row[1]['DATEADDED']
        source_url = row[1]['SOURCEURL']
        
        doc = {
            'GlobalEventId': event_id,
            'DateAdded': date_added,
            'SourceURL': source_url
            }
        
        doc = {key: val for key, val in doc.items() if np.all(pd.notna(val))}
        
        if doc != {}: batch.append(doc)
            
    if batch:
        collection.insert_many(batch)

def load_events(results, collection):
    batch = []
    
    for row in results.iterrows():
        event_code = row[1]['EventCode']
        is_root_event = row[1]['IsRootEvent']
        event_base_code = row[1]['EventBaseCode']
        event_root_code = row[1]['EventRootCode']
        quadclass = row[1]['QuadClass']
        goldstein_scale = row[1]['GoldsteinScale']
        num_mentions = row[1]['NumMentions']
        num_articles = row[1]['NumArticles']
        avg_tone = row[1]['AvgTone']
        
        doc = {
            'EventCode': event_code,
            'IsRootEvent': is_root_event,
            'EventBaseCode': event_base_code,
            'EventRootCode': event_root_code,
            'Quadclass': quadclass,
            'GoldsteinScale': goldstein_scale,
            'NumMentions': num_mentions,
            'NumArticles': num_articles,
            'AvgTone': avg_tone
            }
        
        doc = {key: val for key, val in doc.items() if np.all(pd.notna(val))}
        
        if doc != {}: batch.append(doc)
    
    if batch:
        collection.insert_many(batch)

def load_actors(results, collection):
    batch = []
    
    for row in results.iterrows():
        actor1_code = row[1]['Actor1Code']
        actor1_name = row[1]['Actor1Name']
        actor1_country_code = row[1]['Actor1CountryCode']
        actor1_known_group_code = row[1]['Actor1KnownGroupCode']
        actor1_ethnic_code = row[1]['Actor1EthnicCode']
        actor1_religion_code = []
        if not pd.notna(row[1]['Actor1Religion1Code']):
            actor1_religion_code.append(row[1]['Actor1Religion1Code'])
        if not pd.notna(row[1]['Actor1Religion2Code']):
            actor1_religion_code.append(row[1]['Actor1Religion2Code'])
        actor1_type_code = []
        if not pd.notna(row[1]['Actor1Type1Code']):
            actor1_type_code.append(row[1]['Actor1Type1Code'])
        if not pd.notna(row[1]['Actor1Type2Code']):
            actor1_type_code.append(row[1]['Actor1Type2Code'])
        if not pd.notna(row[1]['Actor1Type3Code']):
            actor1_type_code.append(row[1]['Actor1Type3Code'])
            
        doc1 = {
            'ActorCode': actor1_code,
            'ActorName': actor1_name,
            'ActorCountryCode': actor1_country_code,
            'ActorKnownGroupCode': actor1_known_group_code,
            'ActorEthnicCode': actor1_ethnic_code,
            'ActorReligionCodes': actor1_religion_code,
            'ActorTypeCodes': actor1_type_code
            }
        
        doc1 = {key: val for key, val in doc1.items() if np.all(pd.notna(val))}
        
        if doc1 != {}: batch.append(doc1)
        
        actor2_code = row[1]['Actor2Code']
        actor2_name = row[1]['Actor2Name']
        actor2_country_code = row[1]['Actor2CountryCode']
        actor2_known_group_code = row[1]['Actor2KnownGroupCode']
        actor2_ethnic_code = row[1]['Actor2EthnicCode']
        actor2_religion_code = []
        if not pd.notna(row[1]['Actor2Religion1Code']):
            actor2_religion_code.append(row[1]['Actor2Religion1Code'])
        if not pd.notna(row[1]['Actor2Religion2Code']):
            actor2_religion_code.append(row[1]['Actor2Religion2Code'])
        actor2_type_code = []
        if not pd.notna(row[1]['Actor2Type1Code']):
            actor2_type_code.append(row[1]['Actor2Type1Code'])
        if not pd.notna(row[1]['Actor2Type2Code']):
            actor2_type_code.append(row[1]['Actor2Type2Code'])
        if not pd.notna(row[1]['Actor2Type3Code']):
            actor2_type_code.append(row[1]['Actor2Type3Code'])
            
        doc2 = {
            'ActorCode': actor2_code,
            'ActorName': actor2_name,
            'ActorCountryCode': actor2_country_code,
            'ActorKnownGroupCode': actor2_known_group_code,
            'ActorEthnicCode': actor2_ethnic_code,
            'ActorReligionCodes': actor2_religion_code,
            'ActorTypeCodes': actor2_type_code
            }
        
        doc2 = {key: val for key, val in doc2.items() if np.all(pd.notna(val))}
        
        if doc2 != {}: batch.append(doc2)
    
    if batch:
        collection.insert_many(batch)

def load_actor_geo(results, collection):
    batch = []
    
    for row in results.iterrows():
        actor1_code = row[1]['Actor1Code']
        actor1_geo_type = row[1]['Actor1Geo_Type']
        actor1_geo_fullname = row[1]['Actor1Geo_FullName']
        actor1_geo_country_code = row[1]['Actor1Geo_CountryCode']
        actor1_geo_adm_code = row[1]['Actor1Geo_ADM1Code']
        actor1_geo_lat = row[1]['Actor1Geo_Lat']
        actor1_geo_long = row[1]['Actor1Geo_Long']
        actor1_geo_feature_id = row[1]['Actor1Geo_FeatureID']
        
        doc1 = {
            'GeoActorCode': actor1_code,
            'ActorGeo_Type': actor1_geo_type,
            'ActorGeo_Fullname': actor1_geo_fullname,
            'ActorGeo_CountryCode': actor1_geo_country_code,
            'ActorGeo_ADMCode': actor1_geo_adm_code,
            'ActorGeo_Lat': actor1_geo_lat,
            'ActorGeo_Long': actor1_geo_long,
            'ActorGeo_FeatureId': actor1_geo_feature_id
            }
        
        doc1 = {key: val for key, val in doc1.items() if np.all(pd.notna(val))}
    
        if doc1 != {}: batch.append(doc1)
        
        actor2_code = row[1]['Actor2Code']
        actor2_geo_type = row[1]['Actor2Geo_Type']
        actor2_geo_fullname = row[1]['Actor2Geo_FullName']
        actor2_geo_country_code = row[1]['Actor2Geo_CountryCode']
        actor2_geo_adm_code = row[1]['Actor2Geo_ADM1Code']
        actor2_geo_lat = row[1]['Actor2Geo_Lat']
        actor2_geo_long = row[1]['Actor2Geo_Long']
        actor2_geo_feature_id = row[1]['Actor2Geo_FeatureID']
        
        doc2 = {
            'GeoActorCode': actor2_code,
            'ActorGeo_Type': actor2_geo_type,
            'ActorGeo_Fullname': actor2_geo_fullname,
            'ActorGeo_CountryCode': actor2_geo_country_code,
            'ActorGeo_ADMCode': actor2_geo_adm_code,
            'ActorGeo_Lat': actor2_geo_lat,
            'ActorGeo_Long': actor2_geo_long,
            'ActorGeo_FeatureId': actor2_geo_feature_id
            }
        
        doc2 = {key: val for key, val in doc2.items() if np.all(pd.notna(val))}
    
        if doc2 != {}: batch.append(doc2)
    
    if batch:
        collection.insert_many(batch)

def load_participators(results, collection):
    batch = []
    
    for row in results.iterrows():
        global_event_id = row[1]['GLOBALEVENTID']
        actor1 = row[1]['Actor1Code']
        actor2 = row[1]['Actor2Code']
        event_code = row[1]['EventCode']
        
        doc = {
            'GlobalEventId': global_event_id,
            'Actor1': actor1,
            'Actor2': actor2,
            'EventCode': event_code
            }
        
        doc = {key: val for key, val in doc.items() if np.all(pd.notna(val))}
        
        if doc != {}: batch.append(doc)
    
    if batch:
        collection.insert_many(batch)


if __name__ == '__main__':
    
    gd1 = gdelt.gdelt(version = 1)
    if SHOULD_RESET_TABLES:
        for collection in [participation, data, actor_geography, events, actors]:
            collection.drop()
    
    original_time = time.time()
    year = '2019'
    for month in ['Nov', 'Dec']:
        for day in range(32):
            if day:
                t1 = time.time()
                print(f'Current Date: {year} {month} {day}')
                print(f'Total Time Elapsed: {t1-original_time:.3f}')
            if day:
                day = str(day)
                try:
                    results = gd1.Search(f'{year} {month} {day}', table = 'events', output = 'pandas')
                except ParserError:
                    pass
                
                load_data_management(results, data)
                load_events(results, events)
                load_actors(results, actors)
                load_actor_geo(results, actor_geography)
                load_participators(results, participation)
    year = '2020'
    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']:
        for day in range(32):
            if day == 1:
                t1 = time.time()
                print(f'Current Date: {year} {month} {day}')
                print(f'Total Time Elapsed: {t1-original_time:.3f}')
            if day:
                day = str(day)
                try:
                    results = gd1.Search(f'{year} {month} {day}', table = 'events', output = 'pandas')
                except ParserError:
                    pass
                
                load_data_management(results, data)
                load_events(results, events)
                load_actors(results, actors)
                load_actor_geo(results, actor_geography)
                load_participators(results, participation)