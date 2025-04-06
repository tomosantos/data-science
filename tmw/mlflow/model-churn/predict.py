# %%

import mlflow
mlflow.set_tracking_uri('http://localhost:5000')

# %%
client = mlflow.client.MlflowClient()
version = max([int(i.version) for i in client.get_latest_versions('churn-model')])
version

# %%
# model = mlflow.sklearn.load_model('models:/churn-model/1')
# model = mlflow.sklearn.load_model('models:/churn-model/2')
model = mlflow.sklearn.load_model(f'models:/churn-model/{version}')


# %%

model.feature_names_in_
# %%
import pandas as pd
df = pd.read_csv('data/abt.csv', sep=',')
df

# %%

X = df.head()[model.feature_names_in_]

# %%
proba = model.predict_proba(X)
proba
# %%
