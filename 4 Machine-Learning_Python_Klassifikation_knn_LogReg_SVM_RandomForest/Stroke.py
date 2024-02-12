import pandas as pd
import numpy as np
import sklearn as sklearn
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from pandas import DataFrame
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline as sk_pipe
from sklearn.impute import KNNImputer
from sklearn.metrics import roc_auc_score, recall_score, confusion_matrix, classification_report, precision_score, \
    f1_score
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, StandardScaler
from imblearn.pipeline import Pipeline as imb_pipe
from sklearn.svm import SVC

# Hint: Start reading the code at the end of file (Main)

# adjust console output of DataFrames
pd.options.display.max_columns = 100
pd.options.display.width = 1000

assert sklearn.__version__ >= "1.2"


# +--------------------+
# | Data Preprocessing |
# +--------------------+
def init_data() -> DataFrame:
    # author: Jan Philipp Seng
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

    # Convert entire dataframe to float
    df = df.astype(float)

    return df


def inspect_data(df: DataFrame) -> None:
    # author: Jan Philipp Seng
    df.info()
    print('\nnumber of nulls', df.isnull().sum(), sep='\n')
    print('\nduplicated rows: ', df.duplicated().sum())
    print('\ndata', df.head(), sep='\n')


def prepare_data(df: DataFrame, scaler='standard', knn_neighbors=5) -> DataFrame:
    # author: Jan Philipp Seng
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
    # author: Jan Philipp Seng
    # Split train and test dataset:
    # Equal ratio of data records with/without stroke in training and test data
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-1],
                                                        df['stroke'],
                                                        test_size=test_size,
                                                        shuffle=True,
                                                        stratify=df['stroke'],
                                                        random_state=3)
    # print(f'Percentage of patients with stroke: '
    #       f'train data={round(y_train[y_train == 1].shape[0] / y_train.shape[0] * 100, 2)}% / '
    #       f'test data={round(y_test[y_test == 1].shape[0] / y_test.shape[0] * 100, 2)}%')
    return X_train, X_test, y_train, y_test


def preprocess_data(X, y):
    # author: Jan Philipp Seng
    X = prepare_data(X, scaler='standard')
    # X = prepare_data(X, scaler='minmax')
    # inspect_data(X)
    y = y.astype('int')
    X = X.to_numpy()
    y = y.to_numpy()
    return X, y


# +----------------------------------------------+
# | Code to test various estimators              |
# | Helper functions                             |
# +----------------------------------------------+
def score_auc_recall(y_true, y_pred) -> DataFrame:
    # author: Lars Kleinemeier
    # Erstellt DataFrame mit Recall und AUC Score als Eintrag.
    # Recall-Score ist definiert durch die Gleichung tp / (tp+fn),
    # wobei hier tp die Anzahl von echten Schlaganfällen-Vorhersagen ist,
    # und fn die Anzahl der falsch negativen
    # (d.h. durch unseren Algorithmus kein Schlaganfall vorausgesagt, aber Schlaganfall vorhanden).
    #
    # Je näher der Recall-Score bei 1 ist, desto besser klassifiziert der Algorithmus.

    score = {
        '1': {
            'recall': recall_score(y_true, y_pred, pos_label=1),
            'precision_score': precision_score(y_true, y_pred, pos_label=1),
            'f1': f1_score(y_true, y_pred, pos_label=1),
            'AUC_score': roc_auc_score(y_true, y_pred)
        },
        '0': {
            'recall': recall_score(y_true, y_pred, pos_label=0),
            'precision_score': precision_score(y_true, y_pred, pos_label=0),
            'f1': f1_score(y_true, y_pred, pos_label=0),
            'AUC_score': pd.NA
        }
    }

    df_score = pd.DataFrame.from_dict(score, orient='index')

    return df_score


def GridSearchCV_SMOTE(
        estimator,
        param_grid,
        *,
        scoring=None,
        n_jobs=None,
        refit=True,
        cv=None,
        verbose=0,
        pre_dispatch='2*n_jobs',
        error_score=np.nan,
        return_train_score=False):
    # author: Lars Kleinemeier
    oversample_pipe = imb_pipe([('smote', SMOTE()),
                                ('clf', estimator)])

    new_param_grid = dict()
    for key in param_grid.keys():
        new_param_grid['clf__' + key] = param_grid[key]

    return GridSearchCV(oversample_pipe,
                        new_param_grid,
                        scoring=scoring,
                        n_jobs=n_jobs,
                        refit=refit,
                        cv=cv,
                        verbose=verbose,
                        pre_dispatch=pre_dispatch,
                        error_score=error_score,
                        return_train_score=return_train_score)


