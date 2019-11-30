import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = 'Dash app with pure Altair HTML'

alt.data_transformers.disable_max_rows()

df = pd.read_csv("https://raw.githubusercontent.com/UBC-MDS/DSCI_532_L02_group206_ms1/master/data/cleaned_acc_data.csv")

# Preprocessing
df['intake_year'] = pd.DatetimeIndex(df['intake_monthyear']).year
df['outake_year'] = pd.DatetimeIndex(df['outcome_monthyear']).year

# Plot 1
data_new = df.groupby(by = "intake_monthyear").agg({"animal_type":"count"}).reset_index()
data_new.columns = ["intake_monthyear","count"]
data_new["Type"] = "Intake"
data_new['intake_year'] = pd.DatetimeIndex(data_new['intake_monthyear']).year

data_new1 = df.groupby(by = "outcome_monthyear").agg({"animal_type":"count"}).reset_index()
data_new1.columns = ["outcome_monthyear","count"]
data_new1["Type"] = "Outake"
data_new1['outake_year'] = pd.DatetimeIndex(data_new1['outcome_monthyear']).year

# Plot 2
data_new2 = df.groupby(by = ["intake_year","animal_type","intake_weekday"]).agg({"breed":"count"}).reset_index()
data_new2.columns = ["intake_year","animal_type","intake_weekday","count"]
#data_new2['intake_year'] = pd.DatetimeIndex(data_new2['intake_monthyear']).year
# print (data_new2.head())

# Plot 3
data_new3 = df.groupby(by = ["outake_year","animal_type","outcome_weekday"]).agg({"breed":"count"}).reset_index()
data_new3.columns = ["outake_year","animal_type","outcome_weekday","count"]
#data_new3['outake_year'] = pd.DatetimeIndex(data_new3['outcome_monthyear']).year
# print (data_new3.head())

# Plot 4
data_new4 = df[["intake_year","animal_type", "age_upon_intake_(days)"]].copy()
data_new4["age"] = round(df["age_upon_intake_(days)"]/365,0)
data_new4 = data_new4.drop("age_upon_intake_(days)", axis = 1)

# Plot 5
data_new5 = df[["intake_year","animal_type","intake_condition", "total_time_in_shelter_days"]].copy()
data_new5.rename(columns={'total_time_in_shelter_days':'Days in Shelter'}, inplace = True)

######### Create plotting functions ##########

def make_plot_1(year_range = [2013,2016]):

    
    data_new_filter = data_new[((data_new['intake_year'] >= year_range[0]) & (data_new['intake_year'] <= year_range[1]))]
    chart = alt.Chart(data_new_filter).mark_line().encode(
        alt.X("yearmonth(intake_monthyear):O", title = "Time (Month-Year)"),
        alt.Y('count', title="Count"),
        alt.Color("Type")
        )
    data_new_filter1 = data_new1[data_new1['outcome_monthyear'] != "2018-04"]
    data_new_filter1 = data_new_filter1[((data_new_filter1['outake_year'] >= year_range[0]) & (data_new_filter1['outake_year'] <= year_range[1]))]
    chart1 = alt.Chart(data_new_filter1).mark_line().encode(
        alt.X("yearmonth(outcome_monthyear):O", title = "Time (Month-Year)"),
        alt.Y('count', title="Count"),
        alt.Color("Type")
        )

    return ((chart + chart1).properties(
        title='Trend in Intakes and Out-takes of Animals at AAC',
        width=950, height=300).configure_axisX(
            labelFontSize=14,
            titleFontSize=18,
            labelAngle = 45,
            labelOverlap=True
            ).configure_axisY(
            labelFontSize=14,
            titleFontSize=18
            ).configure_title(
            fontSize=20
            ).configure_legend(
            labelFontSize=18,
            titleFontSize=20,
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='bottom-right'
            )
        )

