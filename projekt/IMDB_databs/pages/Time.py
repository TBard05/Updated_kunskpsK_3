import streamlit as st 
import pandas as pd
import sqlite3
import altair as alt

con = sqlite3.connect('projekt\IMDB_databs\IMDB.db')

# A layered line chart that shows how many movies have been released over the years from the selected country
query_movies_by_year = '''
SELECT country AS Country, date_x, COUNT(names) AS Movies
FROM IMDB
GROUP BY Country, date_x
'''
df_movies_by_year = pd.read_sql(query_movies_by_year, con)

df_movies_by_year[['day', 'month', 'year']] = df_movies_by_year['date_x'].str.split('/', n=2, expand=True)

df_movies_grouped = df_movies_by_year.groupby(['Country', 'year'])['Movies'].sum().reset_index()

countries = sorted(df_movies_grouped['Country'].unique())
specific_country1 = st.selectbox("Select a first country:", countries)
specific_country2 = st.selectbox("Select a second country:", countries)

df_country1 = df_movies_grouped[df_movies_grouped['Country'] == specific_country1]
df_country2 = df_movies_grouped[df_movies_grouped['Country'] == specific_country2]

combined_chart = alt.layer(
    alt.Chart(df_country1).mark_line(color="#6dc02a").encode(
        x=alt.X('year:O', title="Year"),
        y=alt.Y('Movies:Q', title="Number of Movies"),
        tooltip=['year', 'Movies']
    ),
    alt.Chart(df_country2).mark_line(color="#da8bbe").encode(
        x=alt.X('year:O', title="Year"),
        y=alt.Y('Movies:Q', title="Number of Movies"),
        tooltip=['year', 'Movies']
    )
).properties(
    title="First Country = Pink & Second country = Green"
)
st.altair_chart(combined_chart, use_container_width=True)

#a line-chart that reports how genres have been scored over the years
query_genres_years = '''
SELECT genre, date_x, 
AVG(score) AS avg_score
FROM IMDB
WHERE status = ' Released'
GROUP BY genre, date_x;
'''
df_genres_years = pd.read_sql(query_genres_years, con)

df_genres_years['Year'] = df_genres_years['date_x'].str.split('/').str[-1]
df_genres_years = df_genres_years[['genre', 'Year', 'avg_score']]

genre_list = df_genres_years['genre'].unique()
specific_genres = st.multiselect("Select genres to display:", genre_list, default=genre_list[:5])
# specific_genres = st.selectbox("Select genre to display", genre_list)

filtered_data = df_genres_years[df_genres_years['genre'].isin(specific_genres)]
# filtered_data = df_genres_years[df_genres_years['genre'] == specific_genres]

line_chart = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('avg_score:Q', title='Avrage Score'),
    color=alt.Color('genre:N', legend=alt.Legend(title='Genre')), 
    tooltip=['Year', 'genre','avg_score']
).properties()

st.altair_chart(line_chart, use_container_width=True)


