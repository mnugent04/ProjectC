from dash import Input, Output
import pandas as pd

from data_processing import load_data
import plotly.graph_objects as go


df_income, df_wage, df_housing, df_gas = load_data()

def register_callbacks(app):
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('data-dropdown', 'value'),
         Input('year-slider', 'value')
         ]
    )
    def update_line_chart(data_type, year_range):
        start_year, end_year = year_range
        if data_type == 'income':
            filtered_df = df_income[(df_income['Year_only'] >= start_year) & (df_income['Year_only'] <= end_year)]
            fig = go.Figure(
                data=go.Scatter(x=filtered_df['Year_only'], y=filtered_df['Income'], mode='lines', name='Income'))
        elif data_type == 'housing':
            filtered_df = df_housing[(df_housing['Year_only'] >= start_year) & (df_housing['Year_only'] <= end_year)]
            fig = go.Figure(data=go.Scatter(x=filtered_df['Year_only'], y=filtered_df['Housing_Price'], mode='lines',
                                            name='Housing Prices'))
        elif data_type == 'gas':
            filtered_df = df_gas[(df_gas['Year_only'] >= start_year) & (df_gas['Year_only'] <= end_year)]
            fig = go.Figure(
                data=go.Scatter(x=filtered_df['Year_only'], y=filtered_df['Gas_Price'], mode='lines', name='Gas Prices'))
        elif data_type == 'wage':
            filtered_df = df_wage[(df_wage['Year_only'] >= start_year) & (df_wage['Year_only'] <= end_year)]
            fig = go.Figure(
                data=go.Scatter(x=filtered_df['Year_only'], y=filtered_df['Wage'], mode='lines', name='Min Wage'))

        fig.update_layout(title=f'{data_type.capitalize()} Over Time', xaxis_title='Year',
                          yaxis_title=data_type.capitalize())
        return fig

    # Bar chart callback
    @app.callback(
        Output('stacked-bar', 'figure'),
        [Input('desired-income', 'value'),
         Input('gallons-of-gas', 'value'),
         Input('year-slider', 'value')]
    )
    def update_stacked_bar(income, gas, year_range):
        start_year, end_year = year_range

        # Calculate the cost of gas based on user input and average gas prices
        avg_gas_price = df_gas[df_gas['Year_only'] == end_year]['Gas_Price'].mean()
        gas_cost = avg_gas_price * gas

        # Calculate monthly mortgage payments, with 7% interest
        avg_house_price = df_housing[df_housing['Year_only'] == end_year]['Housing_Price'].mean()
        r = 0.07 / 12
        n = 30 * 12
        mortgage_payment = avg_house_price * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

        # Calculate monthly income
        if income is None or income <= 0:
            income = 20000  # Set a minimum positive value to avoid errors

        # Calculate monthly income
        monthly_income = income // 12

        # Calculate min-wage
        min_wage = df_wage[df_wage['Year_only'] == end_year]['Wage'].mean()
        min_wage = ((min_wage * 40) * 4)

        # Calculate average income
        avg_income = df_income[df_income['Year_only'] == end_year]['Income'].mean()
        avg_income = avg_income // 12

        bars = [
            go.Bar(name='Gas Costs', y=['Expenses'], x=[gas_cost], orientation='h'),
            go.Bar(name='House Payments', y=['Expenses'], x=[mortgage_payment], orientation='h')
        ]

        if gas_cost + mortgage_payment < monthly_income:
            bars.append(go.Bar(name='Other', y=['Expenses'], x=[monthly_income - gas_cost - mortgage_payment], orientation='h'))

        fig = go.Figure(data=bars)


        fig.update_layout(
            barmode='stack',
            title=f'Income Breakdown for {end_year}',
            yaxis_title='Categories',
            xaxis_title='Amount ($)',
            xaxis=dict(
                range=[0, 20000],
                fixedrange=True
            ),
            width=800,
        )

        fig.update_layout(
            shapes=[
                dict(
                    type='line',
                    x0=monthly_income,
                    y0=0,
                    x1=monthly_income,
                    y1=1,
                    yref='paper',
                    line=dict(
                        color='#fd7e14',
                        width=3,
                        dash='dashdot'
                    ),
                    name='Monthly Income'
                ),
                dict(
                    type='line',
                    x0=min_wage,
                    y0=0,
                    x1=min_wage,
                    y1=1,
                    yref='paper',
                    line=dict(
                        color='#446e9b',
                        width=3,
                        dash='dashdot'
                    ),
                    name='Min Wage'
                ),
                dict(
                    type='line',
                    x0=avg_income,
                    y0=0,
                    x1=avg_income,
                    y1=1,
                    yref='paper',
                    line=dict(
                        color='#FF69B4',
                        width=3,
                        dash='dashdot'
                    ),
                    name='Avg Income'
                )
            ]
        )

        # Labels
        fig.update_layout(
            annotations=[
                dict(
                    x=monthly_income + 2700,
                    y=1.05,
                    xref='x',
                    yref='paper',
                    text=f"Desired Monthly Income: ${monthly_income}",
                    showarrow=False,
                    font=dict(
                        color='#fd7e14',
                        size=13,
                    ),
                    xshift=10,
                ),
                dict(
                    x=min_wage + 2900,
                    y=0.02,
                    xref='x',
                    yref='paper',
                    text=f"Minimum Wage: ${min_wage}",
                    showarrow=False,
                    font=dict(
                        color='#446e9b',
                        size=13,
                    ),
                    xshift=-10
                ),
                dict(
                    x=avg_income + 2850,
                    y=0.5,
                    xref='x',
                    yref='paper',
                    text=f"Average Wage: ${avg_income}",
                    showarrow=False,
                    font=dict(color='#FF69B4', size=13),
                    xshift=-10
                )
            ]
        )

        return fig

    # Callback to update the summary table based on the selected year range
    @app.callback(
        Output('summary-table', 'data'),
        [Input('year-slider', 'value')]
    )
    def update_summary_table(year_range):
        start_year, end_year = year_range
        # Filter data based on selected year range and combine relevant data into a table
        filtered_df = pd.merge(
            df_income[(df_income['Year_only'] >= start_year) & (df_income['Year_only'] <= end_year)],
            df_housing[(df_housing['Year_only'] >= start_year) & (df_housing['Year_only'] <= end_year)],
            on='Year_only',
            suffixes=('_income', '_housing')
        )

        filtered_df = pd.merge(
            filtered_df,
            df_wage[(df_wage['Year_only'] >= start_year) & (df_wage['Year_only'] <= end_year)],
            on='Year_only',
            suffixes=('_summary', '_wage')
        )
        filtered_df = pd.merge(filtered_df, df_gas[(df_gas['Year_only'] >= start_year) & (df_gas['Year_only'] <= end_year)],
                               on='Year_only',)

        # Return the data to the table
        return filtered_df.to_dict('records')
