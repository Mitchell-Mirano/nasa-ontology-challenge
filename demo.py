import base64
import io
import pathlib
from re import search

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from PIL import Image
from io import BytesIO
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import networkx as nx
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import scipy.spatial.distance as spatial_distance

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()



nasa_themes=['malaysia','hokkaido volcanoes','blue glacier','atlas']
# Import datasets here for running the Local version


with open(PATH.joinpath("demo_intro.md"), "r") as file:
    demo_intro_md = file.read()

with open(PATH.joinpath("demo_description.md"), "r") as file:
    demo_description_md = file.read()

# Methods for creating components in the layout code
def Card(children, **kwargs):
    return html.Section(children, className="card-style")


    return html.Div(
        style={"margin": "25px 5px 30px 0px"},
        children=[
            f"{name}:",
            html.Div(
                style={"margin-left": "5px"},
                children=[
                    dcc.Slider(
                        id=f"slider-{short}",
                        min=min,
                        max=max,
                        marks=marks,
                        step=step,
                        value=val,
                    )
                ],
            ),
        ],
    )


def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f"div-{short}",
        style={"display": "inline-block"},
        children=[
            f"{name}:",
            dcc.RadioItems(
                id=f"radio-{short}",
                options=options,
                value=val,
                labelStyle={"display": "inline-block", "margin-right": "7px"},
                style={"display": "inline-block", "margin-left": "7px"},
            ),
        ],
    )


def create_layout(app):
    # Actual layout of the app
    return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            # Header
            html.Div(
                className="row header",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("dash-logo.png"),
                                className="logo",
                                id="plotly-image",
                            )
                        ],
                        className="three columns header_img",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "t-SNE Explorer",
                                className="header_title",
                                id="app-title",
                            )
                        ],
                        className="nine columns header_title_container",
                    ),
                ],
            ),
            # Demo Description
           html.Div(
                className="row background",
                id="demo-explanation",
                style={"padding": "50px 45px"},
                children=[
                    html.Div(
                        id="description-text", children=dcc.Markdown(demo_intro_md)
                    ),
                    html.Div(
                        html.Button(id="learn-more-button", children=["Learn More"])
                    ),
                ],
            ),
            # Body
            html.Div(
                className="row background",
                style={"padding": "10px"},
                children=[
                    html.Div(
                        className="three columns",
                        children=[
                        dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': i, 'value': i} for i in nasa_themes],
                        value='malaysia'
                        )
                        
                        ]
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(id="graph-3d-plot-tsne", style={"height": "98vh"})
                        ],
                    ),
                ],
            ),
        ],
    )


def demo_callbacks(app):
    
    @app.callback(
    Output('graph-3d-plot-tsne', 'figure'),
    [Input('yaxis-column', 'value')])
    
    def create_neatwork_graph(value):
        df=pd.read_csv('themes.csv')
        documents=[]
        for i,th in enumerate(df['themes'].to_list()):
            if type(th)!=float and 'malaysia' in th:
                documents.append(i)
        
        sims=pd.read_csv('nasa_similarity.csv') 
        edges=sims[sims['edge_start'].isin(documents)]
        G=nx.Graph()
        for x,y in zip(edges['edge_start'],edges['edge_end']):
            G.add_edge(x,y)
            
        pos=nx.random_layout(G)
        
        x=[x[0] for x in pos.values()]
        y=[y[1] for y in pos.values()]
        
        fig = px.scatter(x=x,
                     y=y,
                     size=3)

        return fig
        
        
    