import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

## -------------------------------GARFICO PREDITO X REAL -----------------------------##
# Load data
df_ts = pd.read_csv('../models/results/dengue_mg_total.csv')
#df = pd.read_csv(
#    "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
df_ts.columns = [col.replace("AAPL.", "") for col in df_ts.columns]

# Create figure

figts = go.Figure()

figts.add_trace(
    go.Scatter(x=list(df_ts.Date), y=list(df_ts.High),  name="Real" ))
figts.add_trace(
    go.Scatter(x=list(df_ts.Date), y=list(df_ts.Low), name="Predito"))

# Set title
figts.update_layout(
    title_text="Predição de Notificações de Casos de Dengue",
    xaxis_title="Número de casos",
    yaxis_title="Ano de registro",
)

# Add range slider
figts.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

#figts.show()
'''
figts = px.line(df_ts, x='Date', y='AAPL.High', title='Predição de Notificações de Casos de Dengue')

figts.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
#figts.show()
'''
colors = {
    'background': 'rgba(0, 0, 0, 0)',
    'text': '#7FDBFF'
}

##------------------------Grafico Bolha------------------------##
df1 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
df1.rename(columns={'continent': 'Evolucao', 'life expectancy': 'Proporçao de casos', 'gdp per capita': 'Ano  de ocorrencia'}, inplace=True)
df1["Evolucao"] = df1["Evolucao"].astype('category')
df1["Evolucao"] = df1["Evolucao"].cat.rename_categories(['Ign/Branco', 'Cura', 'Obito pelo agravo notificado','Obito por outra causa', 'Obito em investigacao'])

fig1 = px.scatter(df1, y="Proporçao de casos", x="Ano  de ocorrencia",
                 size="population", color="Evolucao", hover_name="country",
                 log_x=True, size_max=60)

fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

figts.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
###########

# Iris bar figure
def drawFigure():
    long_df = pd.read_csv('../models/results/classificacao_vw.csv')
    long_df.loc[long_df["Descricao"] == "Dengue", "Descricao"] = "Dengue Clássico"
    long_df['Ano'] = pd.DatetimeIndex(long_df['Mes']).year
    long_df = long_df[['Ano', 'Codigo', 'Descricao', 'Casos']]
    long_df = long_df.groupby(['Ano', 'Codigo', 'Descricao']).sum()
    long_df = long_df.reset_index()

    res = long_df.pivot(index='Ano', columns=['Descricao'], values='Casos')
    res
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.area(res, facet_col="Descricao", facet_col_wrap=2).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])
    
def drawMultipleSeriesFigure():
    
    long_df = pd.read_csv('../models/results/faixa_vw.csv')
    long_df['Ano'] = pd.DatetimeIndex(long_df['Mes']).year
    long_df = long_df[['Ano', 'Codigo', 'Descricao', 'Casos']]
    long_df = long_df.groupby(['Ano', 'Codigo', 'Descricao']).sum()
    long_df = long_df.reset_index()

    res = long_df.pivot(index='Ano', columns=['Descricao'], values='Casos')
    res = res.reset_index()
    #res = res.drop(['Descricao'])
    res
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.line(res, x="Ano", y=res.columns,
              title='Evolução de casos da dengue por Faixa Etária').update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ).update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y"),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])
    
# Bubble bar figure
# def drawBubbleFigure():
#     return  html.Div([
#         dbc.Card(
#             dbc.CardBody([
#             html.H4('Distribuição de casos por evolução'),
#             html.P("2014-2021"),
#                 #Bubble graph
#                 dcc.Graph(
#                     id='life-exp-vs-gdp',
#                     figure=fig1
#                 ) 
#             ])
#         ),  
#     ])

# Time Series figure
def drawTimeSeriesFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                #Bubble graph
                dcc.Graph(
                    id='life-exp-vs-gdp2',
                    figure=figts
                ) 
            ])
        ),  
    ])

# Macroregion figure
def drawRegionFigure():
    long_df = pd.read_csv('../models/results/macrorregiao_vw.csv')
    long_df['Ano'] = pd.DatetimeIndex(long_df['Mes']).year
    long_df = long_df[['Ano', 'Codigo', 'Descricao', 'Casos']]
    long_df = long_df.groupby(['Ano', 'Codigo', 'Descricao']).sum()
    long_df = long_df.reset_index()
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(long_df, x="Ano", y="Casos", color="Descricao", title="Casos de dengue por macroregião").update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])
    
# Macroregion figure
def drawBubbleFigure():
    dfr = px.data.iris()
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig1
                )  
            ])
        ),  
    ])
    




# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])
    
# Text field
def drawTotalCasosText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("1422324"),
                    html.H2("Casos Notificados"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])
    
# Text field
def drawYTDCasosText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("2019"),
                    html.H2("Último surto"),
                ], style={'textAlign': 'center'}) 
            ], style={'background':'#3a4f63'})
        ),
    ])
    
# Text field
def drawTotalObitosText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("945"),
                    html.H2("Óbitos YTD"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])
# Text field
def drawTaxaText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("3 anos"),
                    html.H2("Sazonalidade"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Data
df = px.data.iris()

# Build App
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])
@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = px.data.election() # replace with your own data source
    #'Coderre', 'Bergeron', 'Joly'
    #df["color"] = df["color"].astype('category')
    #df["color"] = df["color"].cat.rename_categories(['district', 'Grave ', 'Moderada ', 'Leve', 'total', 'winner', 'result', 'district_id'])
    geojson = px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 4500])
    fig.update_geos(fitbounds="locations", visible=False)
    #fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    return fig

app.layout = html.Div([
      html.H1(
        children='Casos de Dengue em Minas Gerais',
        style={
            'textAlign': 'center',
         #   'color': colors['text']
        }
    ),

    html.Div(children='Avaliação entre 2014 - 2021', style={
        'textAlign': 'center',
        #'color': colors['text']
    }),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawTotalCasosText()
                ], width=3),
                dbc.Col([
                    drawTotalObitosText()
                ], width=3),
                dbc.Col([
                     drawTaxaText()
                ], width=3),
                dbc.Col([
                    drawYTDCasosText()
                ], width=3),
            ], align='center'), 
            html.Br(),
                dbc.Row([
                dbc.Col([
                   #Bubble graph
                   drawTimeSeriesFigure()
                ], width=12),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                # dbc.Col([
                #     drawFigure() 
                # ], width=3),
                dbc.Col([
                    #drawFigure()
                    drawRegionFigure()
                ], width=6),
                dbc.Col([
                   # drawFigure()
                   #Bubble graph
                   drawBubbleFigure()
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure()
                ], width=8),
                 dbc.Col([
                    drawMultipleSeriesFigure()
                ], width=4),
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
#app.run_server(mode='external')
app.run_server(debug=True)
