import csv
import xml.etree.ElementTree as ET
import mysql.connector
from datetime import datetime
import pytz
import re
import gdelt
import time

# INFORMATION ABOUT GDELT LIBRARY: https://pypi.org/project/gdelt/
def main():
    #-----------------------SAMPLE QUERY-----------------------
    
    # Since we only need version 1 data (daily updates, not updates every 15 mins),
    # we set the query version to version 1.
    print('Setting query version')
    gd1 = gdelt.gdelt(version=1)
    
    # Pull data from a single day and output it as a Pandas dataframe.
    date_ranges = [['2019 Nov 02', '2019 Dec 01'],
                   ['2019 Dec 02', '2020 Jan 01'],
                   ['2020 Jan 02', '2020 Feb 01'],
                   ['2020 Feb 02', '2020 Mar 01'],
                   ['2020 Mar 02', '2020 Apr 01'],
                   ['2020 Apr 02', '2020 May 01'],
                   ['2020 May 02', '2020 Jun 01'],
                   ['2020 Jun 02', '2020 Jul 01'],
                   ['2020 Jul 02', '2020 Aug 01'],
                   ['2020 Aug 02', '2020 Sep 01'],
                   ['2020 Sep 02', '2020 Oct 01'],
                   ['2020 Oct 02', '2020 Nov 01'],
                   ['2020 Nov 02', '2020 Dec 01']]
    total_num_entries = 0
    original_time = time.time()
    for i, date_range in enumerate(date_ranges):
        print(f'Query {i+1}')
        t1 = time.time()
        results = gd1.Search(date_range, table='events', output='pandas') # loads from gkg table
        t2 = time.time()
        print(f'\nQuery {i+1} Results:')
        print(f'Query Length: {t2-t1:.3f}')
        current_time = time.time()
        print(f'Total Time Elapsed: {current_time - original_time:.2f}')
        
        # Print length of results for this query and add it to total length
        print(f'Number of events for the date range {date_range}: {len(results)}\n')
        total_num_entries += len(results)
    
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
    
    #-----------------------QUERY FOR DESIRED TIME RANGE-----------------------
    #['2019 Mar 11','2022 Mar 11']
    
    print(f'Total number of events: {total_num_entries}')
    print('DONE')

if __name__ == '__main__':
    main()