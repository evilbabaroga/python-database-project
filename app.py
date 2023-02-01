import json
import os
from flask import Flask, render_template, jsonify, send_from_directory
from src.db_utils import Database
from src.mongo_db_utils import MongoDatabase
from src.utils import clean_company_name
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_FILE = "index.html"
DB_NAME = "semos_companies_data.db"
TABLE = "companies"
MONGO_STR = "mongodb://localhost:27017"
MONGO_KEY = "company_name_cleaned"

db = Database(DB_NAME)
@app.route("/")
def hello():
    return render_template(HTML_FILE, dbName='', tableName='')

@app.route("/cleanDB")
def cleanDB():
    db.update_columns(TABLE, MONGO_KEY, value_pairs=db.get_column_by_pk(TABLE, "name", clean_company_name))
    return render_template(HTML_FILE, dbName='', tableName='')

@app.route("/mongoDBRead")
def mongoDBRead():
    mongo_db = MongoDatabase(db, MONGO_STR, "semos_companies", {TABLE: MONGO_KEY})
    entries = mongo_db.read_db(TABLE, 20)
    for entry in entries:
        entry['_id'] = str(entry['_id'])
    # for entry in entries:
        # del entry['_id']
    return render_template(HTML_FILE, dbName=mongo_db.name, tableName=TABLE, entries=[json.dumps(entry, indent=4) for entry in entries])
        # print('\n'.join(map(str, mongo_db.read_db(TABLE, 20))))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