def make_plot_2(year_range = [2013,2016], animal = "Dog" ):


    if animal == "All":
        data_new2_filter = data_new2[((data_new2['intake_year'] >= year_range[0]) &  
        (data_new2['intake_year'] <= year_range[1]))]
        title = animal + " animals intake by Week Day"
    else :
        data_new2_filter = data_new2[((data_new2['intake_year'] >= year_range[0]) &  
        (data_new2['intake_year'] <= year_range[1])
        & (data_new2['animal_type'] == animal))]
        title = animal + " intake by Week Day"

    data_new2_filter = data_new2_filter.groupby(by = "intake_weekday").agg({"count":"sum"}).reset_index()
    data_new2_filter.columns = ["intake_weekday","count"]

    
    chart = alt.Chart(data_new2_filter).mark_bar(size=40).encode(
            alt.X('intake_weekday:N', title = 'Week Day',sort=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]),
            alt.Y('count:Q', title = 'Animal Count'),
            tooltip=['intake_weekday','count']
        ).properties(title=title,
                    width=300, height=250).configure_axisX(labelFontSize=12,
    titleFontSize=15,
    labelAngle = 45).configure_axisY(labelFontSize=12,
    titleFontSize=15).configure_title(fontSize=17)
    
    return chart

def make_plot_3(year_range = [2013,2016], animal = "Dog"):


    if animal == "All":
        data_new3_filter = data_new3[((data_new3['outake_year'] >= year_range[0]) &  
        (data_new3['outake_year'] <= year_range[1]))]
        title = animal + " animals outake by Week Day"

    else :
        data_new3_filter = data_new3[((data_new3['outake_year'] >= year_range[0]) &  
        (data_new3['outake_year'] <= year_range[1])
        & (data_new3['animal_type'] == animal))]
        title = animal + " outake by Week Day"

    data_new3_filter = data_new3_filter.groupby(by = "outcome_weekday").agg({"count":"sum"}).reset_index()
    data_new3_filter.columns = ["outcome_weekday","count"]

    chart = alt.Chart(data_new3_filter).mark_bar(size=40).encode(
            alt.X('outcome_weekday:N', title = 'Week Day',sort=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]),
            alt.Y('count:Q', title = 'Animal Count'),
            tooltip=['outcome_weekday','count']
        ).properties(title=title,
                    width=300, height=250).configure_axisX(labelFontSize=12,
    titleFontSize=15,
    labelAngle = 45).configure_axisY(labelFontSize=12,
    titleFontSize=15).configure_title(fontSize=17)

    
    return chart

def make_plot_4(year_range = [2013, 2016], animal = "All"):

    # Filtering for intake year via common filter 
    if animal == "All":
        df4 = data_new4[(   (data_new4['intake_year'] >= year_range[0]) & 
                            (data_new4['intake_year'] <= year_range[1])
                        )]
        title_string = "Animal"
    # Filtering for intake year via common filter and animal type
    else:
        df4 = data_new4[(   (data_new4['intake_year'] >= year_range[0]) & 
                            (data_new4['intake_year'] <= year_range[1]) & 
                            (data_new4['animal_type'] == animal))
                        ]
        title_string = animal +"s"

    chart = alt.Chart(df4).mark_bar().encode(
            alt.X("age:Q", bin=alt.Bin(step=1), title = "Age (years)"),
            alt.Y('count():Q', stack = None, title = "Count"),
            tooltip = ['count():Q', 'age:Q']
            ).properties(title= title_string + ' Intake Age Distribution',
                        width=280, height=250
            ).configure_axisX(
                        labelFontSize=12,
                        titleFontSize=15,
                        labelAngle = 0
            ).configure_axisY(
                        labelFontSize=12,
                        titleFontSize=15
            ).configure_title(
                        fontSize=18
            )
    return chart

