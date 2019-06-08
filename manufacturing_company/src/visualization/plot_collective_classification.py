import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from manufacturing_company.src.common.const import *


class PlotCollectiveClassification:
    def __init__(self, path, levels, random_baseline):
        self.path = path
        self.levels = levels
        self.random_baseline = random_baseline
        self.colors = ['red', 'blue', 'black', '#2FBF71', '#FAA916']
        self.markers = ['D', 's', '<', 'o', 'X']
        self.linestyles = ['--', '-', '--', '-', '--']
        self.x_labels = ['90%', '80%', '70%', '60%', '50%', '40%', '30%', '20%', '10%']

    def plot(self):
        sns.set_style("darkgrid")
        sns.set_context("notebook")

        plt.figure(figsize=(10, 6))

        for month in range(1, MONTHS):
            df = pd.read_csv(self.path + '/log_months_' + str(month) + '.csv', sep=';')
            result_series = df.groupby('pct')['f1_score'].max()
            result_series = result_series.sort_index(ascending=False)
            plt.plot(self.x_labels, result_series.tolist(), label=str(month), linestyle=self.linestyles[month-1], marker=self.markers[month-1], color=self.colors[month-1])

        # random result is approximately 0.42 based on the results from random_classification.ipynb

        random_values = [self.random_baseline(self.levels)]*9
        plt.plot(self.x_labels, random_values, label='random', linestyle=':', marker='*', color='black')

        plt.legend(loc='lower left', fontsize='small')
        plt.xlim(-1, 9)
        plt.ylim(0, 1.2)
        plt.xticks(np.arange(0,10))
        plt.xlabel('Percentage of the used features')
        plt.ylabel('f1 score (macro)')
        plt.title('CollectiveClassification - ' + str(self.levels) + ' management levels')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Minimum activity in months')
        plt.savefig(self.path + '/plot.eps', bbox_inches='tight', format='eps')


