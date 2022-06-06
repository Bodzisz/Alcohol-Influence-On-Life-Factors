import numpy as np
import matplotlib.pyplot as plt
from data_processor import get_data


def make_plot(x, y, degree, xlim, ylim,ylabel, filename):
    fx = np.linspace(min(x), max(x), 100)
    coefs = np.polyfit(x, y, degree)
    fitted_curve = np.poly1d(coefs)(fx)

    plt.clf()
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    plt.title("Linear model")
    plt.xlabel("Alcohol per person")
    plt.ylabel(ylabel)
    plt.scatter(x, y, label="observed")
    plt.plot(fx, fitted_curve, c="red", label="fitted")
    plt.grid()
    plt.savefig('plots/' + filename)


# Data: ['Country, 'Alcohol_per_capita, 'Hapiness', 'Life_expectancy', 'GDP']
data = get_data()

for degree, appender in [(1, 'linear'), (4, 'poly')]:
    make_plot(data['Alcohol_per_capita'], data['Happiness'], degree, (0, 16), (3, 8),
                 'Hapinness', 'happiness_dependence_' + appender)
    make_plot(data['Alcohol_per_capita'], data['Life_expectancy'], degree, (0, 16), (50, 90),
                 'Life expectancy', 'life_expectancy_dependence_' + appender)
    make_plot(data['Alcohol_per_capita'], data['GDP'], degree, (0, 16), (1000, 40000),
                 'GDP per capita', 'GDP_dependence_' + appender)

