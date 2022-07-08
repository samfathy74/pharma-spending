# ### Import Libraries


from dash import html, dcc, dash_table, Dash
import dash_bootstrap_components as dbc
# from jupyter_dash import JupyterDash
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import json


# put money in the readable format
def money(x):
    l = ['','K','M', 'B', 'T']
    i = int(math.floor(math.log(x, 1000)))
    return f"${round(x / math.pow(1000, i), 2)}{l[i]}"


# ### Read Data
pharma_data = pd.read_csv('data/final_pharma_data.csv')
pharma_data['Time'] = pd.to_datetime(pharma_data.Time, format='%Y')


# ### Initialization App
 # ================================== Create a Dash app ==================================
app = Dash(__name__,
    external_stylesheets=[
    dbc.themes.BOOTSTRAP, 
    'assets/styleCss.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css',
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css",
    'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.css',
    'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css'
    
    ], title='Pharmaceutical Dashboard',)

server = app.server
server.static_folder = 'image'


# ### ================================== Header ==========================
header = dbc.Row([
            dbc.Col([
                html.P(['Pharmaceutical Dashboard', html.Pre('💊💰', style={"display": "inline"})]),
            ]),
            dbc.Col([
                ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.BOOTSTRAP, dbc.themes.CYBORG], icons={ "left": "fa fa-moon","right": "fa fa-sun" })
            ], width=2, align='center'),
        ], className='header')


# ### ================================== BANS ===========================

cond = pharma_data[pharma_data['TOTAL_SPEND']==pharma_data['TOTAL_SPEND'].max()]

high = cond['Country'].values[0]

low = pharma_data[pharma_data['Time'] == cond['Time'].values[0]].min()['Country']

spnd = money(cond['TOTAL_SPEND'].values[0])

ind = html.Div(className="sc-gauge", children=[
        html.Div(className="sc-background", children=[
            html.Div(className="sc-percentage", id="sc-percentage"),
            html.Div(className="sc-mask"),
            html.Span(className="sc-value", children=f"{spnd}", id='rate-spending'),
    ]),

    html.Span(className="sc-min", children="0"),
    html.Span(className="sc-max", children="1 T"),
])


cards = dbc.Row([
    dbc.Col([
        dbc.Card([
            html.H4(high, className='card-title', style={'font-size': '35px', 'font-family': 'fantasy'}, id='high-spending'),
            html.Br(),
            html.Br(),
            html.P('Highest Country Spending', className='card_p'),
        ], className='cards', outline=False),
    ], width=4),

    dbc.Col([
        dbc.Card([
            ind,
            html.P('Highest Spending Rate ', className='card_p',),
            ], className='cards', outline=False),
    ], width=4),

    dbc.Col([
        dbc.Card([
            html.H4(low, style={'font-size': '35px', 'font-family': 'fantasy'}, id='low-spending'),
            html.Br(),
            html.Br(),
            html.P('Least Spending Country', className='card_p'),
            ], className='cards', outline=False),
    ], width=4),

], style={'text-align': '-webkit-center', 'margin-top':'10px'})


group_of_cards = dbc.Card([
    dbc.CardImg(src="./assets/image/1.jpg",
                top=True,
                style={"height": "270px","width": "100%"},
                ),
            dbc.CardImgOverlay(
                dbc.CardBody([cards]),
        ),
    ])


# ### ================================== Controls ==========================


slider = html.Div([
        dbc.Label("Year", html_for="slider"),
        
        dcc.Slider(id="slider",
                    min=pharma_data.Time.dt.year.unique().min(), 
                    max=pharma_data.Time.dt.year.unique().max(), 
                    step=None,
                    value=pharma_data.Time.dt.year.unique().min(),
                    marks={str(c) : str(c) for c in sorted(pharma_data.Time.dt.year.unique())},
                    persistence=True,
                    included=False
                    ),           
    ], className='slider-css')

