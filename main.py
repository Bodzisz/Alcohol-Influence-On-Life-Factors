import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


def get_wiki_data(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        indiatable = soup.find('table', {'class': "wikitable"})
    else:
        raise Exception("Data fetching failed!")
    return pd.read_html(str(indiatable))


def get_alcohol_per_capita_data():
    df = get_wiki_data("https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita")
    df = pd.DataFrame(df[0])
    df = df[['Country', '2016[8]']].copy()
    df = df.rename(columns={'2016[8]': 'Alcohol_per_capita'})
    df['Alcohol_per_capita'] = pd.to_numeric(df['Alcohol_per_capita'], errors='coerce')
    return df


def get_happiness_data():
    df = get_wiki_data("https://en.wikipedia.org/wiki/World_Happiness_Report")
    try:
        df = pd.DataFrame(df[4])    # 2016 data
    except IndexError:
        df = pd.DataFrame(df[0])
    df = df[['Country or region', 'Score']].copy()
    df = df.rename(columns={'Country or region': 'Country', 'Score': 'Happiness'})
    return df


def get_life_expectancy_data():
    df = get_wiki_data("https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy")
    df = pd.DataFrame(df[0])
    df = df[['Countries', 'all']].copy()
    df = df.rename(columns={'Countries': 'Country', 'all': 'Life_expectancy'})
    return df

def get_gdp_data():
    df = get_wiki_data("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita")
    df = pd.DataFrame(df[0])
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
    return df1, df2, df3


def make_plot_linear_regression(x, y, xlim=(0, 10), ylim=(0, 10), filename='plot'):
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)

    plt.plot(x, y, 'yo', x, poly1d_fn(x), '--k')

    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    plt.savefig(filename)


alcohol_per_capita = get_alcohol_per_capita_data()
hapiness = get_happiness_data()
life_expectancy = get_life_expectancy_data()
gdp_data = get_gdp_data()

alcohol_per_capita, hapiness, life_expectancy = unify_countries(alcohol_per_capita, hapiness, life_expectancy, gdp_data)

data = pd.merge(alcohol_per_capita, hapiness, on='Country')
data = pd.merge(data, life_expectancy, on='Country')
data = pd.merge(data, gdp_data, on='Country')

# Data: ['Country, 'Alcohol_per_capita, 'Hapiness', 'Life_expectancy']

# print(data.values)
# print(len(data.values))

make_plot_linear_regression(data['Alcohol_per_capita'], data['Happiness'], (0, 16), (3, 8), 'happiness_dependence')
make_plot_linear_regression(data['Alcohol_per_capita'], data['Life_expectancy'], (0, 16), (50, 90),
                            'life_expectancy_dependence')
make_plot_linear_regression(data['Alcohol_per_capita'], data['GDP'], (0, 16), (1000, 40000),
                            'GDP_dependence')

