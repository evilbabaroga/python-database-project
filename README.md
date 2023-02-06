# Python Sqlite/MongoDB/Flask Project

A python project with functionalities for sqlite and MongoDB database management:
  * Reading an sqlite database
  * Modifying an sqlite column values
  * Setting up a MongoDB database
  * Reading/Writing to a MongoDB database
  * Encypting for MongoDB database
  * Flask!

A data cleaning example is used to demonstrate these functionalities.

<h2>Description</h2>

This project contains two classes for database manipulation: 
  - Database - <code>src/db_utils.py</code> for sqlite
  - MongoDatabase - <code>src/mongo_db_utils.py</code> for MongoDB

The main script <code>app.py</code> is a flask app that runs on <code>localhost:5000</code> and represents the front-end of the project.

<h2>Contact</h2>

Author
* Kristijan Lazevski  |  kiko_lazevski@yahoo.com

<h2>Table of Contents</h2>

  * Requirements
  * Sqlite Database
  * Data Cleaning Example
  * Custom Database Use

<h2>Requirements</h2>

1. sqlite3
2. pymongo
3. flask
4. flask_cors
5. cryptography

<h2>Sqlite Database</h2>

The sqlite database semos_company_names.db has one table - companies, 7 columns (id, name, country_iso, city, nace, website, company_name_cleaned) and 20 000 rows.

<h2>Data Cleaning Example</h2>

The data cleaning is done on the class Database. The column 'company_name_cleaned' is updated for each row with SQL update query after modifying the column 'name' with <code>get_column_by_pk</code> using the <code>clean_company_name</code> function from <code>src/utils.py</code>.

<h2>Custom Database Use</h2>

You can use this script for any sqlite database you want to read/modify/create a MongoDB with/run on a Flask server.
1. Change DB_NAME to your database file name
2. Change TABLE to the desired table
3. When calling <code>update_columns</code> the <code>column</code> parameter should be set to the column that's to be changed and <code>value_pairs</code> should be a tuple(tuple(key, value)) where key is a primary key and value is the wanted value for that row.
