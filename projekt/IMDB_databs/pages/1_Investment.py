import streamlit as st 
import pandas as pd
import sqlite3
import altair as alt

con = sqlite3.connect('projekt\IMDB_databs\IMDB.db')

st.title("Investments for each Country")
# Highest and lowest budget and revenue comparison section
query_best_worst_investment = '''
SELECT names AS Movies, revenue, status ,budget_x, date_x AS Date, country AS Country 
FROM IMDB 
WHERE status = ' Released'
'''
df_best_worst_investment = pd.read_sql(query_best_worst_investment, con)

df_best_worst_investment['Difference'] = df_best_worst_investment['revenue'] - df_best_worst_investment['budget_x']
df_best_worst_investment = df_best_worst_investment[['Movies', 'Difference','Country', 'Date']]

st.write("### Best and worst movie investments for each country")

countries = sorted(df_best_worst_investment['Country'].unique())
specific_country = st.selectbox("Select a country:", countries)

df_country = df_best_worst_investment[df_best_worst_investment['Country'] == specific_country]

if not df_country.empty:
    max_difference = df_country.loc[df_country['Difference'].idxmax()]
    min_difference = df_country.loc[df_country['Difference'].idxmin()]

    col1, col2 = st.columns(2)
    
    with col1: 
        st.write(f"##### Best Investment in {specific_country}")
        st.write(max_difference)

    with col2: 
        st.write(f"##### Worst Investment in {specific_country}")
        st.write(min_difference)
else:
    st.write("No data available for the selected country.") 
    
    
# Worst flops and greatest achievements for each country
st.write("### Revenue & Budget for the selected genre")

# 10 highest and lowest Budget
query_budget_asc = '''
SELECT names, budget_x, genre, status 
FROM IMDB 
WHERE status = ' Released'
ORDER BY budget_x ASC;'''

query_budget_desc = '''
SELECT names, budget_x, genre, status 
FROM IMDB 
WHERE status = ' Released'
ORDER BY budget_x DESC;'''

df_budget_asc_10 = pd.read_sql(query_budget_asc, con)
df_budget_desc_10 = pd.read_sql(query_budget_desc, con)

# puts together all and budget data so that it becomes easier to manage
df_budget_asc_desc_20 = pd.concat([df_budget_asc_10, df_budget_desc_10])

# 10 highest and lowest revenue
query_revenue_asc_10 = '''
SELECT names, revenue, genre, status 
FROM IMDB 
WHERE status = ' Released'
ORDER BY revenue ASC;'''

query_revenue_desc_10 = '''
SELECT names, revenue, genre, status 
FROM IMDB 
WHERE status = ' Released'
ORDER BY revenue DESC;'''

df_revenue_asc_10 = pd.read_sql(query_revenue_asc_10, con)
df_revenue_desc_10 = pd.read_sql(query_revenue_desc_10, con)

# puts together all and revenue data so that it becomes easier to manage
df_revenue_asc_desc_20 = pd.concat([df_revenue_asc_10, df_revenue_desc_10])

genres = df_budget_asc_desc_20['genre'].unique()
specific_genres = st.selectbox("Select a Genre:", genres)

df_genres_budget = df_budget_asc_desc_20[df_budget_asc_desc_20['genre'] == specific_genres]
df_genres_revenue = df_revenue_asc_desc_20[df_revenue_asc_desc_20['genre'] == specific_genres]

budget_chart = alt.Chart(df_genres_budget).mark_bar(opacity=0.5, color='green').encode(
    x=alt.X('budget_x:Q', title='Budget = Green'),
    y=alt.Y('names:N', title='Movies', sort='-x'))

revenue_chart = alt.Chart(df_genres_revenue).mark_bar(opacity=0.4, color='purple').encode(
    x=alt.X('revenue:Q', title='Revenue = Purple'),
    y=alt.Y('names:N', title='Movies', sort='-x'))

chart_budget_revenue = alt.layer(budget_chart, revenue_chart).resolve_scale(
    x='independent')

st.altair_chart(chart_budget_revenue, use_container_width=True)

# top five movies that has the highest roi(return on investment)
query_roi = '''
SELECT names AS Movies, budget_x AS Budget, status ,revenue AS Revenue, (Revenue - budget_x) * 1.0 / budget_x AS ROI
FROM IMDB
WHERE budget_x > 0 AND revenue > 0
ORDER BY roi DESC
LIMIT 5
'''
df_roi = pd.read_sql(query_roi, con)
 
st.write("### Top 5 movies with highest ROI")
st.write(df_roi)

