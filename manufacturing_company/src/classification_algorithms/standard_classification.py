from manufacturing_company.src.common.const import *
from manufacturing_company.src.classification_algorithms.ModelInfo import ModelInfo
import operator
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from imblearn.pipeline import Pipeline


def assign_management_levels(levels, df_employees, df_positions):
    if levels == 2:
        df_employees[POSITION] = 2
        management_level = df_positions.index
        df_employees.loc[df_employees.index.isin(management_level), POSITION] = 1
    elif levels == 3:
        df_employees[POSITION] = 3

        first_management_level = df_positions[df_positions[POSITION] == 1].index
        second_management_level = df_positions[df_positions[POSITION] == 2].index

        df_employees.loc[df_employees.index.isin(first_management_level), POSITION] = 1
        df_employees.loc[df_employees.index.isin(second_management_level), POSITION] = 2
    else:
        raise Exception("Unsupported number of levels")

    return df_employees


def classification(df, algorithm, parameters, cv_scorer):
    models = []
    pcts = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

    X = df.loc[:, df.columns != POSITION]
    y = df[POSITION]

    feature_names = X.columns.tolist()

    for pct in pcts:
        print('FEATURES %: ', pct * 100)

        model = train(algorithm, X[feature_names], y, cv_scorer,
                      parameters(len(feature_names)))

        print('BEST SCORE: ' + str(model.best_score_))

        modelInfo = ModelInfo(model, parameters, cv_scorer, feature_names, pct)
        models.append(modelInfo)

        sorted_features = sorted(
            dict(zip(feature_names, model.best_estimator_.steps[1][1].
                     feature_importances_)).items(), key=operator.itemgetter(1), reverse=True)

        print('Features sorted from best:\n', sorted_features)

        diff = len(feature_names) - round(len(X.columns) * (pct - 0.1))

        for i in range(0, diff):
            feature_to_delete = sorted_features[i][0]
            feature_names.remove(feature_to_delete)
            print('REMOVED: ', feature_to_delete)

    return models


def train(algorithm, X, y, cv_scorer, parameters):
    smote = SMOTE(random_state=42, sampling_strategy='not majority', k_neighbors=4)

    alg = algorithm(random_state=42)

    pipeline = Pipeline([('smote', smote), ('model', alg)])

    gs = GridSearchCV(pipeline, parameters, cv=5, scoring=cv_scorer, n_jobs=1, iid=False)
    model = gs.fit(X, y)
    return model
