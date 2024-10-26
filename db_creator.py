import mysql.connector
import os
import csv

# connecting to our mysql server on local machine
username = os.environ.get('mysql_user')
password = os.environ.get('mysql_pass')

# Ensure both username and password are not None
if username is None or password is None:
    raise ValueError("Username or password not set in environment variables.")

try:
    conn=mysql.connector.connect(
        host="localhost",
        user=username,
        password=password
    )
    mycursor=conn.cursor()
    print(f"Connected to MySQL Server")

except mysql.connector.Error as error:
    print(error)

# Creating a database named "flights_app" if it doesn't exist
try:
    mycursor.execute("CREATE DATABASE IF NOT EXISTS flights_app;")
    conn.commit()
    print("Database created")
    mycursor.execute("USE flights_app;")
    print("Using database flights_app")
except Exception as e:
    print(e)

# Creating a table flights to load all data
try:
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INT AUTO_INCREMENT PRIMARY KEY,
            Airline VARCHAR(100),
            Date_of_Journey DATE,
            Source VARCHAR(100),
            Destination VARCHAR(100),
            Route VARCHAR(255),
            Dep_Time VARCHAR(10),  -- Changed to VARCHAR
            Duration VARCHAR(100),
            Total_Stops INT,
            Price DECIMAL(10, 2)
        );
    """)
    conn.commit()
    print("Table 'flights' created")
except Exception as e:
    print(e)


# Inserting data from a csv file into our flights table
def data_from_csv(csv_path:str):
    try:
        with open(csv_path, mode='r') as file:
            reader = csv.DictReader(file)  # Read the CSV into a dictionary format
            for row in reader:
                # Extract data from the row
                airline = row['Airline']
                date_of_journey = row['Date_of_Journey']
                source = row['Source']
                destination = row['Destination']
                route = row['Route']
                dep_time = row['Dep_Time']  # This will now be text
                duration = row['Duration']
                total_stops_str = row['Total_Stops']
                if total_stops_str.lower() == "non stops":
                    total_stops = 0  # Set to 0 for "non stops"
                else:
                    try:
                        total_stops = int(total_stops_str.split()[0])  # Get the first part before the space and convert to int
                    except (ValueError, IndexError):
                        total_stops = 0  # Default value or handle as needed

                price = row['Price']
                
                # Insert into the flights table
                sql = """
                    INSERT INTO flights (Airline, Date_of_Journey, Source, Destination, Route, Dep_Time, Duration, Total_Stops, Price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                mycursor.execute(sql, 
                                 (airline, date_of_journey, source, destination, route, dep_time, duration, total_stops, price))
        
        conn.commit()  # Commit the transaction
        print("Data inserted from CSV into 'flights'")

    except Exception as e:
        print(e)

# Call the function with the path to your CSV file
data_from_csv(os.environ.get("flights_data_path"))