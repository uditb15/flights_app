# Flight Data Dashboard

## Overview

This project provides an interactive dashboard for analyzing flight data using a CSV file obtained from Kaggle containing approximately 10,000 records. The application is built with Python, utilizing MySQL for data storage, plotly for data visualization and Streamlit for the web interface. Users can filter flights based on various criteria and visualize key metrics and trends.

## Features

- **`db_creator.py`**: 
  - Automatically creates a MySQL database and table from the provided CSV file.
  
- **`dbhelper.py`**: 
  - Contains a class with methods that execute SQL queries, enabling dynamic data retrieval based on user inputs.
  
- **`app.py`**:
  - A Streamlit application that allows users to filter flights based on:
    - Departure City
    - Destination
    - Price Range (In INR)
    - Preferred Airlines

## Metrics Displayed

- Total Flights
- Unique Airlines
- Minimum Price
- Average Price
- Maximum Price

## Data Visualizations

- Pie Chart: Percentage breakdown of flights by airline.
- Time Series Chart: Number of flights over time.
- Box Plots: Price distribution by airline.
- Scatter Plot: Price vs. Departure Time by airline.

## Requirements

- Python
- MySQL
- Streamlit
- Pandas
- Plotly (for data visualizations)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Before running the application, set the following environment variables:
   ```bash
   export mysql_user='<your_mysql_username>'
   export mysql_pass='<your_mysql_password>'
   export flights_data_path='<path_to_your_csv_file>'
   ```

4. **Run the Database Creation Script**:
   Execute the `db_creator.py` script to create the database and table:
   ```bash
   python db_creator.py
   ```

5. **Launch the Streamlit App**:
   Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```