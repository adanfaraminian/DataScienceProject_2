# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

OptionList = [{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()]
OptionList.insert(0,{'label': 'All', 'value': 'All'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_list',options=OptionList,
                                            value='All',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                #html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                #marks={0: '0',100: '100'},
                                 value=[min_payload , max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_list', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    filtered_df["units"]= [1 for i in range(len(filtered_df))]
    filtered_df = filtered_df.groupby(by=["class"], dropna=False, as_index=False).sum()
    if entered_site == 'All':
        fig = px.pie(spacex_df, values='class', names='Launch Site' ,
        title='Success pie chart')
        return fig
    else:
        fig = px.pie(filtered_df, values='units', names='class',
        title='Success pie chart of '+entered_site+' launch site')
        return fig      
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site_list', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, num):
    df=spacex_df[(spacex_df['Payload Mass (kg)']>=num[0])&(spacex_df['Payload Mass (kg)']<=num[1])] 
    filtered_df = df[df['Launch Site'] == entered_site]
    
    if entered_site == 'All':
        fig = px.scatter(df, x="Payload Mass (kg)", 
        y="class", color="Booster Version Category")
        return fig
    else:
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", 
        y="class", color="Booster Version Category")
        return fig  

# Run the app
if __name__ == '__main__':
    app.run_server()
