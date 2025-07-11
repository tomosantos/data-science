# %%
import pandas as pd

from sklearn import metrics
from sklearn import model_selection
from sklearn import pipeline

from sklearn import tree
from sklearn import linear_model
from sklearn import ensemble
from sklearn import naive_bayes

from feature_engine import imputation

import scikitplot as skplt

# %%
df = pd.read_csv("../data/dados_pontos.csv", sep=";")
df

# %%
features = df.columns.tolist()[3:-1]
target = "flActive"

# %%
X_train, X_test, y_train, y_test = model_selection.train_test_split(df[features],
                                                                    df[target],
                                                                    test_size=0.2,
                                                                    random_state=42,
                                                                    stratify=df[target])

print("Tx. de Resposta Treino: ", y_train.mean())
print("Tx. de Resposta Treino: ", y_test.mean())

# %%
X_train.isna().sum()

# %%
max_avgRecorrencia = X_train['avgRecorrencia'].max()

# %%
features_input_0 = [
    'qtdeRecencia',
    'freqDias',
    'freqTransacoes',
    'qtdListaPresença',
    'qtdChatMessage',
    'qtdTrocaPontos',
    'qtdResgatarPonei',
    'qtdPresençaStreak',
    'pctListaPresença',
    'pctChatMessage',
    'pctTrocaPontos',
    'pctResgatarPonei',
    'pctPresençaStreak',
    'qtdePontosGanhos',
    'qtdePontosGastos',
    'qtdePontosSaldo'
]

input_0 = imputation.ArbitraryNumberImputer(variables=features_input_0,
                                            arbitrary_number=0)

input_max = imputation.ArbitraryNumberImputer(variables=['avgRecorrencia'],
                                              arbitrary_number=max_avgRecorrencia)

model = ensemble.RandomForestClassifier(random_state=42)

params = {
    'n_estimators': [100, 150, 250, 500],
    'min_samples_leaf': [10, 20, 30, 50, 100]
}

grid = model_selection.GridSearchCV(model, param_grid=params,
                                    n_jobs=-1, scoring='roc_auc')

meu_pipeline = pipeline.Pipeline([
    ('input_0', input_0),
    ('input_max', input_max),
    ('model', grid)
])

meu_pipeline.fit(X_train, y_train)

# %%
pd.DataFrame(grid.cv_results_)

# %%
y_train_predict = meu_pipeline.predict(X_train)
y_train_proba = meu_pipeline.predict_proba(X_train)[:, 1]

y_test_predict = meu_pipeline.predict(X_test)
y_test_proba = meu_pipeline.predict_proba(X_test)

# %%
acc_train = metrics.accuracy_score(y_train, y_train_predict)
acc_test = metrics.accuracy_score(y_test, y_test_predict)
print('Acurácia da base train: ', acc_train)
print('Acurácia da base test: ', acc_test)

auc_train = metrics.roc_auc_score(y_train, y_train_proba)
auc_test = metrics.roc_auc_score(y_test, y_test_proba[:, 1])
print('\nAUC da base train: ', auc_train)
print('AUC da base test: ', auc_test)

# %%
f_importance = meu_pipeline[-1].best_estimator_.feature_importances_
pd.Series(f_importance, index=features).sort_values(ascending=False)

# %%
skplt.metrics.plot_roc(y_test, y_test_proba)

# %%
skplt.metrics.plot_cumulative_gain(y_test, y_test_proba)

# %%
usuarios_test = pd.DataFrame(
    {"verdadeiro": y_test,
     "proba": y_test_proba[:,1]}
)

usuarios_test = usuarios_test.sort_values("proba", ascending=False)
usuarios_test["sum_verdadeiro"] = usuarios_test["verdadeiro"].cumsum()
usuarios_test["tx captura"]=usuarios_test["sum_verdadeiro"] / usuarios_test["verdadeiro"].sum()
usuarios_test

# %%
skplt.metrics.plot_lift_curve(y_test, y_test_proba)

# %%
usuarios_test.head(500)['verdadeiro'].mean() / usuarios_test['verdadeiro'].mean()

# %%
skplt.metrics.plot_ks_statistic(y_test, y_test_proba)

# %%
model_s = pd.Series({
    'model': meu_pipeline,
    'features': features,
    'auc_test': acc_test,
    'auc_roc': auc_test
})
model_s

# %%
model_s.to_pickle("modelo_rf.pkl")