# +----------------------------------------------+
# | Code to test various estimators              |
# | For each estimator there is one function     |
# +----------------------------------------------+
def estimator_knn(X_train, y_train, X_test, y_test):
    # author: Gero Krikawa
    y_train = y_train.astype("int")
    # K-NeighborsClassifier

    print("------------------ Verwendung von K-NeighborsClassifier -------------------")
    # NAIV ANSATZ - Oversampling auf gesamten Datensatz X_train UND Y_train
    # ACHTUNG: Oversampling an dieser Stellte auf gesamten Datensatz führt im weiteren Verlauf z.B. bei Cross Validation und Gridsearch zu trügerisch falschen Werten, Abhilfe s.u.
    # oversample = SMOTE()
    # X_train_smote, y_train_smote = oversample.fit_resample(X_train, y_train.ravel())
    # X_train = X_train_smote
    # y_train = y_train_smote

    # -----------------------------------------------------------------------------------------

    # BASIS ANSATZ:
    # Training und Predict auf Trainingsdaten ohne Oversampling und ohne Parameteroptimierung
    knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')  # start n = 5
    knn.fit(X_train, y_train)  # fit
    pred = knn.predict(X_train)  # predict
    auc_score = score_auc_recall(y_train, pred)
    # Ergebnisse
    print("\n")
    print("Ergebnisse für nur fit und predict auf Trainingsdaten ohne Oversampling")
    print("Score: ", knn.score(X_train, y_train))
    print("Confusion_Matrix:", "\n", confusion_matrix(y_train, pred))
    print("Classification_Report:", "\n", classification_report(y_train, pred))
    print("AUC-Score", auc_score)
    print("\n")
    # Ergebnis nicht zufriedenstellend
    # im weiteren Verlauf Versuche zur Optimierung der Ergebnisse

    # print("\n")
    # # Test auf den Testdaten mit Oversampling Smote auf den gesamten Datensatz ohne CrossVal ohne GridSearch
    # print("Test auf den Testdaten mit Oversampling Smote auf den gesamten Datensatz ohne CrossVal ohne GridSearch")
    # pred_test = knn.predict(X_test)  # predict
    # auc_score = score_auc_recall(y_test, pred_test)
    # # Ergebnisse
    # print("\n")
    # print("Ergebnisse für nur fit und predict auf Testdaten mit Oversampling auf gesamten Datensatz")
    # print("Score: ", knn.score(X_test, y_test))
    # print("Confusion_Matrix:", "\n", confusion_matrix(y_test, pred_test))
    # print("Classification_Report:", "\n", classification_report(y_test, pred_test))
    # print("AUC-Score", auc_score)
    # print("\n")

    # ------------------------------------------------------------------------------------------

    # Variation von k und p inkl. cross_validation, score: Precision
    print("Variation von k und p inkl. cross_val ohne Oversampling")
    for k in (1, 2, 5, 10, 50, 100, 150):  # Nachbarn
        for potenz in (1, 2, 3, 4, 50, 100):  # Potenz
            neighbor = KNeighborsClassifier(n_neighbors=k, p=potenz)  # Algorithmus
            print(f"Nachbarn = {k}, Metrik (Potenz) = {potenz}")
            neighbor.fit(X_train, y_train)  # fit
            ergebnis = cross_val_score(neighbor, X_train, y_train, cv=3,
                                       scoring="recall").mean()  # score mit Crossvall (Algortihmus, X (Gesamtmenge!), y, cv= Anzahl der Folds) über gesamte Datenmenge X
            print("Cross Val Score Mean:", ergebnis)
    print("------------------------------------------------------------")
    print("\n")

    # ------------------------------------------------------------------------------------------

    # CROSS_VALIDATION
    # Focus auf recall und AUC, Precision ungeeignet.
    print("\n")
    print("Cross Validation mit Oversampling SMOTE, Score: recall")

    # Cross_Validation mit Naiv Ansatz oben: Oversampling auf gesamten Datensatz
    # knn_results_cross_val_score = cross_val_score(knn,X_train,y_train, cv=5) # Problem Oversampling auf X_train und y_train
    # Z.148 Oversampling auf gesamten Datensatz führt zu trügerischen guten Werten

    # Abhilfe:
    # Cross_Validation mit Oversampling mit SMOTE() nur für Trainingsdaten innherhalb des Cross_Validation durch Pipeline
    # Folge nur Oversampling beim fit und nicht beim predict(Testdaten)

    # Definition einer Pipeling mit Hilfe: from imblearn.pipeline import Pipeline as imb_pipe
    knn_pipe = imb_pipe(
        [('oversample', SMOTE()), ('knn', KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski'))])  # Pipeline
    knn_results_cross_val_score = cross_val_score(knn_pipe, X_train, y_train, cv=5, scoring='recall')
    # Ergebnisse Cross_Val_Score
    print("knn Cross Vall Score", knn_results_cross_val_score)
    print("knn Cross Vall Score Mean", knn_results_cross_val_score.mean())
    print("knn Cross Vall Score Std", knn_results_cross_val_score.std())
    print("\n")

    # ----------------------------------------------------------------------------------------

    # GridSearch Oversampling mit SMOTE() mit Hilfe knn_pipe zur Bestimmung der optimalen Parameter für den predict auf die Testdaten
    print("")
    print("GridSearch mit Oversampling SMOTE, score: recall")
    # Oversampling mit SMOTE() mit Hilfe knn_pipe

    # Varianten von param_grid zur Optimierung je nach Rechenleistung
    # Variante 1
    param_grid = {"knn__n_neighbors": np.arange(1, 200), "knn__p": np.arange(1, 3)}

    # Variante 2
    # param_grid = {"knn__n_neighbors": np.arange(50,200),"knn__p": np.arange(1,3),"knn__weights": ['uniform', 'distance']}

    # Variante 3
    # param_grid = {"knn__n_neighbors": np.arange(70, 200), "knn__p": np.arange(1, 3),"knn__weights": ['uniform', 'distance'],"knn__metric": ['minkowski', 'euclidean', 'manhattan']}

    # Variante 4
    # param_grid = {"knn__n_neighbors": np.arange(50, 200), "knn__p": np.arange(1,3),
    #              "knn__weights": ['uniform', 'distance'], "knn__algorithm": ['ball_tree', 'kd_tree', 'brute'],
    #              "knn__metric": ['minkowski', 'euclidean', 'manhattan']}
    knn_gscv = GridSearchCV(knn_pipe, param_grid, verbose=2, cv=5, scoring="recall")
    knn_gscv.fit(X_train, y_train)
    # Ergebnisse GridSearch
    print("knn best_params_:", knn_gscv.best_params_)
    print("Best score: ", knn_gscv.best_score_)
    print("Best estimator:", knn_gscv.best_estimator_)
    # print("Error Score:", knn_gscv.error_score)
    # print("Return Train Score:", knn_gscv.return_train_score)
    print("\n")

    # -----------------------------------------------------------------------------------------

    # Verwendung der optimalen Paramter aus Gridsearch für die Testdaten zur Vorhersage von Stroke
    print("")
    print("Testergebnisse")
    print("Vorhersage von Stroke mit Oversampling und optimalen Parametern")
    print("Von Grindsearch ermittelte Parameter")
    print("n_neighbors = 185")
    print("p = 1")
    print("weight: = uniform")
    # print("knn_algorith = ")
    print("knn_metric = euclidean")

    knn_pipe_test = imb_pipe([('oversample', SMOTE()), ('knn',KNeighborsClassifier(n_neighbors=183, p=2, metric='euclidean',weights='uniform',algorithm='ball_tree'))])  # Pipeline
    knn_pipe_test.fit(X_train, y_train)
    pred_test = knn_pipe_test.predict(X_test)
    auc_score = score_auc_recall(y_test, pred_test)

    # Ergebnisse der Vorhersage auf den Testdaten
    print("Score: ", knn_pipe_test.score(X_test, y_test))
    print("Confusion_Matrix:", "\n", confusion_matrix(y_test, pred_test))
    print("Classification_Report:", "\n", classification_report(y_test, pred_test))
    print("AUC-Score", auc_score)
    print("\n")
    print("\n")
    print("\n")

    return knn_pipe_test.score(X_test, y_test), \
        confusion_matrix(y_test, pred_test), \
        classification_report(y_test, pred_test), \
        auc_score


def estimator_svc(X_train, X_test, y_train, y_test):
        # author: Lars Kleinemeier
        # Wir testen zur erst den ganz naiven Ansatz in dem wir nichts gegen die unbalancierten Daten tun.
        print('-------------- Naiver Ansatz ---------------')
        estimator_naiv = SVC(kernel='linear')
        
        parameter_grid_naiv = {'kernel': ['linear', 'sigmoid', 'rbf'],
                               'C': [0.1, 0.2, 0.3, 1, 2, 3, 10, 20, 30]
                               }
        
        gridsearch_naiv = GridSearchCV(estimator_naiv,
                                       parameter_grid_naiv,
                                       scoring=['recall', 'precision', 'roc_auc'],
                                       return_train_score=False,
                                       refit='recall')
        
        gridsearch_naiv.fit(X_test, y_test)
        
        df_best_result = pd.DataFrame(gridsearch_naiv.cv_results_).iloc[gridsearch_naiv.best_index_, :]
        
        print(f'Recall_Score naiv: {df_best_result["mean_test_recall"]}')
        print(f'Precision_Score naiv: {df_best_result["mean_test_precision"]}')
        print(f'roc_auc_Score naiv: {df_best_result["mean_test_roc_auc"]}')
        print(f'Recall_Parameter naiv: {df_best_result["params"]}')
        
        # Wir testen nun die Klassengewicht-Variante, welche wir zuerst zufällig mit bestimmten Parametern anwenden.
        print('-------------- Ansatz mit Klassengewicht ---------------')
        estimator_svm = [SVC(class_weight='balanced', random_state=42),
                         SVC(class_weight={0: 0.1, 1: 0.9}, random_state=42),
                         SVC(kernel='linear', class_weight='balanced', random_state=42),
                         SVC(kernel='poly', class_weight='balanced', random_state=42),
                         SVC(kernel='poly', class_weight='balanced', degree=2, random_state=42)]
        
        for estimator in estimator_svm:
            estimator.fit(X_train, y_train.astype('int'))
            y_pred = estimator.predict(X_test)
            print(f'Class weight {estimator.get_params()["class_weight"]} and Kernel {estimator.get_params()["kernel"]}')
            score = score_auc_recall(y_test.astype('int'), y_pred)
            print(score)
        
        # Wir verfeinern die Suche mit einem GridSearch um die beste Variante zu finden.
        # Wir verändern hier die Attribute 'class_weight' und auch den Kernel.
        print('-------------- Ansatz mit Klassengewicht - GridSearch  ---------------')
        parameter_grid_CW = {
            'svc__kernel': ['linear', 'sigmoid', 'rbf'],
            'svc__class_weight': [{
                0: 1,
                1: 10
            },
                {
                    0: 1,
                    1: 100
                },
                {
                    0: 1,
                    1: 1000
                },
                'balanced']
        }
        
        # Wir erstellen eine Pipeline für den Prozess. Für die Vergleichbarkeit wird ein Random_State gesetzt.
        pipeline_withoutpca = sk_pipe([('scaler', StandardScaler()),
                                       ('svc', SVC(kernel='linear', random_state=42))])
        
        print('-------------- Ansatz mit Klassengewicht - Ergebnisse GridSearchCV  ---------------')
        # Wir erstellen ein GridSearch, wo wir nach dem Recall-Score optimieren.
        grid_cv_withCW_recall = GridSearchCV(pipeline_withoutpca,
                                             parameter_grid_CW,
                                             scoring=['recall', 'precision', 'roc_auc'],
                                             return_train_score=True,
                                             refit='recall',
                                             cv=10
                                             )
        
        grid_cv_withCW_recall.fit(X_train, y_train)
        
        df_best_result_CW = pd.DataFrame(grid_cv_withCW_recall.cv_results_).iloc[grid_cv_withCW_recall.best_index_, :]
        
        print(f'Recall_Score naiv: {df_best_result_CW["mean_test_recall"]}')
        print(f'Precision_Score naiv: {df_best_result_CW["mean_test_precision"]}')
        print(f'roc_auc_Score naiv: {df_best_result_CW["mean_test_roc_auc"]}')
        print(f'Recall_Parameter naiv: {df_best_result_CW["params"]}')
        
        print('-------------- Ansatz mit Klassengewicht - Overfitting Befürchtung  ---------------')
        y_pred_train = grid_cv_withCW_recall.best_estimator_.predict(X_train)
        print(score_auc_recall(y_train, y_pred_train))
        print(confusion_matrix(y_train, y_pred_train))
        print('-------------- Ansatz mit Klassengewicht - Bewertung auf Testdaten  ---------------')
        y_pred = grid_cv_withCW_recall.best_estimator_.predict(X_test)
        print(score_auc_recall(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
        print('-------------- Ansatz mit Klassengewicht - Beendet  ---------------')
        
        print('-------------- Ansatz mit Under-sampling ---------------')
        pipe_undersampling = imb_pipe([('scaler', StandardScaler()),
                                       ('under', RandomUnderSampler(random_state=42)),
                                       ('estimator', SVC(random_state=42))])
        
        parametergrid_undersampling = {
            'estimator__kernel': ['linear', 'sigmoid', 'rbf'],
            'under__sampling_strategy': [0.4, 0.5, 0.6, 'auto']
        }
        
        print('-------------- Ansatz mit Undersampling - Ergebnisse GridSearchCV  ---------------')
        grid_cv_us_recall = GridSearchCV(pipe_undersampling,
                                         parametergrid_undersampling,
                                         scoring=['recall', 'precision', 'roc_auc'],
                                         return_train_score=True,
                                         refit='recall',
                                         cv=10
                                         )
        
        grid_cv_us_recall.fit(X_train, y_train)
        
        df_best_result_US = pd.DataFrame(grid_cv_us_recall.cv_results_).iloc[grid_cv_us_recall.best_index_, :]
        
        print(f'Recall_Score naiv: {df_best_result_US["mean_test_recall"]}')
        print(f'Precision_Score naiv: {df_best_result_US["mean_test_precision"]}')
        print(f'roc_auc_Score naiv: {df_best_result_US["mean_test_roc_auc"]}')
        print(f'Recall_Parameter naiv: {df_best_result_US["params"]}')
        print('-------------- Ansatz mit Undersampling - Overfitting Befürchtung  ---------------')
        y_pred_train = grid_cv_us_recall.best_estimator_.predict(X_train)
        print(score_auc_recall(y_train, y_pred_train))
        print(confusion_matrix(y_train, y_pred_train))
        print('-------------- Ansatz mit Undersampling - Bewertung auf Testdaten  ---------------')
        y_pred = grid_cv_us_recall.best_estimator_.predict(X_test)
        print(score_auc_recall(y_test, y_pred))
        print('-------------- Ansatz mit Undersampling - Beendet  ---------------')
        
        print('-------------- Ansatz mit nur SMOTE ---------------')
        smote_pipeline = imb_pipe([('scaler', StandardScaler()),
                                   ('over', SMOTE(random_state=42)),
                                   ('estimator', SVC(random_state=42))])
        
        parametergrid_smote = {
            'estimator__kernel': ['linear', 'sigmoid', 'rbf']
        }
        
        print('-------------- Ansatz mit SMOTE - Ergebnisse GridSearchCV  ---------------')
        grid_cv_smote_recall = GridSearchCV(smote_pipeline,
                                            parametergrid_smote,
                                            scoring=['recall', 'precision', 'roc_auc'],
                                            return_train_score=True,
                                            refit='recall',
                                            cv=10
                                            )
        
        grid_cv_smote_recall.fit(X_train, y_train)
        
        df_best_result_SMOTE = pd.DataFrame(grid_cv_smote_recall.cv_results_).iloc[grid_cv_smote_recall.best_index_, :]
        
        print(f'Recall_Score naiv: {df_best_result_SMOTE["mean_test_recall"]}')
        print(f'Precision_Score naiv: {df_best_result_SMOTE["mean_test_precision"]}')
        print(f'roc_auc_Score naiv: {df_best_result_SMOTE["mean_test_roc_auc"]}')
        print(f'Recall_Parameter naiv: {df_best_result_SMOTE["params"]}')
        print('-------------- Ansatz mit SMOTE - Overfitting Befürchtung  ---------------')
        y_pred_train = grid_cv_smote_recall.best_estimator_.predict(X_train)
        print(score_auc_recall(y_train, y_pred_train))
        print(confusion_matrix(y_train, y_pred_train))
        print('-------------- Ansatz mit SMOTE - Bewertung auf Testdaten  ---------------')
        y_pred = grid_cv_smote_recall.best_estimator_.predict(X_test)
        print(score_auc_recall(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
        print('-------------- Ansatz mit SMOTE - Beendet  ---------------')
        
        print('-------------- Ansatz mit SMOTE und Undersampling ---------------')
        smote_pipeline_withundersampling = imb_pipe([('scaler', StandardScaler()),
                                                     ('under', RandomUnderSampler(random_state=42)),
                                                     ('over', SMOTE(random_state=42)),
                                                     ('estimator', SVC(random_state=42))])
        
        parametergrid_smote_withundersampling = {
            'estimator__kernel': ['linear', 'sigmoid', 'rbf'],
            'under__sampling_strategy': [0.4, 0.5, 0.6, 'auto']
        }
        
        print('-------------- Ansatz mit SMOTE und Undersampling - Ergebnis GridsearchCV  ---------------')
        grid_cv_smote_us_recall = GridSearchCV(smote_pipeline_withundersampling,
                                               parametergrid_smote_withundersampling,
                                               scoring=['recall', 'precision', 'roc_auc'],
                                               return_train_score=True,
                                               refit='recall',
                                               cv=10)
        
        grid_cv_smote_us_recall.fit(X_train, y_train)
        
        df_best_result_SMOTE_US = pd.DataFrame(grid_cv_smote_us_recall.cv_results_).iloc[
                                  grid_cv_smote_us_recall.best_index_, :]
        
        print(f'Recall_Score naiv: {df_best_result_SMOTE_US["mean_test_recall"]}')
        print(f'Precision_Score naiv: {df_best_result_SMOTE_US["mean_test_precision"]}')
        print(f'roc_auc_Score naiv: {df_best_result_SMOTE_US["mean_test_roc_auc"]}')
        print(f'Recall_Parameter naiv: {df_best_result_SMOTE_US["params"]}')
        print('-------------- Ansatz mit SMOTE und Undersampling - Overfitting Befürchtung  ---------------')
        y_pred_train = grid_cv_smote_us_recall.best_estimator_.predict(X_train)
        print(score_auc_recall(y_train, y_pred_train))
        print(confusion_matrix(y_train, y_pred_train))
        print('-------------- Ansatz mit SMOTE und Undersampling - Bewertung auf Testdaten  ---------------')
        y_pred = grid_cv_smote_us_recall.best_estimator_.predict(X_test)
        print(score_auc_recall(y_test, y_pred))
        print('-------------- Ansatz mit SMOTE und Undersampling - Beendet  ---------------')
        
        return {
            'class_weight': {
                0: 1,
                1: 1000
            },
            'kernel': 'linear'
        }

def estimator_randomforrest(X_train, X_test, y_train, y_test):
    # author: Jan Philipp Seng

    #####################################
    # Explanations of terms
    #
    # true positive: correctly predicted element
    # false positive: incorrectly predicted element
    # true negative: correctly unpredicted element
    # false negative: incorrectly unpredicted element
    #
    # recall
    #   definition: true positives / relevant elements
    #   measure of quantity: How complete are the results?
    #   Proportion of correct predictions for a class out of all elements from this class
    #   recall=1: Alle relevanten Elemente wurde korrekt prognostiziert
    #
    # AUC
    #   "Area under curve" of false positive rate / true positive rate
    #
    # F1
    #   definition: 2 * precision * recall / (precision + recall)
    #   harmonic mean of precision and recall
    #
    # precision
    #   definition: true positives / selected elements
    #   measure of quality: How valid are the results?
    #   Proportion of correct predictions for a class out of all predictions
    #
    # https://en.wikipedia.org/wiki/Precision_and_recall

    random_state = 2023

    def fit_predict_scores(estimator):
        estimator.fit(X_train, y_train)
        cvs = cross_val_score(estimator, X_train, y_train, scoring='recall', n_jobs=-1)
        print(f"Crossval recall score={cvs.round(3)}, mean={cvs.mean().round(3):.3f}")
        print(f"scores test data\n{score_auc_recall(y_test, estimator.predict(X_test))}")

    def grid_search_CV(estimator, param_grid, verbose=2):
        scoring_method = 'roc_auc'  # or 'recall'
        grid_search = GridSearchCV(estimator,
                                   param_grid,
                                   scoring=scoring_method,
                                   verbose=verbose,
                                   n_jobs=-1,
                                   cv=5) \
            .fit(X_train, y_train)
        print(f'best parameter={grid_search.best_params_}')
        print(f'{scoring_method} score={grid_search.best_score_:.3f}')
        y_pred = grid_search.best_estimator_.predict(X_test)
        print(f'scores of best estimator for test data=\n{score_auc_recall(y_test, y_pred)}')

    def evaluation_1():
        fit_predict_scores(RandomForestClassifier(random_state=random_state))
        fit_predict_scores(RandomForestClassifier(max_features=None,
                                                  n_estimators=75,
                                                  criterion='entropy',
                                                  random_state=random_state))
        fit_predict_scores(RandomForestClassifier(max_depth=1,
                                                  criterion='gini',
                                                  random_state=random_state))
        fit_predict_scores(RandomForestClassifier(max_features=None,
                                                  max_depth=5,
                                                  n_estimators=100,
                                                  criterion='gini',
                                                  min_samples_leaf=2,
                                                  random_state=random_state))

    def evaluation_2():
        params = {
            'max_features': None,
            'max_depth': 5,
            'n_estimators': 100,
            'criterion': 'gini',
            'min_samples_leaf': 2,
            'random_state': random_state
        }
        for class_weight in ['balanced_subsample',
                             'balanced',
                             dict([(0, 0.25), (1, 0.75)]),
                             dict([(0, 0.1), (1, 0.9)]),
                             dict([(0, 0.0487), (1, 0.9513)]),
                             dict([(0, 0.01), (1, 0.99)]),
                             dict([(0, 0.001), (1, 0.999)]),
                             ]:
            print(f"\nclass_weight='{class_weight}'")
            fit_predict_scores(RandomForestClassifier(**params, class_weight=class_weight))

    def evaluation_2_grid_search():
        ##### Iteration 1 #####
        best_params = {
            'class_weight': 'balanced',
            'min_samples_leaf': 2,
            'random_state': random_state
        }
        grid_search_CV(RandomForestClassifier(**best_params), {
            'max_depth': (1, 2, 3, 4, 5),
            'max_features': (3, 5, 'sqrt', 'log2', None),
            "n_estimators": (1, 3, 5, 10, 25, 50, 100, 150),
            "criterion": ("gini", "entropy", "log_loss")
        })
        # best parameter={'criterion': 'entropy', 'max_depth': 3, 'max_features': None, 'n_estimators': 150}
        # roc_auc score=0.850
        # scores of best estimator for test data=
        #      recall  precision_score        f1 AUC_score
        # 1  0.800000         0.110497  0.194175  0.734362
        # 0  0.668724         0.984848  0.796569      <NA>

        ##### Iteration 2 #####
        best_params = {
            'class_weight': 'balanced',
            'min_samples_leaf': 2,
            'max_features': None,  # Ergebnis aus Iteration 1
            'criterion': 'entropy',  # Ergebnis aus Iteration 1
            'random_state': random_state
        }
        grid_search_CV(RandomForestClassifier(**best_params), {
            'max_depth': (2, 3, 4),
            'min_samples_leaf': (1, 2, 3, 4, 5),
            "n_estimators": (100, 150, 200, 300, 500, 1000, 1500),
        })
        # best parameter={'max_depth': 3, 'min_samples_leaf': 1, 'n_estimators': 1000}
        # roc_auc score=0.851
        # scores of best estimator for test data=
        #      recall  precision_score        f1 AUC_score
        # 1  0.800000         0.110497  0.194175  0.734362
        # 0  0.668724         0.984848  0.796569      <NA>

        ##### Iteration 3 #####
        best_params = {
            'class_weight': 'balanced',
            'max_features': None,  # Ergebnis aus Iteration 1
            'criterion': 'entropy',  # Ergebnis aus Iteration 1
            'min_samples_leaf': 1,  # Ergebnis aus Iteration 2
            'max_depth': 3,  # Ergebnis aus Iteration 2
            'n_estimators': 1000,  # Ergebnis aus Iteration 2
            'random_state': random_state
        }
        grid_search_CV(RandomForestClassifier(**best_params), {
            'max_leaf_nodes': (3, 5, 7, 9, 11),
        })
        # bringt keine Verbesserung mehr im Vergleich zu Iteration 2

    def evaluation_3():
        best_params = {
            'max_features': None,
            'criterion': 'entropy',
            'min_samples_leaf': 1,
            'max_depth': 3,
            'n_estimators': 1000,
            'random_state': random_state
        }
        oversampling_pipe = imb_pipe([('over', SMOTE(random_state=random_state)),
                                      ('estimator', RandomForestClassifier(**best_params))])
        fit_predict_scores(oversampling_pipe)
        # Crossval recall score=[0.875 0.85  0.846 0.8   0.85 ], mean=0.844
        # scores test data
        #      recall  precision_score        f1 AUC_score
        # 1  0.800000         0.124611  0.215633  0.755453
        # 0  0.710905         0.985735  0.826061      <NA>

        grid_search_CV(oversampling_pipe, {
            'estimator__max_depth': [1, 2, 3, 5],
            "estimator__max_features": (5, 10, 15),
            "estimator__n_estimators": (100, 150, 200),
            "estimator__criterion": ("gini", "entropy")
        })
        # best parameter={'estimator__criterion': 'entropy', 'estimator__max_depth': 3, 'estimator__max_features': 5, 'estimator__n_estimators': 150}
        # roc_auc score=0.834
        # scores of best estimator for test data=
        #      recall  precision_score        f1 AUC_score
        # 1  0.860000         0.112272  0.198614  0.755103
        # 0  0.650206         0.989045  0.784606      <NA>

    def evaluation_4():
        best_params = {
            'max_features': None,
            'criterion': 'entropy',
            'min_samples_leaf': 1,
            'max_depth': 3,
            'n_estimators': 1000,
            'random_state': random_state
        }
        fit_predict_scores(imb_pipe([('under', RandomUnderSampler(random_state=random_state, sampling_strategy='auto')),
                                     ('estimator', RandomForestClassifier(**best_params))]))

    evaluation_1()  # simpler Ansatz
    evaluation_2()  # class_weights
    evaluation_2_grid_search()
    evaluation_3()  # Oversampling
    evaluation_4()  # Undersampling


def estimator_logReg_smote(X_train, y_train, X_test, y_test):
    # author: Raffael Hipp
    ####  PCA  ####
    '''from sklearn.decomposition import PCA
    # -- PCA-Model --
    pca = PCA()
    X_pca = pca.fit_transform(X_train)
    # -- Auswertung --
    print('---------------------------------')
    print(f"Erklaerungskraft: {pca.explained_variance_ratio_}")
    print(f"noise: {pca.noise_variance_}")
    print(f"spannweite: {X_pca.max()-X_pca.min()}")
    print()
    # PCA mit 13 components
    pca = PCA(n_components=13)
    X_pca = pca.fit_transform(X_train)
    X_train = X_pca'''
    # => hat keine Verbesserung für diesen Algorithmus bzw. für dieses Modell

    # ===========================================================================
    #####  imbalanced Data  ####
    # => hier die Daten noch nicht mit smote-Methode verändern
    # --> Fehler bei CrossValidation und GridSearch
    # smote = SMOTE(n_jobs=-1, random_state=42)
    # X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    # X_train = X_train_smote
    # y_train = y_train_smote

    print('----------------------------------------------------------------')
    # ===========================================================================
    ##### Estimator: LogisticRegression ####
    print('------ Estimator: Logistic Regression --------------------------')
    print('----------------------------------------------------------------')
    print()

    # in diesem Skript:
    # Ansatz für die imbalanced Data: Verwendung der Methode smote() von imblearn

    # Zuerst: Basisdatensatz verwenden - ohne Beachtung der imbalanced Data

    # --- fit/train model ---
    # - Parameters for model (zum Ausprobieren) -
    solver_name = 'lbfgs'  # 'lbfgs', 'liblinear','newton-cg','newton-cholesky','sag', 'saga'
    weight = 'balanced'  # {0:1, 1:2}
    c = 1  # 0.1, 0.001, 0.0001, 10, 100
    max_iteration = 200
    p = 'l2'  # 'l1'

    # clf_lr = LogisticRegression()  # default settings
    # clf_lr = LogisticRegression(solver=solver_name, penalty=pen, C=c, max_iter=max_iteration, random_state=42) # with settings
    clf_lr = LogisticRegression(solver='lbfgs', penalty='l2', C=1, max_iter=150, random_state=42)
    # clf_lr = LogisticRegression(solver='liblinear', penalty='l1', C=0.1, max_iter=150, random_state=25) # with settings
    clf_lr.fit(X_train, y_train)  # fit

    # Koeffizienten printen
    # print(f'coef: \n{clf_lr.coef_}')
    # print(f'intercept: {clf_lr.intercept_}')

    # -- predictions: recall und auc --
    y_pred = clf_lr.predict(X_train)  # predict
    score_recall_auc = score_auc_recall(y_train, y_pred)
    print(f'Evaluation des Modells auf den Trainingsdaten (ohne oversampling):')
    print()
    print(f'Scores:\n{score_recall_auc}')
    print()

    # -- evaluate model --
    print(f'confusion_matrix: \n{confusion_matrix(y_train, y_pred)}')
    print()

    # ConfusionMatrix in %
    # ConfusionMatrixDisplay.from_estimator(clf_lr, X_train, y_train, normalize='all')
    # plt.show()

    # - Classification_report -
    print('classification_report:')
    print(classification_report(y_train, y_pred))
    print()

    # --- CrossValidation ---
    print(f'---------- CrossValidation ----------------------------------- ')
    print(f'* ohne Oversampling')
    clf_lr_cross_val_score_recall = cross_val_score(clf_lr, X_train, y_train, cv=6, scoring='recall')
    clf_lr_cross_val_score_auc = cross_val_score(clf_lr, X_train, y_train, cv=6, scoring='roc_auc')

    print('  - score: recall')
    # print(f'cv_score_recall : \n{clf_lr_cross_val_score_recall}')
    print(f'     recall_mean: {clf_lr_cross_val_score_recall.mean()}')
    print(f'     recall_std: {clf_lr_cross_val_score_recall.std()}')

    print('  - score: auc')
    # print(f'cv_score_auc : \n{clf_lr_cross_val_score_auc}')
    print(f'     auc_mean: {clf_lr_cross_val_score_auc.mean()}')
    print(f'     auc_std: {clf_lr_cross_val_score_auc.std()}')
    print()

    print(f'* mit Oversampling')
    # Pipline für das oversampling mit der Funktion smote
    # oversampling nur auf den Trainingsdaten -> nur bei fit -> nicht bei predict
    clf_lr_pipe = imb_pipe([('oversample', SMOTE()), (
        'logreg_pipe', LogisticRegression(solver='lbfgs', penalty='l2', C=1, max_iter=200, random_state=42))])
    # clf_lr_pipe = Pipeline([('oversample', SMOTE()),('logreg_pipe', LogisticRegression(solver='liblinear', penalty='l1', C=0.1, max_iter=200, random_state=25))])
    lr_pipe_cross_val_score_recall = cross_val_score(clf_lr_pipe, X_train, y_train, cv=6, scoring='recall')
    lr_pipe_cross_val_score_auc = cross_val_score(clf_lr_pipe, X_train, y_train, cv=6, scoring='roc_auc')

    print('  - score: recall')
    # print(f'cv_score_recall : \n{clf_lr_cross_val_score_recall}')
    print(f'     recall_mean: {lr_pipe_cross_val_score_recall.mean()}')
    print(f'     recall_std: {lr_pipe_cross_val_score_recall.std()}')

    print('  - score: auc')
    # print(f'cv_score_auc : \n{clf_lr_cross_val_score_auc}')
    print(f'     auc_mean: {lr_pipe_cross_val_score_auc.mean()}')
    print(f'     auc_std: {lr_pipe_cross_val_score_auc.std()}')
    # print('----------------------------------------------------------------')
    print()

    # ================ GridSearch for logistic Regression ====================================
    # GridSeach auch mit Oversampling (Methode smote und der pipline clf_lr_pipe)
    print(f'---------- GridSearchCV -------------------------------------- ')
    # -- Parameters for GridSearchCV --
    # zwei Parametersätze um die zu untersuchenden Kombinationen abzudecken, es ist nicht jeder Parameter mit allen Parametern kombinierbar
    param_grid_1 = {
        'logreg_pipe__solver': ['lbfgs', 'newton-cg', 'newton-cholesky'],
        'logreg_pipe__penalty': ['l2'],
        'logreg_pipe__C': [0.001, 0.01, 0.1, 1, 10],
        'logreg_pipe__max_iter': [100, 150, 200]
    }
    param_grid_2 = {
        'logreg_pipe__solver': ['liblinear'],
        'logreg_pipe__penalty': ['l2', 'l1'],
        'logreg_pipe__C': [0.001, 0.01, 0.1, 1, 10],
        'logreg_pipe__max_iter': [100, 150, 200]
    }

    # param_grid_1
    # - score: rec -
    gridsearch_lr_1_rec = GridSearchCV(clf_lr_pipe, param_grid_1, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='recall')
    gridsearch_lr_1_rec.fit(X_train, y_train)
    print('Parametersatz 1: ')
    print(f'Best Para., recall: {gridsearch_lr_1_rec.best_params_}')
    print(f'Best Score, recall: {gridsearch_lr_1_rec.best_score_}')
    print()
    # - score: auc -
    gridsearch_lr_1_auc = GridSearchCV(clf_lr_pipe, param_grid_1, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='roc_auc')
    gridsearch_lr_1_auc.fit(X_train, y_train)
    print(f'Best Para., auc: {gridsearch_lr_1_auc.best_params_}')
    print(f'Best Score, auc: {gridsearch_lr_1_auc.best_score_}')
    print()
    # - param_grid_2 -
    # - score: rec -
    gridsearch_lr_2_rec = GridSearchCV(clf_lr_pipe, param_grid_2, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='recall')
    gridsearch_lr_2_rec.fit(X_train, y_train)
    print('Parametersatz 2: ')
    print(f'Best Para., recall: {gridsearch_lr_2_rec.best_params_}')
    print(f'Best Score, recall: {gridsearch_lr_2_rec.best_score_}')
    # -> ausgewählt: da hier den höchsten recall-score haben
    # -> damit weiter arbeiten
    print()
    # - score: auc -
    gridsearch_lr_2_auc = GridSearchCV(clf_lr_pipe, param_grid_2, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='roc_auc')
    gridsearch_lr_2_auc.fit(X_train, y_train)
    print(f'Best Para., auc: {gridsearch_lr_2_auc.best_params_}')
    print(f'Best Score,auc: {gridsearch_lr_2_auc.best_score_}')
    print()

    print(f'Auswahl folgender Parameter für die weiteren Berechnungen: \n{gridsearch_lr_2_rec.best_params_}')
    print()
    print()

    print('---------- Evaluation des Modells mit den Trainingsdaten ----------- ')
    print()
    # Evaluierung der optimierten Daten
    # an den Testdaten
    # neue Parameter auf das Modell anwenden
    # neue Pipline mit den neuen Parametern erstellen
    # clf_lr_pipe_opt = imb_pipe([('oversample', SMOTE()),('logreg_pipe', LogisticRegression(solver='lbfgs', penalty='l2', C=0.01, max_iter=200, random_state=42))]) # Para1, recall
    # clf_lr_pipe_opt = imb_pipe([('oversample', SMOTE()),('logreg_pipe', LogisticRegression(solver='newton-cholesky', penalty='l2', C=0.01, max_iter=150, random_state=42))]) # Para1, auc
    clf_lr_pipe_opt = imb_pipe([('oversample', SMOTE()), ('logreg_pipe',
                                                          LogisticRegression(solver='liblinear', penalty='l1', C=0.001,
                                                                             max_iter=100,
                                                                             random_state=42))])  # Para2, recall
    # clf_lr_pipe_opt = imb_pipe([('oversample', SMOTE()),('logreg_pipe', LogisticRegression(solver='liblinear', penalty='l1', C=0.01, max_iter=200, random_state=42))]) # Para2, auc

    # -- Modell trainieren/fit --
    clf_lr_pipe_opt.fit(X_train, y_train)

    # -- predictions --
    y_pred_opt_test = clf_lr_pipe_opt.predict(X_test)

    print(f'------- CrossValidation mit den optimierten Parametern ------- ')
    clf_lr_cross_val_score_recall_opt = cross_val_score(clf_lr_pipe_opt, X_train, y_train, cv=6, scoring='recall')
    clf_lr_cross_val_score_auc_opt = cross_val_score(clf_lr_pipe_opt, X_train, y_train, cv=6, scoring='roc_auc')

    print('* score: recall')
    # print(f'cv_score_recall : \n{clf_lr_cross_val_score_recall}')
    print(f'  recall_mean: {clf_lr_cross_val_score_recall_opt.mean()}')
    print(f'  recall_std: {clf_lr_cross_val_score_recall_opt.std()}')

    print('* score: auc')
    # print(f'cv_score_auc : \n{clf_lr_cross_val_score_auc}')
    print(f'  auc_mean: {clf_lr_cross_val_score_auc_opt.mean()}')
    print(f'  auc_std: {clf_lr_cross_val_score_auc_opt.std()}')
    print()

    print('---------- Evaluation des Modells mit den optimierten Parametern und den Testdaten ----------- ')

    # -- evaluate model --
    # - scores (recall + auc) -
    print(f'evaluation: \n{score_auc_recall(y_test, y_pred_opt_test)}')
    print()

    # - confusion matrix -
    print(f'confusion_matrix: \n{confusion_matrix(y_test, y_pred_opt_test)}')
    print()

    # - Classification_report -
    print('classification_report:')
    print(classification_report(y_test, y_pred_opt_test))

    return gridsearch_lr_2_rec.best_params_


def estimator_logReg_clasWeight(X_train, y_train, X_test, y_test):
    # author: Raffael Hipp
    print('----------------------------------------------------------------')
    # ===========================================================================
    #####         Estimator: LogisticRegression ####
    print('------ Estimator: Logistic Regression --------------------------')
    print('----------------------------------------------------------------')
    print()

    # Ansatz für die imbalanced Data: class_weight der LogisticRegression-Klasse von sklearn verwenden
    # --- fit/train model ---
    # - Parameters for model (for testing) -
    solver_name = 'lbfgs'  # 'lbfgs', 'liblinear','newton-cg','newton-cholesky','sag', 'saga'
    weight = 'balanced'  # {0:1, 1:2}
    c = 1  # 0.1, 0.001, 0.0001, 10, 100
    max_iteration = 200
    p = 'l2'  # 'l1'

    # clf_lr = LogisticRegression()  # default settings
    clf_lr = LogisticRegression(solver=solver_name, class_weight=weight, C=c, max_iter=max_iteration, penalty=p,
                                random_state=42)  # settings
    clf_lr.fit(X_train, y_train)

    # Koeffizienten
    # print(f'coef: \n{clf_lr.coef_}')
    # print(f'intercept: {clf_lr.intercept_}')

    # -- predictions --
    y_pred = clf_lr.predict(X_train)
    # print(f'score: {clf_lr.score(X_train, y_train)}')  # Score --> not useful (unbalanced data)

    # -- evaluate model --
    # - scores (recall + auc) -
    print(f'evaluation: \n{score_auc_recall(y_train, y_pred)}')
    print()

    # - confusion matrix -
    print(f'confusion_matrix: \n{confusion_matrix(y_train, y_pred)}')
    print()

    # ConfusionMatrix in %
    # ConfusionMatrixDisplay.from_estimator(clf_lr, X_train, y_train, normalize='all')
    # plt.show()

    # - Classification_report -
    print('classification_report:')
    print(classification_report(y_train, y_pred))
    print()

    # CrossValidation
    print(f'---------- CrossValidation ----------------------------------- ')
    clf_lr_cross_val_score_recall = cross_val_score(clf_lr, X_train, y_train, cv=6, scoring='recall')
    clf_lr_cross_val_score_auc = cross_val_score(clf_lr, X_train, y_train, cv=6, scoring='roc_auc')

    print('* score: recall')
    # print(f'cv_score_recall : \n{clf_lr_cross_val_score_recall}')
    print(f'  recall_mean: {clf_lr_cross_val_score_recall.mean()}')
    print(f'  recall_std: {clf_lr_cross_val_score_recall.std()}')

    print('* score: auc')
    # print(f'cv_score_auc : \n{clf_lr_cross_val_score_auc}')
    print(f'  auc_mean: {clf_lr_cross_val_score_auc.mean()}')
    print(f'  auc_std: {clf_lr_cross_val_score_auc.std()}')
    print()

    # ================ GridSearch for logistic Regression ====================================
    print(f'---------- GridSearchCV -------------------------------------- ')
    # -- Parameters for GridSearchCV --
    # zwei Parametersätze um die zu untersuchenden Kombinationen abzudecken, es ist nicht immer jeder Parameter mit allen Parametern kombinierbar
    # param_grid_1 = {'class_weight': ['balanced'], 'solver': ['lbfgs', 'newton-cg', 'newton-cholesky'],
    param_grid_1 = {
        'class_weight': [{
            0: 1,
            1: 10
        }, {
            0: 1,
            1: 100
        }, {
            0: 1,
            1: 1000
        }, {
            0: 10,
            1: 1
        }, {
            0: 100,
            1: 1
        }, 'balanced'],
        'solver': ['lbfgs', 'newton-cg', 'newton-cholesky'],
        'penalty': ['l2'],
        'C': [0.001, 0.01, 0.1, 1, 10],
        'max_iter': [150, 200]
    }
    param_grid_2 = {
        'class_weight': ['balanced'],
        'solver': ['liblinear'],
        'penalty': ['l2', 'l1'],
        'C': [0.001, 0.01, 0.1, 1, 10],
        'max_iter': [150, 200]
    }

    # -- GridSearch-Object erstellen + fit --
    model_gridsearch_lr = LogisticRegression()

    # param_grid_1
    # - score: rec -
    gridsearch_lr_1_rec = GridSearchCV(model_gridsearch_lr, param_grid_1, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='recall')
    gridsearch_lr_1_rec.fit(X_train, y_train)
    print(f'Best parameters 1, recall: {gridsearch_lr_1_rec.best_params_}')
    print(f'Best score 1, recall: {gridsearch_lr_1_rec.best_score_}')
    print()
    # - score: auc -
    gridsearch_lr_1_auc = GridSearchCV(model_gridsearch_lr, param_grid_1, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='roc_auc')
    gridsearch_lr_1_auc.fit(X_train, y_train)
    print(f'Best parameters 1, auc: {gridsearch_lr_1_auc.best_params_}')
    print(f'Best score 1, auc: {gridsearch_lr_1_auc.best_score_}')
    print()
    # - param_grid_2 -
    # - score: rec -
    gridsearch_lr_2_rec = GridSearchCV(model_gridsearch_lr, param_grid_2, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='recall')
    gridsearch_lr_2_rec.fit(X_train, y_train)
    print(f'Best parameters 2, recall: {gridsearch_lr_2_rec.best_params_}')
    print(f'Best score 2, recall: {gridsearch_lr_2_rec.best_score_}')
    # -> ausgewählt: da hier den höchsten recall-score haben
    # -> damit weiter arbeiten
    print()
    # - score: auc -
    gridsearch_lr_2_auc = GridSearchCV(model_gridsearch_lr, param_grid_2, cv=6, return_train_score=True, n_jobs=-1,
                                       scoring='roc_auc')
    gridsearch_lr_2_auc.fit(X_train, y_train)
    print(f'Best parameters 2, auc: {gridsearch_lr_2_auc.best_params_}')
    print(f'Best score 2,auc: {gridsearch_lr_2_auc.best_score_}')
    print()

    print(f'Auswahl folgender Parameter für die weiteren Berechnungen: \n{gridsearch_lr_1_rec.best_params_}')
    print()
    print()

    print('---------- Evaluation des Modells mit den optimierten Parametern und mit Trainingsdaten ----------- ')
    print()
    clf_lr_opt_test = LogisticRegression(solver='lbfgs', class_weight={
        0: 1,
        1: 100
    }, C=0.1, max_iter=150, penalty='l2', random_state=42)  # Parameters 1, auc
    clf_lr_opt_test.fit(X_train, y_train)

    # -- predictions --
    y_pred_opt_test = clf_lr_opt_test.predict(X_test)

    print(f'------- CrossValidation mit den optimierten Parametern ------- ')
    clf_lr_cross_val_score_recall_opt = cross_val_score(clf_lr_opt_test, X_train, y_train, cv=6, scoring='recall')
    clf_lr_cross_val_score_auc_opt = cross_val_score(clf_lr_opt_test, X_train, y_train, cv=6, scoring='roc_auc')

    print('* score: recall')
    # print(f'cv_score_recall : \n{clf_lr_cross_val_score_recall}')
    print(f'  recall_mean: {clf_lr_cross_val_score_recall_opt.mean()}')
    print(f'  recall_std: {clf_lr_cross_val_score_recall_opt.std()}')

    print('* score: auc')
    # print(f'cv_score_auc : \n{clf_lr_cross_val_score_auc}')
    print(f'  auc_mean: {clf_lr_cross_val_score_auc_opt.mean()}')
    print(f'  auc_std: {clf_lr_cross_val_score_auc_opt.std()}')
    print()

    print('---------- Evaluation des Modells mit den optimierten Parametern und den Testdaten ----------- ')

    # -- evaluate model --
    # - scores (recall + auc) -
    print(f'evaluation: \n{score_auc_recall(y_test, y_pred_opt_test)}')
    print()

    # - confusion matrix -
    print(f'confusion_matrix: \n{confusion_matrix(y_test, y_pred_opt_test)}')
    print()

    # - Classification_report -
    print('classification_report:')
    print(classification_report(y_test, y_pred_opt_test))


# +------------------------+
# |          Main          |
# +------------------------+

df: DataFrame = init_data()
# inspect_data(df)
X_train, X_test, y_train, y_test = split_dataset(df)
X_train, y_train = preprocess_data(X_train, y_train)
X_test, y_test = preprocess_data(X_test, y_test)

evaluate_estimator_knn = False
evaluate_estimator_svc = False
evaluate_estimator_random_forrest = True
evaluate_estimator_logistic_regression = False

if evaluate_estimator_logistic_regression:
    # author: Raffael Hipp
    estimator_logReg_smote(X_train, y_train, X_test, y_test)
    estimator_logReg_clasWeight(X_train, y_train, X_test, y_test)

if evaluate_estimator_svc:  # 200 Zeilen
    # author: Lars Kleinemeier
    estimator_svc(X_train, X_test, y_train, y_test)

if evaluate_estimator_knn:  # 140 Zeilen
    # author: Gero Krikawa
    knn_score, knn_confusion_matrix, knn_classification_report, knn_auc_score = estimator_knn(X_train,
                                                                                              y_train,
                                                                                              X_test,
                                                                                              y_test)
    print("-------------Ausgabe KNN im Hauptprogramm - Score: recall -------------")
    print("knn_score", knn_score)
    print("knn_confusion_matrix", "\n", knn_confusion_matrix)
    print("knn_classification_report", "\n", knn_classification_report)
    print("knn_auc_score", knn_auc_score)

if evaluate_estimator_random_forrest:
    # author: Jan Philipp Seng
    estimator_randomforrest(X_train, X_test, y_train, y_test)
