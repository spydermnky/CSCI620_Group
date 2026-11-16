# File to Load GDELT Dataset into MySQL
# Group Members: Gunnika Kapoor, Peter Khomchenko, Timothy Ockrin
# Code written by Gunnika Kapoor

import csv
import xml.etree.ElementTree as ET
import mysql.connector
from datetime import datetime
import pytz
import re
import gdelt
import time
import pandas as pd
import numpy as np


''' 
SET THE VALUES OF THE VARIABLES BELOW SO YOU CAN
CONNECT TO THE DATABASE

(DELETE THEM BEFORE PUSHING TO GITHUB)
'''

# username = ''
# password = ''
# host = ''
# port = 
# database = ''

#---------------------------------------------------------------------------------------------------------
#-------------------------------LOAD DATA FROM GDELT LIBRARY INTO PANDAS DF-------------------------------
#---------------------------------------------------------------------------------------------------------

'''
Function to Load in Data from GDELT

Input
--------------
    - date_ranges: Nested list of date ranges from which to pull data

Output
--------------
    - GDELT_df: Dataframe of GDELT results
'''
def GDELT_Loader(date_ranges):
    # Since we only need version 1 data (daily updates, not updates every 15 mins),
    # we set the query version to version 1.
    gd1 = gdelt.gdelt(version=1)

    # Initialize variables for query fetching
    total_num_entries = 0
    original_time = time.time()
    GDELT_df = None

    # Iterate over all date ranges
    for i, date_range in enumerate(date_ranges):
        print(f'Query {i+1} for range {date_range}')
        t1 = time.time()

        # Add retry logic for timeouts
        '''
        The retry logic, specifically the attempt try clause logic, was written by Gemini.
        This helps ensure that if a portion of the query fails, the entire query does not.
        '''
        success = False
        attempts = 3 # Allow three attempts to fetch a given subquery
        results = None

        # Attempt to search for the event
        for attempt in range(attempts):
            try:
                # Load data from gkg table
                results = gd1.Search(date_range, table='events', output='pandas')
                success = True
                break
            except Exception as e: # Data loading failed, so retry
                print(f"Attempt {attempt+1} failed due to: {e}. Retrying...")
                time.sleep(2) # Wait 2 seconds before retrying

        # No success loading, so skip that date range
        if not success:
            print(f"Skipping range {date_range} after {attempts} failed attempts.")
            continue

        # Print length of results for this query and add it to total length
        t2 = time.time()
        print(f'Query Length: {t2-t1:.3f}s | Number of events: {len(results)}\n')
        total_num_entries += len(results)

        # Combine the intermediate results into the master df
        if GDELT_df is None:
            GDELT_df = results
        else:
            GDELT_df = pd.concat([GDELT_df, results], ignore_index=True)

    print(f'Total number of events: {total_num_entries}')
    return GDELT_df


'''
Main function to call the GDELT_Loader function and load in the GDELT data into a df.
'''
def main():
    # Create an array of data ranges of form [[start_date, end_date]] to load from the GDELT library.
    # This allows the data request to be broken into subrequests, improving the efficiency
    # with which the data can be collected.

    # Full date ranges list
    date_ranges = [
                    ['2019 Nov 01', '2019 Nov 05'],
                    ['2019 Nov 06', '2019 Nov 10'],
                    ['2019 Nov 11', '2019 Nov 15'],
                    ['2019 Nov 16', '2019 Nov 20'],
                    ['2019 Nov 21', '2019 Nov 25'],
                    ['2019 Nov 26', '2019 Nov 30'],

                    ['2019 Dec 01', '2019 Dec 05'],
                    ['2019 Dec 06', '2019 Dec 10'],
                    ['2019 Dec 11', '2019 Dec 15'],
                    ['2019 Dec 16', '2019 Dec 20'],
                    ['2019 Dec 21', '2019 Dec 25'],
                    ['2019 Dec 26', '2019 Dec 31'],

                    ['2020 Jan 01', '2020 Jan 05'],
                    ['2020 Jan 06', '2020 Jan 10'],
                    ['2020 Jan 11', '2020 Jan 15'],
                    ['2020 Jan 16', '2020 Jan 20'],
                    ['2020 Jan 21', '2020 Jan 25'],
                    ['2020 Jan 26', '2020 Jan 31'],

                    ['2020 Feb 01', '2020 Feb 05'],
                    ['2020 Feb 06', '2020 Feb 10'],
                    ['2020 Feb 11', '2020 Feb 15'],
                    ['2020 Feb 16', '2020 Feb 20'],
                    ['2020 Feb 21', '2020 Feb 25'],
                    ['2020 Feb 26', '2020 Feb 28'],

                    ['2020 Mar 01', '2020 Mar 05'],
                    ['2020 Mar 06', '2020 Mar 10'],
                    ['2020 Mar 11', '2020 Mar 15'],
                    ['2020 Mar 16', '2020 Mar 20'],
                    ['2020 Mar 21', '2020 Mar 25'],
                    ['2020 Mar 26', '2020 Mar 31'],

                    ['2020 Apr 01', '2020 Apr 05'],
                    ['2020 Apr 06', '2020 Apr 10'],
                    ['2020 Apr 11', '2020 Apr 15'],
                    ['2020 Apr 16', '2020 Apr 20'],
                    ['2020 Apr 21', '2020 Apr 25'],
                    ['2020 Apr 26', '2020 Apr 30'],
                    
                    ['2020 May 01', '2020 May 05'],
                    ['2020 May 06', '2020 May 10'],
                    ['2020 May 11', '2020 May 15'],
                    ['2020 May 16', '2020 May 20'],
                    ['2020 May 21', '2020 May 25'],
                    ['2020 May 25', '2020 May 31'],

                    ['2020 Jun 01', '2020 Jun 05'],
                    ['2020 Jun 06', '2020 Jun 10'],
                    ['2020 Jun 11', '2020 Jun 15'],
                    ['2020 Jun 16', '2020 Jun 20'],
                    ['2020 Jun 21', '2020 Jun 25'],
                    ['2020 Jun 26', '2020 Jun 30'],

                    ['2020 Jul 01', '2020 Jul 05'],
                    ['2020 Jul 06', '2020 Jul 10'],
                    ['2020 Jul 11', '2020 Jul 15'],
                    ['2020 Jul 16', '2020 Jul 20'],
                    ['2020 Jul 21', '2020 Jul 25'],
                    ['2020 Jul 26', '2020 Jul 31'],

                    ['2020 Aug 01', '2020 Aug 05'],
                    ['2020 Aug 06', '2020 Aug 10'],
                    ['2020 Aug 11', '2020 Aug 15'],
                    ['2020 Aug 16', '2020 Aug 20'],
                    ['2020 Aug 21', '2020 Aug 25'],
                    ['2020 Aug 26', '2020 Aug 31'],

                    ['2020 Sep 01', '2020 Sep 05'],
                    ['2020 Sep 06', '2020 Sep 10'],
                    ['2020 Sep 11', '2020 Sep 15'],
                    ['2020 Sep 16', '2020 Sep 20'],
                    ['2020 Sep 21', '2020 Sep 25'],
                    ['2020 Sep 26', '2020 Sep 30'],

                    ['2020 Oct 01', '2020 Oct 05'],
                    ['2020 Oct 06', '2020 Oct 10'],
                    ['2020 Oct 11', '2020 Oct 15'],
                    ['2020 Oct 16', '2020 Oct 20'],
                    ['2020 Oct 21', '2020 Oct 25'],
                    ['2020 Oct 26', '2020 Oct 31'],

                    ['2020 Nov 01', '2020 Nov 05'],
                    ['2020 Nov 06', '2020 Nov 10'],
                    ['2020 Nov 11', '2020 Nov 15'],
                    ['2020 Nov 16', '2020 Nov 20'],
                    ['2020 Nov 21', '2020 Nov 25'],
                    ['2020 Nov 26', '2020 Nov 30'],
                ]

    # Call function to collect GDELT data and pass it the desired date ranges
    GDELT_df = GDELT_Loader(date_ranges)

    # Print out all headers in dataframe
    print(list(GDELT_df.columns.values))

    print(f"\n\n{GDELT_df[:1]}")

    return GDELT_df