dropdown1 = dcc.Dropdown(id='drop-scop',
                        options=['world', 'africa', 'asia', 'europe', 'north america', 'south america'],
                        value='world',
                        placeholder='select scope',
                        multi=False,
                        clearable=False,
                        searchable=True,
                        )

dropdown2 = dcc.Dropdown(id='drop-relation',
                        options=['PC_HEALTHXP', 'PC_GDP', 'USD_CAP', 'TOTAL_SPEND'],
                        value='TOTAL_SPEND',
                        placeholder='Another Perspectives',
                        multi=False,
                        clearable=False,
                        searchable=True,
                        )

dropdown3 = dcc.Dropdown(id='drop-country',
                        options=[{'label': i, 'value': i} for i in pharma_data['Country'].unique()],
                        value='',
                        placeholder='Select Country',
                        multi=True,
                        clearable=True,
                        searchable=True,
                        style={'margin': '0px', 'padding': '0px'}
                        )


controls = dbc.Row([
                dbc.Col([
                    slider
                        ], width=12),

                dbc.Col([
                    dropdown1
                        ], width=4),

                dbc.Col([
                    dropdown2
                        ], width=4),
                ], className='dropdown-row')


# ### ================================= Graphs ================================= 


graph1 = dbc.Row([
            controls,
            dbc.Row([
                dbc.Col([
                    dbc.Row([dcc.Graph(id='graph-1'),], style={'display': 'inline'}),
                        ], width=8),

                dbc.Col([
                    dbc.Card([
                    dbc.CardImg(src="", id='flag-1'),
                    dbc.CardBody([
                        html.Div(children=[], id='data-1'),
                ]),
            ], style={'display': 'contents'}, outline=False),

        ], width=3, id='map-card'),
    ], className='graph-row'),
], style={'margin': '15px 0px', 'margin': '15px 0px 5px 5px'})



graph2 = dbc.Row([
    dbc.Col([
        dbc.Row([
            dcc.Graph(id='graph-2'),
        ]),
    ], width=6),
    
    dbc.Col([#GDP based on purchasing-power-parity from 1985-2016 by country, Pharmaceutical Spending as % of GDP 1985-2016
            html.P(["GDP based on purchasing-power-parity from 1985-2016 by country"], style={'color': '#1675aa','font-size': '22px','font-family': 'fantasy'}),

            dbc.Row([
                dropdown3
            ], style={'width':'400px'}),
            
            dbc.Row([
                dcc.Graph(id='graph-3'),
            ]),
    ], width=6, style={'justify-content': 'center','text-align': '-webkit-center'}),
])


graph3= dbc.Row([
    dcc.Graph(id='graph-4'),
], style={'padding': '0px 30px 20px 30px'})


# ### ================================== Body ============================


content = dbc.Row([
    # html.Div(["Pharmaceutical Drug Spending by countries"]),
    group_of_cards,
    
    graph1,

    html.Div([
        html.Hr(style={'margin': '15px 0px 25px 0px', 'width': '84%', 'height':'3px', 'background-color': '#23809d', 'border-radius': '20px', 'box-shadow': '#054d63 0px 0px 2px 1px'}),
    ], style={'text-align': '-webkit-center'}),

    graph2,

    html.Div([
        html.Hr(style={'margin-top': '20px', 'width': '84%', 'height':'3px', 'background-color': '#23809d', 'border-radius': '20px', 'box-shadow': '#054d63 0px 0px 2px 1px'}),
    ], style={'text-align': '-webkit-center'}),
    graph3,

], className='content')


# ### ================================== Layout ==========================
# 


app.layout = html.Div([
    dbc.Col([
        header, 
        content,
    ])
], id='main-div', className="dbc")


# ### ================================== Callback ==========================


