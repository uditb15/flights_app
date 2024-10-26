import mysql.connector
import os
import pandas as pd

class database_conn:
    def __init__(self):
        # connecting to our mysql server on local machine
        username=os.environ.get('mysql_user')
        password=os.environ.get('mysql_pass')

        # Ensure both username and password are not None
        if username is None or password is None:
            raise ValueError("Username or password not set in environment variables.")

        try:
            self.conn=mysql.connector.connect(
                host="localhost",
                user=username,
                password=password
            )
            self.mycursor=self.conn.cursor()
            print(f"Connection Established")

        except mysql.connector.Error as error:
            print("Error in Connection")
    
    def from_cities(self):
        city=[]
        self.mycursor.execute(
            """
            SELECT DISTINCT Source
            FROM flights_app.flights
            """
        )
        data=self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
        return city
    
    def to_cities(self):
        city=[]
        self.mycursor.execute(
            """
            SELECT DISTINCT Destination
            FROM flights_app.flights
            """
        )
        data=self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
        return city
    
    def fetch_stops(self):
        stops=[]
        self.mycursor.execute(
            """
            SELECT DISTINCT Total_Stops
            FROM flights_app.flights
            """
        )

        data=self.mycursor.fetchall()
        for item in data:
            stops.append(item[0])
        return stops
    
    def fetch_airline(self):
        airline=[]
        self.mycursor.execute(
            """
            SELECT DISTINCT Airline
            FROM flights_app.flights
            """
        )

        data=self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
        return airline
    
    def fetch_flights(self,source,destination,opt1,opt2,opt3):
        if isinstance(opt1, list):
            opt1 = ', '.join(["'{}'".format(x) for x in opt1])

        self.mycursor.execute(
            """
            SELECT Airline,Date_of_Journey,Source,Destination, Dep_time,Duration,Total_Stops,Price
            FROM flights_app.flights
            WHERE Source = %s AND Destination = %s AND Airline IN ({}) AND Total_Stops <= %s AND Price BETWEEN %s AND %s
            """.format(opt1),
            (source,destination, opt2,opt3[0],opt3[1])
        )
        data=self.mycursor.fetchall()
        return data
    
    def airline_frequencies(self,source,destination,opt1,opt2,opt3):
        if isinstance(opt1, list):
            opt1 = ', '.join(["'{}'".format(x) for x in opt1])  # Format for SQL

        airline=[]
        freq=[]
        self.mycursor.execute(
            """
            SELECT Airline, COUNT(*) as Frequency
            FROM flights_app.flights
            WHERE Source = %s AND Destination = %s AND Airline IN ({}) AND Total_Stops <= %s AND Price BETWEEN %s AND %s
            GROUP BY Airline
            ORDER BY Frequency DESC
            """.format(opt1),
            (source,destination, opt2,opt3[0],opt3[1])
        )
        data=self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            freq.append(item[1])
        return airline, freq

    def flights_by_date(self,source,destination,opt1,opt2,opt3):
        opt1 = ', '.join(["'{}'".format(x) for x in opt1])
        date=[]
        freq=[]
        self.mycursor.execute(
            """
            SELECT Date_of_Journey as flight_date, COUNT(*) as num_flights
            FROM flights_app.flights
            WHERE Source = %s AND Destination = %s AND Airline IN ({}) AND Total_Stops <= %s AND Price BETWEEN %s AND %s
            GROUP BY flight_date
            ORDER BY 1 DESC

            """.format(opt1),
            (source,destination, opt2,opt3[0],opt3[1])
        )
        data=self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            freq.append(item[1])
        return date, freq
        
    def make_boxplot(self,source,destination,opt1,opt2,opt3):
        opt1 = ', '.join(["'{}'".format(x) for x in opt1])
        prices=[]
        stops=[]
        airline=[]
        self.mycursor.execute(
            """
            SELECT Price, Total_Stops, Airline
            FROM flights_app.flights
             WHERE Source = %s AND Destination = %s AND Airline IN ({}) AND Total_Stops <= %s AND Price BETWEEN %s AND %s
            """.format(opt1),
            (source,destination, opt2,opt3[0],opt3[1])
        )
        data=self.mycursor.fetchall()
        prices=[item[0] for item in data]
        stops=[item[1] for item in data]
        airline=[item[2] for item in data]
        return prices,stops,airline

    def make_scatter(self,source,destination,opt1,opt2,opt3):
        opt1 = ', '.join(["'{}'".format(x) for x in opt1])
        self.mycursor.execute(
            """
            SELECT Price, HOUR(Dep_time) as dep_hour,Airline
            FROM flights_app.flights
            WHERE Source = %s AND Destination = %s AND Airline IN ({}) AND Total_Stops <= %s AND Price BETWEEN %s AND %s
            ORDER BY dep_hour
            """.format(opt1),
            (source,destination, opt2,opt3[0],opt3[1])
        )
        data=self.mycursor.fetchall()
        price=[item[0] for item in data]
        dep_hour=[item[1] for item in data]
        airline=[item[2] for item in data]

        return price,dep_hour,airline
    
    def minmax_price(self):
        self.mycursor.execute(
            """
            SELECT Price
            FROM flights_app.flights
            """
        )
        data=self.mycursor.fetchall()
        price=[float(item[0]) for item in data]
        return price