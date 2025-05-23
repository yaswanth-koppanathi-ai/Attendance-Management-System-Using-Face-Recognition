from db_util import AttendanceDB

db = AttendanceDB(
    host="localhost",
    user="root",
    password="Yashu@2432",
    database="attendance_db"
)

print("🚀 Connecting to database...")
db.connect()
print("✅ Connected successfully!")

print("🛠 Creating table...")
db.create_table()
print("✅ Table created successfully!")

db.close()
print("🔒 Connection closed.")
