# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
# import base64
# import io
# import plotly.graph_objects as go
# import matplotlib.pyplot as plt
# from datetime import datetime
# import time 
# from numpy.ma.core import shape

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


# df = pd.read_csv("D:\UNIVERSIDAD/tesis/webPageCovid/sel-datos23jul2022.csv",encoding='latin')
# df = pd.read_csv("sel-datos23jul2022.csv",encoding='UTF16')
# pd.options.display.max_rows = 20000000
# df = pd.read_csv("https://www.dropbox.com/s/ies34f4n2cptfeg/sel-datos23jul2022.csv?dl=0",encoding="latin")
url = 'https://drive.google.com/file/d/1VLmHtnwqGKjffEsBa3lR8yyqq8lT8cfd/view?usp=share_link'
file_id = url.split('/')[-2]
dwn_url = 'https://drive.google.com/uc?id=' + file_id
df = pd.read_csv(dwn_url,encoding='latin')
print(df.head())

# https://drive.google.com/file/d/1VLmHtnwqGKjffEsBa3lR8yyqq8lT8cfd/view?usp=share_link
# https://itchilpancingo-my.sharepoint.com/:x:/g/personal/l16520276_chilpancingo_tecnm_mx/EZLZbcL3VdFGnu1-qkbRkqMBfgjR59ZQwkdzhKH4xuoSkQ?e=ejeHUN

def obtenerSIPadecimientos(tupla,total_re):
    neumonia = tupla[(tupla["NEUMONIA"]=='SI')]
    diabetes = tupla[(tupla["DIABETES"]=='SI')]
    epoc = tupla[(tupla["EPOC"]=='SI')]
    asma = tupla[(tupla["ASMA"]=='SI')]
    inmusupr = tupla[(tupla["INMUSUPR"]=='SI')]
    hipertension = tupla[(tupla["HIPERTENSION"]=='SI')]
    otra_com = tupla[(tupla["OTRA_COM"]=='SI')]
    cardiovascular = tupla[(tupla["CARDIOVASCULAR"]=='SI')]
    obesidad = tupla[(tupla["OBESIDAD"]=='SI')]
    renal = tupla[(tupla["RENAL_CRONICA"]=='SI')]
    tabaquismo = tupla[(tupla["TABAQUISMO"]=='SI')]
    
    dfPadecimientos = pd.DataFrame({'Padecimientos': ['NEUMONIA','DIABETES','EPOC', 'ASMA', 'INMUSUPR','HIPERTENSION', 'OTRA_COM', 'CARDIOVASCULAR','OBESIDAD', 'RENAL_CRONICA', 'TABAQUISMO'],
    'Cantidad': [len(neumonia),len(diabetes),len(epoc),len(asma),len(inmusupr),len(hipertension),len(otra_com),len(cardiovascular),len(obesidad),len(renal),len(tabaquismo)],
    'Porcentaje': [obtenerPorcentaje(len(neumonia),total_re),obtenerPorcentaje(len(diabetes),total_re),obtenerPorcentaje(len(epoc),total_re),obtenerPorcentaje(len(asma),total_re),obtenerPorcentaje(len(inmusupr),total_re),obtenerPorcentaje(len(hipertension),total_re),obtenerPorcentaje(len(otra_com),total_re),obtenerPorcentaje(len(cardiovascular),total_re),obtenerPorcentaje(len(obesidad),total_re),obtenerPorcentaje(len(renal),total_re),obtenerPorcentaje(len(tabaquismo),total_re)]})
    return dfPadecimientos

def obtenerPorcentaje(nDat, totRes):
    resPorcen = (100/int(totRes))*int(nDat)
    return round(resPorcen, 4)

totalHabEstado = 3540685

total_rows=len(df.axes[0]) #===> Axes of 0 is for a row
porcentajeRegDeToH = (100/int(totalHabEstado))*int(total_rows)
print(total_rows, " de registros, equivalente a ", round(porcentajeRegDeToH, 2) , "% de su total de habitantes en el 2020")

print("\n\n**** FALLECIDOS QUE REQUIRIERON UCI:\n")
soloDefunciones = df[(df["FECHA_DEF"]!='9999-99-99')]
total_fallecidos = len(soloDefunciones.axes[0])
soloUICDef = soloDefunciones[(soloDefunciones["UCI"]=='SI')]
cantindadMP2 = soloUICDef[(soloUICDef["SEXO"]=='M')]
cantindadHP2 = soloUICDef[(soloUICDef["SEXO"]=='H')]
resDefUIC = soloUICDef.groupby(['SEXO']).size()
print(resDefUIC)
print(total_fallecidos, " de fallecidos, equivalente a ", round((100/int(total_rows))*int(total_fallecidos), 2) , "% del total de registros")

print("\n\n**** PORCENTAJE DEFUNCIONES DEL TOTAL DE REGISTROS:\n")
print("MUJERES: ", round((100/int(total_rows))*int(len(cantindadMP2.axes[0])), 6),"% -  HOMBRES: ", round((100/int(total_rows))*int(len(cantindadHP2.axes[0])), 6), "%")

# soloUICDef.groupby('SEXO')['ID_REGISTRO'].size().plot(kind='bar')
# eje_x = resDefUIC[0].tolist()
# ## Valores para el eje y
# eje_y = resDefUIC[0].tolist() 
#GRAFICA
# plt.bar(resultadoPadComunesInd['Padecimientos'],resultadoPadComunesInd['Cantidad'])
# plt.ylim(0, 1900)
# plt.title('Padecimientos en indigenas')
# plt.show()
# # print(df.head())




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# ENTIDAD_NAC


