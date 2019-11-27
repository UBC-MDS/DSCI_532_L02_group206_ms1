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
def make_plot_4(animal_type = "Cat"):

    # Filter according to animals
    df_wrangled4 = df_wrangled.query("animal_type == @animal_type")

    chart = alt.Chart(df_wrangled4).mark_bar(opacity = 0.6).encode(
            alt.X("age:Q", bin=alt.Bin(step=1), title = "Age (years)"),
            alt.Y('count():Q', stack = None),
            tooltip = ['count():Q', 'age:Q']
            ).properties(title=animal_type + 's Intake Age Distribution',
                        width=400, height=250
            ).configure_axisX(
                        labelFontSize=12,
                        titleFontSize=15,
                        labelAngle = 0
            ).configure_axisY(
                        labelFontSize=12,
                        titleFontSize=15
            ).configure_title(
                        fontSize=20
            )
    return chart

def make_plot_5(intake_health_condition = "Healthy"):

    # Filter according to intake_condition
    if intake_health_condition == "All":
        df_wrangled5 = df_wrangled
    else:
        df_wrangled5 = df_wrangled.query("intake_condition == @intake_health_condition")

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
            ], style={'display': 'inline-block',
                        'background-color':'white'}),
            
            html.Div([
                dcc.RadioItems(
                    id='plot4-radio',
                    options=[
                        {'label': 'Cats', 'value': 'Cat'},
                        {'label': 'Dogs', 'value': 'Dog'},
                        {'label': 'Birds', 'value': 'Bird'},
                        {'label': 'Others', 'value': 'Other'}
                    ],
                    value='Cat',
                    labelStyle={'display': 'table'}
                ),
            ], style={'vertical-align':'top',
                        'display': 'inline-block',
                        'background-color':'white'}),

        ],style={'background-color':'lightblue',
                    'display': 'inline-block'}),

        html.Div([], style={'vertical-align':'top'}),
        
        html.Div([
            html.Div([   
                dcc.RadioItems(
                    id='plot5-radio',
                    options=[
                        {'label': 'Healthy', 'value': 'Healthy'},
                        {'label': 'Injured', 'value': 'Injured'},
                        {'label': 'Aged', 'value': 'Aged'},
                        {'label': 'Sick', 'value': 'Sick'},
                        {'label': 'Feral', 'value': 'Feral'},
                        {'label': 'Pregnant', 'value': 'Pregnant'},
                        {'label': 'Nursing', 'value': 'Nursing'},
                        {'label': 'Other', 'value': 'Other'},
                        {'label': 'All', 'value': 'All'}
                    ],
                    value='Healthy',
                    labelStyle={'display': 'table'}
                ),
            ], style={'vertical-align':'top',
                        'display': 'inline-block',
                        'background-color':'white'}),

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
            ], style={'display': 'inline-block',
                        'background-color':'white'}),

        ],style={'background-color':'yellow',
                    'display': 'inline-block'}),

    ],  style={"align":"center"}),

])


@app.callback(
    dash.dependencies.Output('plot4', 'srcDoc'),
    [dash.dependencies.Input('plot4-radio', 'value')]
    )
def update_plot4(animal_types_list):

    # wrangle df based on new filter

    updated_plot4 = make_plot_4(animal_types_list).to_html()

    return updated_plot4

@app.callback(
    dash.dependencies.Output('plot5', 'srcDoc'),
    [dash.dependencies.Input('plot5-radio', 'value')]
    )
def update_plot5(intake_condition):

    # wrangle df based on new filter

    updated_plot5 = make_plot_5(intake_condition).to_html()

    return updated_plot5



if __name__ == '__main__':
    app.run_server(debug=True)