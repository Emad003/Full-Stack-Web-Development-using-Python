import psycopg2
hostname='localhost'
database='users'
username='postgres'
pwd='test'
port_id=5432
conn=None
try:
    conn=psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur=conn.cursor()
except Exception as error:
    print("Failed to connect to the database!")
    input()
