import pandas as pd
import os


class Data:
    def __init__(self, train_path=None):
        self.train_path = train_path if train_path else os.path.abspath(os.path.dirname(__name__)) + '\\petfinder-adoption-prediction\\train\\train.csv'
        # Lecture du fichier des données d'entrainement
        self.df = pd.read_csv(self.train_path, sep=',')
        self.columns_names = self.df.columns.values.tolist()

    def get_description(self):
        return self.df['Description'].tolist()

    def show_columns_names(self):
        print(self.columns_names)

if __name__ == '__main__':
    datas = Data()
    print("Done.")