def make_plot_5(year_range = [2013, 2016], intake_health_condition = "Healthy"):

    # Filtering for intake year via common filter 
    if intake_health_condition == "All":
        df5 = data_new5[(   (data_new5['intake_year'] >= year_range[0]) & 
                            (data_new5['intake_year'] <= year_range[1])
                        )]
    # Filtering for intake year via common filter and intake condition
    else:
        df5 = data_new5[(   (data_new5['intake_year'] >= year_range[0]) & 
                            (data_new5['intake_year'] <= year_range[1]) & 
                            (data_new5['intake_condition'] == intake_health_condition)
                        )]


    chart = alt.Chart(df5).mark_boxplot(size=40,extent='min-max').encode(
        alt.X("animal_type:N", title = "Animal Type"),
        alt.Y('Days in Shelter:Q', title="Days",scale=alt.Scale(type='log'))
        ).properties(title='Time spent in shelter',
                    width=300, height=250
        ).configure_axisX(labelFontSize=12,
                    titleFontSize=15,
                    labelAngle = 0
        ).configure_axisY(labelFontSize=12,
                    titleFontSize=15
        ).configure_title(fontSize=20)
    
    return chart

############### APP LAYOUT BEGINS ##############

app.layout = html.Div([

dbc.Container
    ([
            html.Div([
                # Logo
                html.Img(src='https://raw.githubusercontent.com/UBC-MDS/DSCI_532_L02_group206_ms1/master/img/aac_logo.jpg', style={"display":"block", "margin":"auto"}),
            ], style={"width":"100%"}),

            html.Br(),

            dbc.Row([

                html.Div([
                    # Plot 1
                    html.Iframe(
                    sandbox='allow-scripts',
                    id='trend_plot',
                    height='450',
                    width='1300',
                    style={'margin': 'auto',
                            'border-width':'0'},
                    ################ The magic happens here
                    srcDoc = make_plot_1().to_html()
                    ################ The magic happens here
                    ),
                ]),
            ],style={"width":"100%"}, align="center"
            ),
            
            html.Div([
                html.H3("Year Range", style={"textAlign":"center"}),
            ]),


            dbc.Row([
                # Time Slider Common Filter
                dcc.RangeSlider(
                    id='my-range-slider',
                    min=2013,
                    max=2018,
                    step=1,
                    marks={
                        2013: '2013',
                        2014: '2014',
                        2015: '2015',
                        2016: '2016',
                        2017: '2017',
                        2018: '2018'
                    },
                    value=[2014, 2017],
                    pushable = 1,
                    className="margin"
                    )
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([                 
                    # Plot 2
                    dbc.Col([
                            html.Iframe(
                            sandbox='allow-scripts',
                            id='plot2',
                            height='450',
                            width='450',
                            style={'border-width': '0', 'md':'4'},
                            ################ The magic happens here
                            srcDoc = make_plot_2().to_html()
                            ################ The magic happens here
                            ),          
                            ],md=4),

                    # Dropdown List for Plot 2 and 3
                    dbc.Col(
                        html.Div([
                            html.Br(),
                            dcc.Markdown("Select Animal"),
                            dcc.Dropdown(
                            id='plot23-drop',
                            options=[
                                 {'label': 'All', 'value': 'All'},
                                {'label': 'Dog', 'value': 'Dog'},
                                {'label': 'Cat', 'value': 'Cat'},
                                {'label': 'Bird', 'value': 'Bird'},
                                {'label': 'Other', 'value': 'Other'}                                
                                # Missing option here
                            ],
                            value='Dog',
                            style={"width":'75%', "margin-left":"50px","margin-top":"2px"}
                                ),                   
                         ], style={'textAlign': 'center',"margin-top":"2px","margin-right":"35px",
                         "padding": "0px"}),md=4),

                    dbc.Col([
                            html.Iframe(
                            sandbox='allow-scripts',
                            id='plot3',
                            height='450',
                            width='450',
                            style={'border-width': '0'},
                            ################ The magic happens here
                            srcDoc = make_plot_3().to_html()
                            ################ The magic happens here
                            ),
                    ],md=4)        
                
            ]),

            html.Br(),

            dbc.Row([
                    # Plot 4                 
                    dbc.Col([
                            html.Iframe(
                                sandbox='allow-scripts',
                                id='plot4',
                                height='450',
                                width='400',
                                style={'border-width': '0', 'md':'4'},
                                ################ The magic happens here
                                srcDoc = make_plot_4().to_html()
                                ################ The magic happens here
                            ),          
                            ],width = 4),

                    dbc.Col([
                        
                        # Buffer space between
                        html.Div([], style={
                                            #"background":"black",
                                            "width":"35px",
                                            "height":"100px", 
                                            "display":"inline-block", 'vertical-align':'top',}),
                        
                        # Radio buttons for Plot 4
                        html.Div([
                            dcc.Markdown("Animal Type"),
                            html.Div([
                                dcc.RadioItems(
                                    id='plot4-radio',
                                    options=[
                                        {'label': 'All', 'value': 'All'},
                                        {'label': 'Cats', 'value': 'Cat'},
                                        {'label': 'Dogs', 'value': 'Dog'},
                                        {'label': 'Birds', 'value': 'Bird'},
                                        {'label': 'Others', 'value': 'Other'}
                                    ],
                                    value='All',
                                    style={"display":"table"}
                                    )
                            ],style={"width":"70px"})
                        ], style={"display":"inline-block", "width":"35%", 'vertical-align':'top',}),

                        # Buffer space between
                        html.Div([], style={
                                            #"background":"black",
                                            "width":"75px",
                                            "height":"100px", 
                                            "display":"inline-block",'vertical-align':'top',}),

                        # Radio buttons for Plot 5
                        html.Div([
                            dcc.Markdown("Intake Condition", style={"textAlign":"right"}),
                            
                            html.Div([

                                # Buffer space between
                                html.Div([], style={
                                                #"background":"black",
                                                "width":"30px",
                                                "height":"1px", 
                                                "display":"inline-block",'vertical-align':'top'}),

                                html.Div([
                                    dcc.RadioItems(
                                        id='plot5-radio',
                                        options=[
                                                    {'label': 'All', 'value': 'All'},
                                                    {'label': 'Healthy', 'value': 'Normal'},
                                                    {'label': 'Injured', 'value': 'Injured'},
                                                    {'label': 'Aged', 'value': 'Aged'},
                                                    {'label': 'Sick', 'value': 'Sick'},
                                                    {'label': 'Feral', 'value': 'Feral'},
                                                    {'label': 'Pregnant', 'value': 'Pregnant'},
                                                    {'label': 'Nursing', 'value': 'Nursing'},
                                                    {'label': 'Other', 'value': 'Other'},
                                                    
                                                ],
                                        value='All',
                                        style={"display":"table"}
                                    ),
                                ],style={"width":"80px","display":"inline-block", 'vertical-align':'top'})
                            ], )
                        ], style={"display":"inline-block", "width":"35%",'vertical-align':'top'}),

                    ], width = {"size":4, "offset":0}, style={"padding":"0"}),
                    
                    # Plot 5
                    dbc.Col([
                            html.Iframe(
                                sandbox='allow-scripts',
                                id='plot5',
                                height='450',
                                width='450',
                                style={'border-width': '0'},
                                ################ The magic happens here
                                srcDoc = make_plot_5().to_html()
                                ################ The magic happens here
                            ),
                            ], width=4)
                         
                
                
            ]),


        
    ])
 
])

@app.callback(
    dash.dependencies.Output('trend_plot', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_plot1(year_range):
    
    update_plot1 = make_plot_1(year_range).to_html()
    return update_plot1

@app.callback(
    dash.dependencies.Output('plot2', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('plot23-drop', 'value')])
def update_plot2(year_range, animal):
    
    update_plot2 = make_plot_2(year_range,animal).to_html()
    return update_plot2

@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('plot23-drop', 'value')])
def update_plot3(year_range, animal):

    update_plot3 = make_plot_3(year_range,animal).to_html()
    return update_plot3

@app.callback(
    dash.dependencies.Output('plot4', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('plot4-radio', 'value')])
def update_plot4(year_range, animal):
    
    update_plot4 = make_plot_4(year_range, animal).to_html()
    return update_plot4

@app.callback(
    dash.dependencies.Output('plot5', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('plot5-radio', 'value')])
def update_plot5(year_range, health_condition):
    
    update_plot5 = make_plot_5(year_range, health_condition).to_html()
    return update_plot5


if __name__ == '__main__':
    app.run_server(debug=True)