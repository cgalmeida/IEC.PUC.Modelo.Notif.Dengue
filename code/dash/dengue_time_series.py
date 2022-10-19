'''
Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.
'''

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df1 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig1 = px.scatter(df1, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Casos de Dengue em Minas Gerais',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
     #Dropdown Itens
    # html.Div([
    # html.Div(children=[
    #         html.Label('Dropdown'),
    #         dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

    #         html.Br(),
    #         html.Label('Multi-Select Dropdown'),
    #         dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
    #                      ['Montréal', 'San Francisco'],
    #                      multi=True),

    #         html.Br(),
    #         html.Label('Radio Items'),
    #         dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
    #     ], style={'padding': 10, 'flex': 1}),

    #     html.Div(children=[
    #         html.Label('Checkboxes'),
    #         dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
    #                       ['Montréal', 'San Francisco']
    #         ),

    #         html.Br(),
    #         html.Label('Text Input'),
    #         dcc.Input(value='MTL', type='text'),

    #         html.Br(),
    #         html.Label('Slider'),
    #         dcc.Slider(
    #             min=0,
    #             max=9,
    #             marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
    #             value=5,
    #         ),
    #     ], style={'padding': 10, 'flex': 1})
    # ], style={'display': 'flex', 'flex-direction': 'row'}),
        
    ############ bar graph
    dcc.Graph(
        id='example-graph-2',
        figure=fig
    ),
    
    #Bubble graph
    html.Div([
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure=fig1
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
