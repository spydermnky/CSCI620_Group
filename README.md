# CSCI620_Group
Group project repo for CSCI 620 @ RIT

Gunnika Kapoor
Peter Khomchenko
Timothy Ockrin

# Data
## GDELT Dataset Layout

1. GlobalEventId: Globally unique identifier, may have some duplicates
2. Day: Date in YYYYMMDD Format
3. MonthYear: Date in YYYMM Format
4. Year: Date in YYYY Format
5. FractionDate: Date in YYYY.FFFF format, where FFFF is the percentage of the year completed by that day

*Actor Attributes:*

6. Actor1Code: Raw CAMEO code for Actor 1
7. Actor1Name: Actual name of Actor 1
8. Actor1CountryCode: 3-character Cameo code for country affiliation
9. Actor1KnownGroupCode: Used if Actor1 is in a IGO/NGO/rebel organization with a CAMEO code
10. Actor1EthnicCode: Included if ethnic affiliation of Actor1 has CAMEO entry
11. Actor1Religion1Code: Included if religious affiliation of Actor1 has CAMEO entry
12. Actor1Religion2Code: Included for multiple religious codes
13. Actor1Type1Code: 3 character CAMEO code for CAMEO type or role
14. Actor1Type2Code: Included if multiple type/role codes
15. Actor1Type2Code: Included if multiple type/role codes

CAN BE REPEATED FOR AN ACTOR 2

*Event Action Attributes:*

16. IsRootEvent: Proxy for rough importance of an event
17. EventCode: Raw CAMEO action code describing action Actor11 performed on Actor2
18: EventBaseCode: Defines part of the three-level taxonomy of CAMEO event codes
19. EventRootCode: Defines root level of event code
20. QuadClass: Events can be organized in 1 of 4 classifications
21. GoldsteinScale: Numeric code capturing theoretical potential impact of the event on the stability of the country
22. NumMentions: Total number of mentions of the event across source documents
23. NumSources: Total number of information sources containing one or more mentions of this event
24. NumArticles: Total number of source documents containing one or more mentions of this event
25. AvgTone: The average tone of all documents containing one or more mentions of this event

*Event Geography:*

26. Actor1Geo_Type: Resolves the match type as a COUNTRY, USSTATE, USCITY, WORLDCITY, or WORLDSTATE
27. Actor1Geo_Fullname: Full human-readable name of the matched location
28. Actor1Geo_CountryCode: Two-character country code for the location
29. Actor1Geo_ADM1Code: Two-character country code followed by two-character administrative division 1 code
30. Actor1Geo_Lat: Centroid latitude of the landmark
31. Actor1Geo_Long: Centroid longitude of the landmark
32. Actor1Geo_FeatureId: GNS or GNIS FeatureId for a location

CAN BE REPEATED FOR ACTOR 2 AND ACTION, USING PREFIXES

*Data Management Fields:*

33. DateAdded: Date the event was added to the master database
34. SourceUrl: URL of the news article the event was found in


