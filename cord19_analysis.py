import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========== APP TITLE ==========
st.set_page_config(page_title="Global Pulse of COVID-19 Research", layout="wide")
st.title("🌍 Global Pulse of COVID-19 Research")
st.write("Exploring the heartbeat of scientific publications from the CORD-19 dataset.")

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv", low_memory=False)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].astype(str).apply(lambda x: len(x.split()))
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ The file `metadata.csv` was not found. Please place it in this folder.")
    st.stop()

# ========== SIDEBAR FILTERS ==========
st.sidebar.header("🔍 Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
keyword = st.sidebar.text_input("Search by Keyword in Title", "")

filtered_df = df[df['year'].between(year_range[0], year_range[1])]
if keyword:
    filtered_df = filtered_df[filtered_df['title'].str.contains(keyword, case=False, na=False)]

st.sidebar.write(f"Total Results: {len(filtered_df)}")

# ========== DATA SAMPLE ==========
st.subheader("📋 Data Sample")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year', 'abstract_word_count']].head(10))

# ========== PUBLICATIONS BY YEAR ==========
st.subheader("📈 Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis", ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
ax.set_title("Number of Publications per Year")
st.pyplot(fig)

# ========== TOP JOURNALS ==========
st.subheader("🏛 Top 10 Journals")
top_journals = filtered_df['journal'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="mako", ax=ax)
ax.set_xlabel("Paper Count")
ax.set_ylabel("Journal")
ax.set_title("Top Journals Publishing COVID-19 Research")
st.pyplot(fig)

# ========== HEATMAP (YEAR vs JOURNAL) ==========
st.subheader("🔥 Heatmap: Publications by Year & Journal")
journal_year = filtered_df.groupby(['year', 'journal']).size().unstack(fill_value=0).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.heatmap(journal_year.T, cmap="YlGnBu", ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Journal")
ax.set_title("Publication Frequency Heatmap")
st.pyplot(fig)

# ========== PIE CHART: TOP SOURCES ==========
st.subheader("📊 Top Sources")
top_sources = filtered_df['source_x'].value_counts().head(5)

fig, ax = plt.subplots()
ax.pie(top_sources.values, labels=top_sources.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Top Publication Sources")
st.pyplot(fig)

# ========== ABSTRACT WORD COUNT DISTRIBUTION ==========
st.subheader("📝 Abstract Word Count Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df['abstract_word_count'], bins=30, kde=True, color='teal', ax=ax)
ax.set_xlabel("Word Count")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Abstract Word Counts")
st.pyplot(fig)

# ========== FOOTER ==========
st.success("✅ Analysis Complete — Community Knowledge Shared.")
