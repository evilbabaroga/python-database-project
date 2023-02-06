import json
import os
from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from src.db_utils import Database
from src.mongo_db_utils import MongoDatabase
from src.utils import clean_company_name
from flask_cors import CORS
from src.utils import replace_all

app = Flask(__name__)
CORS(app)

HTML_FILE = "index.html"
DB_NAME = "semos_companies_data.db"
TABLE = "companies"
MONGO_STR = "mongodb://localhost:27017"
MONGO_KEY = "company_name_cleaned"
db = Database(DB_NAME)
view = "json"

def create_mongo_db(start=1, end=20):
    try:
        mongo_db = MongoDatabase(db, MONGO_STR, "semos_companies", {TABLE: MONGO_KEY})
        entries = mongo_db.read_db(TABLE, start, end)
        numdocs = replace_all(",", ".", format(mongo_db.num_docs(TABLE), ","))
        mongo_db_key = mongo_db.keys[TABLE]
        columns = mongo_db.columns[TABLE]
        tableEntries = [['MongoDB key'] + columns]
        rows = [[list(entry.keys())[1]] + list(entry[list(entry.keys())[1]].values()) for entry in entries]
        tableEntries.extend(rows)
        for entry in entries:
            entry['_id'] = str(entry['_id'])
    except ValueError:
        return render_template(HTML_FILE, error=True)
    return render_template(HTML_FILE, dbName=mongo_db.name, tableName=TABLE, numdocs=numdocs, mongo_db_key=mongo_db_key, entries=[json.dumps(entry, indent=4) for entry in entries], tableEntries=tableEntries, loaded=True)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == "POST":
        db.update_columns(TABLE, MONGO_KEY, value_pairs=db.get_column_by_pk(TABLE, "name", clean_company_name))
        return render_template(HTML_FILE, dbName="-- DB not loaded --", tableName="-- DB not loaded --", cleaned="True")
    return render_template(HTML_FILE, dbName="-- DB not loaded --", tableName="-- DB not loaded --")

# @app.route("/cleanDB")
# def cleanDB():
    # db.update_columns(TABLE, MONGO_KEY, value_pairs=db.get_column_by_pk(TABLE, "name", clean_company_name))
    # return redirect(url_for("/"))

@app.route("/mongoDBRead/", methods=['GET', 'POST'])
def mongoDBRead():
    if request.method == "POST":
        try:
            start = request.form["from"]
            end = request.form["to"]
        except Exception:
            return hello()
        try:
            start = int(start)
            end = int(end)
            return create_mongo_db(start, end)
        except Exception:
            return create_mongo_db(0, 0)
    return create_mongo_db()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
