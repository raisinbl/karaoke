import streamlit as st
import pandas as pd
from pandas import DataFrame
import re
from unidecode import unidecode

def get_yt_title(yt_link):
    from pytube import YouTube
    yt = YouTube(yt_link)
    return yt.title

st.title('Hưng\'s karaoke song')

# Load data
# skip row index, strip white space
@st.cache_data
def load_data():
    return pd.read_csv('song.csv', index_col=False, skipinitialspace=True)

def normalize_vietnamese_text(text):
    """
    Chuẩn hóa text tiếng Việt: 
    - Chuyển về chữ thường
    - Loại bỏ dấu câu
    - Chuyển các ký tự có dấu về không dấu
    """
    if text is None: return None
    # Chuyển về chữ thường
    text = text.lower()
    # Loại bỏ dấu câu
    text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]', ' ', text)
    # Chuyển về không dấu
    text = unidecode(text)
    # Loại bỏ khoảng trắng thừa
    text = ' '.join(text.split())
    return text

@st.cache_data
def norm_data(df: DataFrame) -> DataFrame:
    return df.applymap(normalize_vietnamese_text)

# Search bar
search_query = st.text_input("Search",
                             placeholder="Search for song title, singer, etc.")

df = load_data()
norm_df = norm_data(df.astype(str))
# Filter data based on search query
# query on certain columns except 'karaoke' and 'perform'
query_columns = df.columns.difference(['karaoke', 'perform'])
if search_query:
    search_query = normalize_vietnamese_text(search_query)
    filtered_df = df.loc[norm_df[query_columns].apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)]
else:
    filtered_df = df

# Show data
st.dataframe(
        filtered_df.set_index('title', inplace=False),
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
