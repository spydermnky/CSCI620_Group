USE GDELT;

-- INDEX 1: ParticipatesIn(Day, EventCode, GlobalEventId)
CREATE INDEX idx_pi_day_event ON ParticipatesIn (`Day`, EventCode, GlobalEventId);

-- INDEX 2: ParticipatesIn(Actor1, Actor2, EventCode)
CREATE INDEX idx_pi_actors ON ParticipatesIn (Actor1, Actor2, EventCode);

-- INDEX 3: ActionGeo(ActionGeo_CountryCode, GlobalEventId)
CREATE INDEX idx_ag_country ON ActionGeo (ActionGeo_CountryCode, GlobalEventId);

-- INDEX 4: EventAction(QuadClass, EventCode)
CREATE INDEX idx_ea_quad ON EventAction (QuadClass, EventCode);

-- INDEX 5: ActionGeo(ActionGeo_Lat, ActionGeo_Long)
CREATE INDEX idx_ag_latlong ON ActionGeo (ActionGeo_Lat, ActionGeo_Long);

-- INDEX 6: EventImportance(NumArticles)
CREATE INDEX idx_ei_articles ON EventImportance (NumArticles);

-- INDEX 7: DataManagement(SourceDomain)
ALTER TABLE DataManagement
    ADD COLUMN SourceDomain varchar(128)
        AS (SUBSTRING_INDEX(SUBSTRING_INDEX(
              SUBSTRING_INDEX(SourceURL, '://', -1), '/', 1), '?', 1)) STORED;
CREATE INDEX idx_dm_domain ON DataManagement (SourceDomain);