@app.callback(
    # first graph
    Output(component_id='graph-1', component_property='figure'),
    Output(component_id='data-1', component_property='children'),
    Output(component_id='flag-1', component_property='src'),

    # BANS
    Output(component_id='rate-spending', component_property='children'),
    Output(component_id='sc-percentage', component_property='style'),
    Output(component_id='high-spending', component_property='children'),
    Output(component_id='low-spending', component_property='children'),
    
    Input(component_id='slider', component_property='value'),
    Input(component_id='drop-relation', component_property='value'),
    Input(component_id='drop-scop', component_property='value'),
    Input(component_id='graph-1', component_property='hoverData'),
    
)
# +============================================================================= [Function] =============================================================================
def map_graph(input_value, drop_relation, drop_scop, graph_input):
    time = input_value; 
    colors = drop_relation; 
    scope = drop_scop
    df = pharma_data[pharma_data.Time.dt.year==time].sort_values(by='TOTAL_SPEND', ascending=True)
    COLOR ="#0691be"
    TCOLOR ='#1675aa'

# ========================== {first graph} ======================================================
    fig = px.choropleth(df, 
    locations="Location", 
    color=drop_relation, 
    hover_name="Country", 
    scope=drop_scop.lower(), width=800, height=400, 
    # projection="natural earth"
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="#e5efe7",
            showocean=True,
            oceancolor="#b2dcf6",
            showcountries=True,
            projection_type="equirectangular",
            bgcolor="rgba(0,0,0,0)",
            ),
        font=dict(family="fantasy", size=15, color="#4143BF"),
        title=f"{colors.replace('_', ' ')} in {time} in {scope}",
        title_font_color=TCOLOR,
        title_x=0.5,
        margin=dict(pad=0, l=0, r=0, t=60, b=10),
    )

    fig.update_coloraxes(
        colorbar=dict(
            title=colors.replace('_', ' ').title(),
            ticks="outside",
            ticklen=3,
            len=0.7,
            thickness=15,
        ),
        )

        
# ---------------------------------------------------[BANS part]-------------------------------------------------------------
    high=None; low=None; high_spend=None; high_spend_value=None
    df_BANS = df.sort_values(by='TOTAL_SPEND', ascending=False).head(1)

    high = df_BANS['Country'].values[0]
    low = df.head(1)['Country'].values[0]

    high_spend = df_BANS['TOTAL_SPEND'].values[0]
    high_spend_value = 180 * (high_spend/1000_000)

# ---------------------------------------------------[Map part]-----------------------------------------------------
    load_data = json.loads(json.dumps(graph_input))
    # card_vis = 'visible'
    flag = None
    summary_data = None
    
    if load_data:
        cond_details = (pharma_data.Time.dt.year == time) & (pharma_data.Country == load_data['points'][0]['hovertext'])
        summary_data = pharma_data[cond_details].to_dict('records')
        if summary_data:
            flag = pharma_data[pharma_data.Country == load_data['points'][0]['hovertext']]['Flag'].unique()[0]
        
            x1 = summary_data[0]['Location']
            x2 = summary_data[0]['Country']
            x3 = summary_data[0]['Time'].year
            x4 = summary_data[0]['TOTAL_SPEND']
            x5 = summary_data[0]['PC_GDP']
            x6 = summary_data[0]['PC_HEALTHXP']
            x7 = summary_data[0]['USD_CAP']
        
            table_data = pd.DataFrame.from_dict({
                '-':['🌏', '🌍', '⏳', '💵', '💰', '💉', '🧍🏻‍♂️'],
                'Summary':['Country', 'Country Code', 'Year ', 'Total Spend $', 'GDP %', 'Health Expenditure %', 'USD Capita'],
                'value':[x2, x1, x3, x4, x5, x6, x7]})

            summary_data = dash_table.DataTable(data=table_data.to_dict(orient = 'records'), 
                                                cell_selectable=False, 
                                                style_table={'border-radius': '10px', 'background-color': 'transparent'}, 
                                                style_cell={'backgroundColor': 'transparent','textAlign': 'center', 'font-size': '13px', 'font-family': 'Arial', 'margin': '2px', 'padding': '6px'})
        else:
            flag = pharma_data[pharma_data.Country == load_data['points'][0]['hovertext']]['Flag'].unique()[0]
            summary_data = f"No Data per {load_data['points'][0]['hovertext']} in this {time}"
    else:
        tb = pharma_data[pharma_data.Country == high].values[0]
        table_data = pd.DataFrame.from_dict({
            '-':['🌏', '🌍', '⏳', '💵', '💰', '💉', '🧍🏻‍♂️'],
            'Summary':['Country', 'Country Code', 'Year ', 'Total Spend $', 'GDP %', 'Health Expenditure %', 'USD Capita'],
            'value':[tb[2], tb[1], tb[4].year, tb[8], tb[6], tb[5], tb[7]]})

        flag=tb[3]
        summary_data = dash_table.DataTable(data=table_data.to_dict(orient = 'records'), 
                                            cell_selectable=False, 
                                            style_table={'border-radius': '10px', 'background-color': 'transparent'}, 
                                            style_cell={'backgroundColor': 'transparent','textAlign': 'center', 'font-size': '13px', 'font-family': 'Arial', 'margin': '2px', 'padding': '6px'}
                                            )
        
        
    return fig, summary_data, flag, money(high_spend * 1000_000), {'transform': f'rotate({high_spend_value}deg)'}, high, low


