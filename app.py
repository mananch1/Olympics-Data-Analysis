import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Stats')
    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    
    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    
    nations_overtime = helper.data_over_time(df,'region')
    fig = px.line(nations_overtime,x='Year',y='count')
    st.title('No of nations participating over the years')
    st.plotly_chart(fig,key='regions')

    events_overtime = helper.data_over_time(df,'Event')
    fig = px.line(events_overtime,x='Year',y='count')
    st.title('No of Events participating over the years')
    st.plotly_chart(fig,key='events')

    athletes_overtime = helper.data_over_time(df,'Name')
    fig = px.line(athletes_overtime,x='Year',y='count')
    st.title('No of Athelets participating over the years')
    st.plotly_chart(fig,key='athletes')

    st.title('No of events overtime (Every Sport)')

    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Succesful Atheletes')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)