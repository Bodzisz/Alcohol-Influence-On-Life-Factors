import pandas as pd
import requests
from bs4 import BeautifulSoup

ALCOHOL_DATA_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita"
HAPPINESS_DATA_URL = "https://en.wikipedia.org/wiki/World_Happiness_Report"
LIFE_EXPECTANCY_DATA_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy"
GDP_DATA_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita"


def get_wiki_data(url, table_num, backup_filename=None, multi_index=False):
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        indiatable = soup.find('table', {'class': "wikitable"})
        df = pd.read_html(str(indiatable))
        return pd.DataFrame(df[table_num])
    else:
        if backup_filename is not None:
            if not multi_index:
                df = pd.read_csv("data_backup/" + backup_filename + ".csv")
            else:
                df = pd.read_csv("data_backup/" + backup_filename + ".csv", header=[0, 1])
                df.columns = pd.MultiIndex.from_tuples(df.columns)
            return df
        else:
            raise Exception("Data fetching failed!")


def get_alcohol_per_capita_data():
    df = get_wiki_data(ALCOHOL_DATA_URL, 0, "alcohol_per_capita")
    df = df[['Country', '2016[8]']].copy()
    df = df.rename(columns={'2016[8]': 'Alcohol_per_capita'})
    df['Alcohol_per_capita'] = pd.to_numeric(df['Alcohol_per_capita'], errors='coerce')
    return df


def get_happiness_data():
    df = get_wiki_data(HAPPINESS_DATA_URL, 0, "happiness")
    df = df[['Country or region', 'Score']].copy()
    df = df.rename(columns={'Country or region': 'Country', 'Score': 'Happiness'})
    return df


def get_life_expectancy_data():
    df = get_wiki_data(LIFE_EXPECTANCY_DATA_URL, 0, "life_expectancy")
    df = df[['Countries', 'all']].copy()
    df = df.rename(columns={'Countries': 'Country', 'all': 'Life_expectancy'})
    return df


def get_gdp_data():
    df = get_wiki_data(GDP_DATA_URL, 0, "gdp_per_capita", True)
    df = df.loc[:, (['Country/Territory', 'World Bank[7]'], ['Country/Territory', 'Estimate'])]
    df.columns = ['Country', 'GDP']
    df['Country'] = df['Country'].map(lambda x: x.replace('\u202f*', ''))
    return df


def unify_countries(df1, df2, df3, df4):
    countries = list(set(df1['Country']) & set(df2['Country']) & set(df3['Country']) & set(df4['Country']))
    df1 = df1[df1['Country'].isin(countries)]
    df2 = df2[df2['Country'].isin(countries)]
    df3 = df3[df3['Country'].isin(countries)]
    df4 = df4[df4['Country'].isin(countries)]
    return df1, df2, df3, df4


def get_data():
    alcohol_per_capita = get_alcohol_per_capita_data()
    hapiness = get_happiness_data()
    life_expectancy = get_life_expectancy_data()
    gdp_data = get_gdp_data()

    alcohol_per_capita, hapiness, life_expectancy, gdp_data = unify_countries(alcohol_per_capita, hapiness,
                                                                              life_expectancy, gdp_data)

    data = pd.merge(alcohol_per_capita, hapiness, on='Country')
    data = pd.merge(data, life_expectancy, on='Country')
    data = pd.merge(data, gdp_data, on='Country')
    return data
