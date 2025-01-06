import streamlit as st
import pandas as pd
from pandas import DataFrame
import re
from unidecode import unidecode

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
    return df.map(normalize_vietnamese_text)

# Search bar
# Chia làm 2 ô search theo chiều ngang
col1, col2 = st.columns(2)
with col1:
    search_title_query = st.text_input("Search Title",
                                       placeholder="Search for song title, singer, etc.")
with col2:
    search_theme_query = st.text_input("Search Theme",
                                       placeholder="Search for song theme, tempo, mood, etc.")

df = load_data()
norm_df = norm_data(df.astype(str))
# Filter data based on search query
# query on certain columns except 'karaoke' and 'perform'
# query các thông tin dễ thấy nhất(thường để trên title một bài hát)
query_title_columns = ['title', 'singer(s)', 'songwriter(s)']
if search_title_query:
    search_title_query = normalize_vietnamese_text(search_title_query)
    filtered_df = df.loc[norm_df[query_title_columns].apply(lambda row: row.str.contains(search_title_query, case=False).any(), axis=1)]
else:
    filtered_df = df
# query on theme, tempo, mood
query_theme_columns = ['theme', 'tempo', 'mood']
if search_theme_query:
    search_theme_query = normalize_vietnamese_text(search_theme_query)
    filtered_df = filtered_df.loc[norm_df[query_theme_columns].apply(lambda row: row.str.contains(search_theme_query, case=False).any(), axis=1)]

# Show data
st.data_editor(
        # st dataframe chỉ cho pin index
        filtered_df.set_index('title'),
        column_config={
            # 'title': st.column_config.Column(
            #     pinned=True
            #     ),
            'karaoke': st.column_config.LinkColumn(
                help='Link to karaoke video',
                width="small",
                ),
            'perform': st.column_config.LinkColumn(
                help='Link to singer perform song',
                width="small"
                ),
            'duet': st.column_config.SelectboxColumn(
                help='is this Duet song?',
                width="small",
                options=['xx','xy', 'yy', None]
                ),
            'theme': st.column_config.SelectboxColumn(
                help='chủ đề bài hát',
                width="small",
                options=['tet', 'wedding', 'love']
                ),
            'tempo': st.column_config.SelectboxColumn(
                help='tiết tấu bài hát',
                width="small",
                options=['slow', 'medium', 'fast']
                ),
            'mood': st.column_config.SelectboxColumn(
                help='tâm trạng bài',
                width="small",
                options=["happy", "sad", "love"]
                ),
            },
        num_rows='dynamic'
        # hide_index=True,
        )
