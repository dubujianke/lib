import os
import pickle
import numpy as np
from sklearn import datasets
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import graphviz
# dot -Tpng bottom11_8.dot -o bottom11_8.png
from itertools import *
import warnings

warnings.filterwarnings("ignore")

drops = ["gap120(9)", "gap120(8)", "gap120(7)", "gap120(6)", "gap120(5)",
         "gap250(9)", "gap250(8)", "gap250(7)", "gap250(6)", "gap250(5)",
         "zhenf(9)", "zhenf(8)", "zhenf(7)", "zhenf(6)", "zhenf(5)",
         "price_(9)", "price_(8)", "price_(7)", "price_(6)", "price_(5)",
         "price(9)", "price(8)", "price(7)", "price(6)", "price(5)",
         "prev(9)", "prev(8)", "prev(7)", "prev(6)", "prev(5)", "max"]
drops = ["mtP2", "mtP1", "mtP0", "max", "curMinute"]
# ALL = ["2023-10-10", "2023-10-11", "2023-10-12", "2023-10-13",
#        "2023-10-16", "2023-10-17", "2023-10-18", "2023-10-19", "2023-10-20",
#        "2023-10-23", "2023-10-24", "2023-10-25", "2023-10-26", "2023-10-27",
#        "2023-10-30", "2023-10-31", "2023-11-01", "2023-11-02", "2023-11-03",
#        "2023-11-06", "2023-11-07", "2023-11-08", "2023-11-09", "2023-11-10",
#        "2023-11-13", "2023-11-14", "2023-11-15", "2023-11-16", "2023-11-17",
#        "2023-11-20", "2023-11-21", "2023-11-22", "2023-11-23", "2023-11-24",
#        "2023-11-27", "2023-11-28", "2023-11-29", "2023-11-30", "2023-12-01",
#        "2023-12-04", "2023-12-05", "2023-12-06", "2023-12-07", "2023-12-08",
#        "2023-12-11", "2023-12-12", "2023-12-13", "2023-12-14", "2023-12-15",
#        "2023-12-18", "2023-12-19", "2023-12-20", "2023-12-21", "2023-12-22",
#        "2023-12-25", "2023-12-26", "2023-12-27", "2023-12-28", "2023-12-29",
#        "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05","2024-01-08",
#        "2024-01-08", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-15",
#        "2024-01-16", "2024-01-17", "2024-01-17", "2024-01-18", "2024-01-15",
#        "2024-01-19", "2024-01-22"
#        ]

ALL = [
       "2023-12-25", "2023-12-26", "2023-12-27", "2023-12-28", "2023-12-29",
       "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05","2024-01-08",
       "2024-01-08", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-15",
       "2024-01-16", "2024-01-17", "2024-01-17", "2024-01-18", "2024-01-15",
       "2024-01-19", "2024-01-22"
       ]
df = pd.DataFrame({'ID': [1, 2, 3], 'NAME': ['LL', 'TG', 'FL']})
df.to_excel('D:/practise.xlsx')

ret0 = []
ret1 = []
ret2 = []
ret3 = []
ret4 = []

def processDate(treeClf, date, destDir):
    print(date)
    predatads = pd.read_excel(r'D:\stock\Test\res\bottom\ret1\{}.xlsx'.format(date), index_col=None)
    predatads.fillna(1000, inplace=True)
    predatads.replace(float('inf'), 1000, inplace=True)
    predatads.drop(drops, axis=1, inplace=True)

    y_train2 = predatads.iloc[:, 7].map(lambda x: x > 7.3 and 1 or 0).values
    x_train2 = predatads.iloc[:, 8:].values
    return processDataPredict(treeClf, date, y_train2, x_train2, destDir)


