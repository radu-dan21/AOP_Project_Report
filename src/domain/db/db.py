from playhouse.db_url import connect
from src.constants import DB_URL


db = connect(DB_URL)
db.connect()
