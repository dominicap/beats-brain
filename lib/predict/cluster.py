import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sqlite3

from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering


def main():
    dataframe = dataframe_from_database('db/billboard-200.db',
                                        'acoustic_features')
    dataframe.index = dataframe['song'] + ' ' + dataframe['artist']

    dataframe = dataframe.dropna()

    columns = ['id', 'song', 'album', 'artist', 'album_id', 'date']
    dataframe = dataframe.drop(columns=columns)

    values = dataframe.values
    scaler = preprocessing.MinMaxScaler()
    values = scaler.fit_transform(values)

    dataframe = pd.DataFrame(values, columns=dataframe.columns, index=dataframe.index)

    sample = dataframe.sample(frac=0.01)

    cluster = AgglomerativeClustering(n_clusters=(int(0.01 * len(dataframe) * 0.5)))
    cluster.fit(sample)

    sample['labels'] = cluster.labels_

    sample = sample.sort_values(by=['labels'])
    sample.to_csv('sample.csv')


def dataframe_from_database(database, table):
    connection = sqlite3.connect(database)
    query = "SELECT * FROM" + " " + table

    return pd.read_sql_query(query, connection)


if __name__ == '__main__':
    main()
