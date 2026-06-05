from database import conn, cursor

cursor.execute("""
INSERT INTO users(username,email,password)
VALUES(?,?,?)
""", (
    "admin",
    "admin@gmail.com",
    "1234"
))

conn.commit()

print("User Added Successfully")