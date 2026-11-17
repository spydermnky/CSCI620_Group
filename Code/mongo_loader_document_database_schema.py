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
DB_NAME = 'gdelt_data_2'
COLLECTION_NAME_DATA = 'data'

SHOULD_RESET_TABLES = True

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
data = db[COLLECTION_NAME_DATA]
                
def load_data(results, collection):
    batch = []
    
    for row in results.iterrows():
        event_id = row[1]['GLOBALEVENTID']
        date_added = row[1]['DATEADDED']
        source_url = row[1]['SOURCEURL']
        
        event_code = row[1]['EventCode']
        is_root_event = row[1]['IsRootEvent']
        event_base_code = row[1]['EventBaseCode']
        event_root_code = row[1]['EventRootCode']
        quadclass = row[1]['QuadClass']
        goldstein_scale = row[1]['GoldsteinScale']
        num_mentions = row[1]['NumMentions']
        num_articles = row[1]['NumArticles']
        avg_tone = row[1]['AvgTone']
        
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
        
        actor1_code = row[1]['Actor1Code']
        actor1_geo_type = row[1]['Actor1Geo_Type']
        actor1_geo_fullname = row[1]['Actor1Geo_FullName']
        actor1_geo_country_code = row[1]['Actor1Geo_CountryCode']
        actor1_geo_adm_code = row[1]['Actor1Geo_ADM1Code']
        actor1_geo_lat = row[1]['Actor1Geo_Lat']
        actor1_geo_long = row[1]['Actor1Geo_Long']
        actor1_geo_feature_id = row[1]['Actor1Geo_FeatureID']
        
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
            
        actor2_geo_type = row[1]['Actor2Geo_Type']
        actor2_geo_fullname = row[1]['Actor2Geo_FullName']
        actor2_geo_country_code = row[1]['Actor2Geo_CountryCode']
        actor2_geo_adm_code = row[1]['Actor2Geo_ADM1Code']
        actor2_geo_lat = row[1]['Actor2Geo_Lat']
        actor2_geo_long = row[1]['Actor2Geo_Long']
        actor2_geo_feature_id = row[1]['Actor2Geo_FeatureID']
        
        action_geo_type = row[1]['ActionGeo_Type']
        action_geo_fullname = row[1]['ActionGeo_FullName']
        action_geo_country_code = row[1]['ActionGeo_CountryCode']
        action_geo_adm_code = row[1]['ActionGeo_ADM1Code']
        action_geo_lat = row[1]['ActionGeo_Lat']
        action_geo_long = row[1]['ActionGeo_Long']
        action_geo_feature_id = row[1]['ActionGeo_FeatureID']
        
        doc = {
            'GlobalEventId': event_id,
            'DateAdded': date_added,
            'SourceURL': source_url,
            
            'EventCode': event_code,
            'IsRootEvent': is_root_event,
            'EventBaseCode': event_base_code,
            'EventRootCode': event_root_code,
            'Quadclass': quadclass,
            'GoldsteinScale': goldstein_scale,
            'NumMentions': num_mentions,
            'NumArticles': num_articles,
            'AvgTone': avg_tone,
            
            'Actor1':
                {
                    'Actor1Code': actor1_code,
                    'Actor1Name': actor1_name,
                    'Actor1CountryCode': actor1_country_code,
                    'Actor1KnownGroupCode': actor1_known_group_code,
                    'Actor1EthnicCode': actor1_ethnic_code,
                    'Actor1ReligionCodes': actor1_religion_code,
                    'Actor1TypeCodes': actor1_type_code,
                    'Actor1Geo_Type': actor1_geo_type,
                    'Actor1Geo_Fullname': actor1_geo_fullname,
                    'Actor1Geo_CountryCode': actor1_geo_country_code,
                    'Actor1Geo_ADMCode': actor1_geo_adm_code,
                    'Actor1Geo_Lat': actor1_geo_lat,
                    'Actor1Geo_Long': actor1_geo_long,
                    'Actor1Geo_FeatureId': actor1_geo_feature_id
                },
            
            'Actor2':
                {
                    'Actor2Code': actor2_code,
                    'Actor2Name': actor2_name,
                    'Actor2CountryCode': actor2_country_code,
                    'Actor2KnownGroupCode': actor2_known_group_code,
                    'Actor2EthnicCode': actor2_ethnic_code,
                    'Actor2ReligionCodes': actor2_religion_code,
                    'Actor2TypeCodes': actor2_type_code,
                    'Actor2Geo_Type': actor2_geo_type,
                    'Actor2Geo_Fullname': actor2_geo_fullname,
                    'Actor2Geo_CountryCode': actor2_geo_country_code,
                    'Actor2Geo_ADMCode': actor2_geo_adm_code,
                    'Actor2Geo_Lat': actor2_geo_lat,
                    'Actor2Geo_Long': actor2_geo_long,
                    'Actor2Geo_FeatureId': actor2_geo_feature_id
                },
            
            'ActionGeo':
                {
                    'ActionGeo_Type': action_geo_type,
                    'ActionGeo_Fullname': action_geo_fullname,
                    'ActionGeo_CountryCode': action_geo_country_code,
                    'ActionGeo_ADMCode': action_geo_adm_code,
                    'ActionGeo_Lat': action_geo_lat,
                    'ActionGeo_Long': action_geo_long,
                    'ActionGeo_FeatureId': action_geo_feature_id
                },
            
            
            }
        
        doc = {key: val for key, val in doc.items() if np.all(pd.notna(val))}
        
        if doc != {}: batch.append(doc)
            
    if batch:
        collection.insert_many(batch)


if __name__ == '__main__':
    
    gd1 = gdelt.gdelt(version = 1)
    if SHOULD_RESET_TABLES:
        data.drop()
    
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
                
                load_data(results, data)
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
                
                load_data(results, data)