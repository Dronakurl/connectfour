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

app.layout = html.Div(
    className="container",
    style={"max-width":"1200px",
        "margin-top":"15px"},
    children=[
        html.Div(className="row",
            children=[
                html.Div(
                    className="seven columns",
                    style={"background-color":"lightyellow",
                        "padding-top":"10px"},
                    children=buttons
                    ),
                html.Div(
                    className="five columns",
                    style={"text-align":"center","vertical-align":"center"},
                    children=html.Div(className="logo",children="4 GEWINNT!")
                    )
                ]
            ),
        html.Div(className="row",
            children=[
                html.Div(
                    className="seven columns",
                    style={"background-color":"rgb(210,210,220)",
                        "padding-top":"10px",
                        "padding-bottom":"10px",
                        },
                    children=chips
                ),
                html.Div(
                    id="kommandobereich",
                    className="five columns",
                    style={"text-align":"center"},
                    children=[
                        html.Button(
                            "Neustart",
                            id='neustart', 
                            className="button-primary", 
                            n_clicks=0
                        ),
                        html.Div(
                            "Wer ist dran",
                            id="whoseturn",
                            style={"background-color":"red"}
                        ),
                        dcc.Textarea(
                            id="ausgabefeld",
                            className="u-full-width",
                            style={
                                "display":"none",
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

# from boardfunctions import converttoouputlist,sm
from connectfour import Connectfour
cf=Connectfour()

# Callback für das drücken der Buttons
@app.callback(*alloutputs,
              Output('whoseturn','style'),
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
    return *cf.converttoouputlist(), cf.turntostyle()

# @app.callback(Output('ausgabefeld',"value"),
#               Input('neustart','n_clicks'))
# def neustart(neustartbtn):
#     if ctx.triggered_id is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         global cf
#         cf.reset()
#         cf.print()
#         return "Neustart"

if __name__ == '__main__':
    app.run_server(debug=True)

# Starten mit gunicorn mydash:server -b :8000
