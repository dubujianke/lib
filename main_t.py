import pickle

import numpy as np
from sklearn import datasets
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import graphviz
# dot -Tpng rett.dot -o rett.png
import warnings
from itertools import *


warnings.filterwarnings("ignore")
drops = ["上月z幅"]

DEEPTH = 3
IDX = 9
DEEPTH = 4
datads = pd.read_excel(r'D:\new_tdx_info\res\bottom\{}.xlsx'.format('09'), index_col=None)
datads.fillna(1000, inplace=True)
datads.replace(float('inf'), 1000, inplace=True)
datads.drop(drops, axis=1, inplace=True)
clms = datads.columns[8:]
classNames = datads.columns[7]

def processDataPredict(tree_clf, y_train, x_train):
    tree_clf.fit(x_train, y_train)
    y_train_hat = tree_clf.predict(x_train)
    yy = np.row_stack((y_train, y_train_hat))
    yy1 = np.where(yy[1] == 1)
    yy2 = np.where((yy[1] == 1) & (yy[0] == 1))
    ret = len((yy2[0])) / len((yy1[0]))
    print("==>{}/{} recall:{} acc:{}".format(len(yy2[0]), len(yy1[0]), ret, accuracy_score(y_train, y_train_hat)))

def processData(y_train, x_train):
    print(x_train.shape)
    print(y_train.shape)
    tree_clf = DecisionTreeClassifier(max_depth=DEEPTH, class_weight='balanced', criterion='gini')
    tree_clf.fit(x_train, y_train)
    y_train_hat = tree_clf.predict(x_train)
    yy = np.row_stack((y_train, y_train_hat))
    yy1 = np.where(yy[1] == 1)
    yy2 = np.where((yy[1] == 1) & (yy[0] == 1))
    ret = len((yy2[0])) / len((yy1[0]))
    print("{} recall:{} acc:{}".format(len((yy2[0])), ret, accuracy_score(y_train, y_train_hat)))
    dot_data = tree.export_graphviz(
        tree_clf,
        out_file='{}.dot'.format('rett'),
        feature_names=clms,
        class_names=['False', 'True'],
        rounded=True,
        filled=True,
        fontname="SimHei"
    )
    # graph = graphviz.Source(dot_data)
    # graph.render('09')
    # graph.write_png('tree_09.png')
    return tree_clf


y_train = datads.iloc[:, 7].map(lambda x: x > 9.7 and 1 or 0).values
x_train = datads.iloc[:, 8:].values
processData(y_train, x_train)


