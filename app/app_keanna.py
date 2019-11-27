import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Austin Animal Center Dashboard'

df = pd.read_csv("https://raw.githubusercontent.com/UBC-MDS/DSCI_532_L02_group206_ms1/master/data/cleaned_acc_data.csv")

df_wrangled = df # add additional wrangling/common filtering step
df_wrangled["age"] = round(df_wrangled["age_upon_intake_(days)"]/365,0)

## Plotting function begins here
def make_plot_2(animal = ['Cats', 'Dogs', 'Birds', 'Others']):

    # wrangle data for weekdays        #should/can we wrangle this somewhere else?
    df_weekdays = df_wrangled[df_wrangled['intake_monthyear'
                        ].str.contains('2017')
                   ].groupby(by = "intake_weekday"
                            ).agg({"animal_type":"count"}
                                 ).reset_index()
    
    df_weekdays.columns = ["intake_weekday","count"]
    
    # create weekday intake plot
    chart = alt.Chart(df_weekdays).mark_bar(size=40).encode(
            alt.X('intake_weekday:N', title = 'Week Day',
                  sort=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]),
            alt.Y('count:Q', title = 'Animal Count')
            ).properties(title='Animal Intake in Shelter by Week Day',
                        width=400, height=250).configure_axisX(labelFontSize=12,
            titleFontSize=15,
            labelAngle = 45).configure_axisY(labelFontSize=12,
            titleFontSize=15).configure_title(fontSize=20)
    
    return chart


def make_plot_3():

    # wrangle data for weekday outcomes   #should/can we wrangle this somewhere else?
    df_weekdays = df_wrangled[df_wrangled['outcome_monthyear'
                                         ].str.contains('2017')
                             ].groupby(by = "outcome_weekday"
                                      ).agg({"animal_type":"count"}
                                           ).reset_index()
    df_weekdays.columns = ["outcome_weekday","count"]
    
    
    # create weekday outtake plot
    chart = alt.Chart(df_weekdays).mark_bar(size=40).encode(
            alt.X('outcome_weekday:N', title = 'Week Day',
                  sort=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]),
            alt.Y('count:Q', title = 'Animal Count')
            ).properties(title='Animal Out-take in Shelter by Week Day',
                        width=400, height=250).configure_axisX(labelFontSize=12,
            titleFontSize=15,
            labelAngle = 45).configure_axisY(labelFontSize=12,
            titleFontSize=15).configure_title(fontSize=20)
    
    return chart
    

## plotting function ends


app.layout = html.Div([

    ### Dashboard title / text
    html.H1('Austin Animal Shelter Operations'),

    html.Div([
    
        # display plot 2 
        html.Div([
            html.Iframe(
            sandbox='allow-scripts',
            id='plot2',
            height='450',
            width='625',
            style={'border-width': '0'},
            ################ The magic happens here
            srcDoc = make_plot_2().to_html()
            ################ The magic happens here
            ), 
        ], style={'display': 'inline-block'}),
        
        # plot 2 and 3 dropdown selector
        html.Div([
            html.Label('Multi-Select Dropdown'),
                dcc.Dropdown(
                    options=[
                    {'label': 'Cats', 'value': 'Cats'},
                    {'label': 'Dogs', 'value': 'Dogs'},
                    {'label': 'Birds', 'value': 'Birds'},
                    {'label': 'Others', 'value': 'Others'}
                ],
                value=['Cats', 'Dogs', 'Birds', 'Others'],
                multi=True,
            ),
         ], style={'vertical-align':'top',
                    'display': 'inline-block',
                    'width': '10%'}),

        
       # display plot 3
        html.Div([
            html.Iframe(
            sandbox='allow-scripts',
            id='plot3',
            height='450',
            width='625',
            style={'border-width': '0'},
            ################ The magic happens here
            srcDoc = make_plot_3().to_html()
            ################ The magic happens here
            ),
        ], style={'display': 'inline-block'}),

    ],  style={"align":"center"}),
    

])

if __name__ == '__main__':
    app.run_server(debug=True)