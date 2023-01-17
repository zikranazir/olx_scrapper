from helper import query
from lib import mongo


class SaveData:
    def __init__(self):
        self.db = mongo.connect()

    def save(self, data):
        query.insert_data(self.db, "tanahOLX", data)

    def check_duplicate(self, product_id):
        data = query.check_track_ads(self.db, product_id)
        count = 1 if data else 0
        return count