'''
This if statement handles the logic of calling the function to collect the GDELT data and loading it into the database.
'''
if __name__ == '__main__':
    start = datetime.now(pytz.utc) # Time at the start of the entire operation
    print(f"\n\n----------------------------------------------------------\nTIME AT START: {start.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")
    
    GDELT_df = main()


    #---------------------------------------------------------------------------------------------------------
    #------------------------------------DATAFRAME CLEANING AND PROCESSING------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ''' 
    The columns of the Pandas DF are follows:
    1. 'GLOBALEVENTID', 2. 'SQLDATE', 3. 'MonthYear', 4. 'Year', 5. 'FractionDate'

    6. 'Actor1Code', 7. 'Actor1Name', 8. 'Actor1CountryCode', 9. 'Actor1KnownGroupCode', 10. 'Actor1EthnicCode', 11. 'Actor1Religion1Code', 12. 'Actor1Religion2Code'
    13. 'Actor1Type1Code', 14. 'Actor1Type2Code', 15. 'Actor1Type3Code'

    16. 'Actor2Code', 17. 'Actor2Name', 18. 'Actor2CountryCode', 19. 'Actor2KnownGroupCode', 20. 'Actor2EthnicCode', 21. 'Actor2Religion1Code', 22. 'Actor2Religion2Code'
    23. 'Actor2Type1Code', 24. 'Actor2Type2Code', 25. 'Actor2Type3Code'

    26. 'IsRootEvent', 27. 'EventCode', 28. 'CAMEOCodeDescription', 29. 'EventBaseCode', 30. 'EventRootCode', 31. 'QuadClass', 32. 'GoldsteinScale'
    33. 'NumMentions', 34. 'NumSources', 35. 'NumArticles', 36. 'AvgTone'

    37. 'Actor1Geo_Type', 38. 'Actor1Geo_FullName', 39. 'Actor1Geo_CountryCode', 40. 'Actor1Geo_ADM1Code', 41. 'Actor1Geo_Lat', 42. 'Actor1Geo_Long', 43. 'Actor1Geo_FeatureID'

    44. 'Actor2Geo_Type', 45. 'Actor2Geo_FullName', 46. 'Actor2Geo_CountryCode', 47. 'Actor2Geo_ADM1Code', 48. 'Actor2Geo_Lat', 49. 'Actor2Geo_Long', 50. 'Actor2Geo_FeatureID'

    51. 'ActionGeo_Type', 52. 'ActionGeo_FullName', 53. 'ActionGeo_CountryCode', 54. 'ActionGeo_ADM1Code', 55. 'ActionGeo_Lat', 56. 'ActionGeo_Long', 57. 'ActionGeo_FeatureID'

    58. 'DATEADDED', 59. 'SOURCEURL'

    '''

    # Drop the following columns since they are repetitive (same information as Date): MonthYear (integer), Year (integer), FractionDate
    GDELT_df.drop(columns=["MonthYear", "Year", "FractionDate"])

    # Remove all rows where Actor1Code and / or Actor2Code have NaNs

    print(f"\nHandling Actor Codes:")
    # Check how many rows have a NaN in Actor1Code
    print(f"Actor1 NaNs: {GDELT_df['Actor1Code'].isna().sum()}")

    # Check how many rows have a NaN in Actor2Code
    print(f"Actor2 NaNs: {GDELT_df['Actor2Code'].isna().sum()}")

    # Remove the rows that have NaNs for Actor1Code and/or Actor2Code
    results_actor1_good = GDELT_df[GDELT_df['Actor1Code'].notna()]
    GDELT_df = results_actor1_good[results_actor1_good['Actor2Code'].notna()]

    print(f"AFTER REMOVING ACTOR1 AND ACTOR2 WITH NANS: {len(GDELT_df)}")
    print(GDELT_df[:5][['Actor1Code', 'Actor2Code']])


    # Make sure no rows now have ActorName null

    print(f"\nHandling Actor Names:")
    # Check how many rows have a NaN in Actor1Name
    print(f"Actor1 NaNs: {GDELT_df['Actor1Name'].isna().sum()}")

    # Check how many rows have a NaN in Actor2Name
    print(f"Actor2 NaNs: {GDELT_df['Actor2Name'].isna().sum()}")

    # Remove the rows that have NaNs for Actor1Name and/or Actor2Name
    results_actor1_good = GDELT_df[GDELT_df['Actor1Name'].notna()]
    GDELT_df = results_actor1_good[results_actor1_good['Actor2Name'].notna()]

    print(f"AFTER REMOVING ACTOR1 AND ACTOR2 WITH NANS: {len(GDELT_df)}")
    print(GDELT_df[:5][['Actor1Name', 'Actor2Name']])

    #---------------------------------------------------------------------------------------------------------
    #-----------------------------------------------ACTOR TABLE-----------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############

    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    ############# CALCULATE THE LARGEST POSSIBLE VALUES FOR VARCHAR ATTRIBUTES IN THE TABLE #############

    # In order to determine what the maximum capacity of the varchars should be in the database,
    # we determine what the maximum length of those values is in the files we are loading in.

    # --------- ActorCode ---------
    print(f"\n-------------------------\nActorCode\n-------------------------\n")
    max_length_actor1 = GDELT_df["Actor1Code"].str.len().max()
    max_length_actor2 = GDELT_df["Actor2Code"].str.len().max()
    max_length_actor = max(max_length_actor1, max_length_actor2)
    print(f"\n\n\nmax length: ActorCode = {max_length_actor1} and actor_2 = {max_length_actor2} --> final max = {max_length_actor}")

    # --------- ActorName ---------
    print(f"\n-------------------------\nActorName\n-------------------------\n")
    max_length_actor1name = GDELT_df["Actor1Name"].str.len().max()
    max_length_actor2name = GDELT_df["Actor2Name"].str.len().max()
    max_length_actorname = max(max_length_actor1name, max_length_actor2name)
    print(f"\n\n\nmax length: ActorCode = {max_length_actor1name} and actor_2 = {max_length_actor2name} --> final max = {max_length_actorname}")

    # --------- ActorKnownGroupCode ---------
    print(f"\n-------------------------\nActorKnownGroupCode\n-------------------------\n")
    max_length_actor1groupcode = GDELT_df["Actor1KnownGroupCode"].str.len().max()
    max_length_actor2groupcode = GDELT_df["Actor2KnownGroupCode"].str.len().max()
    maxlength_actorgroupcode = max(max_length_actor1groupcode, max_length_actor2groupcode)
    print(f"\n\n\nmax length: ActorCode = {max_length_actor1groupcode} and actor_2 = {max_length_actor2groupcode} --> final max = {maxlength_actorgroupcode}")

    # --------- ActorEthnicCode ---------
    print(f"\n-------------------------\nActorEthnicCode\n-------------------------\n")
    max_length_actor1ethniccode = GDELT_df["Actor1EthnicCode"].str.len().max()
    max_length_actor2ethniccode = GDELT_df["Actor2EthnicCode"].str.len().max()
    maxlength_actorethniccode = max(max_length_actor1ethniccode, max_length_actor2ethniccode)
    print(f"\n\n\nmax length: ActorCode = {max_length_actor1ethniccode} and actor_2 = {max_length_actor2ethniccode} --> final max = {maxlength_actorethniccode}")


    # To determine how long it took to load the data into the Actor table, we display the time before and after value insertion.
    # The code to display the time was modified from this link: https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python
    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore Actor Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # Creating the cursor object
    c = conn.cursor(prepared=True)

    # We add each Actor1 and Actor2 to the Actor table separately. So, we create two views of the dataframe for each actor type

    # Collect Actor 1 Attributes and drop rows with duplicate Actor1Codes
    actor_1_attrs = GDELT_df[["Actor1Code", "Actor1Name", "Actor1CountryCode", "Actor1KnownGroupCode", "Actor1EthnicCode"]]
    actor_1_attrs = actor_1_attrs.drop_duplicates(subset=["Actor1Code"], keep="first") # Drop based on the Actor1Code column and keep the first instance

    # Collect Actor 2 Attributes and drop rows with duplicate Actor1Codes
    actor_2_attrs = GDELT_df[["Actor2Code", "Actor2Name", "Actor2CountryCode", "Actor2KnownGroupCode", "Actor2EthnicCode"]]
    actor_2_attrs = actor_2_attrs.drop_duplicates(subset=["Actor2Code"], keep="first") # Drop based on the Actor2Code column and keep the first instance

    # Ensure all columns of the df are the correct type before insertion
    actor_1_attrs = actor_1_attrs.astype({"Actor1Code": str, "Actor1Name": str, "Actor1CountryCode": str, "Actor1KnownGroupCode": str, "Actor1EthnicCode": str})
    actor_2_attrs = actor_2_attrs.astype({"Actor2Code": str, "Actor2Name": str, "Actor2CountryCode": str, "Actor2KnownGroupCode": str, "Actor2EthnicCode": str})

    # Rename the columns of each df to the names that will be used in the final SQL table
    actor_1_attrs = actor_1_attrs.rename(columns={"Actor1Code": "ActorCode", "Actor1Name": "ActorName", "Actor1CountryCode": "ActorCountryCode", 
                                                  "Actor1KnownGroupCode": "ActorKnownGroupCode", "Actor1EthnicCode": "ActorEthnicCode"})
    actor_2_attrs = actor_2_attrs.rename(columns={"Actor2Code": "ActorCode", "Actor2Name": "ActorName", "Actor2CountryCode": "ActorCountryCode", 
                                                      "Actor2KnownGroupCode": "ActorKnownGroupCode", "Actor2EthnicCode": "ActorEthnicCode"})

    # Recombine the actor 1 and actor 2 attreibutes into one df
    actor_attrs = pd.concat([actor_1_attrs, actor_2_attrs], ignore_index=True)

    # Convert the df into a list of tuples for insertion into mysql
    '''
    The code below was written by Gemini, as before this line of code, I was getting errors related to the input data
    being too long for the columns. This is due to the Nones being treated as float-based NaNs. This code corrected that error.
    '''
    actor_attrs = actor_attrs.astype(object).replace({np.nan: None})

    # Drop rows with duplicate ActorCodes, since that is the primary key
    actor_attrs["ActorCode"] = actor_attrs["ActorCode"].str.upper() # Convert all ActorCodes to uppercase so duplicates are properly deleted
    actor_attrs = actor_attrs.drop_duplicates(subset=["ActorCode"], keep="first")

    actors_to_insert = actor_attrs.to_numpy().tolist()

    ############# CREATE TABLE #############
    max_length_actorcode = max_length_actor + 10
    max_length_actorname = max_length_actorname + 10
    maxlength_actorgroupcode = maxlength_actorgroupcode + 10
    maxlength_actorethniccode = maxlength_actorethniccode + 10

    print(f"{actors_to_insert[0]}")

    c.execute("DROP TABLE IF EXISTS Actor;")

    create_actor_table_query = f"""
        CREATE TABLE IF NOT EXISTS Actor (
            ActorCode VARCHAR({max_length_actorcode}) PRIMARY KEY,
            ActorName VARCHAR({max_length_actorname}),
            ActorCountryCode VARCHAR(5),
            ActorKnownGroupCode VARCHAR({maxlength_actorgroupcode}),
            ActorEthnicCode VARCHAR({maxlength_actorethniccode})
        );
    """
    c.execute(create_actor_table_query)


    ############# INSERT TUPLES #############
    # Actor(ActorCode (PK), ActorName, ActorCountryCode, ActorKnownGroupCode, ActorEthnicCode) 
    query = """INSERT INTO Actor (ActorCode, ActorName, ActorCountryCode, ActorKnownGroupCode, ActorEthnicCode) VALUES(?, ?, ?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, actors_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter Actor Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    #---------------------------------------------------------------------------------------------------------
    #--------------------------------------------RELIGIONCODE TABLE-------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    ############# CONNECT TO DATABASE #############
        
    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    ############# CALCULATE THE LARGEST POSSIBLE VALUES FOR VARCHAR ATTRIBUTES IN THE TABLE #############

    # In order to determine what the maximum capacity of the varchars should be in the database,
    # we determine what the maximum length of those values is in the files we are loading in.

    # --------- ReligionCode ---------
    print(f"\n-------------------------\nReligionCode\n-------------------------\n")
    max_length_actor1religion1 = GDELT_df["Actor1Religion1Code"].str.len().max()
    max_length_actor1religion2 = GDELT_df["Actor1Religion2Code"].str.len().max()

    max_length_actor2religion1 = GDELT_df["Actor2Religion1Code"].str.len().max()
    max_length_actor2religion2 = GDELT_df["Actor2Religion2Code"].str.len().max()

    max_length_religion = max(max_length_actor1religion1, max_length_actor1religion2, max_length_actor2religion1, max_length_actor2religion2)
    print(f"\n\n\nmax length:{max_length_religion}")


    # To determine how long it took to load the data into the ReligionCode table, we display the time before and after value insertion.
    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore ReligionCode Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # --------- Create df for Type Codes ---------

    # We add each Actor1 and Actor2 to the Actor table separately. So, we create two views of the dataframe for each actor type

    # Collect Actor 1 Attributes and drop rows with duplicate Actor and Religion Codes. Rename columns to match with final df.
    actor_1_religion_1_attrs = GDELT_df[["Actor1Code", "Actor1Religion1Code"]]
    actor_1_religion_1_attrs = actor_1_religion_1_attrs.drop_duplicates(subset=["Actor1Code", "Actor1Religion1Code"], keep="first") # Drop any duplicate pairs of Actor and Religion
    actor_1_religion_1_attrs = actor_1_religion_1_attrs.rename(columns={"Actor1Code": "ActorCode", "Actor1Religion1Code": "ReligionCode"}) # Rename attributes

    actor_1_religion_2_attrs = GDELT_df[["Actor1Code", "Actor1Religion2Code"]]
    actor_1_religion_2_attrs = actor_1_religion_2_attrs.drop_duplicates(subset=["Actor1Code", "Actor1Religion2Code"], keep="first") # Drop any duplicate pairs of Actor and Religion
    actor_1_religion_2_attrs = actor_1_religion_2_attrs.rename(columns={"Actor1Code": "ActorCode", "Actor1Religion2Code": "ReligionCode"}) # Rename attributes

    # Collect Actor 1 Attributes and drop rows with duplicate Actor and Type Codes. Rename columns to match with final df.
    actor_2_religion_1_attrs = GDELT_df[["Actor2Code", "Actor2Religion1Code"]]
    actor_2_religion_1_attrs = actor_2_religion_1_attrs.drop_duplicates(subset=["Actor2Code", "Actor2Religion1Code"], keep="first") # Drop any duplicate pairs of Actor and Religion
    actor_2_religion_1_attrs = actor_2_religion_1_attrs.rename(columns={"Actor2Code": "ActorCode", "Actor2Religion1Code": "ReligionCode"}) # Rename attributes

    actor_2_religion_2_attrs = GDELT_df[["Actor2Code", "Actor2Religion2Code"]]
    actor_2_religion_2_attrs = actor_2_religion_2_attrs.drop_duplicates(subset=["Actor2Code", "Actor2Religion2Code"], keep="first") # Drop any duplicate pairs of Actor and Religion
    actor_2_religion_2_attrs = actor_2_religion_2_attrs.rename(columns={"Actor2Code": "ActorCode", "Actor2Religion2Code": "ReligionCode"}) # Rename attributes


    # Combine all actor 1 attributes together and drop any duplicates again
    actor_1_attrs = pd.concat([actor_1_religion_1_attrs, actor_1_religion_2_attrs], ignore_index=True)
    actor_1_attrs = actor_1_attrs.drop_duplicates(subset=["ActorCode", "ReligionCode"], keep="first")

    # Combine all actor 2 attributes together and drop any duplicates again
    actor_2_attrs = pd.concat([actor_2_religion_1_attrs, actor_2_religion_2_attrs], ignore_index=True)
    actor_2_attrs = actor_2_attrs.drop_duplicates(subset=["ActorCode", "ReligionCode"], keep="first")

    # Ensure all columns of the df are the correct type before insertion
    actor_1_attrs = actor_1_attrs.astype({"ActorCode": str, "ReligionCode": str})
    actor_2_attrs = actor_2_attrs.astype({"ActorCode": str, "ReligionCode": str})

    # Combine actor 1 and actor 2 atrributes into one table and drop any duplicates a final time
    religion_attrs = pd.concat([actor_1_attrs, actor_2_attrs], ignore_index=True)

    # --------- Combine Type Codes and Actors ---------

    # Drop nulls from the table
    results_religion_good = religion_attrs[religion_attrs['ReligionCode'].notna()]

    # Replace float style NaNs with None
    results_religion_good = results_religion_good.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate ActorCodes, since that is the primary key
    results_religion_good["ActorCode"] = results_religion_good["ActorCode"].str.upper() # Convert all ActorCodes to uppercase so duplicates are properly deleted
    results_religion_good = results_religion_good.drop_duplicates(subset=["ActorCode"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    religions_to_insert = results_religion_good.to_numpy().tolist()

    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS ReligionCode;")

    maxlength_actorcode = max_length_actor + 10
    maxlength_religion_code = max_length_religion + 10
    
    create_religion_table_query = f"""
        CREATE TABLE IF NOT EXISTS ReligionCode (
            ActorCode VARCHAR({maxlength_actorcode}) PRIMARY KEY,
            ReligionCode VARCHAR({maxlength_religion_code})
        );
    """

    c.execute(create_religion_table_query)

    ############# INSERT TUPLES #############
    # ReligionCode(ActorCode (PK, FK to ActorCode in Actor Table), ReligionCode)  
    query = """INSERT INTO ReligionCode (ActorCode, ReligionCode) VALUES(?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, religions_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter ReligionCode Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------TYPECODE TABLE----------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############
    
    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    ############# CALCULATE THE LARGEST POSSIBLE VALUES FOR VARCHAR ATTRIBUTES IN THE TABLE #############

    # In order to determine what the maximum capacity of the varchars should be in the database,
    # we determine what the maximum length of those values is in the files we are loading in.

    # --------- TypeCode ---------
    print(f"\n-------------------------\nTYPECODE\n-------------------------\n")
    #'Actor1Type1Code', 14. 'Actor1Type2Code', 15. 'Actor1Type3Code'
    max_length_actor1type1 = GDELT_df["Actor1Type1Code"].str.len().max()
    max_length_actor1type2 = GDELT_df["Actor1Type2Code"].str.len().max()
    max_length_actor1type3 = GDELT_df["Actor1Type3Code"].str.len().max()

    max_length_actor2type1 = GDELT_df["Actor2Type1Code"].str.len().max()
    max_length_actor2type2 = GDELT_df["Actor2Type2Code"].str.len().max()
    max_length_actor2type3 = GDELT_df["Actor2Type3Code"].str.len().max()

    max_length_type = max(max_length_actor1type1, max_length_actor1type2, max_length_actor1type3, max_length_actor2type1, max_length_actor2type2, max_length_actor2type3)
    print(f"\n\n\nmax length:{max_length_type}")


    # To determine how long it took to load the data into the TypeCode table, we display the time before and after value insertion.
    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore TypeCode Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # --------- Create df for Type Codes ---------

    # We add each Actor1 and Actor2 to the Actor table separately. So, we create two views of the dataframe for each actor type

    # Collect Actor 1 Attributes and drop rows with duplicate Actor and Type Codes. Rename columns to match with final df.
    actor_1_type_1_attrs = GDELT_df[["Actor1Code", "Actor1Type1Code"]]
    actor_1_type_1_attrs = actor_1_type_1_attrs.drop_duplicates(subset=["Actor1Code", "Actor1Type1Code"], keep="first") # Drop any duplicate pairs of Actor and Type
    actor_1_type_1_attrs = actor_1_type_1_attrs.rename(columns={"Actor1Code": "ActorCode", "Actor1Type1Code": "TypeCode"}) # Rename attributes

    actor_1_type_2_attrs = GDELT_df[["Actor1Code", "Actor1Type2Code"]]
    actor_1_type_2_attrs = actor_1_type_2_attrs.drop_duplicates(subset=["Actor1Code", "Actor1Type2Code"], keep="first") # Drop any duplicate pairs of Actor and Type
    actor_1_type_2_attrs = actor_1_type_2_attrs.rename(columns={"Actor1Code": "ActorCode", "Actor1Type2Code": "TypeCode"}) # Rename attributes

    actor_1_type_3_attrs = GDELT_df[["Actor1Code", "Actor1Type3Code"]]
    actor_1_type_3_attrs = actor_1_type_3_attrs.drop_duplicates(subset=["Actor1Code", "Actor1Type3Code"], keep="first") # Drop any duplicate pairs of Actor and Type
    actor_1_type_3_attrs = actor_1_type_3_attrs.rename(columns={"Actor1Code": "ActorCode", "Actor1Type3Code": "TypeCode"}) # Rename attributes

    # Collect Actor 1 Attributes and drop rows with duplicate Actor and Type Codes. Rename columns to match with final df.
    actor_2_type_1_attrs = GDELT_df[["Actor2Code", "Actor2Type1Code"]]
    actor_2_type_1_attrs = actor_2_type_1_attrs.drop_duplicates(subset=["Actor2Code", "Actor2Type1Code"], keep="first") # Drop any duplicate pairs of Actor and Type
    actor_2_type_1_attrs = actor_2_type_1_attrs.rename(columns={"Actor2Code": "ActorCode", "Actor2Type1Code": "TypeCode"}) # Rename attributes

    actor_2_type_2_attrs = GDELT_df[["Actor2Code", "Actor2Type2Code"]]
    actor_2_type_2_attrs = actor_2_type_2_attrs.drop_duplicates(subset=["Actor2Code", "Actor2Type2Code"], keep="first") # Drop any duplicate pairs of Actor and Type
    actor_2_type_2_attrs = actor_2_type_2_attrs.rename(columns={"Actor2Code": "ActorCode", "Actor2Type2Code": "TypeCode"}) # Rename attributes

    actor_2_type_3_attrs = GDELT_df[["Actor2Code", "Actor2Type3Code"]]
    actor_2_type_3_attrs = actor_2_type_3_attrs.drop_duplicates(subset=["Actor2Code", "Actor2Type3Code"], keep="first") # Drop any duplicate pairs of Actor and Type
    actor_2_type_3_attrs = actor_2_type_3_attrs.rename(columns={"Actor2Code": "ActorCode", "Actor2Type3Code": "TypeCode"}) # Rename attributes


    # Combine all actor 1 attributes together and drop any duplicates again
    actor_1_attrs = pd.concat([actor_1_type_1_attrs, actor_1_type_2_attrs, actor_1_type_3_attrs], ignore_index=True)
    actor_1_attrs = actor_1_attrs.drop_duplicates(subset=["ActorCode", "TypeCode"], keep="first")

    # Combine all actor 2 attributes together and drop any duplicates again
    actor_2_attrs = pd.concat([actor_2_type_1_attrs, actor_2_type_2_attrs, actor_2_type_3_attrs], ignore_index=True)
    actor_2_attrs = actor_2_attrs.drop_duplicates(subset=["ActorCode", "TypeCode"], keep="first")

    # Ensure all columns of the df are the correct type before insertion
    actor_1_attrs = actor_1_attrs.astype({"ActorCode": str, "TypeCode": str})
    actor_2_attrs = actor_2_attrs.astype({"ActorCode": str, "TypeCode": str})

    # Combine actor 1 and actor 2 atrributes into one table and drop any duplicates a final time
    type_attrs = pd.concat([actor_1_attrs, actor_2_attrs], ignore_index=True)
    type_attrs = type_attrs.drop_duplicates(subset=["ActorCode", "TypeCode"], keep="first")

    # --------- Combine Type Codes and Actors ---------

    # Drop nulls from the table
    results_type_good = type_attrs[type_attrs['TypeCode'].notna()]

    # Replace float style NaNs with None
    results_type_good = results_type_good.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate ActorCodes, since that is the primary key
    results_type_good["ActorCode"] = results_type_good["ActorCode"].str.upper() # Convert all ActorCodes to uppercase so duplicates are properly deleted
    results_type_good = results_type_good.drop_duplicates(subset=["ActorCode"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    types_to_insert = results_type_good.to_numpy().tolist()

    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS TypeCode;")

    # CREATE TABLE TypeCode (ActorCode varchar(30), TypeCode varchar(10), 
    # PRIMARY KEY (ActorCode));

    maxlength_actorcode = max_length_actor + 10
    maxlength_type_code = max_length_type + 10
    
    create_typecode_table_query = f"""
        CREATE TABLE IF NOT EXISTS TypeCode (
            ActorCode VARCHAR({maxlength_actorcode}) PRIMARY KEY,
            TypeCode VARCHAR({maxlength_type_code})
        );
    """

    c.execute(create_typecode_table_query)

    ############# INSERT TUPLES #############
    # SQL query to insert data into database
    # TypeCode(ActorCode (PK, FK to ActorCode in Actor Table), TypeCode) 
    query = """INSERT INTO TypeCode (ActorCode, TypeCode) VALUES(?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, types_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter TypeCode Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    #---------------------------------------------------------------------------------------------------------
    #-------------------------------------------EVENTACTION TABLE---------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############
    
    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    ############# CALCULATE THE LARGEST POSSIBLE VALUES FOR VARCHAR ATTRIBUTES IN THE TABLE #############

    # In order to determine what the maximum capacity of the varchars should be in the database,
    # we determine what the maximum length of those values is in the files we are loading in.

    # --------- EventAction ---------
    print(f"\n-------------------------\nEVENTCODE\n-------------------------\n")
    max_length_eventcode = GDELT_df["EventCode"].str.len().max()
    print(f"\n\n\nmax length EventCode:{max_length_eventcode}")

    print(f"\n-------------------------\nEVENTBASECODE\n-------------------------\n")
    max_length_eventbasecode = GDELT_df["EventBaseCode"].str.len().max()
    print(f"\n\n\nmax length EventBaseCode:{max_length_eventbasecode}")

    print(f"\n-------------------------\nEVENTROOTCODE\n-------------------------\n")
    max_length_eventrootcode = GDELT_df["EventRootCode"].str.len().max()
    print(f"\n\n\nmax length EventRootCodet:{max_length_eventrootcode}")

    print(f"\n-------------------------\nCAMEOCODEDESCRIPTION\n-------------------------\n")
    max_length_eventcameo = GDELT_df["CAMEOCodeDescription"].str.len().max()
    print(f"\n\n\nmax length CAMEOCodeDescription:{max_length_eventcameo}")


    # To determine how long it took to load the data into the EventAction table, we display the time before and after value insertion.
    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore EventAction Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # --------- Create df for Event Action ---------

    # Collect EventAction Attributes
    event_attrs = GDELT_df[["EventCode", "EventBaseCode", "EventRootCode", "QuadClass", "GoldsteinScale", "CAMEOCodeDescription"]]

    # Ensure all columns of the df are the correct type before insertion
    event_attrs = event_attrs.astype({"EventCode": str, "EventBaseCode": str, "EventRootCode": str, "QuadClass": int, "GoldsteinScale": float, "CAMEOCodeDescription": str})

    # --------- Combine Type Codes and Actors ---------

    # Replace float style NaNs with None
    event_attrs = event_attrs.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate EventCodes, since that is the primary key
    event_attrs["EventCode"] = event_attrs["EventCode"].str.upper() # Convert all EventCodes to uppercase so duplicates are properly deleted
    event_attrs = event_attrs.drop_duplicates(subset=["EventCode"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    events_to_insert = event_attrs.to_numpy().tolist()

    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS EventAction;")

    max_length_eventcode = max_length_eventcode + 10
    max_length_eventbasecode = max_length_eventbasecode + 10
    max_length_eventrootcode = max_length_eventrootcode + 10
    max_length_eventcameo = max_length_eventcameo + 10
    
    create_eventaction_table_query = f"""
        CREATE TABLE IF NOT EXISTS EventAction (
            EventCode VARCHAR({max_length_eventcode}) PRIMARY KEY,
            EventBaseCode VARCHAR({max_length_eventbasecode}),
            EventRootCode VARCHAR({max_length_eventrootcode}),
            QuadClass INT,
            GoldsteinScale DECIMAL(4, 2),
            CAMEOCodeDescription VARCHAR({max_length_eventcameo})
        );
    """

    c.execute(create_eventaction_table_query)

    ############# INSERT TUPLES #############
    # SQL query to insert data into database
    # EventAction (EventCode (PK), EventBaseCode, EventRootCode, QuadClass, GoldsteinScale, CAMEOCodeDescription)
    query = """INSERT INTO EventAction (EventCode, EventBaseCode, EventRootCode, QuadClass, GoldsteinScale, CAMEOCodeDescription) VALUES(?, ?, ?, ?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, events_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter EventAction Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    # ---------------------------------------------------------------------------------------------------------
    # ------------------------------------------EVENTIMPORTANCE TABLE------------------------------------------
    # ---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############

    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore EventImportance Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # Collect Event Attributes
    eventimp_attrs = GDELT_df[["GLOBALEVENTID", "IsRootEvent", "NumMentions", "NumSources", "NumArticles", "AvgTone"]]

    # Ensure all columns of the df are the correct type before insertion
    eventimp_attrs = eventimp_attrs.astype({"GLOBALEVENTID": int, "IsRootEvent": int, "NumMentions": int, "NumSources": int, "NumArticles": int, "AvgTone": float})

    # Rename GLOBALEVENTID to fit the camelcase writing style of the remaining attributes
    eventimp_attrs = eventimp_attrs.rename(columns={"GLOBALEVENTID": "GlobalEventId"})

    # Replace float style NaNs with None
    eventimp_attrs = eventimp_attrs.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate GlobalEventIds, since that is the primary key
    eventimp_attrs = eventimp_attrs.drop_duplicates(subset=["GlobalEventId"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    eventsimp_to_insert = eventimp_attrs.to_numpy().tolist()

    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS EventImportance;")
    
    create_eventimportance_table_query = f"""
        CREATE TABLE IF NOT EXISTS EventImportance (
            GlobalEventId INT PRIMARY KEY,
            IsRootEvent INT,
            NumMentions INT,
            NumSources INT,
            NumArticles INT,
            AvgTone DECIMAL(7, 4)
        );
    """

    c.execute(create_eventimportance_table_query)

    ############# INSERT TUPLES #############
    # EventImportance(GlobalEventId (PK), IsRootEvent, NumMentions, NumSources, NumArticles, AvgTone)  
    query = """INSERT INTO EventImportance (GlobalEventId, IsRootEvent, NumMentions, NumSources, NumArticles, AvgTone)  VALUES(?, ?, ?, ?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, eventsimp_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter EventImportance Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()
    

    #---------------------------------------------------------------------------------------------------------
    #----------------------------------------------ACTORGEO TABLE---------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    # ############# CONNECT TO DATABASE #############
    
    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    ############# CALCULATE THE LARGEST POSSIBLE VALUES FOR VARCHAR ATTRIBUTES IN THE TABLE #############

    # In order to determine what the maximum capacity of the varchars should be in the database,
    # we determine what the maximum length of those values is in the files we are loading in.

    # --------- ActorGeo_FullName ---------
    print(f"\n-------------------------\nACTORGEO_FULLNAME\n-------------------------\n")
    max_length_geo1 = GDELT_df["Actor1Geo_FullName"].str.len().max()
    max_length_geo2 = GDELT_df["Actor2Geo_FullName"].str.len().max()
    max_length_geo = max(max_length_geo1, max_length_geo2)
    print(f"\n\n\nmax length: ActorGeo_FullName = {max_length_geo1} and actor_2 = {max_length_geo2} --> final max = {max_length_geo}")


    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore ActorGeo Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # Since we have separate attributes for Actor1, Actor2, and Actions, we will collect them separately before combining later on

    # Collect Actor 1 Attributes and drop rows with duplicate GlobalEventId
    actor_1_attrs = GDELT_df[["GLOBALEVENTID", "Actor1Code", "Actor1Geo_Type", "Actor1Geo_FullName", "Actor1Geo_CountryCode", "Actor1Geo_ADM1Code", "Actor1Geo_Lat", "Actor1Geo_Long", "Actor1Geo_FeatureID"]]
    actor_1_attrs = actor_1_attrs.drop_duplicates(subset=["GLOBALEVENTID"], keep="first") # Drop based on the GlobalEventId column and keep the first instance
    
    # Rename GLOBALEVENTID to fit the camelcase writing style of the remaining attributes
    actor_1_attrs = actor_1_attrs.rename(columns={"GLOBALEVENTID": "GlobalEventId"})

    # Collect Actor 2 Attributes and drop rows with duplicate GlobalEventId
    actor_2_attrs = GDELT_df[["GLOBALEVENTID", "Actor2Code", "Actor2Geo_Type", "Actor2Geo_FullName", "Actor2Geo_CountryCode", "Actor2Geo_ADM1Code", "Actor2Geo_Lat", "Actor2Geo_Long", "Actor2Geo_FeatureID"]]
    actor_2_attrs = actor_2_attrs.drop_duplicates(subset=["GLOBALEVENTID"], keep="first") # Drop based on the GlobalEventId column and keep the first instance

    # Rename GLOBALEVENTID to fit the camelcase writing style of the remaining attributes
    actor_2_attrs = actor_2_attrs.rename(columns={"GLOBALEVENTID": "GlobalEventId"})

    # Ensure all columns of the df are the correct type before insertion
    '''Code written by Gemini to convert the non-integer values into ints'''
    numeric_cols = ["GlobalEventId", "Actor1Geo_Type", "Actor1Geo_FeatureID", "Actor1Geo_Lat", "Actor1Geo_Long"]
    for col in numeric_cols:
        actor_1_attrs[col] = pd.to_numeric(actor_1_attrs[col], errors='coerce')

    numeric_cols = ["GlobalEventId", "Actor2Geo_Type", "Actor2Geo_FeatureID", "Actor2Geo_Lat", "Actor2Geo_Long"]
    for col in numeric_cols:
        actor_2_attrs[col] = pd.to_numeric(actor_2_attrs[col], errors='coerce')

    actor_1_attrs = actor_1_attrs.astype({"Actor1Code": str, "Actor1Geo_FullName": str, "Actor1Geo_CountryCode": str, "Actor1Geo_ADM1Code": str})
    actor_2_attrs = actor_2_attrs.astype({"Actor2Code": str, "Actor2Geo_FullName": str, "Actor2Geo_CountryCode": str, "Actor2Geo_ADM1Code": str})

    # Rename the columns of each df to the names that will be used in the final SQL table
    actor_1_attrs = actor_1_attrs.rename(columns={"GlobalEventId": "GlobalEventId", "Actor1Code": "GeoActorCode", "Actor1Geo_Type": "ActorGeo_Type", "Actor1Geo_FullName": "ActorGeo_FullName", 
                                                  "Actor1Geo_CountryCode": "ActorGeo_CountryCode", "Actor1Geo_ADM1Code": "ActorGeo_ADM1Code", "Actor1Geo_Lat": "ActorGeo_Lat", 
                                                  "Actor1Geo_Long": "ActorGeo_Long", "Actor1Geo_FeatureID": "ActorGeo_FeatureID"})
    actor_2_attrs = actor_2_attrs.rename(columns={"GlobalEventId": "GlobalEventId", "Actor2Code": "GeoActorCode", "Actor2Geo_Type": "ActorGeo_Type", "Actor2Geo_FullName": "ActorGeo_FullName", 
                                                  "Actor2Geo_CountryCode": "ActorGeo_CountryCode", "Actor2Geo_ADM1Code": "ActorGeo_ADM1Code", "Actor2Geo_Lat": "ActorGeo_Lat", 
                                                  "Actor2Geo_Long": "ActorGeo_Long", "Actor2Geo_FeatureID": "ActorGeo_FeatureID"})

    # Recombine the actor 1 and actor 2 attributes into one df and drop any rows with duplicate GlobalEventIds and ActorCodes
    actorgeo_attrs = pd.concat([actor_1_attrs, actor_2_attrs], ignore_index=True)

    # Replace float style NaNs with None
    actorgeo_attrs = actorgeo_attrs.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate GlobalEventIds, since that is the primary key
    actorgeo_attrs = actorgeo_attrs.drop_duplicates(subset=["GlobalEventId"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    actorsgeo_to_insert = actorgeo_attrs.to_numpy().tolist()

    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS ActorGeo;")

    max_length_geo = max_length_geo + 10
    max_length_geocode = max_length_actor + 10
    
    create_actorgeo_table_query = f"""
        CREATE TABLE IF NOT EXISTS ActorGeo (
            GlobalEventId INT PRIMARY KEY,
            GeoActorCode VARCHAR({max_length_geocode}),
            ActorGeo_Type INT,
            ActorGeo_FullName VARCHAR({max_length_geo}),
            ActorGeo_CountryCode CHAR(2),
            ActorGeo_ADMCode CHAR(4),
            ActorGeo_Lat DECIMAL(8, 4),
            ActorGeo_Long DECIMAL(8, 4),
            ActorGeo_FeatureId INT
        );
    """

    c.execute(create_actorgeo_table_query)


    ############# INSERT TUPLES #############
    # ActorGeo(GlobalEventId (PK), GeoActorCode (FK on ActorCode in Actor Table), 
    # ActorGeo_Type, ActorGeo_Fullname, ActorGeo_CountryCode, 
    # ActorGeo_ADMCode, ActorGeo_Lat, ActorGeo_Long, ActorGeo_FeatureId) 
    query = """INSERT INTO ActorGeo (GlobalEventId, GeoActorCode, ActorGeo_Type, ActorGeo_Fullname, ActorGeo_CountryCode, ActorGeo_ADMCode, ActorGeo_Lat, ActorGeo_Long, ActorGeo_FeatureId) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, actorsgeo_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter ActorGeo Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    #---------------------------------------------------------------------------------------------------------
    #----------------------------------------------ACTIONGEO TABLE--------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############
        
    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    ############# CALCULATE THE LARGEST POSSIBLE VALUES FOR VARCHAR ATTRIBUTES IN THE TABLE #############

    # In order to determine what the maximum capacity of the varchars should be in the database,
    # we determine what the maximum length of those values is in the files we are loading in.

    # --------- ActionGeo_FullName ---------
    print(f"\n-------------------------\nACTIONGEO_FullName\n-------------------------\n")
    max_length_geo = GDELT_df["ActionGeo_FullName"].str.len().max()
    print(f"\n\n\nmax length: {max_length_geo}")


    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore ActionGeo Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # Collect Action Attributes
    action_attrs = GDELT_df[["GLOBALEVENTID", "EventCode", "ActionGeo_Type", "ActionGeo_FullName", "ActionGeo_CountryCode", "ActionGeo_ADM1Code", "ActionGeo_Lat", "ActionGeo_Long", "ActionGeo_FeatureID"]]

    # Rename GLOBALEVENTID to fit the camelcase writing style of the remaining attributes
    action_attrs = action_attrs.rename(columns={"GLOBALEVENTID": "GlobalEventId"})

    # Ensure all columns of the df are the correct type before insertion
    numeric_cols = ["GlobalEventId", "ActionGeo_Type", "ActionGeo_FeatureID", "ActionGeo_Lat", "ActionGeo_Long"]
    for col in numeric_cols:
        action_attrs[col] = pd.to_numeric(action_attrs[col], errors='coerce')

    action_attrs = action_attrs.astype({"EventCode": str, "ActionGeo_FullName": str, "ActionGeo_CountryCode": str, "ActionGeo_ADM1Code": str})

    # Rename the columns of each df to the names that will be used in the final SQL table
    action_attrs = action_attrs.rename(columns={"GlobalEventId": "GlobalEventId", "EventCode": "GeoActionCode", "ActionGeo_Type": "ActionGeo_Type", "ActionGeo_FullName": "ActionGeo_FullName", 
                                                  "ActionGeo_CountryCode": "ActionGeo_CountryCode", "ActionGeo_ADM1Code": "ActionGeo_ADM1Code", "ActionGeo_Lat": "ActionGeo_Lat", 
                                                  "ActionGeo_Long": "ActionGeo_Long", "ActionGeo_FeatureID": "ActionGeo_FeatureID"})

    # Replace float style NaNs with None
    action_attrs = action_attrs.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate GlobalEventIds, since that is the primary key
    action_attrs = action_attrs.drop_duplicates(subset=["GlobalEventId"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    actions_to_insert = action_attrs.to_numpy().tolist()

    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS ActionGeo;")

    max_length_geo = max_length_geo + 10
    max_length_eventcode = max_length_actor + 10
    
    create_actiongeo_table_query = f"""
        CREATE TABLE IF NOT EXISTS ActionGeo (
            GlobalEventId INT PRIMARY KEY,
            GeoActionCode VARCHAR({max_length_eventcode}),
            ActionGeo_Type INT,
            ActionGeo_FullName VARCHAR({max_length_geo}),
            ActionGeo_CountryCode CHAR(2),
            ActionGeo_ADMCode CHAR(4),
            ActionGeo_Lat DECIMAL(8, 4),
            ActionGeo_Long DECIMAL(8, 4),
            ActionGeo_FeatureId INT
        );
    """

    c.execute(create_actiongeo_table_query)

    ############# INSERT TUPLES #############
    # ActionGeo(lobalEventId (PK), GeoActionCode (PK, FK on EventCode in EventAction Table), ActionGeo_Type, ActionGeo_Fullname, ActionGeo_CountryCode, ActionGeo_ADMCode, ActionGeo_Lat, ActionGeo_Long, ActionGeo_FeatureId)
    query = """INSERT INTO ActionGeo (GlobalEventId, GeoActionCode, ActionGeo_Type, ActionGeo_Fullname, ActionGeo_CountryCode, ActionGeo_ADMCode, ActionGeo_Lat, ActionGeo_Long, ActionGeo_FeatureId) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, actions_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter ActionGeo Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    #---------------------------------------------------------------------------------------------------------
    #-------------------------------------------DATAMANAGEMENT TABLE------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############

    conn = mysql.connector.connect(user=username, password=password,
                                host=host,
                                port=port,
                                database=database)


    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore DataManagement Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # Collect Event Attributes and drop rows with duplicate GlobalEventId Codes
    data_attrs = GDELT_df[["GLOBALEVENTID", "DATEADDED", "SOURCEURL"]]

    # Rename columns to fit the camelcase writing style of the remaining attributes
    data_attrs = data_attrs.rename(columns={"GLOBALEVENTID": "GlobalEventId", "DATEADDED": "DateAdded", "SOURCEURL": "SourceURL"})

    # Ensure all columns of the df are the correct type before insertion
    data_attrs = data_attrs.astype({"GlobalEventId": int, "SourceURL": str})
    data_attrs["DateAdded"] = pd.to_datetime(data_attrs["DateAdded"])

    data_attrs = data_attrs.astype(object).replace({np.nan: None})
    
    # Drop rows with duplicate GlobalEventIds, since that is the primary key
    data_attrs = data_attrs.drop_duplicates(subset=["GlobalEventId"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    data_to_insert = data_attrs.to_numpy().tolist()


    ############# CREATE TABLE #############
    c.execute("DROP TABLE IF EXISTS DataManagement;")

    create_datamanagement_table_query = f"""
        CREATE TABLE IF NOT EXISTS DataManagement (
            GlobalEventId INT PRIMARY KEY,
            DateAdded DATETIME,
            SourceURL TEXT
        );
    """
    c.execute(create_datamanagement_table_query)

    ############# INSERT TUPLES #############
    # DataManagement(GlobalEventId (PK), DateAdded, SourceURL) 
    query = """INSERT INTO DataManagement (GlobalEventId, DateAdded, SourceURL)  VALUES(?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, data_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter DataManagement Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()


    #---------------------------------------------------------------------------------------------------------
    #------------------------------------------PARTICIPATESIN TABLE-------------------------------------------
    #---------------------------------------------------------------------------------------------------------

    ############# CONNECT TO DATABASE #############
        
    conn = mysql.connector.connect(user=username, password=password,
                                    host=host,
                                    port=port,
                                    database=database)


    before = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nBefore ParticipatesIn Insert Executed: {before.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")


    ############# PREPROCESS DATA #############
    # creating the cursor object
    c = conn.cursor(prepared=True)

    # Collect attributes
    actor_attrs = GDELT_df[["GLOBALEVENTID", "Actor1Code", "Actor2Code", "EventCode", "SQLDATE"]]
    
    # Rename columns to fit the camelcase writing style of the remaining attributes
    actor_attrs = actor_attrs.rename(columns={"GLOBALEVENTID": "GlobalEventId", "SQLDATE": "Day"})

    # Ensure all columns of the df are the correct type before insertion
    actor_attrs = actor_attrs.astype({"GlobalEventId": int, "Actor1Code": str, "Actor2Code": str, "EventCode": str})
    actor_attrs["Day"] = pd.to_datetime(actor_attrs["Day"], format="%Y%m%d")

    # Rename the columns of each df to the names that will be used in the final SQL table
    actor_attrs = actor_attrs.rename(columns={"GlobalEventId": "GlobalEventId", "Actor1Code": "Actor1", "Actor2Code": "Actor2", "EventCode": "EventCode", "Day": "Day"})

    # Replace all float-style NaNs with None
    actor_attrs = actor_attrs.astype(object).replace({np.nan: None})
        
    # Drop rows with duplicate sets of GlobalEventIds and ActorCodes, since those comprise the primary key
    actor_attrs["Actor1"] = actor_attrs["Actor1"].str.upper()
    actor_attrs["Actor2"] = actor_attrs["Actor2"].str.upper()
    actor_attrs = actor_attrs.drop_duplicates(subset=["GlobalEventId", "Actor1", "Actor2"], keep="first")

    # Convert the df into a list of tuples for insertion into mysql
    actors_to_insert = actor_attrs.to_numpy().tolist()


    ############# CREATE TABLE #############
    max_length_participateactor = max_length_actor + 10
    max_length_participateeventcode = max_length_actor + 10

    c.execute("DROP TABLE IF EXISTS ParticipatesIn;")

    create_participatesin_table_query = f"""
        CREATE TABLE IF NOT EXISTS ParticipatesIn (
            GlobalEventId INT,
            Actor1 VARCHAR({max_length_participateactor}),
            Actor2 VARCHAR({max_length_participateactor}),
            EventCode VARCHAR({max_length_participateeventcode}),
            Day DATETIME,
            PRIMARY KEY (GlobalEventId, Actor1, Actor2)
        );
    """
    c.execute(create_participatesin_table_query)

    ############# INSERT TUPLES #############
    # SQL query to insert data into database
    # ParticipatesIn(GlobalEventId (PK), Actor1 (FK to ActorCode in Actor Table), Actor2 
    # (FK to ActorCode in Actor Table), EventCode (FK to EventAction Table's EventCode), Day)
    query = """INSERT INTO ParticipatesIn (GlobalEventId, Actor1, Actor2, EventCode, Day) VALUES(?, ?, ?, ?, ?)"""

    # executing cursor object to batch insert
    c.executemany(query, actors_to_insert)
    conn.commit()

    after = datetime.now(pytz.utc) # Display time after operation
    print(f"\n\n----------------------------------------------------------\nAfter ParticipatesIn Insert Executed: {after.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")

    print(f"TOTAL TIME = {after - before}")

    # Close the database connection
    conn.close()

    end = datetime.now(pytz.utc) # Time before insertion
    print(f"\n\n----------------------------------------------------------\nTIME AT END: {end.astimezone(pytz.timezone('US/Eastern')).time()}\n----------------------------------------------------------\n")