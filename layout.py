from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def create_layout():
    """Creates the layout for the app."""
    return dbc.Container([
        # Title
        dbc.Row(
            dbc.Col([html.H2(
                    "California Socioeconomic Data Visualization",
                    className="text-center bg-primary text-white p-2",
                    ),
                html.H4(
                    "Meghan Nugent CS-150 Community Action Computing",
                    className="text-center bg-primary text-white p-2"
                )]
            )
        ),

        # Tab Layout
        dbc.Tabs([
            # Data Visualizations Tab
            dbc.Tab(label='Data Visualizations', children=[
                dbc.Row([
                    # Left column - Inputs
                    dbc.Col([
                        dcc.Dropdown(
                            id='data-dropdown',
                            options=[
                                {'label': 'Income', 'value': 'income'},
                                {'label': 'Housing Prices', 'value': 'housing'},
                                {'label': 'Gas Prices', 'value': 'gas'},
                                {'label': 'Minimum Wage', 'value': 'wage'}
                            ],
                            value='income',
                            className="mb-3"
                        ),
                        html.Label("Choose a Year Range"),
                        dcc.RangeSlider(
                            id='year-slider',
                            min=2001,
                            max=2023,
                            step=1,
                            marks={i: str(i) for i in range(2001, 2023, 3)},
                            value=[2001, 2023],
                            className="mb-4"
                        ),
                        html.Label("Choose Desired Income ($): "),
                        dcc.Input(id="desired-income", type="number", value=50000, step=1000),
                        html.Br(),
                        html.Label("Enter Gallons of Gas Used: "),
                        dcc.Input(id="gallons-of-gas", type="number", value=50, step=1),
                    ], width=4),

                    dbc.Col([
                        dcc.Graph(id='line-chart', className="mb-4"),
                        dcc.Graph(id='stacked-bar')
                    ], width=8),
                ])
            ]),

            # Results Tab
            dbc.Tab(label='Results', children=[
                dbc.Row([
                    dbc.Col([
                        html.H4('Summary Table', className="mt-4"),
                        dash_table.DataTable(
                            id='summary-table',
                            columns=[
                                {"name": "Date", "id": "Year_only"},
                                {"name": "Income ($)", "id": "Income"},
                                {"name": "Housing Price ($)", "id": "Housing_Price"},
                                {"name": "Gas Price ($/gal)", "id": "Gas_Price"},
                                {"name": "Min Wage ($/hr)", "id": "Wage"}
                            ],
                            page_size=15,
                            style_table={'height': '400px', 'overflowY': 'auto'},
                            style_cell={'textAlign': 'center'}
                        ),
                    ], width=12),
                ])
            ]),

            # About Tab
            dbc.Tab(label='About', children=[
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H3("California Socioeconomic Data Dashboard"),
                        html.P(
                            "This dashboard provides an interactive overview of key socioeconomic data for California between the years of 2001 - 2023. "
                            "The data includes household income, gas prices, housing prices, and minimum wage trends over the years."
                        ),
                    ], className="p-4"), width=12)
                ])
            ])
        ]),

        # Footer
        html.Footer(
            html.Div(
                "Created by Meghan Nugent | CS-150 Community Action Computing",
                className="footer text-center"
            )
        )
    ], fluid=True)
