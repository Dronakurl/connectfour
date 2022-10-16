import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import numpy 
import time

# initialize the board and buttons 
allinputs=[]
alloutputs=[]
chips=[]
buttons=[]
for xi in range(0,6):
   for yi in range(0,7):
        myid=str(xi)+str(yi)
        alloutputs.append(Output(myid,'className'))
        chips.append(
            html.Div(className="chipstuete",
                    children=
                    html.Div(
                        "",
                        id=str(xi)+str(yi), 
                        className="chips grau"
                    )))   

for yi in range(0,7):
    bid="b"+str(yi)
    allinputs.append(Input(bid,'n_clicks'))
    buttons.append(html.Div(className="buttontuete",
                    children=html.Button(
                        "",
                        id=bid,
                        className="mybutton button-primary",
                        n_clicks=0
                        )
                    ))

## dash Layout aufsetzen
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Lato&display=swap']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets) 
server=app.server

# app.head = [html.Link(rel='stylesheet', href='//fonts.googleapis.com/css?family=Lato:400,300,600')]
app.css.config.serve_locally = True
app.title="Connect 4 - the game"

app.layout = html.Div(
    className="container",
    style={ "max-width":"1200px",
            "margin-top":"15px"},
    children=[
        html.Div(className="row",
            children=[
                html.Div(
                    className="seven columns",
                    id="buttonrow",
                    children=buttons
                    ),
                html.Div(
                    className="five columns",
                    id="logobox",                    
                    children=[ html.Div(id="logo",children="CONNECT 4!"),
                        html.Div(children="Tap buttons on the top to play"),
                        html.Div(children="Computer plays yellow")]
                    )
                ]
            ),
        html.Div(className="row",
            children=[
                html.Div(
                    className="seven columns",
                    id="board",
                    children=chips
                ),
                html.Div(
                    id="command",
                    className="five columns",
                    children=[
                        html.Div(
                            "red's turn",
                            id="whoseturn",
                            style={"background-color":"#D50000"}
                        ),html.Br(),
                        html.Button(
                            "restart",
                            id='restart', 
                            className="button-primary", 
                            n_clicks=0
                        ),
                        html.Button(
                            "Save to disk",
                            id='savetodisk', 
                            className="button-primary", 
                            n_clicks=0
                        ),
                        dcc.Dropdown(
                            ["player vs player","player vs computer"],
                            "player vs player",
                            id="modeselect"
                        ),
                        dcc.Textarea(
                            id="textarea",
                            className="u-full-width",
                            value="text",
                        )
                    ]
                )
            ]
        ),
        dcc.Store(id="store")
    ]
)

# TODO This is not multi-user-ready
# the connectfour-Object cannot be serialized easily
# because of some strange stuff with the int-numpy-array, thing
# so jsonpickle doesn't work
# The way forward is to store the data on the server
from connectfour import Connectfour
cf=Connectfour()

@app.callback(*alloutputs,
              Output('whoseturn','style'),
              Output('whoseturn','children'),
              # Output("store","data"),
              *allinputs,
              Input('restart','n_clicks'))
def udpateboard(b0,b1,b2,b3,b4,b5,b6,nst):
    # start = time.time()
    global cf
    if ctx.triggered_id is None:
        raise dash.exceptions.PreventUpdate
    elif ctx.triggered_id == "restart":
        cf.reset()
    else:
        cf.doturn(int(ctx.triggered_id[1]))
    # end = time.time()
    # print("time to update board ", end - start)

    return (*cf.converttoouputlist(), *cf.turntostyle())

@app.callback(Output('textarea',"value"),
              Input('savetodisk','n_clicks'),
              Input('modeselect','value'))
def savetodisk(btn,value):
    if ctx.triggered_id is None:
        raise dash.exceptions.PreventUpdate
    elif ctx.triggered_id=="savetodisk":
        global cf
        cf.writetodisk()
        return "to disk"
    elif ctx.triggered_id=="modeselect":
        cf.mode=value
        return "mode "+cf.mode+" selected"

server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# stat with: gunicorn dashgui:server -b :8000