app.layout = html.Div([
    html.H1("Analisis de datos COVID-19 Guerrero - México", style={"textAlign":"center"}),
    html.Hr(),
    html.Div(html.Div([
        html.P('Tipos de Graficas:')
    ])),
    html.Div(html.Div([
        dcc.Dropdown(
            id='opciones', clearable=False,
            value="edad",
            options=[
                {'label': 'Edades', 'value': 'edad'},
                {'label': 'Población Indigena','value':'indigena'},
                {'label': 'Padecimientos asociados al COVID','value':'padecimientos'},
                {'label': 'Hospitalizaciones','value':'hospital'},
            ],
        )
    ],className="three columns"),className="row"),
    # html.Div(id='output-data-upload'),
    # html.P("Selecciona el estado:"),
    # html.Div(html.Div([
    #     dcc.Dropdown(id='opciones', clearable=False,
    #                  value="Edades",
    #                 options=[{'label': 'Edades', 'value': 'edad',
    #                         'label': 'Población Indigena','value':'indigena'},
    #                         'label': 'Padecimientos asociados al COVID','value':'padecimientos',
    #                         'label': 'Género','value':'genero',
    #                         }]),
    # # print(dcc.value)
    # ],className="two columns"),className="row"),

    # html.H1(id="saludo"),
    html.Div(id="output-div", children=[]),
])

@app.callback(
    Output('output-div', 'children'),
    Input('opciones', 'value')
)

# print(resultadoUICPorPadecimientos)
# def graficas():

def update_output(value):
    #Selección opción de Padecimientos Asociados al COVID - Pastel
    if value == 'indigena':
        print("Ingena")
        print("\n\n**** PADECIMIENTOS EN INDIGENAS:\n")
        soloIndigenas = df[(df["INDIGENA"]=='SI')]
        resultadoPadComunesInd = obtenerSIPadecimientos(soloIndigenas,total_rows)
        print(resultadoPadComunesInd)

        figIndig = px.bar(x=resultadoPadComunesInd['Padecimientos'], y=resultadoPadComunesInd['Cantidad'])
        return[
            html.Div([
                # html.Div([
                #     html.H1('Enfermedad que mas padecieron:')
                # ]),
                    html.Div([dcc.Graph(figure=figIndig)], className="nine columns"),
                    # html.Div([dcc.Graph(figure=figBarras)], className="six columns"),
                    # fig.show(), className="six columns"
            ])
        ]
    if value == 'padecimientos':
        print("HOLA")
        #1.- ¿Que tipo de padecimiento hace que las personas infectadas requieran ingresar a una unidad de cuidados intesivo?
        print("\n\n**** UIC POR PADECIMIENTO:\n")
        soloUCI = df[(df["UCI"]=='SI')]
        resultadoUICPorPadecimientos = obtenerSIPadecimientos(soloUCI,total_rows)
        print(resultadoUICPorPadecimientos)

        # fig_pie = plt.pie(resultadoUICPorPadecimientos['Cantidad'], labels=resultadoUICPorPadecimientos['Padecimientos'],autopct="%0.1f %%")
        # fig = go.Figure(data=[go.Pie(labels=resultadoUICPorPadecimientos['Padecimientos'],values=resultadoUICPorPadecimientos['Cantidad'])])
        fig = px.pie(values=resultadoUICPorPadecimientos['Cantidad'],names=resultadoUICPorPadecimientos['Padecimientos'])
        figBarras = px.bar(x=resultadoUICPorPadecimientos['Padecimientos'],y=resultadoUICPorPadecimientos['Cantidad'])
        suma_padecimientos = 0
        for padecimiento in resultadoUICPorPadecimientos['Cantidad']:
         suma_padecimientos  += padecimiento
        print(suma_padecimientos)
        # fig.show()
        return[
            html.Div([                  
                    html.Div([
                        html.Div(html.H1(f'Personas que sufrieron un padecimiento: {suma_padecimientos}', style={'font-size':'20px'}),
                        style={'align-content':'center','background-color':'white'} ),
                        # html.Div(html.H1(f'Personas que sufrieron un padecimiento: {suma_padecimientos}', style={'font-size':'12px'}), className="six columns",
                        # style={'align-content':'center','background-color':'red'} ),
                        # html.Div(html.H1(f"                                     "), className="six columns",
                        # style={'align-content':'center','background-color':'yellow'}),
                    ],style={'align-content':'center','background-color':'yellow'}),

                    html.Br(),
                    html.Div([
                        html.Div([dcc.Graph(figure=fig)], className="nine columns", style={'align-content':'center',}),
                        html.Div([dcc.Graph(figure=figBarras)], className="nine columns"),
                    ],style={'align-content':'center'})
                    # fig.show(), className="six columns"
            ],style={'align-content':'center'}),
        ]
    if value == 'hospital':
        print("Hospital")
        #3.- ¿Que porcentaje por padecimiento requirio hospitalizacion?
        print("\n\n**** PADECIMIENTOS CON HOSPITALIZACION:\n")
        soloHosp = df[(df["TIPO_PACIENTE"]=='hosp')]
        resultadoUICPorPadecimientos = obtenerSIPadecimientos(soloHosp,total_rows)
        print(resultadoUICPorPadecimientos)

        figSex = px.bar(x=resultadoUICPorPadecimientos['Padecimientos'],y=resultadoUICPorPadecimientos['Cantidad'])


        return[
            html.Div([
                    html.Div([dcc.Graph(figure=figSex)], className="six columns"),
                    # html.Div([dcc.Graph(figure=figBarras)], className="six columns"),
                    # fig.show(), className="six columns"
            ])
        ]    # return [




# def update_output(value):
#     if value is None:
#         raise 'Vacio'
#     else:
#         return f'El estado selecccionado es: {value}'

# ini = time.time_ns()


if __name__ == '__main__':
    app.run_server(debug=False)
