import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import base64

import database as db


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# --- DEMO PURPOSE ONLY --- #
placeholder = st.empty()
placeholder.info("App em teste!!")
# ------------------------- #

# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
passwords = [user["password"] for user in users]
hashed_passwords = stauth.Hasher(passwords).generate()


authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    placeholder.empty()
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Selecione o filtro:")
    selected_league = st.sidebar.selectbox('Liga', ['England', 'Germany', 'Italy', 'Spain', 'France'])

    st.sidebar.header("Season")
    selected_season = st.sidebar.selectbox('Periodo', ['2021/2022', '2020/2021', '2019/2020'])


    # WebScraping Football Data
    def load_data(league, season):

        if selected_league == 'England':
            league = 'E0'
        if selected_league == 'Germany':
            league = 'D1'
        if selected_league == 'Italy':
            league = 'I1'
        if selected_league == 'Spain':
            league = 'SP1'
        if selected_league == 'France':
            league = 'F1'

        if selected_season == '2021/2022':
            season = '2122'
        if selected_season == '2020/2021':
            season = '2021'
        if selected_season == '2019/2020':
            season = '1920'

        url = "https://www.football-data.co.uk/mmz4281/" + season + "/" + league + ".csv"
        data = pd.read_csv(url)
        return data


    df = load_data(selected_league, selected_season)

    st.subheader("Dataframe: " + selected_league)
    st.dataframe(df)


    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="Base_de_Dados.csv">Download CSV File</a>'
        return href


    st.markdown(filedownload(df), unsafe_allow_html=True)

