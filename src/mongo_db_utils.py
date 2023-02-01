from src.db_utils import Database
import pymongo
from cryptography.fernet import Fernet
import json

# password = "ASDFGHJKLR$9a-fuj20,f-./d=-.2,2E$D%"

class MongoDatabase:
    """
    A class to represent a Mongo database created from an sqlite database.
    """
    def __init__(self, sqlite_database: Database, mongo_str, name, keys) -> None:
        """
        Connect to a Mongo client and create a Mongo database by converting and encrypting all the tables in a given sqlite database to a Mongo structured database.

        params:
            sqlite_database: Database - the sqlite database
            mongo_str: str - Mongo server
            name: str - name of the database
            keys: list(str) - name of the keys in the Mongo key:pair structure for each table in the database
        """
        print("[-] Initializing MongoDB")
        self.name = name
        self.tables = sqlite_database.tables
        self.primary_keys = sqlite_database.primary_keys
        client = pymongo.MongoClient(mongo_str, serverSelectionTimeoutMS=5000)
        try:
            client.server_info()
        except Exception as e:
            print("[!] Mongo Database creation failed")
            print(e)
            return
        self.mongo_db = client[self.name]
        if self.mongo_db.name in client.list_database_names():
            print("[+] MongoDB initialized")
            return
        with open("crypto_key.txt", "rb") as file_key:
            crypto_key = file_key.read()
        fernet = Fernet(crypto_key)
        for table in self.tables:
            documents = dict()
            table_collection = self.mongo_db[table]
            data_chunks = sqlite_database.read_db(table, chunk_size=2000)
            columns = sqlite_database.columns(table)
            key = keys[table]
            for data_chunk in data_chunks:
                for row in data_chunk:
                    entry = {pair[0]:pair[1] for pair in zip(columns, row)}
                    curr_key = entry[key]
                    del entry[key]
                    print(curr_key, type(curr_key))
                    entry_no_id = {val for val in entry if val[0] != "id"}
                    if curr_key in documents.keys():
                        if entry_no_id not in documents[curr_key]:
                            documents[curr_key].append(entry_no_id)
                            encrypted_key = fernet.encrypt(bytes(curr_key, "utf-8")).decode()
                            encrypted_val = fernet.encrypt(bytes(json.dumps(entry, indent=4), "utf-8")).decode()
                            table_collection.insert_one({encrypted_key:encrypted_val})
                    else:
                        documents[curr_key] = [entry_no_id]
                        encrypted_key = fernet.encrypt(bytes(curr_key, "utf-8")).decode()
                        encrypted_val = fernet.encrypt(bytes(json.dumps(entry, indent=4), "utf-8")).decode()
                        table_collection.insert_one({encrypted_key:encrypted_val})
        print("[+] MongoDB initialized")

    def read_db(self, table, num):
        """
        Read a given number of elements successively from the Mongo database.

        params:
            table: str - name of the table
            num: int - number of elements to read
        """
        with open("crypto_key.txt", "rb") as file_key:
            crypto_key = file_key.read()
        fernet = Fernet(crypto_key)
        entries = []
        cursor = self.mongo_db[table].find()
        i = 0
        for documnet in cursor:
            if i == num:
                break
            curr = dict()
            for key, val in documnet.items():
                if key == '_id':
                    curr.update({'_id':val})
                else:
                    decrypted_key = fernet.decrypt(bytes(key, "utf-8")).decode()
                    decrypted_val = fernet.decrypt(bytes(val, "utf-8")).decode()
                    curr.update({decrypted_key:json.loads(decrypted_val)})
            entries.append(curr)
            i += 1
        return entries
