# Streamlit CORD-19 Explorer
# Author: [Your Name]
# Date: 2025-09-19

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# ================================
# Load Data
# ================================
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv", low_memory=False)
    df = df[['title', 'abstract', 'publish_time', 'journal', 'authors', 'source_x']]
    df['title'] = df['title'].fillna("No Title")
    df['abstract'] = df['abstract'].fillna("No Abstract")
    df['journal'] = df['journal'].fillna("Unknown Journal")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df = df.dropna(subset=['publish_time'])
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# ================================
# Streamlit Layout
# ================================
st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers (CORD-19 metadata)")

# Data Preview
if st.checkbox("Show raw data"):
    st.dataframe(df.head(20))

# Year Range Filter
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select year range:", year_min, year_max, (2020, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Publications Over Time
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
year_counts.plot(kind="bar", color="skyblue", ax=ax)
ax.set_title("Publications by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
top_journals.plot(kind="bar", color="orange", ax=ax)
ax.set_title("Top 10 Journals")
ax.set_xlabel("Journal")
ax.set_ylabel("Count")
st.pyplot(fig)

# Word Cloud
st.subheader("Word Cloud of Titles")
all_titles = " ".join(filtered['title'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_titles)
fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Source Distribution
st.subheader("Top Sources")
fig, ax = plt.subplots()
filtered['source_x'].value_counts().head(10).plot(kind="bar", color="green", ax=ax)
ax.set_title("Top Sources")
ax.set_xlabel("Source")
ax.set_ylabel("Count")
st.pyplot(fig)
