
import pypyodbc




def get_db_cursor_obj(driver, server_name, database_name, user_id, password, autocommit=True):
    conn_str = f"Driver={{{driver}}};Server={server_name};Database={database_name};uid={user_id};pwd={password}"
    cnxn = pypyodbc.connect(conn_str, autocommit=True)
    return cnxn.cursor()


def get_create_table_query(tablename, cols, datatypes):
    # Ensure columns are not too long
    cols = [col[:128] for col in cols]
    
    # Pair each column with its datatype
    paired_cols = [f'"{col}" {datatype}' for col, datatype in zip(cols, datatypes)]
    
    # Create the final query string
    query = f'CREATE TABLE "{tablename}" ( ' + ', '.join(paired_cols) + ' );'
    
    print("\nCreate Table Query:\n", query)

    return query



def create_table(cursor, tablename, cols, datatypes):
    # Ensure columns are not too long
    cols = [col[:128] for col in cols]
    
    # Pair each column with its datatype
    paired_cols = [f'"{col}" {datatype}' for col, datatype in zip(cols, datatypes)]
    
    # Create the final query string
    query = f'CREATE TABLE "{tablename}" ( ' + ', '.join(paired_cols) + ' );'
    
    cursor.execute(p)
    return True


def get_tables_in_target_db(cursor):
    query = "SELECT sobjects.name FROM sysobjects sobjects WHERE sobjects.xtype = 'U'"
    cursor.execute(query)
    tables = [table[0] for table in cursor.fetchall()]
    return tables



def get_db_table_row_count(cursor, table_name):
    cursor.execute(f'SELECT count(*) FROM "{table_name}"')
    return cursor.fetchone()[0]


def get_table_row_count(cursor, table_name):
    try:
        count_query = f'SELECT count(*) FROM "{table_name}"'
        cursor.execute(count_query)
        return cursor.fetchone()[0]
    except Exception as fetch_error:
        print(f"Error fetching row count: {fetch_error}")
        raise


def generate_insert_query(target_table_name, processed_cols, computed_datatypes):
    """Generate an INSERT INTO query based on table name and columns."""
    
    # Make sure processed_cols and computed_datatypes have the same length
    if len(processed_cols) != len(computed_datatypes):
        raise ValueError("The number of columns and data types must match.")
    
    # Create the column names string for the query
    columns_str = ', '.join([f'"{col}"' for col in processed_cols])

    # Create a placeholder for each column. In standard SQL, '?' is used as a placeholder.
    # Depending on your database driver, this might be '%s' or another symbol.
    values_placeholder = ', '.join(['?'] * len(processed_cols))

    # Build the INSERT INTO query
    query = f'INSERT INTO "{target_table_name}" ({columns_str}) VALUES ({values_placeholder})'
    
    return query
'''
USAGE:

target_table_name = "example_table"
processed_cols = ["col1", "col2", "col3"]
computed_datatypes = ["INT", "TEXT", "FLOAT"]  # This isn't used in the function but is kept for consistency with the function parameters

print(generate_insert_query(target_table_name, processed_cols, computed_datatypes))


OUTPUT:

INSERT INTO "example_table" ("col1", "col2", "col3") VALUES (?, ?, ?)


'''


def delete_tables(cursor, table_names):
    """
    Delete tables from the database.

    Parameters:
    cursor: A database cursor object from an established database connection.
    table_names: A list of table names to be deleted.
    """
    for table_name in table_names:
        try:
            # Construct the SQL command
            sql_command = f"DROP TABLE IF EXISTS {table_name}"
            
            # Execute the SQL command
            cursor.execute(sql_command)
        except Exception as e:
            print(f"An error occurred while deleting {table_name}: {e}")
            # Optionally, you might want to break the loop or handle the exception differently

    # Commit the changes
    cursor.commit()





def get_existing_rows_ids(cursor, tablename, filter_by):
    """Return a set of existing row IDs (or the chosen filter field) in a given table."""
    cursor.execute(f'SELECT {filter_by} FROM "{tablename}"')
    return {str(row[0]) for row in cursor.fetchall()}

def filter_unmigrated_rows(cursor, tablename, formatted_rows, filter_by='SourceFileRowOrder', filter_col_index=-1):
    """Return the rows from formatted_rows that are not present in tablename."""
    
    # Get existing row IDs from the target table
    existing_row_ids = get_existing_rows_ids(cursor, tablename, filter_by)
    
    
    # Use the retrieved IDs to filter out rows that already exist in the target database
    unmigrated_rows = [row for row in formatted_rows if str(row[filter_col_index]) not in existing_row_ids]
    
    return unmigrated_rows


def get_table_rows(cursor, table_name):
    query = f'SELECT * FROM {table_name}'
    cursor.execute(query)
    rows = cursor.fetchall()
    return [list(row) for row in rows]


def insert_into_table(cursor, tablename, cols, row):
    """
    Insert a row of data into the specified table.
    
    :param cursor: Database cursor object.
    :param tablename: Name of the table to insert data into.
    :param cols: List of column names.
    :param row: List of values corresponding to the columns.
    """
    columns = ', '.join(cols)
    placeholders = ', '.join(['?'] * len(row))  # Use '?' for pypyodbc
    query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, tuple(row))

