import streamlit as st
from dbhelper import database_conn
import mysql.connector
import plotly.express as px
import pandas as pd
import numpy as np

db=database_conn()
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
from_cities=db.from_cities()
to_cities=db.to_cities()
airlines=db.fetch_airline()
stops=db.fetch_stops()
prices=db.minmax_price()

source=st.sidebar.selectbox('From',sorted(from_cities))
destination=st.sidebar.selectbox('Destination',sorted(to_cities))
opt1=st.sidebar.multiselect("Select Airline",sorted(airlines),  default=['Air India'])
opt2=st.sidebar.selectbox("Maximum Stops", sorted(stops), placeholder="Choose Stops")
opt3=st.sidebar.slider("Select Price Range",min_value=np.round(min(prices),0), max_value=np.round(max(prices),0), 
value=(np.round(min(prices),0), np.round(max(prices),0)))

data=db.fetch_flights(source, destination,opt1,opt2,opt3)
list_data=[]
for item in data:
        new={
        "Airline": item[0],
        "Date": item[1],
        "From": item[2],
        "Destination": item[3],
        "Dep_time": item[4],
        "Duration": item[5],
        "Total_Stops": item[6],
        "Price": item[7]
        }
        list_data.append(new)
all_df=pd.DataFrame(list_data)

st.title('Welcome to the Flights Database Application:blue')

if all_df.shape[0]==0:
        st.write("The Query Yielded No Results. Try to Enter Different Search Paramers")
else:
    col1, col2, col3, col4,col5 = st.columns(5)
    unique_airlines = all_df['Airline'].nunique()
    avg_price=np.round(all_df['Price'].mean(),1)
    min_price=all_df['Price'].astype("float").min()
    max_price=all_df['Price'].astype("float").max()

    num_flights=all_df.shape[0]
    col2.metric("Unique Airlines",unique_airlines)
    col4.metric("Average Price", avg_price)
    col3.metric("Minimum Price", min_price)
    col1.metric("Total Flights",num_flights)
    col5.metric("Maximum Price", max_price)

with st.expander("Click Here to Review Results"):
        st.dataframe(all_df,use_container_width=True)

airline,freq=db.airline_frequencies(source,destination,opt1,opt2,opt3)
df=pd.DataFrame(
    {
        'Airline': airline,
        'Num_flights': freq     
    }
)
if df.empty:
       st.write('No Flights')
else:
    fig = px.pie(
            df,names='Airline',
            values="Num_flights",
            title='Flights by Airline')
    fig.update_layout(width=1000, height=600,legend=dict(xanchor='center',yanchor='top'),
                        title=dict(
            text='Flights by Airline',
            font=dict(size=32),
            x=0.5,               
            xanchor='center'    
        ))
    st.plotly_chart(fig)

## busy airport

# Flights by day
days,freq=db.flights_by_date(source,destination,opt1,opt2,opt3)
df=pd.DataFrame(
    {
        'Day': days,
        'Num_Flights': freq
    }
)
fig3 = px.line(df,
                x='Day', y='Num_Flights',title='Flights by Date',width=500)
fig3.update_layout(width=1200, height=600, title=dict(
        text='Flights by Date',
        font=dict(size=32),
        x=0.5,               
        xanchor='center'    
    ))
fig3.update_traces(line=dict(width=2))
st.plotly_chart(fig3)

# Price Box Plot
prices,stops,airline=db.make_boxplot(source,destination,opt1,opt2,opt3)
df=pd.DataFrame(
    {
        "Price":prices,
        "Stops":stops,
        "airline":airline
    }
        )
fig4 = px.box(df, y='Price', title='Price Box Plot',color="airline")
fig4.update_layout(width=1200, height=600,title=dict(
        text='Price Distribution by Airline',
        font=dict(size=32),
        x=0.5,               
        xanchor='center'    
    ))
st.plotly_chart(fig4)

# Scatter Plot
price,dep_hour,airline=db.make_scatter(source,destination,opt1,opt2,opt3)
df=pd.DataFrame(
       {"price":price,
        'dep_hour':dep_hour,
        'airline':airline
        
        }
        )
fig5 = px.scatter(df, x='dep_hour',y='price',color='airline')
fig5.update_layout(
    xaxis_title='Departure Hour',
    width=1200, height=600,
    title=dict(
    text='Price vs Departure Time by Airline',
    font=dict(size=32),
    x=0.5, xanchor='center'    
    )
    )
st.plotly_chart(fig5)