import sqlite3

# 🔹 SQLite Database File
db_file = "data/hydrodata.sqlite"

# Connect to SQLite Database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to Execute SQL Scripts
def execute_sql_file(filename):
    with open(filename, "r") as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    conn.commit()

# 🔹 Run Table Creation and Metadata Insertion
execute_sql_file("sql/create_tables.sql")
execute_sql_file("sql/populate_metadata.sql")

print("✅ Database and Metadata Initialized Successfully!")

# Close the Connection
conn.close()
