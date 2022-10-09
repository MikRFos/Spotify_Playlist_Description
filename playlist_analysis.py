import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from database import Song
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)



class PlaylistAnalysis:
    def __init__(self, song_list: list):
        self.playlist_df = pd.DataFrame(song_list)

    def get_data(self):
        return self.playlist_df

    def get_common(self, category: str):
        return str(self.playlist_df[category].mode()[0])

    def get_average(self, category: str):
        return float(self.playlist_df[category].mean())

    def plot_data(self, category: str):
        unique_values = self.playlist_df[category].unique()
        data = [(self.playlist_df[category].values == val).sum() for val in unique_values]
        ind = np.arange(len(unique_values))
        big_x = [num for num in ind]

        fig, ax = plt.subplots()
        bars = ax.bar(big_x, data, align="center")

        ax.set_ylabel("Songs")
        ax.set_title(f"Number of Songs of each {category.title()}")
        ax.set_xticks(big_x, labels=unique_values)
        ax.legend()

        plt.xticks(rotation=45)
        ax.bar_label(bars)
        fig.set_figwidth(15)
        fig.tight_layout()

        return fig
