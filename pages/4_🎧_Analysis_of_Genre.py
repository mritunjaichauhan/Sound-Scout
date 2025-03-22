import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from streamlit_extras.switch_page_button import switch_page 

st.set_page_config(page_title="Analysis of Genre", page_icon="🎧",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

col1,col2=st.columns([8,1])
with col1:
    st.title("Analysis of Genre")
with col2:
    for _ in range(2):
        st.write(" ")
    if st.button("🏠"):
        switch_page("home page")
st.write("PieChart")

# Load and preprocess the dataset
df = pd.read_csv("billboard.csv")
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
df['Genres'] = df['Genre'].str.split(',')
df = df.explode('Genre')

# Flatten the list of genres
genres_list = [genre for genres in df['Genres'] for genre in genres]

# Calculate the frequency of each genre
genre_counts = pd.Series(genres_list).value_counts()

top_20_genres = genre_counts.index[:20]
top_20_counts = genre_counts[:20]

# Select top 10 genres and group the rest as "Others"
top_genres = genre_counts.head(6)
other_count = genre_counts[6:].sum()
top_genres['Others'] = other_count

# Create a Pie chart using Plotly Express
fig = px.pie(top_genres, values=top_genres.values, names=top_genres.index, title='Genre Distribution')

# Display the chart using Streamlit
st.plotly_chart(fig)
st.write(" ")
st.write("BarGraph")

# Plot a histogram of the top 20 genre counts
fig_hist = px.bar(top_20_counts, x=top_20_genres, y=top_20_counts.values,
                  labels={'x': 'Genre', 'y': 'Count'}, title='Top 20 Genres')
fig_hist.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_hist)

st.write(" ")
st.write("Analysis of a selected Genre")



# Create a dropdown menu to select the genre
selected_genre = st.selectbox("Select a genre:", genre_counts.index)

# Filter the dataset for the selected genre
genre_data = df[df['Genre'].str.contains(selected_genre)]

# Group and aggregate data at the yearly level
grouped = genre_data.groupby('Year').size().reset_index(name='Count')

# Plot the graph of genre frequency over the years
fig = px.line(grouped, x='Year', y='Count', title='Genre Count Over the Years - Selected Genre: ' + selected_genre)
st.plotly_chart(fig)


genre_count = genre_counts[selected_genre]
st.write(" ")
st.write("Count of", selected_genre, ":", genre_count)
total_count = sum(genre_counts)
st.write(" ")
st.write("Total Count of All Genres:", total_count)
