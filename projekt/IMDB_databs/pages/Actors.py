import streamlit as st 
import pandas as pd
import sqlite3
import altair as alt


con = sqlite3.connect('projekt\IMDB_databs\IMDB.db')

# Showing all actors and characters from the database along with the movie title and status
query = '''
SELECT crew, names AS Movies, date_x, status
FROM IMDB
'''
df = pd.read_sql(query, con)

df_exploded = df.explode('crew')

# Separating the large string of text to get two separate values
df_exploded['Actor'] = df_exploded['crew'].str.split(', ').str[0]
df_exploded['Character'] = df_exploded['crew'].str.split(', ', expand=True)[1]

df_exploded['Year'] = df_exploded['date_x'].str.split('/').str[-1]

df_exploded = df_exploded[['Actor', 'Character', 'Movies', 'status','Year']]

# Group by Actor and count the number of movies
df_grouped = df_exploded.groupby('Actor').size().reset_index(name='Num_Movies')

# Merge the grouped data with the original DataFrame
df_merged = pd.merge(df_exploded, df_grouped, on='Actor')

st.title("Actors")

actor_list = df_merged['Actor'].unique()
specific_actor = st.selectbox("Select an Actor:", actor_list)

if specific_actor:
    filtered_data = df_merged[df_merged['Actor'] == specific_actor]

    if not filtered_data.empty:
        st.subheader(f"Details for {specific_actor}")
        st.write(f"Number of movies: {filtered_data['Num_Movies'].iloc[0]}")
        st.write(filtered_data[['Actor', 'Character', 'Movies', 'status','Year']])
    else:
        st.write(f"No data found for {specific_actor}.")
else:
    st.write("Please select an actor from the dropdown.")
    
# View a list of actors who have produced the most films.
query_top_actors = '''
SELECT crew AS Actors, COUNT(names) AS movie_count
FROM IMDB
WHERE crew IS NOT NULL
GROUP BY crew
ORDER BY movie_count DESC
LIMIT 20
'''
df_top_actors = pd.read_sql(query_top_actors, con)
st.write ("## Top 10 Most used teams of actors")
 
bar_chart_directors = alt.Chart(df_top_actors).mark_bar(color='green').encode(
    x=alt.X('movie_count:Q', title='Number of Movies'),
    y=alt.Y('Actors:N', title='Actors', sort='-x'),
    tooltip=['Actors', 'movie_count']
).properties()
 
st.altair_chart(bar_chart_directors, use_container_width=True)



















