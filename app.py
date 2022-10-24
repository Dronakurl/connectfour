# remove previous logs 
import os
os.system("rm -f -v *.log")

# remove old file system store files from ServersideOutput
os.system("cd file_system_store && find . -type f -name '*' -mmin +15 -exec rm -v {} \; && cd ..")

# start logging
import logging
logging.basicConfig(filename='log.log', level=logging.WARNING)
logging.info("start the app")

# reroute stdout for debugging
import sys
log_file = open("sysout.log","w")
sys.stdout = log_file

import dash
from dash_extensions.enrich import dcc, html, Dash, Output, Input, State, ServersideOutput
from dash import ctx
import numpy 
import time
import connectfour

# initialize the inputs for the callback and the circles on the game board
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

# setup dash app 
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Lato&display=swap']
dashapp = Dash(__name__,external_stylesheets=external_stylesheets) 
dashapp.css.config.serve_locally = True
dashapp.title="Connect 4 - the game"

dashapp.layout = html.Div(
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
                    className="three columns",
                    id="logobox",                    
                    children=[ html.Div(id="logo",children="CONNECT 4!")
                        ])
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
                    className="three columns",
                    children=[
                        html.Div(children="Tap buttons on the top to play",className="explain"),
                        html.Div(children="Computer plays yellow",className="explain"),
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
                        dcc.Dropdown(
                            ["player vs player","player vs computer"],
                            "player vs computer",
                            id="modeselect"
                        ),
                        html.Div("search depth of computer enemy",className="explain",
                            style={"margin-top":"10px","margin-bottom":"5px"}
                        ),
                        dcc.Dropdown(
                            [2,3,4,5],
                            2,
                            id="kselect"
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

@dashapp.callback(*alloutputs,
              Output('whoseturn','style'),
              Output('whoseturn','children'),
              ServersideOutput("store","data"),
              Input('modeselect','value'),
              *allinputs,
              Input('restart','n_clicks'),
              Input('kselect','value'),
              State("store","data"))
def udpateboard(mode,b0,b1,b2,b3,b4,b5,b6,nst,k,cf):
    logging.debug("updateboard is called")
    if cf is None:
        cf=connectfour.Connectfour(mode=mode,k=k)
    if ctx.triggered_id is None:
        raise dash.exceptions.PreventUpdate
    elif ctx.triggered_id == "restart":
        cf.reset()
    elif ctx.triggered_id=="modeselect":
        cf.mode=mode
    elif ctx.triggered_id=="kselect":
        cf.k=k
        logging.info("depth set to: %d",k)
    else:
        logging.debug("%s was triggered",ctx.triggered_id[1])
        cf.doturn(int(ctx.triggered_id[1]))
    return (*cf.converttoouputlist(), *cf.turntostyle(), cf)

app=dashapp.server
app.secret_key = 'super secret key'

if __name__ == '__main__':
    dashapp.run_server(debug=True)

# start with: gunicorn app:app -b :8000
