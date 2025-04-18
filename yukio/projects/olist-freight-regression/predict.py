# %%
import mlflow
import pandas as pd
import os

base_dir = 'data/'

mlflow.set_tracking_uri('http://localhost:5000')

# %%

client = mlflow.client.MlflowClient()
version = max([int(i.version) for i in client.get_latest_versions('freight-prediction')])
version

# %%
model = mlflow.xgboost.load_model(f'models:/freight-prediction/{version}')

# %%
model.features_names_in_

# %%
df = pd.read_csv(os.path.join(base_dir, 'df_final.csv'))
df.head()

# %%
X = df.head()[model.features_names_in_]

# %%
y_pred = model.predict(X)
y_pred