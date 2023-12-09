import pyodbc
import json

class DatabaseManager:
    def __init__(self, config_file):
        with open(config_file, 'r') as json_file:
            config = json.load(json_file)
        
        self.conn_str = (
            f"Driver={config['Driver']};"
            f"Server=tcp:{config['ServerName']},1433;"
            f"Database={config['DatabaseName']};"
            f"Uid={config['UserID']};"
            f"Pwd={config['Password']};"
            f"Encrypt={config['Encrypt']};"
            f"TrustServerCertificate={config['TrustServerCertificate']};"
            f"Connection Timeout={config['ConnectionTimeout']};"
        )

    def get_conn_obj(self):
        conn = pyodbc.connect(self.conn_str)
        return conn

    def create_tables(self, sql_file):
        conn = self.get_conn_obj()
        cursor = conn.cursor()

        with open(sql_file, 'r') as file:
            sql_script = file.read()

        # Split the script into individual statements (assuming each statement ends with a semicolon)
        sql_commands = sql_script.split(';')

        for command in sql_commands:
            # Execute each command from the input file
            if command.strip():
                cursor.execute(command)
        
        conn.commit()
        cursor.close()
        conn.close()

db = DatabaseManager('config/db_config.json')
db.create_tables('db_schema.sql')
