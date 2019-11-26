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

app.title = 'Dash app with pure Altair HTML'

df = pd.read_csv("https://raw.githubusercontent.com/UBC-MDS/DSCI_532_L02_group206_ms1/master/data/cleaned_acc_data.csv")

df_wrangled = df # add additional wrangling/common filtering step
df_wrangled["age"] = round(df_wrangled["age_upon_intake_(days)"]/365,0)

## Plotting function begins here
def make_plot_4():

    # Create animal age histogram 
    

    chart = alt.Chart(df_wrangled).mark_bar().encode(
            alt.X("age", bin=alt.Bin(step=1), title = "Age (years)"),
            alt.Y('count()', stack = None),
            ).properties(title='Animal intake age distribution',
                        width=400, height=250).configure_axisX(labelFontSize=12,
        titleFontSize=15,
        labelAngle = 0).configure_axisY(labelFontSize=12,
        titleFontSize=15).configure_title(fontSize=20)
    return chart

def make_plot_5():

    # Create Boxplot data

    chart = alt.Chart(df_wrangled).mark_boxplot(size=40,extent='min-max').encode(
        alt.X("animal_type:N", title = "Animal Type"),
        alt.Y('total_time_in_shelter_days', title="Days",scale=alt.Scale(type='log')),
        ).properties(title='Time spent in shelter',
                    width=400, height=250).configure_axisX(labelFontSize=12,
    titleFontSize=15,
    labelAngle = 0).configure_axisY(labelFontSize=12,
    titleFontSize=15).configure_title(fontSize=20)
    
    return chart


## plotting function ends


app.layout = html.Div([

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('Austin Animal Shelter Operations'),
    html.H2('Show your love for dogs, cats and birds!'),

    html.Div([

        html.Div([
            html.Iframe(
            sandbox='allow-scripts',
            id='plot4',
            height='450',
            width='625',
            style={'border-width': '0'},
            ################ The magic happens here
            srcDoc = make_plot_4().to_html()
            ################ The magic happens here
            ), 
        ], style={'display': 'inline-block'}),
        
        html.Div([
            dcc.Checklist(
                options=[
                    {'label': 'Cats', 'value': 'Cats'},
                    {'label': 'Dogs', 'value': 'Dogs'},
                    {'label': 'Birds', 'value': 'Birds'},
                    {'label': 'Others', 'value': 'Others'}
                ],
                value=['Cats'],
                labelStyle={'display': 'table'}
            ),
        ], style={'vertical-align':'top',
                    'display': 'inline-block'}),

        html.Div([   
            dcc.RadioItems(
                options=[
                    {'label': 'Healthy', 'value': 'Healthy'},
                    {'label': 'Injured', 'value': 'Injured'},
                    {'label': 'Aged', 'value': 'Aged'},
                    {'label': 'Sick', 'value': 'Sick'},
                    {'label': 'Feral', 'value': 'Feral'},
                    {'label': 'Pregnant', 'value': 'Pregnant'},
                    {'label': 'Nursing', 'value': 'Nursing'},
                    {'label': 'Other', 'value': 'Other'}
                ],
                value='Healthy',
                labelStyle={'display': 'table'}
            ),
        ], style={'vertical-align':'top',
                    'display': 'inline-block'}),

        html.Div([
            html.Iframe(
            sandbox='allow-scripts',
            id='plot5',
            height='450',
            width='625',
            style={'border-width': '0'},
            ################ The magic happens here
            srcDoc = make_plot_5().to_html()
            ################ The magic happens here
            ),
        ], style={'display': 'inline-block'}),

    ],  style={"align":"center"}),
    
    html.H3('This is a Dropdown'),
    dcc.Dropdown(
        options = [
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': "San Francisco", 'value': 'SF'}
        ],
    value = "MTL", style = dict(width='45%')
    ),

    html.H3('This is a slider'),

    dcc.Slider(
    min=0,
    max=9,
    marks={i: 'Label {}'.format(i) for i in range(10)},
    value=5,
    ),
    dcc.Checklist(
            options=[
                {'label': 'Cats', 'value': 'Cats'},
                {'label': 'Dogs', 'value': 'Dogs'},
                {'label': 'Birds', 'value': 'Birds'},
                {'label': 'Others', 'value': 'Others'}
            ],
            value=['Cats']
        ),

])

if __name__ == '__main__':
    app.run_server(debug=True)