### Voting ###
# Autor: Raffael Hipp 

import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.impute import KNNImputer
from sklearn.metrics import r2_score, roc_auc_score, recall_score
from sklearn.model_selection import train_test_split, cross_val_score
from pandas import DataFrame, Series
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, OrdinalEncoder, StandardScaler
import sklearn as sklearn

# adjust output of printed DataFrames
pd.options.display.max_columns = 100
pd.options.display.width = 1000

# import for logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, precision_score, f1_score
from sklearn.model_selection import GridSearchCV

# import for voting
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imb_pipe
import plotly.express as px

assert sklearn.__version__ >= "1.2"


def init_data() -> DataFrame:
    df = pd.read_csv("healthcare-dataset-stroke-data.csv")

    # Structural adjustments to the raw data that can be applied before splitting into training and test data

    ##### Column 'id' does not provide useful information #####
    df.drop(columns=['id'], inplace=True)

    ##### Drop rows with gender='Other'
    # The data set contains just one record with gender='Other'
    # Since either the training set or the test set is missing a record with Gender='Other', this record is deleted.
    df.drop(df[df['gender'] == 'Other'].index, inplace=True)

    ##### Transform column 'ever_married' #####
    for old_value, new_value in (('No', 0),
                                 ('Yes', 1)):
        df.loc[df['ever_married'] == old_value, 'ever_married'] = new_value

    ##### Transform column 'smoking_status' #####
    # Assuming that smoking increases the risk of a stroke, the feature 'smoking_status' is ordered.
    # The value 'Unknown' is placed in the middle
    for old_value, new_value in (('never smoked', 0),
                                 ('Unknown', 1),
                                 ('formerly smoked', 2),
                                 ('smokes', 3)):
        df.loc[df['smoking_status'] == old_value, 'smoking_status'] = new_value

    ##### 'One Hot Encoding' of categorical columns #####
    # Because machine learning algorithms assume (and require) your data to be numeric,
    # categorical data must be pre-processed in order for it to be accepted.
    transformer = make_column_transformer(
        (OneHotEncoder(), ['gender', 'work_type', 'Residence_type']),
        remainder='passthrough')
    df = DataFrame(
        transformer.fit_transform(df),
        columns=transformer.get_feature_names_out()
    )
    # Remove prefixes in column names added by OneHotEncoder()
    df.columns = df.columns.str.removeprefix('onehotencoder__')
    df.columns = df.columns.str.removeprefix('remainder__')

    return df


def inspect_data(df: DataFrame) -> None:
    df.info()
    print('\nnumber of nulls', df.isnull().sum(), sep='\n')
    print('\nduplicated rows: ', df.duplicated().sum())
    print('\ndata', df.head(), sep='\n')


def prepare_data(df: DataFrame, scaler='standard', knn_neighbors=5) -> DataFrame:
    ##### Scale columns #####
    sc = MinMaxScaler() if scaler == 'minmax' else StandardScaler()
    df = sc.set_output(transform='pandas').fit_transform(df)

    ##### Fill in missing values #####
    # We suspect that 'bmi' correlates strongly with stroke.
    # Therefore, a more precise fill-up of missing values is reasonable
    df = KNNImputer(n_neighbors=knn_neighbors) \
        .set_output(transform='pandas') \
        .fit_transform(df)

    # Alternative: Replace missing values with median
    # df['bmi'] = df['bmi'].fillna(round(df['bmi'].median(), 2))

    return df


def split_dataset(df: DataFrame):
    # Split train and test dataset:
    # Equal ratio of data records with/without stroke in training and test data
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-1],
                                                        df['stroke'],
                                                        test_size=test_size,
                                                        shuffle=True,
                                                        stratify=df['stroke'],
                                                        random_state=3)
    print(f'Percentage of patients with stroke: '
          f'train data={round(y_train[y_train == 1].shape[0] / y_train.shape[0] * 100, 2)}% / '
          f'test data={round(y_test[y_test == 1].shape[0] / y_test.shape[0] * 100, 2)}%')
    return X_train, X_test, y_train, y_test


def preprocess_data(X, y):
    X = prepare_data(X, scaler='standard')
    # X = prepare_data(X, scaler='minmax')
    # inspect_data(X)
    y = y.astype('int')
    # X = X.to_numpy()
    # y = y.to_numpy()
    return X, y


