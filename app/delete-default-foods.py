import sqlite3

conn = sqlite3.connect("/home/oskar/Documents/apps/macrotrack/app/db/app_database.db")
conn.execute("DELETE FROM user_food WHERE id <= 487")
conn.commit()
conn.close()
print("Deleted all user_food rows with id <= 487.")