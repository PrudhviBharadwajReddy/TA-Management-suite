
from db_utils import *


db_config = {
    "Driver": "ODBC Driver 17 for SQL Server",
    "ServerName": "devdbinstance01.database.windows.net",
    "DatabaseName": "TAManagementSuite",
    "UserID": "ServerAdminPro",
    "Password": "S3cure#Adm!nPr0",
    "Encrypt": "yes",
    "TrustServerCertificate": "no",
    "ConnectionTimeout": 130
}

db_cursor = get_db_cursor_obj(db_config["Driver"],
                              db_config["ServerName"],
                              db_config["DatabaseName"],
                              db_config["UserID"],
                              db_config["Password"],
                              autocommit=True)

print(f'List of all tables in {db_config["DatabaseName"]}', get_tables_in_target_db(db_cursor))

delete_tables(db_cursor, get_tables_in_target_db(db_cursor))

print(f'List of all tables in {db_config["DatabaseName"]}', get_tables_in_target_db(db_cursor))
