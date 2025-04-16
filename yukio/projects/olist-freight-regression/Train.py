# %%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.tree import DecisionTreeRegressor

from category_encoders import CatBoostEncoder

# %%
import mlflow

mlflow.set_tracking_uri("http://localhost:5000/")
mlflow.set_experiment(experiment_id=535394779431182411)

# %%
# Define the base directory for the data files
data_dir = 'data'

# Load the dataset
df = pd.read_csv(os.path.join(data_dir, 'df_final.csv'))

df.head()

# %%
# Splitting in X and Y
X = df.drop(columns='freight_value', axis=1)
y = df.freight_value

# %%
# Splitting in train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)

# %%
# Initializing models
model_XGBoost = XGBRegressor(n_estimators = 1000, max_depth = 8, learning_rate = 1e-3, random_state = 0)
model_LightGBM = LGBMRegressor(n_estimators = 1000, max_depth = 8, num_leaves = 2^8, learning_rate = 1e-3, n_jobs = -1, verbose = -1, random_state = 0)
model_Catboost = CatBoostRegressor(n_estimators = 1000, max_depth = 8, learning_rate = 1e-3, random_state = 0, verbose = 0)
model_DecisionTree = DecisionTreeRegressor(random_state = 0, max_depth = 8, min_samples_split = 2)

# %%
# Feature importance

encoder = CatBoostEncoder()
X_train_encoded = X_train.copy()
X_test_encoded = X_test.copy()

for col in X_train_encoded.select_dtypes(include=['object']).columns:
    X_train_encoded[col] = encoder.fit_transform(X_train_encoded[col], y_train)
    X_test_encoded[col] = encoder.transform(X_test_encoded[col])

model_XGBoost.fit(X_train_encoded, y_train)
r = permutation_importance(model_XGBoost, X_test_encoded, y_test, n_repeats=30, random_state=0)

# %%
importances = pd.DataFrame({'Feature': X_test_encoded.columns, 'importance': r.importances_mean})
importances = importances.sort_values(by='importance', ascending=False)
importances

# %%
less_important_columns = ['purchase_day_of_week', 'approval_order_time', 'estimated_delivery_time', 'christmas', 'black_friday']

X_train = X_train.drop(columns=less_important_columns)
X_test = X_test.drop(columns=less_important_columns)

# %%
