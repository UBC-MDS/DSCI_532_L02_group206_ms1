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

df = pd.read_csv("https://raw.githubusercontent.com/UBC-MDS/DSCI_532_L02_group206_ms1/master/data/cleaned_acc_data.csv")

df['intake_year'] = pd.DatetimeIndex(df['intake_monthyear']).year
df['outake_year'] = pd.DatetimeIndex(df['outcome_monthyear']).year

data_new = df.groupby(by = "intake_monthyear").agg({"animal_type":"count"}).reset_index()
data_new.columns = ["intake_monthyear","count"]
data_new["Type"] = "Intake"
data_new['intake_year'] = pd.DatetimeIndex(data_new['intake_monthyear']).year

data_new1 = df.groupby(by = "outcome_monthyear").agg({"animal_type":"count"}).reset_index()
data_new1.columns = ["outcome_monthyear","count"]
data_new1["Type"] = "Outake"
data_new1['outake_year'] = pd.DatetimeIndex(data_new1['outcome_monthyear']).year

data_new2 = df.groupby(by = ["intake_year","animal_type","intake_weekday"]).agg({"breed":"count"}).reset_index()
data_new2.columns = ["intake_year","animal_type","intake_weekday","count"]
#data_new2['intake_year'] = pd.DatetimeIndex(data_new2['intake_monthyear']).year
print (data_new2.head())

data_new3 = df.groupby(by = ["outake_year","animal_type","outcome_weekday"]).agg({"breed":"count"}).reset_index()
data_new3.columns = ["outake_year","animal_type","outcome_weekday","count"]
#data_new3['outake_year'] = pd.DatetimeIndex(data_new3['outcome_monthyear']).year
print (data_new3.head())


def make_plot_1(year_range = [2013,2016]):

    print (year_range[0])
    data_new_filter = data_new[((data_new['intake_year'] >= year_range[0]) & (data_new['intake_year'] <= year_range[1]))]
    chart = alt.Chart(data_new_filter).mark_line().encode(
        alt.X("intake_monthyear:N", title = "Time (Month-Year)"),
        alt.Y('count', title="Count"),
        alt.Color("Type")
        )
    data_new_filter1 = data_new1[data_new1['outcome_monthyear'] != "2018-04"]
    data_new_filter1 = data_new_filter1[((data_new_filter1['outake_year'] >= year_range[0]) & (data_new_filter1['outake_year'] <= year_range[1]))]
    chart1 = alt.Chart(data_new_filter1).mark_line().encode(
        alt.X("outcome_monthyear:N", title = "Time (Month-Year)"),
        alt.Y('count', title="Count"),
        alt.Color("Type")
        )

    return ((chart + chart1).properties(title='Trend of number of intake and outake of animals in shelter with time',
                        width=800, height=250).configure_axisX(labelFontSize=12,
        titleFontSize=15,
        labelAngle = 90).configure_axisY(labelFontSize=12,
        titleFontSize=15).configure_title(fontSize=20).configure_legend(labelFontSize=15,
        titleFontSize=20))

def make_plot_2(year_range = [2013,2016], animal = "Dog" ):

    data_new2_filter = data_new2[((data_new2['intake_year'] >= year_range[0]) &  
    (data_new2['intake_year'] <= year_range[1])
    & (data_new2['animal_type'] == animal))]

    data_new2_filter = data_new2_filter.groupby(by = "intake_weekday").agg({"count":"sum"}).reset_index()
    data_new2_filter.columns = ["intake_weekday","count"]


    chart = alt.Chart(data_new2_filter).mark_bar(size=40).encode(
            alt.X('intake_weekday:N', title = 'Week Day',sort=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]),
            alt.Y('count:Q', title = 'Animal Count')
        ).properties(title='Animal Intake in Shelter by Week Day',
                    width=300, height=250).configure_axisX(labelFontSize=12,
    titleFontSize=15,
    labelAngle = 45).configure_axisY(labelFontSize=12,
    titleFontSize=15).configure_title(fontSize=20)
    
    return chart

def make_plot_3(year_range = [2013,2016], animal = "Dog"):

    data_new3_filter = data_new3[((data_new3['outake_year'] >= year_range[0]) &  
    (data_new3['outake_year'] <= year_range[1])
    & (data_new3['animal_type'] == animal))]

    data_new3_filter = data_new3_filter.groupby(by = "outcome_weekday").agg({"count":"sum"}).reset_index()
    data_new3_filter.columns = ["outcome_weekday","count"]

    chart = alt.Chart(data_new3_filter).mark_bar(size=40).encode(
            alt.X('outcome_weekday:N', title = 'Week Day',sort=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]),
            alt.Y('count:Q', title = 'Animal Count')
        ).properties(title='Animal Outake in Shelter by Week Day',
                    width=300, height=250).configure_axisX(labelFontSize=12,
    titleFontSize=15,
    labelAngle = 45).configure_axisY(labelFontSize=12,
    titleFontSize=15).configure_title(fontSize=20)

    
    return chart

app.layout = html.Div([

dbc.Container
    ([
            
            dbc.Row([
            html.H1('Austin Animal Shelter'),
   
            html.Iframe(
            sandbox='allow-scripts',
            id='trend_plot',
            height='450',
            width='1425',
            style={'border-width': '0'},
            ################ The magic happens here
            #srcDoc=open('chart.html').read()
            srcDoc = make_plot_1().to_html()
            ################ The magic happens here
        )                   ,
            ]),
            
            dbc.Row([
                html.Center(html.H3("Year Range")),
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
                    value=[2013, 2014],
                    className="margin10"
        
                    )
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([                 
                    dbc.Col([
                            html.Iframe(
                            sandbox='allow-scripts',
                            id='plot2',
                            height='450',
                            width='450',
                            style={'border-width': '0', 'md':'4'},
                            ################ The magic happens here
                            #srcDoc=open('chart.html').read()
                            srcDoc = make_plot_2().to_html()
                            ################ The magic happens here
                            ),          
                            ],md=4),
                    
                    

                    dbc.Col(
                        html.Div([
                            html.Br(),
                            dcc.Markdown("Select Animal"),
                            dcc.Dropdown(
                            id='ddd-chart',
                            options=[
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
                            #srcDoc=open('chart.html').read()
                            srcDoc = make_plot_3().to_html()
                            ################ The magic happens here
                            ),
                    ],md=4)
                         
                
                
                ])

        
    ])
 
])

@app.callback(
    dash.dependencies.Output('trend_plot', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_plot(year_range):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    
    update_plot = make_plot_1(year_range).to_html()
    return update_plot

@app.callback(
    dash.dependencies.Output('plot2', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('ddd-chart', 'value')])
def update_plot2(year_range, animal):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    
    update_plot2 = make_plot_2(year_range,animal).to_html()
    return update_plot2

@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('ddd-chart', 'value')])
def update_plot3(year_range, animal):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    
    update_plot3 = make_plot_3(year_range,animal).to_html()
    return update_plot3


if __name__ == '__main__':
    app.run_server(debug=True)