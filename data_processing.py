import pandas as pd

def load_data():
    # Load income data
    df_income = pd.read_csv('data/median_household_income.csv')
    df_income.rename(columns={'observation_date': 'Date', 'MEHOINUSCAA646N': 'Income'}, inplace=True)
    df_income['Date'] = pd.to_datetime(df_income['Date'])
    df_income['Year_only'] = df_income['Date'].dt.year

    # Load housing data
    df_housing = pd.read_csv('data/ZHVI.csv')
    df_housing.rename(columns={'observation_date': 'Date', 'CAUCSFRCONDOSMSAMID': 'Housing_Price'}, inplace=True)
    df_housing['Date'] = pd.to_datetime(df_housing['Date'])
    df_housing['Year_only'] = df_housing['Date'].dt.year


    # Load gas price data
    df_gas = pd.read_csv("./data/gas_prices.csv", skiprows=4)
    df_gas.columns = ["Month", "Gas_Price"]
    df_gas["Date"] = pd.to_datetime(df_gas["Month"], format="%b %Y")
    df_gas['Year_only'] = df_gas['Date'].dt.year
    df_gas["Gas_Price"] = pd.to_numeric(df_gas["Gas_Price"], errors="coerce")



    # Load minimum wage data
    df_wage = pd.read_csv('data/min_wage.csv')
    df_wage.rename(columns={'observation_date': 'Date', 'STTMINWGCA': 'Wage'}, inplace=True)
    df_wage['Date'] = pd.to_datetime(df_wage['Date'])
    df_wage['Year_only'] = df_wage['Date'].dt.year


    return df_income, df_wage, df_housing, df_gas
