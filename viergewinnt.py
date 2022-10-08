import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import numpy 

# dash Layout aufsetzen
app = dash.Dash(__name__) 
server=app.server

#Einfach mal alle Buttons durchnummeriere
allids=[]
allinputs=[]
alloutputs=[]
buttons=[]
for xi in range(0,7):
    for yi in range(0,6):
        myid=str(xi)+str(yi)
        allids.append(myid)
        allinputs.append(Input(myid,'n_clicks'))
        alloutputs.append(Output(myid,'className'))
        buttons.append(
            html.Div(className="chipstuete",
                    children=
                    html.Button(
                        str(xi)+str(yi),
                        id=str(xi)+str(yi), 
                        className="chips grau",
                        style={"aspect-ratio":"1/1"},
                        n_clicks=0
                    )))   

# DASH setup
app.layout = html.Div(
    className="container",
    style={"max-width":"1200px"},
    children=[
        html.H1(children='Vier gewinnt'),
        html.Div(className="row",
            children=[
                html.Div(
                    className="seven columns",
                    style={"background-color":"rgb(210,210,220)","aspect-ratio":"7/6","padding-top":"10px"},
                    children=buttons
                ),
                html.Div(
                    id="kommandobereich",
                    className="three columns",
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


# Callback für das drücken eines Buttons
@app.callback(Output('ausgabefeld', 'value'),
              alloutputs[0],
              *allinputs)
def chipangeklickt(b00,b10,b20,b30,b40,b50,b60,
                   b01,b11,b21,b31,b41,b51,b61,
                   b02,b12,b22,b32,b42,b52,b62,
                   b03,b13,b23,b33,b43,b53,b63,
                   b04,b14,b24,b34,b44,b54,b64,
                   b05,b15,b25,b35,b45,b55,b65):

    return ctx.triggered_id,"chips rot"

if __name__ == '__main__':
    app.run_server(debug=True)

# Starten mit gunicorn mydash:server -b :8000
