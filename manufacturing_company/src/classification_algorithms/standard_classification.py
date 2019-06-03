from manufacturing_company.src.common.const import *
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from imblearn.pipeline import Pipeline


def train(algorithm, X, y, cv_scorer, parameters):
    groups = len(set(y))
    if groups == 2:
        smote = SMOTE(random_state=42, ratio={1: len(X.loc[y[y == 2].index])}, k_neighbors=4)
    else:
        smote = SMOTE(random_state=42, ratio={1: len(X.loc[y[y == 3].index]), 2: len(X.loc[y[y == 3].index])},
                      k_neighbors=4)

    alg = algorithm(random_state=42)

    pipeline = Pipeline([('smote', smote), ('model', alg)])

    gs = GridSearchCV(pipeline, parameters, cv=5, scoring=cv_scorer, n_jobs=1)
    model = gs.fit(X, y)
    return model
