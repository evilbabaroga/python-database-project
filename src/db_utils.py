import sqlite3

class Database:
    """Interface for reading and writing to an sqlite database in python."""

    def __init__(self, file_name):
        """
        Connect to the database file and initialize the values for the tables and all the primary keys in them.

        params: 
            file_name: str - name of the database file
        """
        print("[-] Initializing Database")
        self.db_file = file_name
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = tuple(map(lambda x: x[0], curr.fetchall()))
        self.primary_keys = dict()
        for table in self.tables:
            sql = f"PRAGMA table_info({table})"
            table_info = list(curr.execute(sql))

            pk = tuple([el[1] for el in table_info if el[-1] == 1])
            if len(pk) == 0:
                pk = (table_info[0][1], )
            self.primary_keys[table] = pk
        con.close()
        print("[+] Database initialized")
    
    def columns(self, table):
        """
        Get the names of all the columns for a given table in the database.

        params: 
            table: str - name of the table
        returns: 
            tuple(str) - the column names
        """
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        sql = f"PRAGMA table_info({table})"
        table_info = list(curr.execute(sql))
        return tuple([elem[1] for elem in table_info])

    def read_db(self, table, chunk_size, entries="*"):
        """
        Get the rows in the database for a given table in chunks for memory optimization, with specified columns.

        params: 
            table: str - name of the table
            chunk_size int - size of a chunk
            entries: list(str) - filter for columns
        returns: 
            list(list(obj)) - list of chunks (lists) that contain the values in the row
        """
        print("[-] Reading Database")
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        rows = list(curr.execute(f"SELECT {entries} from {table}"))
        data_chunks = [[] for _ in range((len(rows) // chunk_size))]
        for i, row in enumerate(rows):
            data_chunks[i // chunk_size].append(row)
        con.close()
        print("[+] Database read")
        return data_chunks

    def update_columns(self, table, column, value_pairs):
        """
        Update a specified column in each of the rows corresponding to the key in value_pairs.

        params: 
            table: str - name of the table
            column: str - name of the column
            value_pairs: tuple(obj, obj) - a tuple containing a value for the primary key as the first element and a value for the column with the corresponding primary key as the second element
        """
        print("[-] Updating Database")
        total = len(value_pairs)
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        print("    0% updated...")
        for counter, (pk, val) in enumerate(value_pairs, start=2):
            if int(counter / total * 100) > int((counter - 1) / total * 100) and int(counter / total * 100) % 10 == 0:
                print(f"    {int(counter / total * 100)}% updated...")
            curr.execute(f"UPDATE {table} SET {column} = ? WHERE {', '.join(self.primary_keys[table])} = ?", (val, pk))
        con.commit()
        con.close()
        print("[+] Database updated")

    def get_column_by_pk(self, table, column, function=lambda x: x):
        """
        Get a (key - pk, value - a function of the given column) pair for every row in the specified table of the database.

        params: 
            table: str - name of the table
            column: str - name of the column
            function (optional): function - a transformation preformed on each of the values
        returns: 
            tuple(tuple(obj, obj)) - tuple containing key, value pairs of the pk and transformed value of the specified column for each row in the database
        """
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        pks = ", ".join(self.primary_keys[table])
        column_by_pk = tuple(map(lambda key_val_pair: (key_val_pair[0], function(key_val_pair[1])), list(curr.execute(f"SELECT {f'{pks}, {column}'} from {table}"))))
        con.close()
        return column_by_pk
 