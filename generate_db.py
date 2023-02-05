import os

from app.database import create_db_and_tables
from app.db_function import create_products_type_from_propulate_db, create_user_test


# Remove SQLite DB
sqlite_db: str = "database.db"
# If file exists, delete it.
if os.path.isfile(sqlite_db):
    os.remove(sqlite_db)

# Create DB
create_db_and_tables()

# Populate DB
create_products_type_from_propulate_db()

# Create user test
create_user_test()

print("DB successfully reset")
print(f"Create user test: 'username'='maistodos' 'password'='maistodos")
print("Authentication through Basic Auth")
