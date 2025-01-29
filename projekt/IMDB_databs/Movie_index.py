import pandas as pd
import numpy as np
import sqlite3
import streamlit as st

con = sqlite3.connect('projekt\IMDB_databs\IMDB.db')

# Think it good tho show the viever the data we have to offer 
query_data = '''
SELECT names AS Movies, genre AS Genre, status ,date_x AS Date, score AS Score, country AS Country 
FROM IMDB
'''
df_data = pd.read_sql(query_data, con)

# Showing all the movies in post-production or in production for easier access
query_status_check = '''
SELECT names AS Movies, genre AS Genre, status ,date_x AS Date, score AS Score, country AS Country 
FROM IMDB
WHERE status IN (' In Production', ' Post Production');
'''
df_st_check = pd.read_sql(query_status_check, con)

df_data_index = df_data[['Movies', 'Genre', 'Date', 'Score', 'status', 'Country']]
st.write("## All the movies we have in the database")
st.write(df_data_index)

st.write('## Know your movie?')
movies = df_data_index['Movies'].unique()
specific_movie = st.selectbox("Select a movie title:", movies)

if specific_movie:
    filtered_data = df_data_index[df_data_index['Movies'] == specific_movie]

    if not filtered_data.empty:
        st.write(f"Details for {specific_movie}")
        st.write(filtered_data[['Genre', 'Date', 'Score', 'status', 'Country']])
    else:
        st.write(f"No data found for {specific_movie}.")
else:
    st.write("Please select an actor from the dropdown.")
    
    
# Unreleased movies    
st.write('## All movies in post production or in production')

df_status_check = df_st_check[['Movies', 'Genre', 'Date', 'Score', 'status', 'Country']]
st.write(df_status_check)