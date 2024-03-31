import streamlit as st
from streamlit_option_menu import option_menu


st.markdown('''
<div style="text-align: center;">
    <span style="font-size:3.3em; font-weight: bold;">
        <strong>ENGLISH PREMIER LEAGUE</strong>
    </span>
</div>
''', unsafe_allow_html=True)


with st.container():
    selected = option_menu(
    menu_title = None,
    options = ['CLUB COMPARISON'],
    icons=['ball'],
    orientation="horizontal",
    styles={
        "nav-link-selected": {"background-color": "#3f4459"},
    }
    )

if selected=="CLUB COMPARISON":
    with st.container():
        import requests
        import warnings
        warnings.filterwarnings("ignore")
        url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        data_url = requests.get(url)
        html_text = data_url.text
        import pandas as pd
        table_data = pd.read_html(html_text)
        club_data1 = table_data[0].iloc[:, [1,6,7,8,11,12,13]]
        club_data2 = table_data[2].iloc[:, [0,2,3,9,14,15,18,20,21]]
        club_data2.columns = club_data2.columns.map(lambda x: x[1].split(',')[0].replace(" ", ""))
        club_data3 = table_data[4].iloc[:, [0,14]]
        club_data3.columns = club_data3.columns.map(lambda x: x[1].split(',')[0].replace(" ", ""))
        club_data4 = table_data[8].iloc[:, [0,4,5]]
        club_data4.columns = club_data4.columns.map(lambda x: x[1].split(',')[0].replace(" ", ""))
        club_data5 = table_data[10].iloc[:, [0,5]]
        club_data5.columns = club_data5.columns.map(lambda x: x[1].split(',')[0].replace(" ", ""))
        club_data = pd.merge(pd.merge(pd.merge(pd.merge(club_data1, club_data2, on='Squad'), 
                                       club_data3, on='Squad'), club_data4, on='Squad'), club_data5, on='Squad')
        squads_list = club_data['Squad'].tolist()
        metrics_list = club_data.columns[1:].tolist()

        col1,col2 = st.columns([3,3])
        with col1:
            club1 = st.selectbox('Choose Club 1',squads_list)
            color1 = st.color_picker('Choose Color 1', '#3f4459')
        with col2:
            club2 = st.selectbox('Choose Club 2',squads_list)
            color2 = st.color_picker('Choose Color 2', '#3f4459')
    selected_metrics = st.multiselect(
                'Choose The Metrics',metrics_list)
    
    st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    if st.button("Create Visualization"):
        selected_club_data = club_data[(club_data['Squad']==club1) | (club_data['Squad']==club2)].reset_index()
        metrics = ['Squad']+selected_metrics
        selected_club_data = selected_club_data[metrics]
        ranges = []
        a_values = []
        b_values = []
        for x in selected_metrics:
            a = min(selected_club_data[selected_metrics][x])
            a = a - (a*.25)
            
            b = max(selected_club_data[selected_metrics][x])
            b = b + (b*.25)
            
            ranges.append((a,b))
        for x in range(len(selected_club_data['Squad'])):
            if selected_club_data['Squad'][x] == club1:
                a_values = selected_club_data.iloc[x].values.tolist()
            if selected_club_data['Squad'][x] == club2:
                b_values = selected_club_data.iloc[x].values.tolist()

        a_values = a_values[1:]
        b_values = b_values[1:]
        values = [a_values,b_values]

        title = dict(
            title_name= club1,
            title_color = color1,
            title_name_2= club2,
            title_color_2 = color2,
            title_fontsize = 18,
            subtitle_fontsize=15
        )
        endnote = 'Soccerplots - Data via FBREF'

        from soccerplots.radar_chart import Radar
        radar = Radar(fontfamily="Arial")
        fig,ax = radar.plot_radar(ranges=ranges,params=selected_metrics,values=values,
                                radar_color=[color1,color2],
                                alphas=[.75,.6],title=title,endnote=endnote,
                                compare=True)
        st.pyplot(fig)
        
