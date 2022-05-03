import os, zipfile
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from catboost import CatBoostClassifier, Pool
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

def get_data_from_zip(zip_path):
    zf = zipfile.ZipFile(zip_path)
    method_files = [(f , f.split('/')[-3], f.split('/')[-2], "method.csv") for f in zf.namelist() if f.endswith('method.csv')]
    class_files = [(f , f.split('/')[-3], f.split('/')[-2], "class.csv") for f in zf.namelist() if f.endswith('class.csv')]
    variable_files = [(f , f.split('/')[-3], f.split('/')[-2], "variable.csv") for f in zf.namelist() if f.endswith('variable.csv')]
    field_files = [(f , f.split('/')[-3], f.split('/')[-2], "field.csv") for f in zf.namelist() if f.endswith('field.csv')]

    df = pd.DataFrame(method_files + class_files + variable_files + field_files, columns=["full_path", "class", "project_name", "file_type"])
    X = []
    Y = []
    i = 0
    cols = []

    for class_name, samples in df.groupby("class"):
        for project_name, project_samples in samples.groupby("project_name"):
            project_data = []
            failed = 0
            for path in project_samples.sort_values(by="file_type")[['full_path','file_type']].values:
                dddf=pd.read_csv(zf.open(path[0])).select_dtypes(exclude=[object]).fillna(0).mean()
                if len(dddf) == 0:
                    failed+=1
                    if i == 0: cols = []
                    break
                project_data += dddf.to_list()
                if i == 0:
                    cols += [f'{path[-1][:-4]}_{cname}' for cname in dddf.index]
            if failed == 0:
                i+=1
                project_data = np.array(project_data).reshape(1,-1)
                X += project_data.tolist()
                Y.append(class_name)
    print(f"Total {i}")
    return np.array(X), Y, cols

def get_data_from_csv(train_path='../Data/train.csv', test_path='../Data/test.csv', print_stat=False):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    if print_stat:
        pass
    return train_df, test_df

def train_models():
    train_df, test_df = get_data_from_csv()

    Xtrain, ytrain = train_df.drop('label',axis=1).values, train_df.label.values
    Xtest, ytest = test_df.drop('label',axis=1).values, test_df.label.values

    print("DecisionTreeClassifier")
    dt = DecisionTreeClassifier()
    dt.fit(Xtrain, ytrain)
    ypred = dt.predict(Xtest)
    print(classification_report(ytest, ypred))

    print("RandomForestClassifier")
    rf = RandomForestClassifier()
    rf.fit(Xtrain, ytrain)
    ypred = rf.predict(Xtest)
    print(classification_report(ytest, ypred))

    train_data = Pool(data=Xtrain, label=ytrain)
    print("CatBoostClassifier")
    cb = CatBoostClassifier(verbose=False)
    cb.fit(train_data)
    ypred = cb.predict(Xtest)
    print(classification_report(ytest, ypred))

    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(Xtrain)
    X_test_std = scaler.transform(Xtest)

    print("LogisticRegression")
    lr = LogisticRegression()
    lr.fit(X_train_std, ytrain)
    ypred = lr.predict(X_test_std)
    print(classification_report(ytest, ypred))

    print("neural network")
    from sklearn.neural_network import MLPClassifier
    nn_clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

    nn_clf.fit(X_train_std, ytrain)
    ypred = nn_clf.predict(X_test_std)
    print(classification_report(ytest, ypred))

    print("KNN")
    knn = KNeighborsClassifier()
    knn.fit(X_train_std, ytrain)
    ypred = knn.predict(X_test_std)
    print(classification_report(ytest, ypred))

    print("SVM")
    svmclf = SVC()
    svmclf.fit(X_train_std, ytrain)
    ypred = svmclf.predict(X_test_std)
    print(classification_report(ytest, ypred))

    print("GaussianNB")
    gnb = GaussianNB()
    y_pred = gnb.fit(X_train_std, ytrain).predict(X_test_std)
    print(classification_report(ytest, y_pred))


if __name__ == '__main__':
    train_models()
