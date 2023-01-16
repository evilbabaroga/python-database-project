from flask import Flask
from src.utils import clean_company_name
from src.db_utils import Database

if __name__ == '__main__':
    app = Flask(__name__)
    html_location = "index.html"
    db_name = "semos_companies_data.db"
    table = "companies"

    db = Database(db_name)
    read = input("Read DB (y/n): ")
    if read.upper() == 'Y':
        data_chunks = db.read_db(table, chunk_size=1000) 
    clean = input("Clean DB (y/n): ")
    if clean.upper() == 'Y':
        modified_names = db.get_column_by_pk(table, "name", function=clean_company_name)
        db.update_columns(table, "company_name_cleaned", modified_names)

    html = ""
    with open(html_location, "r") as f:
        html = f.read()
    @app.route("/")
    def hello():
        return html

    app.run(debug=True)
