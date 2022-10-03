import dash
from dash import dcc, html, Input, Output, State, ctx
import sys
import pandas as pd
import plotly.graph_objects as go
import dash_cytoscape as cyto

# Das Spielfeld für Vier Gewinnt malen
fig = go.Figure()
fig.update_xaxes(range=[0, 7], zeroline=True,showgrid=False)
fig.update_yaxes(range=[0, 6])
fig.update_layout(xaxis_title=False, yaxis_title=False)
fig.update_layout()#width=700*0.8,height=600*0.8)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)


# Mit Cyto eine Zeichnung machen
mynodes=[]
for xi in range(0,7):
    for yi in range(0,6):
        sh={'data': {'id': str(xi)+"."+str(yi), 'label': str(xi)+"."+str(yi)},
                'position': {'x': xi*100+150, 'y': yi*100+150},
                'locked':True, 'classes':''}
        mynodes.append(sh)

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {   
        'selector': '.red',
        'style' : {
            'background-color': 'red'
         }
    }
]

# dash Layout aufsetzen
app = dash.Dash(__name__) 
server=app.server

app.layout = html.Div(
    className="container",
    style={"max-width":"1200px"},
    children=[
        html.H1(children='Vier gewinnt'),
        html.Div(className="row",
            children=[
                html.Div(
                    className="nine columns",
                    style={"background-color":"rgb(210,210,220)","aspect-ratio":"7/6"},
                    children=[
                        html.Div(
                            cyto.Cytoscape(
                                id='meingraph',
                                stylesheet=default_stylesheet, 
                                panningEnabled=False,
                                userZoomingEnabled=False,
                                layout={'name': 'preset'},
                                style={'width':'100%',
                                    'height':'100%'},
                                elements=mynodes
                            ),
                            style={
                                "aspect-ratio":"7/6"
                            }
                        )
                    ]
                ),
                html.Div(
                    id="kommandobereich",
                    className="three columns",
                    # style={"background-color":"red"},
                    children=[
                        dcc.Input(
                            id='input-on-submit', 
                            className="u-full-width", 
                            type='text'
                        ),
                        html.Button(
                            "Abschicken",
                            id='submit-val', 
                            className="button-primary", 
                            n_clicks=0,
                            value="Submit"
                        ),
                        dcc.Textarea(
                            id="ausgabefeld",
                            className="u-full-width",
                            style={
                                "display":"block",
                                "margin-top":"20px",
                                "height":"300px"
                            },
                            value="initaler Text",
                        )
                    ]
                )
            ]
        ),
    ]
)

# Callback für das drücken eines Nodes
@app.callback(Output('meingraph', 'elements'),
              [Input('meingraph', 'tapNodeData')],
              State('meingraph', 'elements'))
def displayTapNode(data,curele):
    elements=curele
    if data is not None:
        indexe=[i for i, elem in enumerate(elements) if elem["data"]["id"]==data["id"]]   
        elements[indexe[0]]["classes"]="red" 
    return elements

if __name__ == '__main__':
    app.run_server(debug=True)

# Starten mit gunicorn mydash:server -b :8000
