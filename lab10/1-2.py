import psycopg2

# Парольсіз қосылу
conn = psycopg2.connect(
    host="localhost",
    database="PhoneBook",
    user="qurmanbek"  
)

cur = conn.cursor()
cur.execute("SELECT * FROM contacts")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
