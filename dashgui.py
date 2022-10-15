import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import numpy 

#Einfach mal alle Chips durchnummeriere
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
                        # str(xi)+str(yi),
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
app.title="connect 4 - the game"

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
                    children=html.Div(id="logo",children="4 GEWINNT!")
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
                    id="kommandobereich",
                    className="five columns",
                    children=[
                        html.Div(
                            "red's turn",
                            id="whoseturn",
                            style={"background-color":"#D50000"}
                        ),html.Br(),
                        html.Button(
                            "Neustart",
                            id='neustart', 
                            className="button-primary", 
                            n_clicks=0
                        ),
                        html.Button(
                            "Save to disk",
                            id='savetodisk', 
                            className="button-primary", 
                            n_clicks=0
                        ),
                        dcc.Textarea(
                            id="ausgabefeld",
                            className="u-full-width",
                            value="initaler Text",
                        )
                    ]
                )
            ]
        ),
    ]
)

# from boardfunctions import converttoouputlist,sm
from connectfour import Connectfour
cf=Connectfour()

# Callback für das drücken der Buttons
@app.callback(*alloutputs,
              Output('whoseturn','style'),
              Output('whoseturn','children'),
              *allinputs,
              Input('neustart','n_clicks'))
def udpateboard(b0,b1,b2,b3,b4,b5,b6,nst):
    global cf
    if ctx.triggered_id is None:
        raise dash.exceptions.PreventUpdate
    elif ctx.triggered_id == "neustart":
        cf.reset()
    else:
        cf.doturn(int(ctx.triggered_id[1]))

    return *cf.converttoouputlist(), *cf.turntostyle()

@app.callback(Output('ausgabefeld',"value"),
              Input('savetodisk','n_clicks'))
def savetodisk(btn):
    if ctx.triggered_id is None:
        raise dash.exceptions.PreventUpdate
    else:
        global cf
        cf.writetodisk()
        return "geschrieben"

if __name__ == '__main__':
    app.run_server(debug=True)

# Starten mit gunicorn mydash:server -b :8000
