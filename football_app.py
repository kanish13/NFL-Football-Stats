import streamlit as st
import pandas as pd
import base64

st.title('NFL Football Stats')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2020))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm

@st.cache_data
def load_data(year):
    try:
        url = f"https://www.pro-football-reference.com/years/{year}/rushing.htm"
        html = pd.read_html(url, header=1)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        return playerstats
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

playerstats = load_data(selected_year)

# Sidebar - Team selection
if not playerstats.empty:
    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)
else:
    selected_team = []

# Sidebar - Position selection
unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
if not df_selected_team.empty:
    st.write(f'Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
    st.dataframe(df_selected_team)
else:
    st.write('No data available for the selected team(s) and position(s).')

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings - bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

if not df_selected_team.empty:
    st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
