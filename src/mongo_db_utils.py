from src.db_utils import Database
import pymongo

class MongoDatabase:
    def __init__(self, sqlite_database: Database, mongo_str, name, keys) -> None:
        print("[-] Initializing MongoDB")
        self.tables = sqlite_database.tables
        self.primary_keys = sqlite_database.primary_keys
        client = pymongo.MongoClient(mongo_str, serverSelectionTimeoutMS=5000)
        try:
            client.server_info()
        except Exception as e:
            print(e)
            print("[!] Mongo Database creation failed")
            return
        self.mongo_db = client[name]
        if self.mongo_db.name in client.list_database_names():
            return
        for table in self.tables:
            table_collection = self.mongo_db[table]
            data_chunks = sqlite_database.read_db(table, chunk_size=2000)
            columns = sqlite_database.columns(table)
            for data_chunk in data_chunks:
                for row in data_chunk:
                    key = keys[table]
                    entry = {pair[0]:pair[1] for pair in zip(columns, row) if pair[0] != 'id'}
                    # entry['_id'] = ObjectId(hashlib.shake_128(str(entry[primary_key]).encode('utf-8')).digest(12))
                    curr_key = entry[key]
                    del entry[key]
                    table_collection.insert_one({curr_key:entry})
        print("[+] MongoDB initialized")

    def read_db(self, table, num):
        entries = []
        cursor = self.mongo_db[table].find()
        i = 0
        for documnet in cursor:
            if i == num:
                break
            entries.append(documnet)
            i += 1
        return entries