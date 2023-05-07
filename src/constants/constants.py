import os.path


DB = {
    "type": "mysql",
    "user": "root",
    "password": "root",
    "ip": "localhost",
    "port": "3306",
    "db_name": "weather",
}
DB_URL = "{type}://{user}:{password}@{ip}:{port}/{db_name}".format(**DB)

SRC_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGING_ROOT = os.path.join(SRC_ROOT, "logging")