# #### Line Graph
@app.callback(
    Output(component_id='graph-3', component_property='figure'),
    Input(component_id='drop-country', component_property='value')
)

def update_graph(drop_country):
    cont = list(drop_country) #dropdown Country
    COLOR="#0691be"
    TCOLOR='#1675aa'

    if cont != []:
        line_fig = px.line(
            data_frame=pharma_data[pharma_data.Country.isin(cont)].sort_values('Time'),
            x='Time',
            y='PC_GDP',
            color='Country',
            markers=True,
            # title=f'Pharmaceutical Spending in{cont} as % of GDP 1985-2016',
            # width=600,
            # height=600,
            line_shape='spline',
        )
    else:
        line_fig = px.line(
        data_frame=pharma_data[pharma_data.Country.isin(["Japan"])].sort_values('Time'),
        x='Time',
        y='PC_GDP',
        color='Country',
        markers=True,
        # width=600,
        # height=600,
        line_shape='spline',
    )

    # update layout properties
    line_fig.update_layout(
        autosize=True,
        height=600,
        width=600,
        bargap=0.04,
        bargroupgap=0.05,
        margin=dict(pad=0, l=0, r=0, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Time",
        xaxis_title_font_family='system-ui',
        xaxis_tickfont_size=14,
        xaxis_tickfont_family='system-ui',
        xaxis_tickangle=45,
        yaxis_title="GDP percent",
        yaxis_title_font_family='system-ui',
        yaxis_tickfont_family='system-ui',
        xaxis =  {'showgrid': True, 'gridcolor': '#BFBFBF', 'gridwidth': 1, 'zeroline': True, 'showline': True, 'linecolor': '#BFBFBF', 'linewidth': 1},
        yaxis = {'showgrid': False},
        
        
        xaxis_tickfont_color=COLOR,
        xaxis_title_font_color=COLOR,
        yaxis_title_font_color=COLOR,
        yaxis_tickfont_color=COLOR,
        legend_font_color=COLOR,
    )

    return line_fig


# ### Horizontal Bar Chart


@app.callback(
    Output(component_id='graph-2', component_property='figure'),
    Input(component_id='slider', component_property='value'),
)

def update_graph3(input_value):
    time = input_value
    df = pharma_data[pharma_data.Time.dt.year==time].sort_values(by='TOTAL_SPEND', ascending=True)
    COLOR="#0691be"
    TCOLOR='#1675aa' #64c571

    fig2 = px.bar(data_frame=df.head(20),
        y='Country', 
        width=600,
        height=600,
        x='TOTAL_SPEND', 
        orientation='h', 
        hover_data={'Country':False, 'TOTAL_SPEND':True, 'Location':False, 'Flag':False, 'Time':True},
        # facet_col_wrap=2,
        # facet_col_spacing=1,
        log_x=True,
        hover_name='Country',
        opacity=1,
        text_auto=True,
        # color_discrete_sequence =['green']*len(df),
    )
    
    fig2.update_traces(marker_color='#158bcc', textposition='inside')
    # update layout properties
    fig2.update_layout(
    autosize=True,
    # height=600,
    # width=600,
    bargap=0.04,
    bargroupgap=0.05,
    title=f"Top(20) Countries Spending The Most For Medicinal Drugs in {time}",
    title_x=0.5,
    title_font_size=22,
    title_font_family='fantasy',

    margin=dict(pad=0, l=0, r=0, t=60, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    xaxis_title="Total Expenditure (USD)",
    xaxis_title_font_family='system-ui',
    
    xaxis_tickfont_size=14,
    xaxis_tickfont_family='system-ui',
    xaxis_tickangle=45,
    xaxis_showgrid=True,
    yaxis_showgrid=False,
    yaxis_title="Country",
    yaxis_title_font_family='system-ui',
    yaxis_tickfont_family='system-ui',

    title_font_color=TCOLOR,
    yaxis_tickfont_color=COLOR, 
    yaxis_title_font_color=COLOR,
    xaxis_tickfont_color=COLOR, 
    xaxis_title_font_color=COLOR
    )
    return fig2


# #### Double Vertical Bar Chart


@app.callback(
    Output(component_id='graph-4', component_property='figure'),
    Input(component_id='slider', component_property='value'),
)

def update_graph(input_value):
    time = input_value; 
    df = pharma_data[pharma_data.Time.dt.year==time].sort_values(by='TOTAL_SPEND', ascending=False)

    c = df['Country'].to_list()
    cp = df['PC_GDP'].tolist()
    ch = df['PC_HEALTHXP'].tolist()
    
    COLOR="#0691be"
    TCOLOR='#1675aa'

    double_bar_fig = go.Figure()

    double_bar_fig.add_trace(
        go.Scatter(
            x=c,
            y=cp,
            name="USD per capita",
            mode='lines+markers', 
            marker= dict(size=7,
            symbol = 'diamond',
            color ='RGB(251, 177, 36)',
            line_width = 2
            ),
            line = dict(color='firebrick', width=3)
        )
        )

    double_bar_fig.add_trace(
        go.Bar(
        x=c,
        y=ch,
        name="% Health Spending",
        text = df['PC_HEALTHXP'],
        textposition='outside',
        textfont=dict(
        size=13,
        color='#158bcc')
    )
    )

    double_bar_fig.update_traces(texttemplate='%{text:.2s}', marker_color='#158bcc')
    double_bar_fig.update_layout(
        barmode='group', 
        # xaxis_tickangle=-45, 
        autosize=True,
        height=600,
        # width=600,
        bargap=0.04,
        bargroupgap=0.05,
        title=f"Analysis Countries by Health Expenditure and GDP per Capita in {time}",
        title_x=0.5,
        title_font_size=22,
        title_font_family='fantasy',
        
        
        margin=dict(pad=0, l=0, r=0, t=65, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        xaxis_title="Country",
        xaxis_title_font_family='system-ui',
        xaxis_tickfont_size=14,
        xaxis_tickfont_family='system-ui',
        xaxis_tickangle=45,
        xaxis_showgrid=False,

        yaxis_title="% of GDP \n % of Health Spending",
        yaxis_title_font_family='system-ui',
        yaxis_tickfont_family='system-ui',
        yaxis_showgrid=True,

        legend_orientation="h",
        legend_x=0.7,
        legend_y=1.2,
        legend_title="Legend",
        legend_title_font_size=14,
        # legend_title_font_family='fantasy',
        legend_font_size=13,
        legend_font_family='system-ui',

        title_font_color=TCOLOR,
        yaxis_title_font_color=COLOR,
        yaxis_tickfont_color=COLOR,
        xaxis_title_font_color=COLOR,
        legend_title_font_color=COLOR,
        legend_font_color=COLOR,
        xaxis_tickfont_color=COLOR,
    )
    return double_bar_fig


# #### Run Server
if __name__ == '__main__':
    app.run_server(debug=True)