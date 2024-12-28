import streamlit as st
import pandas as pd

def get_yt_title(yt_link):
    from pytube import YouTube
    yt = YouTube(yt_link)
    return yt.title

st.title('Hưng\'s karaoke song')

# Load data
# skip row index, strip white space
df = pd.read_csv('song.csv', index_col=0, skipinitialspace=True)

# Search bar
search_query = st.text_input("Search",
                             placeholder="Search for song title, singer, etc.")

# Filter data based on search query
# query on certain columns except 'karaoke' and 'perform'
query_columns = df.columns.difference(['karaoke', 'perform'])
if search_query:
    filtered_df = df[df[query_columns].apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
else:
    filtered_df = df

# Show data
st.dataframe(
        filtered_df,
        column_config={
            # 'title': st.column_config.Column(
            #     pinned=True
            #     ),
            'karaoke': st.column_config.LinkColumn(
                help='Link to karaoke video',
                max_chars=50,
                width="small",
                ),
            'perform': st.column_config.LinkColumn(
                help='Link to singer perform song',
                max_chars=50,
                width="small"
                ),
            'duet': st.column_config.CheckboxColumn(
                help='is this Duet song?',
                width="small"
                )
            },
        # hide_index=True,
        )
