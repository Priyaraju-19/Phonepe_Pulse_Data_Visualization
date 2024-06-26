import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import json
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open(r"/Users/padhmapriya/Downloads/ICN.png")
st.set_page_config(page_title="Phonepe Pulse Data Visualization",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created by *Padhma Priya*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

# Creating connection with MySQL workbench
mydb = sql.connect(host="127.0.0.1",
                   user="root",
                   password="12345",
                   database="phonepe_pulse",
                   port="3307")
mycursor = mydb.cursor(buffered=True)

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Top Charts", "Explore Data", "About"], 
                           icons=["house", "graph-up-arrow", "bar-chart-line", "exclamation-circle"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain:] Fintech")
        st.markdown("### :violet[Technologies used:] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview:] In this Streamlit web app, you can visualize the PhonePe Pulse data and gain a lot of insights on transactions, number of users, top 10 states, districts, pin codes, and which brand has the most number of users, and so on. Bar charts, Pie charts, and Geo map visualizations are used to get some insights.")

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1, 1.5], gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
            """
            #### From this menu we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """, icon="🔍"
        )

    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT state, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"SELECT district, SUM(Count) AS Total_Count, SUM(Amount) AS Total FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT pincode, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM top_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY pincode ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
    # Top Charts - USERS          
    if Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry, no data to display for 2022 Qtr 2, 3, 4")
            else:
                mycursor.execute(f"SELECT brands, SUM(count) AS Total_Count, AVG(percentage)*100 AS Avg_Percentage FROM agg_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY brands ORDER BY Total_Count DESC LIMIT 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)
    
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"SELECT district, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_Appopens FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)
