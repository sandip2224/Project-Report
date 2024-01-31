import pyodbc
import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def connect_to_database(server, database, username, password):
    try:
        conn = pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}')
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None

def fetch_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tutorials")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        print(f"Error fetching data: {e}")
        return None

def create_html_table(data):
    html_table = "<table border='1'><tr>"
    # Assuming the first row contains column names
    for col in data[0].cursor_description:
        html_table += f"<th>{col[0]}</th>"
    html_table += "</tr>"
    for row in data:
        html_table += "<tr>"
        for value in row:
            html_table += f"<td>{value}</td>"
        html_table += "</tr>"
    html_table += "</table>"
    return html_table

def send_email(sender_email, receiver_email, password, smtp_server, smtp_port, html_content):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Tutorials Data"

    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

def load_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    # Load configuration from YAML file
    config = load_config('config.yaml')

    # Iterate through each database configuration
    for db_config in config['databases']:
        server = db_config['server']
        database = db_config['database']
        username = db_config['username']
        password = db_config['password']

        # Connect to the database
        conn = connect_to_database(server, database, username, password)
        if conn:
            # Perform operations on the database (e.g., execute queries)
            # Example: cursor = conn.cursor()
            # Example: cursor.execute("SELECT * FROM TableName")
            # Example: rows = cursor.fetchall()

            conn.close()


# Load configuration from YAML file
config = load_config('config.yaml')

# Database connection details
db_config = config['database']
server = db_config['server']
database = db_config['database']
username = db_config['username']
password = db_config['password']

# Email details
email_config = config['email']
sender_email = email_config['sender_email']
receiver_email = email_config['receiver_email']
email_password = email_config['email_password']
smtp_server = email_config['smtp_server']
smtp_port = email_config['smtp_port']

# Connect to the database
conn = connect_to_database(server, database, username, password)
if conn:
    # Fetch data from the database
    data = fetch_data(conn)
    if data:
        # Create HTML table
        html_table = create_html_table(data)
        # Send email
        send_email(sender_email, receiver_email, email_password, smtp_server, smtp_port, html_table)
    conn.close()
