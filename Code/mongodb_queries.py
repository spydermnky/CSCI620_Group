from pymongo import MongoClient

DB_NAME = "gdelt_data_2"
COLLECTION = "data"
CAMEO = "cameo_codes"
URI = "mongodb://localhost:27017/"

QM1 = [
    {"$match": {"ActionGeo.ActionGeo_CountryCode": {"$ne": None}, "GoldsteinScale": {"$ne": None}}},
    {"$group": {"_id": {"country": "$ActionGeo.ActionGeo_CountryCode", "month": {"$floor": {"$divide": ["$DateAdded", 100]}}},
                "nEvents": {"$sum": 1}, "avgGold": {"$avg": "$GoldsteinScale"}, "avgTone": {"$avg": "$AvgTone"},
                "conflicts": {"$sum": {"$cond": [{"$eq": ["$Quadclass", 4]}, 1, 0]}}}},
    {"$match": {"nEvents": {"$gte": 50}}},
    {"$project": {"_id": 0, "country": "$_id.country", "month": "$_id.month", "nEvents": 1,
                "avgGold": {"$round": ["$avgGold", 3]},
                "avgTone": {"$round": ["$avgTone", 3]},
                "conflictShare": {"$round": [{"$divide": ["$conflicts", "$nEvents"]}, 3]}}},
    {"$sort": {"avgGold": 1, "nEvents": -1}},
    {"$limit": 25}
]

QM2 = [
    {"$match": {"Actor1.Actor1TypeCodes": {"$exists": True, "$ne": []}}},
    {"$unwind": "$Actor1.Actor1TypeCodes"},
    {"$group": {"_id": "$Actor1.Actor1TypeCodes", "nEvents": {"$sum": 1}, "conflicts": {"$sum": {"$cond": [{"$eq": ["$Quadclass", 4]}, 1, 0]}},
                "avgGold": {"$avg": "$GoldsteinScale"}, "avgTone": {"$avg": "$AvgTone"}}},
    {"$project": {"_id": 0, "actorType": "$_id", "nEvents": 1, "conflicts": 1,
                  "conflictShare": {"$round": [{"$divide": ["$conflicts", "$nEvents"]}, 3]}, "avgGold": {"$round": ["$avgGold", 2]},
                  "avgTone": {"$round": ["$avgTone", 3]}}},
    {"$sort": {"conflictShare": -1}},
]

QM3 = [
    {"$match": {"Quadclass": 4}},
    {"$group": {"_id": "$EventCode", "nEvents": {"$sum": 1}, "avgArticles": {"$avg": "$NumArticles"}, "avgTone": {"$avg": "$AvgTone"}, 
                "countries": {"$addToSet": "$ActionGeo.ActionGeo_CountryCode"}}},
    {"$sort": {"nEvents": -1}},
    {"$limit": 25},
    {"$lookup": {"from": CAMEO, "localField": "_id", "foreignField": "_id", "as": "cameo"}},
    {"$project": {"_id": 0, "eventCode": "$_id", "nEvents": 1, "description": {"$arrayElemAt": ["$cameo.description", 0]},
                  "rootCode": {"$arrayElemAt": ["$cameo.rootCode", 0]}, "avgArticles": {"$round": ["$avgArticles", 2]},
                  "avgTone": {"$round": ["$avgTone", 3]}, "nCountries": {"$size": "$countries"}}},
    {"$sort": {"nEvents": -1}},
]

QM4  = [
    {"$geoNear": {"near": {"type": "Point", "coordinates": [30.5167, 50.4333]}, "distanceField": "metersAway", "maxDistance": 150000,
                  "query": {"Quadclass": 4}, "spherical": True}},
    {"$limit": 25},
    {"$project": {"_id": 0, "place": "$ActionGeo.ActionGeo_Fullname", "eventCode": "$EventCode", "goldstein": "$GoldsteinScale",
                  "articles": "$NumArticles", "kmAway": {"$round": [{"$divide": ["$metersAway", 1000]}, 1]}}},
]

STATE = ["GOV", "MIL", "COP", "JUD"]
QM5 = [
    {"$match": {"Quadclass": {"$in": [3, 4]}}},
    {"$project": {"AvgTone": 1, "GoldsteinScale": 1, "NumArticles": 1, "a1State": {"$size": {"$filter": {"input": {"$ifNull": ["$Actor1.Actor1TypeCodes", []]},
        "as": "t", "cond": {"$in": ["$$t", STATE]}}}}, "a2State": {"$size": {"$filter": {"input": {"$ifNull": ["$Actor2.Actor2TypeCodes", []]}, 
                                                                                         "as": "t", "cond": {"$in": ["$$t", STATE]}}}}}},
    {"$project": {"AvgTone": 1, "GoldsteinScale": 1, "NumArticles": 1, "pairing": {"$concat": [{"$cond": [{"$gt": ["$a1State", 0]}, "state", "non-state"]}, " -> ",
                                                                                               {"$cond": [{"$gt": ["$a2State", 0]}, "state", "non-state"]}]}}},
    {"$group": {"_id": "$pairing", "nEvents": {"$sum": 1}, "avgTone": {"$avg": "$AvgTone"}, "avgGold": {"$avg": "$GoldsteinScale"}, "avgArticles": {"$avg": "$NumArticles"}}},
    {"$project": {"_id": 0, "pairing": "$_id", "nEvents": 1, "avgTone": {"$round": ["$avgTone", 3]}, "avgGold": {"$round": ["$avgGold", 2]}, "avgArticles": {"$round": ["$avgArticles", 1]}}},
    {"$sort": {"nEvents": -1}},
]

QUERIES = {
    "QM1": ("Conflict intensity by country and month", QM1),
    "QM2": ("Actor types driving material conflict ($unwind)", QM2),
    "QM3": ("Top conflict event types with cameo labels ($lookup)", QM3),
    "QM4": ("Conflict events near Kyiv (geospatial)", QM4),
    "QM5": ("State vs non-state conflict ($filter)", QM5),
}

def run_all(db):
    for name, (title, pipeline) in QUERIES.items():
        print(f"\n{'='*70}\n{name}.{title}\n{'='*70}")
        rows = list(db[COLLECTION].aggregate(pipeline))
        if not rows:
            print("no rows")
        for r in rows[:10]:
            print("  " + "  ".join(f"{k}={v}" for k, v in r.items()))

if __name__ == "__main__":
    db = MongoClient(URI)[DB_NAME]
    run_all(db)