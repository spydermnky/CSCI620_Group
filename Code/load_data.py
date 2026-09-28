import csv
import xml.etree.ElementTree as ET
import mysql.connector
from datetime import datetime
import pytz
import re
import gdelt

# INFORMATION ABOUT GDELT LIBRARY: https://pypi.org/project/gdelt/

#-----------------------SAMPLE QUERY-----------------------

# Since we only need version 1 data (daily updates, not updates every 15 mins),
# we set the query version to version 1.
print(f"Setting query version")
gd1 = gdelt.gdelt(version=1)

# Pull data from a single day and output it as a Pandas dataframe.
print(f"Query 1")
results= gd1.Search('2017 Nov 01',table='events', output='pandas') # loads from gkg table
print(f"Query 1 Results")

# Print length of results and first five data points
print(len(results))
print(results[:5])

#-----------------------PRINT OUT HEADERS-----------------------

'''
HEADERS RETURNED:
['GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate',
'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode', 'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code', 'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code',
'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code', 'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code',
'IsRootEvent', 'EventCode', 'CAMEOCodeDescription', 'EventBaseCode', 'EventRootCode', 'QuadClass', 'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone',
'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor1Geo_FeatureID',
'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code', 'Actor2Geo_Lat', 'Actor2Geo_Long', 'Actor2Geo_FeatureID',
'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID',
'DATEADDED', 'SOURCEURL']
'''

# Print out all headers in dataframe
print(list(results.columns.values))

#-----------------------QUERY FOR DESIRED TIME RANGE-----------------------

# NOT YET TESTED
#full_query= gd1.Search(['2019 Mar 11','2022 Mar 11'],table='events', output='pandas')

# Print length of results and first five data points
# print(len(full_query))
# print(full_query[:5])

print(f"DONE")
