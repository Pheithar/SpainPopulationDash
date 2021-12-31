import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd

import json

df_communities = pd.read_csv("./02002Processed.csv")

with open("spain-communities.geojson", "r") as f:
    communities = json.load(f)


selected_communities = []


app = dash.Dash(__name__)


# ------------------------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------------------------

with open("README.md", "r") as f:
    header_text = f.read()

header = dcc.Markdown(className="header",
                      children=header_text)

# Year slider
year_slider = html.Div(className="year-slider-div",
                       children=[
                          html.Label('Year Selector'),
                          dcc.Slider(id='year-slider',
                                     className="slider",
                                     min=df_communities['Año'].min(),
                                     max=df_communities['Año'].max(),
                                     value=df_communities['Año'].min(),
                                     marks={str(year): str(year)
                                            for year in df_communities['Año'].unique()},
                                     step=None
                                    )
                        ])

gender_dropdown = html.Div(className="gender-dropdown-div",
                           children=[
                              html.Label('Gender Selector'),
                              dcc.Dropdown(id='gender-dropdown',
                                           className="dropdown",
                                           options=[
                                              {"label": x, "value": x}
                                              for x in df_communities["Sexo"].unique()
                                           ],
                                           value='Ambos sexos',
                                           clearable=False
                                           )
                            ])

age_dropdown = html.Div(className="age-dropdown-div",
                        children=[
                          html.Label('Age Selector'),
                          dcc.Dropdown(id='age-dropdown',
                                       className="dropdown",
                                       options=[
                                          {"label": x, "value": x}
                                          for x in df_communities["Edad (grupos quinquenales)"].unique()
                                       ],
                                       value='Total Edades',
                                       clearable=False
                                      )
                        ])

nationality_dropdown = html.Div(className="nationality-dropdown-div",
                                children=[
                                  html.Label('Nationality Selector'),
                                  dcc.Dropdown(id='nationality-dropdown',
                                               className="dropdown",
                                               options=[
                                                  {"label": x, "value": x}
                                                  for x in df_communities["Españoles/Extranjeros"].unique()
                                               ],
                                               value='Total',
                                               clearable=False
                                              )
                                ])

relative_checklist = html.Div(className="relative-check-div",
                              children=[
                                html.Label('Display in relative values'),
                                dcc.Checklist(id='relative-check',
                                              className="checklist",
                                              options=[
                                                {"label": "Proportional to population size", "value": "relative"}
                                              ],
                                              value=[]
                                              )
                              ])

# HTML of the controllers
input_controllers = html.Div(className="controllers",
                             children=[
                                html.Div(className="left-controllers",
                                         children=[
                                            gender_dropdown,
                                            age_dropdown
                                         ]),
                                html.Div(className="filler-controllers"),
                                html.Div(className="right-controllers",
                                         children=[
                                            nationality_dropdown,
                                            relative_checklist
                                         ]),
                                html.Div(className="bottom-controllers",
                                         children=[
                                            year_slider
                                         ]),
                             ])

# Graphs

graphs = html.Div(className="graphs-div",
                  children=[
                    html.Div(className="left-graphs",
                             children=[
                                dcc.Graph(id='geo-graph-fig',
                                          className="graph"
                                         ),
                             ]),
                    html.Div(className="right-graphs",
                             children=[
                                dcc.Graph(id='total-line-graph',
                                          className="graph"
                                         ),
                                dcc.Graph(id='communities-line-graph',
                                          className="graph"
                                         )
                             ]),
                  ])


content_container = html.Div(
    className="container",
    children = [
        input_controllers,
        graphs
    ]
)

# Layout
app.layout = html.Div(
    children = [
        header,
        content_container
    ]
)

# ------------------------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------------------------

# Update values map with multiple inputs
@app.callback(
    Output('geo-graph-fig', 'figure'),
    Input('year-slider', 'value'),
    Input('gender-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('nationality-dropdown', 'value'),
    Input('relative-check', 'value')
)
def updateMap(year, gender, age, nationality, relative_value):

    graph_color = "Total"

    if len(relative_value):
        graph_color = "Total relative"


    filtered_df = df_communities.loc[(df_communities["Año"] == year) &
                                     (df_communities["Edad (grupos quinquenales)"] == age) &
                                     (df_communities["Españoles/Extranjeros"] == nationality) &
                                     (df_communities["Sexo"] == gender)
                                    ]

    fig = px.choropleth_mapbox(filtered_df, geojson=communities,
                               featureidkey="properties.noml_ccaa",
                               locations='Comunidades', color=graph_color,
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=4.75,
                               center = {"lat": 38.969659, "lon": -5.045792},
                               opacity=0.4,
                               hover_name="Nombre Comunidad",
                               hover_data={"Total"},
                               title="Population map of Spain"
                               )
    fig.update_layout(margin={"r":0,"t":75,"l":0,"b":0})
    fig.update_layout(transition_duration=500)

    return fig


# Update total graph with multiple inputs
@app.callback(
    Output('total-line-graph', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('nationality-dropdown', 'value')
)
def foo(gender, age, nationality):
    filtered_df = df_communities.loc[(df_communities["Edad (grupos quinquenales)"] == age) &
                                 (df_communities["Españoles/Extranjeros"] == nationality) &
                                 (df_communities["Sexo"] == gender)
                                ]

    filtered_df = filtered_df.groupby("Año").sum().reset_index()


    fig = px.line(filtered_df, x="Año", y="Total", title=f'Population change in Spain through the years(Age: {age}; Nationality: {nationality}; Gender: {gender})')

    fig.update_layout(margin={"r":0,"t":75,"l":0,"b":0})
    fig.update_layout(transition_duration=500)

    return fig

# Update communities graph with multiple inputs
@app.callback(
    Output('communities-line-graph', 'figure'),
    Input('geo-graph-fig', 'clickData'),
    Input('gender-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('nationality-dropdown', 'value')
)
def display_click_community(clickData, gender, age, nationality):
    if clickData:
        clickedCommunity = clickData["points"][0]["location"]
        if clickedCommunity in selected_communities:
            selected_communities.remove(clickedCommunity)
        else:
            selected_communities.append(clickedCommunity)

    filtered_df = df_communities.loc[(df_communities["Edad (grupos quinquenales)"] == age) &
                                     (df_communities["Españoles/Extranjeros"] == nationality) &
                                     (df_communities["Sexo"] == gender) &
                                     (df_communities["Comunidades"].isin(selected_communities))
                                    ]

    fig = px.line(filtered_df, x="Año", y="Total", color="Comunidades", title=f'Population change in the communities of Spain through the years<br><sup>Age: {age}\t Nationality: {nationality}\t Gender: {gender}</sup>')

    fig.update_layout(margin={"r":0,"t":75,"l":0,"b":0})
    fig.update_layout(transition_duration=500)

    return fig

# ------------------------------------------------------------------------------
# APP RUN
# ------------------------------------------------------------------------------

app.run_server(debug=True)
