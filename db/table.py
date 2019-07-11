import sqlite3


class Table():
    '''
        Table class for making tables in the database and interaction.
    '''

    def __init__(self, table_name, db_name="cross.db"):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = self.connect()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def exists(self) -> bool:
        '''
            Returns true if table exists in the database
        '''
        cursor = self.conn.cursor()

        cursor.execute(
            '''SELECT count(name) FROM sqlite_master
               WHERE type='table' AND name='{}';'''
            .format(self.table_name))

        return cursor.fetchone()[0] == 1

    def init_table(self, columns) -> None:
        '''
            Create table using the given columns.
            If table exists then adds columns not present in th table which are
            provided.
        '''
        if self.exists():
            update = self._diff(columns)
            if update:
                self.add_columns(update)
                print("updated")
            return

        columns = ["{} TEXT".format(col) for col in columns]

        statement = '''CREATE TABLE IF NOT EXISTS {} ('''.format(
            self.table_name)

        statement += ", ".join(columns)
        statement += ");"

        cursor = self.conn.cursor()
        cursor.execute(statement)

        self.commit()
        print("Table created!")

    def insert_row(self, row: dict, force=False) -> bool:
        '''
            Insert row in table. If the row exists and force is False
            does not add the row. A row is identified by its ID attribute (Primary Key).
            It is not explicitly defined as a primary key but it acts like one.
        '''

        id_ = row.get("id", None)

        if id_ is None:
            raise AttributeError("ID field is")

        if not force:
            if self.find_by_id(id_):
                print("found")
                return False

        statement = f'''INSERT INTO {self.table_name}('''

        cols = self._get_column_names()

        column_statement = ""
        value_statement = "VALUES("

        for col in cols:
            column_statement += f"{col}, "

            # if field is empty adds dashes instead
            val = row.get(col, "---").strip()

            if not len(val):
                val = "---"

            value_statement += f"'{val}', "

        column_statement = column_statement.rstrip(", ")
        value_statement = value_statement.rstrip(", ")

        column_statement += ")"
        value_statement += ")"

        # SQL statement to add column
        statement += column_statement + " "
        statement += value_statement

        self.conn.cursor().execute(statement)
        self.commit()

        return True

    def find_by_id(self, id_=None, many=False):
        '''
            Finds a row in the table by the given ID. if id is none
            return all the rows. If many exists with the same ID, many param must be True
            else returns only the first row.
        '''

        if id_ is None:
            statement = f'''SELECT * FROM {self.table_name}'''

            cursor = self.conn.cursor()
            cursor.execute(statement)

            return cursor.fetchall()

        statement = f'''SELECT * FROM {self.table_name} WHERE ID='{id_}';'''
        cursor = self.conn.cursor()
        cursor.execute(statement)

        if many:
            # In distributed table the ID attribute repesents
            # distribution ID and has multiple rows. Hence this
            # workaround is required instead of using a Composite Key attribute.
            res = cursor.fetchall()
        else:
            res = cursor.fetchone()

        return res

    def delete_by_id(self, id_=None):
        '''
            Deletes row identified by the ID.
            If ID is none deletes all
        '''
        cursor = self.conn.cursor()
        if id_ is None:
            cursor.execute(f"delete from {self.table_name}")
            return True
        cursor.execute(f"DELETE FROM {self.table_name} WHERE id='{id_}'")

        self.commit()

        return True

    def _get_column_names(self) -> list:

        cursor = self.conn.cursor()

        cursor = cursor.execute("select * from " + self.table_name)
        names = list(map(lambda x: x[0], cursor.description))

        return names

    def _diff(self, columns) -> list:
        '''
            returns columns present in the columns parameter and
            not in the database
        '''
        in_table = self._get_column_names()
        d = list(set(columns) - set(in_table))

        return d

    def execute(self, statement: str):
        '''
            Executes a raw statement as provided
        '''
        cursor = self.conn.cursor()
        cursor.execute(statement)

        self.commit()

        if "SELECT" in statement.upper():
            return cursor.fetchall()

    def add_columns(self, columns) -> None:
        '''
            Adds given columns to the table
        '''
        columns = ["{} TEXT".format(col) for col in columns]

        for col in columns:
            statement = '''ALTER TABLE {} ADD COLUMN {}'''.format(
                self.table_name, col)
            cursor = self.conn.cursor()
            cursor.execute(statement)

        self.commit()

    def drop(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE " + self.table_name)
        self.commit()

    def __del__(self):
        self.close()

    def close(self) -> None:
        self.conn.close()

    def commit(self):
        self.conn.commit()
