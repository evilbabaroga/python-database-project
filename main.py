from flask import Flask
from src.db_utils import Database
from src.mongo_db_utils import MongoDatabase
from src.utils import clean_company_name

app = Flask(__name__)

if __name__ == '__main__':
    HTML_LOCATION = "index.html"
    DB_NAME = "semos_companies_data.db"
    TABLE = "companies"
    MONGO_STR = "mongodb://localhost:27017"
    MONGO_KEY = "company_name_cleaned"

    db = Database(DB_NAME)
    db.update_columns(TABLE, MONGO_KEY, value_pairs=db.get_column_by_pk(TABLE, "name", clean_company_name))
    mongo_db = MongoDatabase(db, MONGO_STR, "semos_companies", {TABLE: MONGO_KEY})
    print('\n'.join(map(str, mongo_db.read_db(TABLE, 20))))
