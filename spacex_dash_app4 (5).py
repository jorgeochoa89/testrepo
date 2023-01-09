# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
from dash import no_update


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df['Launch Site'].unique()

#this variable will create a list of dictionaries for the dropdown
list_options = [{'label': 'ALL',  'value': 'ALL'},]
for site in launch_sites:
    dict_launches= {'label': site,  'value': site}
    list_options.append(dict_launches)

# Create a dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True  
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                 dcc.Dropdown(id='site-dropdown',
                                    options= list_options,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                 # return the outcomes piechart for a selected site
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        100: '100'},
                                    value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
filtered_df= spacex_df[['Launch Site','class']]

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
        
def get_pie_chart(l_site):
  
    if l_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='title')
        return fig
    else: 
        fig = px.pie(filtered_df.loc[filtered_df['Launch Site'] == l_site, 'class'], values='class', 
        names='class', 
        title='title')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
filtered_df2= spacex_df[['Launch Site','class','Payload Mass (kg)','Booster Version Category']]

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(l_site,value):
    if l_site == 'ALL':
        fig = px.scatter(spacex_df.loc[spacex_df['Payload Mass (kg)'].between(value[0],value[1])], x = 'Payload Mass (kg)', y = 'class' ,color="Booster Version Category")
        return fig
    else:
                
        fig = px.scatter(spacex_df.loc[(spacex_df['Launch Site'] == l_site) & (spacex_df['Payload Mass (kg)'].between(value[0],value[1]))], x = 'Payload Mass (kg)', y = 'class' ,color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
