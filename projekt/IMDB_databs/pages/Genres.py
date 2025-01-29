import streamlit as st 
import pandas as pd
import sqlite3
import altair as alt

con = sqlite3.connect('projekt\IMDB_databs\IMDB.db')

# Analyze the most popular genres in each country based on average rating
query_popular_genres_by_country = '''
SELECT country, genre, AVG(score) AS avg_score
FROM IMDB
GROUP BY country, genre
ORDER BY avg_score DESC
'''
df_popular_genres_by_country = pd.read_sql(query_popular_genres_by_country, con)
 
selected_country = st.selectbox("Select a country:", sorted(df_popular_genres_by_country['country'].unique()))
 
df_country_genres = df_popular_genres_by_country[df_popular_genres_by_country['country'] == selected_country]
 
bar_chart = alt.Chart(df_country_genres).mark_bar(color='magenta').encode(
    x=alt.X('avg_score:Q', title='Average Score'),
    y=alt.Y('genre:N', title='Genre', sort='-x'),
    tooltip=['genre', 'avg_score']
).properties(title=f"Popular Genres in {selected_country}")
 
st.altair_chart(bar_chart, use_container_width=True)