# remove previous logs and old data storage
import os
os.system("rm -f *.log")
os.system("cd file_system_store && find . -type f -name '*' -mmin +15 -exec rm {} \; && cd ..")
import logging
logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.info("start the app")
import dash
from dash_extensions.enrich import dcc, html, Dash, Output, Input, State, ServersideOutput
from dash import ctx
import numpy 
import time
import connectfour
# for debugging
import sys
log_file = open("sysout.log","w")
sys.stdout = log_file
print("this will be written to message.log")

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
dashapp = Dash(__name__,external_stylesheets=external_stylesheets) 

# dashapp.head = [html.Link(rel='stylesheet', href='//fonts.googleapis.com/css?family=Lato:400,300,600')]
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
              State("store","data"))
def udpateboard(mode,b0,b1,b2,b3,b4,b5,b6,nst,cf):
    logging.debug("updateboard is called")
    if cf is None:
        cf=connectfour.Connectfour(mode=mode)
    if ctx.triggered_id is None:
        raise dash.exceptions.PreventUpdate
    elif ctx.triggered_id == "restart":
        cf.reset()
    elif ctx.triggered_id=="modeselect":
        cf.mode=mode
    else:
        logging.debug("%s was triggered",ctx.triggered_id[1])
        cf.print()
        cf.doturn(int(ctx.triggered_id[1]))
    return (*cf.converttoouputlist(), *cf.turntostyle(), cf)

app=dashapp.server

if __name__ == '__main__':
    dashapp.run_server(debug=True)

# start with: gunicorn app:app -b :8000
