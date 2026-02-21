import streamlit as st
import pandas as pd
import preprocessor
import helper

athelete_df = pd.read_csv("data\\athlete_events.csv")
region_df = pd.read_csv('data\\noc_regions.csv')

df = preprocessor.preprocess(athelete_df,region_df)

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete-wise Analysis')
)

#st.dataframe(df)
st.sidebar.title('Olympics Analysis')

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years )
    selected_country = st.sidebar.selectbox('Select Country',country )

    medal_tally = helper.fetch_medal_tally(df,year=selected_year,country=selected_country)
    if selected_year =='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    elif selected_year =='Overall':
        st.title(selected_country +" Overall Peformance")
    elif selected_country =='Overall':
        st.title('Medal Tally in '+str(selected_year)+" Olympics")
    else:
        st.title(selected_country +" Peformance in "+str(selected_year))
    st.table(medal_tally)

