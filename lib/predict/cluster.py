import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
import sqlite3
import sys

from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
from sklearn.externals import joblib
from azureml.core import Workspace
from azureml.core.model import Model


ws = Workspace.get(name="beatsBrain-local", subscription_id='66f8937f-1057-4155-aefd-52c32c7de0d5', resource_group='beats-brain')

library = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(library)

import data.search as search


def cluster(token):
    storage = pd.HDFStore('models/dataframes/preprocessed_dataframe.h5')

    dataframe = __dataframe_from_database('lib/predict/db/billboard-200.db', 'acoustic_features')
    dataframe = __preprocessd_dataframe(dataframe, token)

    storage.put('preprocessd_dataframe', dataframe, format='table', data_columns=True)
    storage.close()

    dataframe = pd.read_hdf('models/dataframes/preprocessed_dataframe.h5')

    sample = dataframe.sample(frac=0.25)

    cluster = AgglomerativeClustering(n_clusters=(int(len(sample) * 0.5)))
    cluster.fit(sample)

    joblib.dump(value=cluster, filename="cluster.pkl")

    model = Model.register(workspace=ws, model_path="cluster.pkl", model_name="cluster")
    model.download(target_dir=os.getcwd(),exist_ok = True)

    sample['labels'] = cluster.labels_

    sample = sample.sort_values(by=['labels'])
    sample.to_csv('models/samples/sample.csv')


def __preprocessd_dataframe(dataframe, token):
    dataframe.index = dataframe['song'] + ' - ' + dataframe['artist']
    dataframe = dataframe.dropna().head(100)

    key_genres = ['rap', 'trap', 'hip', 'hop', 'hip-hop', 'hip hop']
    dataframe = __remove_genres(dataframe, token, key_genres)

    columns = ['id', 'song', 'album', 'artist', 'album_id', 'date']
    dataframe = dataframe.drop(columns=columns)

    dataframe = __normalize(dataframe)

    return dataframe


def __remove_genres(dataframe, token, key_genres):
    for index, row in dataframe.iterrows():
        track_id = row['id']
        genres = search.search_artist_genres(token, track_id)

        for genre in genres:
            if not any(key_genre in genre for key_genre in key_genres):
                dataframe = dataframe.drop(str(index), axis=0)

    return dataframe


def __normalize(dataframe):
    values = dataframe.values
    scaler = preprocessing.MinMaxScaler()
    values = scaler.fit_transform(values)

    dataframe = pd.DataFrame(values, columns=dataframe.columns, index=dataframe.index)

    return dataframe


def __dataframe_from_database(database, table):
    connection = sqlite3.connect(database)
    query = "SELECT * FROM" + " " + table

    return pd.read_sql_query(query, connection)
