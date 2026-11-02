CREATE DATABASE GDELT;

USE GDELT;

-- ######################### TABLE DEFINITIONS #########################

-- ----------- ACTOR TABLE -----------
-- Actor (ActorCode (PK), Actorname, ActorCountryCode, ActorKnownGroupCode, ActorEthnicCode)
CREATE TABLE Actor(ActorCode varchar(30), ActorName varchar(100), ActorCountryCode char(3), ActorKnownGroupCode varchar(10), ActorEthnicCode varchar(10),  
PRIMARY KEY(ActorCode));

-- ----------- RELIGIONCODE TABLE -----------
-- ReligionCode (ActorCode (FK), ReligionCode)

CREATE TABLE ReligionCode(ActorCode varchar(30), ReligionCode varchar(10), 
PRIMARY KEY (ActorCode));
    
ALTER Table ReligionCode
	ADD CONSTRAINT FOREIGN KEY (ActorCode) REFERENCES Actor(ActorCode) ON DELETE CASCADE;
    
-- ----------- TYPECODE TABLE -----------
-- TypeCode (ActorCode (FK), TypeCode)

CREATE TABLE TypeCode (ActorCode varchar(30), TypeCode varchar(10), 
PRIMARY KEY (ActorCode));
    
ALTER Table TypeCode
	ADD CONSTRAINT FOREIGN KEY (ActorCode) REFERENCES Actor(ActorCode) ON DELETE CASCADE; 

-- ----------- EVENTACTION TABLE -----------
-- EventAction (EventCode (PK), EventBaseCode, EventRootCode, QuadClass, GoldsteinScale, CAMEOCodeDescription)

CREATE TABLE EventAction (EventCode varchar(10), EventBaseCode varchar(10), EventRootCode varchar(10), QuadClass int, GoldsteinScale decimal, CAMEOCodeDescription varchar(100), 
PRIMARY KEY (EventCode));
    
-- ----------- EVENTIMPORTANCE TABLE -----------
-- EventImportance (GlobalEventId (PK), IsRootEvent, NumMentions, NumSources, NumArticles, AvgTone)

CREATE TABLE EventImportance (GlobalEventId int, IsRootEvent int, NumMentions int, NumSources int, NumArticles int, AvgTone decimal, 
PRIMARY KEY (GlobalEventId));
    
-- ----------- ACTORGEO TABLE -----------
-- ActorGeo (GlobalEventId (PK), GeoActorCode (FK), ActorGeo_Type, ActorGeo_Fullname, ActorGeo_CountryCode, ActorGeo_ADMCode, ActorGeo_Lat, ActorGeo_Long, ActorGeo_FeatureId)

CREATE TABLE ActorGeo (GlobalEventId int, GeoActorCode varchar(30), ActorGeo_Type int, ActorGeo_FullName varchar(150), ActorGeo_CountryCode char(2), ActorGeo_ADMCode char(4), ActorGeo_Lat decimal, ActorGeo_Long decimal, ActorGeo_FeatureId int, 
PRIMARY KEY (GlobalEventId));
    
ALTER Table ActorGeo
	ADD CONSTRAINT FOREIGN KEY (GeoActorCode) REFERENCES Actor(ActorCode) ON DELETE CASCADE;
    
-- ----------- ACTIONGEO TABLE -----------
-- ActionGeo (GlobalEventId (PK), GeoActionCode (FK), ActionGeo_Type, ActionGeo_FullName, ActionGeo_CountryCode, ActionGeo_ADMCode, ActionGeo_Lat, ActionGeo_Long, ActionGeo_FeatureId)

CREATE TABLE ActionGeo (GlobalEventId int, GeoActionCode varchar(10), ActionGeo_Type int, ActionGeo_FullName varchar(150), ActionGeo_CountryCode char(2), ActionGeo_ADMCode char(4), ActionGeo_Lat decimal, ActionGeo_Long decimal, ActionGeo_FeatureId int,
PRIMARY KEY (GlobalEventId));

ALTER Table ActionGeo
	ADD CONSTRAINT FOREIGN KEY (GeoActionCode) REFERENCES EventAction(EventCode) ON DELETE CASCADE; 

-- ----------- DATAMANAGEMENT TABLE -----------
-- DataManagement (GlobalEventId, DateAdded, SourceURL)

CREATE TABLE DataManagement (GlobalEventId int, DateAdded datetime, SourceURL text, 
PRIMARY KEY (GlobalEventId));

-- ----------- PARTICIPATESIN TABLE -----------
-- ParticipatesIn (GlobalEventId (PK), Actor1 (FK), Actor2 (FK), EventCode (FK), Day)

CREATE TABLE ParticipatesIn (GlobalEventId int, Actor1 varchar(30), Actor2 varchar(30), EventCode varchar(10), Day datetime,
PRIMARY KEY (GlobalEventId));
    
ALTER Table ParticipatesIn
	ADD CONSTRAINT FOREIGN KEY (Actor1) REFERENCES Actor(ActorCode) ON DELETE CASCADE;

ALTER Table ParticipatesIn
	ADD CONSTRAINT FOREIGN KEY (Actor2) REFERENCES Actor(ActorCode) ON DELETE CASCADE;
    
ALTER Table ParticipatesIn
	ADD CONSTRAINT FOREIGN KEY (EventCode) REFERENCES EventAction(EventCode) ON DELETE CASCADE;
    
    
    
    
    
    
    
    
    
    
    