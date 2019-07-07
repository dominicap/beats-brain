import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
import sqlite3
import sys

from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
from sklearn.mixture import GaussianMixture as mixture
from sklearn.externals import joblib

from azureml.core import Workspace
from azureml.core.model import Model

ws = Workspace.get(name="beatsBrain-local4", subscription_id='66f8937f-1057-4155-aefd-52c32c7de0d5', resource_group='beats-brain')
library = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(library)

import data.search as search


from pprint import pprint


def cluster(token, sample):
    
    cluster = AgglomerativeClustering(n_clusters=(findAIC(sample)))
    cluster.fit(sample)

    sample['labels'] = cluster.labels_

    sample = sample.sort_values(by=['labels'])
    sample.to_csv('models/samples/sample.csv')

    return cluster


def sample(token):
    storage = pd.HDFStore('models/dataframes/preprocessed_dataframe.h5')

    dataframe = __dataframe_from_database('lib/predict/db/billboard-200.db', 'acoustic_features')
    dataframe = __preprocessd_dataframe(dataframe, token)

    storage.put('preprocessd_dataframe', dataframe, format='table', data_columns=True)
    storage.close()

    dataframe = pd.read_hdf('models/dataframes/preprocessed_dataframe.h5')

    pprint(dataframe)

    return dataframe


def azure_deploy(token):
    result = None
    joblib.dump(value=token, filename="cluster.pkl")
    model = Model.register(workspace=ws, model_path="cluster.pkl", model_name="cluster")
    result = Model.deploy_from_model(beatsBrain-local4, model)
    return result

def azure_download(model):
    return model.download(target_dir=os.getcwd(), exist_ok = True)

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

def findAIC(sample):
    length = (sample.shape)
    range_n_clusters = range(1, len(sample))
    aic_list = []

    num_clusters = 1

    for n_clusters in range_n_clusters:
        model = mixture(n_components=n_clusters, init_params='kmeans')
        model.fit(sample)
        aic_list.append(model.aic(sample))

    i = 0
    while i < len(aic_list):
        if (aic_list[i] == min(aic_list)):
            num_clusters = i + 1
        i += 1




    #print(length)
    #print(num_clusters)
    #print(sample)
    #print(range_n_clusters)
    #print(aic_list)


    return num_clusters

