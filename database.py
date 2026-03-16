import mysql.connector

db = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="srms"
)

cursor = db.cursor(buffered=True)
