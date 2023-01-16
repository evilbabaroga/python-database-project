import sqlite3

class Database:
    def __init__(self, file_name) -> None:
        self.db_file = file_name
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = tuple(map(lambda x: x[0], curr.fetchall()))
        self.primary_keys = dict()
        for table in self.tables:
            sql = f"PRAGMA table_info({table})"
            table_info = list(curr.execute(sql))

            pk = tuple([ el[1] for el in table_info if el[-1] == 1 ])
            if len(pk) == 0:
                pk = (table_info[0][1], )
            self.primary_keys[table] = pk
        con.close()

    def read_db(self, table, chunk_size, entries="*"):
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        rows = list(curr.execute(f"SELECT {entries} from {table}"))
        data_chunks = [[] for _ in range((len(rows) // chunk_size))]
        for i, row in enumerate(rows):
            data_chunks[i // chunk_size].append(row)
        con.close()
        return data_chunks

    def update_columns(self, table, column, value_pairs):
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        for pk, val in value_pairs:
            curr.execute(f"UPDATE {table} SET {column} = ? WHERE {', '.join(self.primary_keys[table])} = ?", (val, pk))
        con.commit()
        con.close()

    def get_column_by_pk(self, table, column, function=lambda x: x):
        con = sqlite3.connect(self.db_file)
        curr = con.cursor()
        pks = ", ".join(self.primary_keys[table])
        column_by_pk = tuple(map(lambda key_val_pair: (key_val_pair[0], function(key_val_pair[1])), list(curr.execute(f"SELECT {f'{pks}, {column}'} from {table}"))))
        con.close()
        return column_by_pk