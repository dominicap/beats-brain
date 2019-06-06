import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3

from pprint import pprint
from sklearn.cluster import AgglomerativeClustering


def main():
    dataframe = dataframe_from_database('db/billboard-200.db',
                                        'acoustic_features')

    pprint(dataframe.iloc[:1])


def dataframe_from_database(database, table):
    connection = sqlite3.connect(database)
    query = "SELECT * FROM" + " " + table

    return pd.read_sql_query(query, connection)


if __name__ == '__main__':
    main()