def processDataPredict(tree_clf, date, y_train, x_train, destDir):
    y_train_hat = tree_clf.predict(x_train)

    yy = np.row_stack((y_train, y_train_hat))
    yytotal = len(y_train_hat)
    zt = np.where(yy[0] == 1)
    yy1 = np.where(yy[1] == 1)
    yy2 = np.where((yy[1] == 1) & (yy[0] == 1))
    if (len((yy1[0])) > 0):
        ret = len((yy2[0])) / len((yy1[0]))
    else:
        ret = '*'
    print("==>total:{}/{} {}/{} recall:{} acc:{}".format(len(zt[0]), yytotal, len(yy2[0]), len(yy1[0]), ret,
                                                         accuracy_score(y_train, y_train_hat)))

    str = "{} {}/{} {}/{}".format(date, len(zt[0]), yytotal, len(yy2[0]), len(yy1[0]))
    predatads = pd.read_excel(r'D:\stock\Test\res\bottom\ret1\{}.xlsx'.format(date), index_col=None)
    predatads.fillna(1000, inplace=True)
    predatads.replace(float('inf'), 1000, inplace=True)
    predatads = predatads.iloc[yy1]
    predatads = predatads[predatads['上月z幅'] <= 13]
    predatads = predatads[predatads['上周涨幅'] <= 4]

    predatads.to_excel("{}/{}.xlsx".format(destDir, date), index=False)
    return str


def processData(y_train, x_train, clms, FFNAME, DEEPTH):
    print(x_train.shape)
    print(y_train.shape)
    tree_clf = DecisionTreeClassifier(max_depth=DEEPTH, class_weight='balanced', criterion='gini')
    tree_clf.fit(x_train, y_train)
    y_train_hat = tree_clf.predict(x_train)

    yy = np.row_stack((y_train, y_train_hat))
    yy1 = np.where(yy[1] == 1)
    yy2 = np.where((yy[1] == 1) & (yy[0] == 1))
    ret = len((yy2[0])) / len((yy1[0]))
    print("{}/{} recall:{} acc:{}".format(len((yy2[0])), len((yy1[0])), ret, accuracy_score(y_train, y_train_hat)))
    dot_data = tree.export_graphviz(
        tree_clf,
        out_file='{}.dot'.format(FFNAME),
        feature_names=clms,
        class_names=['False', 'True'],
        rounded=True,
        filled=True
    )
    return tree_clf


#########################################################
def process(PRELEN, idx):
    fs = ALL[idx:idx + PRELEN]
    # predictDates = ALL[idx + PRELEN:idx + PRELEN + 2]
    # PRECRDAE = predictDates[0]
    predictDates = ALL[idx:idx + PRELEN + 2]
    PRECRDAE = ALL[idx + PRELEN:idx + PRELEN + 2][0]
    DEEPTH = 3
    destDir = "d:/stock/Test/res/bottom/ret_{}".format(PRECRDAE)
    if os.path.exists(destDir):
        return
    if not os.path.exists(destDir):
        os.mkdir(destDir)
    FFNAME = "bottom_{}_{}".format(PRECRDAE, DEEPTH)

    ffs = []
    for index, item in enumerate(fs):
        adatads = pd.read_excel(r'D:\stock\Test\res\bottom\ret1\{}.xlsx'.format(item), index_col=None)
        adatads.fillna(1000, inplace=True)
        adatads.replace(float('inf'), 1000, inplace=True)
        ffs.append(adatads)

    datads = pd.concat(ffs, ignore_index=True)
    datads.drop(drops, axis=1, inplace=True)
    num_rows = len(datads)
    clms = datads.columns[8:]
    classNames = datads.columns[7]

    if datads.values.all() > 0:
        print("hahah")


    y_train = datads.iloc[:, 7].map(lambda x: x > 7.3 and 1 or 0).values
    x_train = datads.iloc[:, 8:].values

    treeClf = processData(y_train, x_train, clms, FFNAME, DEEPTH)
    print('----------------------------\r\n')

    str0 = ""
    str1 = ""
    str2 = ""
    str3 = ""
    str4 = ""
    for index, item in enumerate(predictDates):
        str = processDate(treeClf, item, destDir)
        if (index == 0):
            str0 = str
        if (index == 1):
            str1 = str
        if (index == 2):
            str2 = str
        if (index == 3):
            str3 = str
        if (index == 4):
            str4 = str
        if str0 != "" and str1 != "" and str2 != "" and str3 != "" and str4 != "":
            ret0.append(str0)
            ret1.append(str1)
            ret2.append(str2)
            ret3.append(str3)
            ret4.append(str4)
        print('----------------------------')


PRELEN = 20

# for i in range(0, 38):
for i in range(0, 1):
    process(PRELEN, i)

df = pd.DataFrame({'d0': ret0, 'd1': ret1, 'd2': ret2, 'd3': ret3, 'd4': ret4})
df.to_excel('D:/practise_{}.xlsx'.format(PRELEN))
