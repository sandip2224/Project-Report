import pyodbc

# Establish connection to the source database
source_conn_str = 'DRIVER={DriverName};SERVER=ServerName;DATABASE=SourceDB;UID=Username;PWD=Password'
source_conn = pyodbc.connect(source_conn_str)
source_cursor = source_conn.cursor()

# Execute select query to fetch data from the source table
source_cursor.execute("SELECT * FROM SourceTable")

# Establish connection to the destination database
dest_conn_str = 'DRIVER={DriverName};SERVER=ServerName;DATABASE=DestDB;UID=Username;PWD=Password'
dest_conn = pyodbc.connect(dest_conn_str)
dest_cursor = dest_conn.cursor()

# Create insert query for the destination table
dest_table_name = 'DestTable'
columns = ','.join([col[0] for col in source_cursor.description])
placeholders = ','.join(['?' for _ in range(len(source_cursor.description))])
insert_query = f"INSERT INTO {dest_table_name} ({columns}) VALUES ({placeholders})"

# Fetch data in batches and insert into the destination table
batch_size = 100
while True:
    rows = source_cursor.fetchmany(batch_size)
    if not rows:
        break
    dest_cursor.executemany(insert_query, rows)
    dest_conn.commit()

# Close connections
source_cursor.close()
source_conn.close()
dest_cursor.close()
dest_conn.close()
