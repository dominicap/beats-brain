import ijson
import numpy
from keras.models import Sequential




filename = "song_list.json"
with open(filename, 'r') as f:
objects = ijson.items(f, 'meta.view.columns.item')

data = list(objects)
labels = ['match', 'no match']

for j in data.columns[:-1]:
    mean = data[j].mean()
    data[j] = data[j].replace(0,mean)
    data[j] = pd.cut(data[j],bins=len(labels), labels = labels)


def count(data, colname, label, target):
    condition = (data[colname] == label) & (data['Outcome'] == target)
    return len(data[condition])

probabilities = {0: {}, 1:{}}

train_percent = 75
train_len = int((train_percent*len(data))/100)
train_x = data.iloc[:train_len,:]

test_x = data.iloc[train_len+1:,:-1]
test_y = data.iloc[train_len+1:,-1]

count_0 = count(train_x, 'Outcome', 0,0)
count_1 = count(train_x, 'Outcome',1,1)

prob_0 = count_0/len(train_x)
prob_1 = count_1/len(train_x)

for col in train_x.columns[:-1]:
    probabilities[0][col] = {}
    probabilities[0][col] = {}

    for category in labels:
        count_ct_0 = count(train_x, col, category, 0)
        count_ct_1 = count(train_x,col,category,1)

        probabilities[0][col][category] = count_ct_0 / count_0
        probabilities[1][col][category] = count_ct_1 / count_1



