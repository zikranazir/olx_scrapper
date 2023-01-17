from pymongo import TEXT, DESCENDING, HASHED, IndexModel, errors


def insert_data(db, coll, data):
    try:
        return db[coll].insert_one(data)
    except errors.DuplicateKeyError as dup:
        print("Duplicate " + str(dup))

def check_track_ads(db, product_id):
    coll = "tanahOLX"
    news = db[coll].find_one({"content_id": product_id})
    return news