def score_auc_recall(y_true, y_pred) -> DataFrame:
    # Erstellt DataFrame mit Recall und AUC Score als Eintrag.
    # Recall-Score ist definiert durch die Gleichung tp / (tp+fn), wobei hier tp die Anzahl von echten Schlaganfällen-Vorhersagen ist,
    # und fn die Anzahl der falsch negativen (d.h. durch unseren Algorithmus kein Schlaganfall vorrausgesagt, aber Schlaganfall vorhanden).
    #
    # Je näher der Recall-Score bei 1 ist, desto besser klassifiziert der Algorithmus.

    score = {'1': {'recall': recall_score(y_true, y_pred, pos_label=1),
                   'precision_score': precision_score(y_true, y_pred, pos_label=1),
                   'f1': f1_score(y_true, y_pred, pos_label=1),
                   'AUC_score': roc_auc_score(y_true, y_pred)},
             '0': {'recall': recall_score(y_true, y_pred, pos_label=0),
                   'precision_score': precision_score(y_true, y_pred, pos_label=0),
                   'f1': f1_score(y_true, y_pred, pos_label=0),
                   'AUC_score': pd.NA}}

    df_score = pd.DataFrame.from_dict(score, orient='index')

    return df_score


##### Main #####

df: DataFrame = init_data()
# inspect_data(df)
X_train, X_test, y_train, y_test = split_dataset(df)

print('prepare training data')
X_train, y_train = preprocess_data(X_train, y_train)

print('prepare test data')
X_test, y_test = preprocess_data(X_test, y_test)
print('-------------------------------------------------------')


##### voting #####

# -- all used classifier --
clf_knn = imb_pipe([('oversample', SMOTE()), ('knn_pipe', KNeighborsClassifier(n_neighbors=185, p=1, weights='uniform', metric='euclidean'))])
clf_lr = LogisticRegression(C=0.001, class_weight={0: 1, 1: 100}, max_iter=150, penalty='l2', solver='lbfgs', random_state=42)
clf_rf = RandomForestClassifier(class_weight='balanced', max_features=None, criterion='entropy', min_samples_leaf=1, max_depth=3, n_estimators=1000)
clf_svc = SVC(class_weight={0: 1, 1: 1000}, kernel='linear')

# -- voting --
eclf = VotingClassifier(estimators=[ ('knn', clf_knn), ('lr', clf_lr), ('rf', clf_rf), ('svc', clf_svc)], voting='hard', n_jobs=-1)
eclf = eclf.fit(X_train, y_train)

# -- evaluation --
# - voting -
predictions = eclf.predict(X_test)
print(f'Voting result: \n{score_auc_recall(y_test, predictions)}')
print()
print('-------------------------------------------------------')

# - Result of each Classifier (knn, lr, rf, svc) -
print('Score-Results of each Classifier (knn, lr, rf, svc):')
clf_sep_rec = []
clf_sep_rec.append(cross_val_score(clf_knn,X_train,y_train,scoring='recall',cv=10, n_jobs=-1).mean())
clf_sep_rec.append(cross_val_score(clf_lr,X_train,y_train,scoring='recall',cv=10, n_jobs=-1).mean())
clf_sep_rec.append(cross_val_score(clf_rf,X_train,y_train,scoring='recall',cv=10, n_jobs=-1).mean())
clf_sep_rec.append(cross_val_score(clf_svc,X_train,y_train,scoring='recall',cv=10, n_jobs=-1).mean())
print(f'recall: {clf_sep_rec}')
#print('-------------------------------------------------------')

# - Result of each Classifier (knn, lr, rf, svc) -
clf_sep_auc = []
clf_sep_auc.append(cross_val_score(clf_knn,X_train,y_train,scoring='roc_auc',cv=10, n_jobs=-1).mean())
clf_sep_auc.append(cross_val_score(clf_lr,X_train,y_train,scoring='roc_auc',cv=10, n_jobs=-1).mean())
clf_sep_auc.append(cross_val_score(clf_rf,X_train,y_train,scoring='roc_auc',cv=10, n_jobs=-1).mean())
clf_sep_auc.append(cross_val_score(clf_svc,X_train,y_train,scoring='roc_auc',cv=10, n_jobs=-1).mean())
print(f'auc: {clf_sep_auc}')


# -- Plot --
# - recall -
x_label = ('knn', 'lr', 'rf', 'svc')
x_pos = np.arange(len(x_label))
plt.bar(x_pos, clf_sep_rec)
plt.xticks(x_pos, x_label)
plt.xlabel('Klassifikatoren')
plt.ylabel('Recall-Score')
plt.title('Vergleich der Klassifikatoren: Recall-Score')
plt.show()

# -- auc--
plt.bar(x_pos, clf_sep_auc)
plt.xticks(x_pos, x_label)
plt.xlabel('Klassifikatoren')
plt.ylabel('AUC-Score')
plt.title('Vergleich der Klassifikatoren: AUC-Score')
plt.show()