# Show the correlation between the film's budget and average ratingst
query_budget_score_corr = '''
SELECT budget_x, score
FROM IMDB
WHERE budget_x IS NOT NULL AND score IS NOT NULL
'''
df_budget_score_corr = pd.read_sql(query_budget_score_corr, con)
 
scatter_chart_corr = alt.Chart(df_budget_score_corr).mark_circle(size=60).encode(
    x=alt.X('budget_x:Q', title='Budget'),
    y=alt.Y('score:Q', title='Score'),
    tooltip=['budget_x', 'score']
).properties()
st.altair_chart(scatter_chart_corr, use_container_width=True)
 

# Show a distribution of budgets and earnings for movies in a scatter plot
query_budget_revenue_scatter = '''
SELECT names, budget_x, revenue, genre
FROM IMDB
WHERE budget_x IS NOT NULL AND revenue IS NOT NULL
'''
df_budget_revenue_scatter = pd.read_sql(query_budget_revenue_scatter, con)
 
scatter_chart = alt.Chart(df_budget_revenue_scatter).mark_circle(size=60).encode(
    x=alt.X('budget_x:Q', title='Budget'),
    y=alt.Y('revenue:Q', title='Revenue'),
    color=alt.Color('genre:N', title='Genre'),
    tooltip=['names', 'budget_x', 'revenue', 'genre']
).properties(title="Budget vs Revenue for Movies")
 
st.altair_chart(scatter_chart, use_container_width=True)

# Movie count for each country and average score on those movies 
query_movie_count_countreis = '''
SELECT country, 
COUNT(names) AS movie_count, 
AVG(score) AS avg_score 
FROM IMDB 
GROUP BY country
'''
df_movie_count_countreis = pd.read_sql(query_movie_count_countreis, con)

# A comparison between countries for average score, movie count, and how much profit has been made
query_all_profit_all_movies = '''
SELECT budget_x, revenue, names, country, date_x 
FROM IMDB 
GROUP BY country
'''
df_all_profit_all_movies = pd.read_sql(query_all_profit_all_movies, con)

df_all_profit_all_movies['difference'] = df_all_profit_all_movies['revenue'] - df_all_profit_all_movies['budget_x']
df_profit = df_all_profit_all_movies[['names', 'difference', 'country', 'date_x']]

st.write("### Movie count and average score by country")

country_list = df_movie_count_countreis['country'].unique()
country1 = st.selectbox("Select first country:", country_list)
country2 = st.selectbox("Select second country:", country_list)

data_country1 = df_movie_count_countreis[df_movie_count_countreis['country'] == country1]
data_country2 = df_movie_count_countreis[df_movie_count_countreis['country'] == country2]

profit_country1 = df_profit[df_profit['country'] == country1]
profit_country2 = df_profit[df_profit['country'] == country2]

if not data_country1.empty:
    movie_count1 = data_country1['movie_count'].values[0]
    avg_score1 = data_country1['avg_score'].values[0]
    total_profit1 = profit_country1['difference'].sum()
    st.write(f"Country 1: {country1}, Number of Movies: {movie_count1} , Average Score: {avg_score1:.2f} , Total Profit/Loss: {total_profit1:.2f}")
    
if not data_country2.empty:
    movie_count2 = data_country2['movie_count'].values[0]
    avg_score2 = data_country2['avg_score'].values[0]
    total_profit2 = profit_country2['difference'].sum()
    st.write(f"Country 2: {country2} , Number of Movies: {movie_count2} , Average Score: {avg_score2:.2f} , Total Profit/Loss: {total_profit2:.2f}")

avg_score_chart = alt.Chart(pd.concat([data_country1, data_country2])).mark_bar(opacity=0.7, color=('green') ).encode(
    x=alt.X('avg_score:Q', title='Average Score'),
    y=alt.Y('country:N', title='Country'),
).properties(title="Average Score by Country")

movie_count_chart = alt.Chart(pd.concat([data_country1, data_country2])).mark_bar(opacity=0.7, color=('pink')).encode(
    x=alt.X('movie_count:Q', title='Number of Movies'),
    y=alt.Y('country:N', title='Country'),
).properties(title="Number of Movies by Country")

profit_chart = alt.Chart(pd.concat([profit_country1, profit_country2])).mark_bar(opacity=0.7, color=('purple')).encode(
    x=alt.X('difference:Q', title='Profit/Loss'),
    y=alt.Y('country:N', title='Country'),
).properties(title="Profit/Loss by Country")

st.altair_chart(avg_score_chart, use_container_width=True)
st.altair_chart(movie_count_chart, use_container_width=True)
st.altair_chart(profit_chart, use_container_width=True)
