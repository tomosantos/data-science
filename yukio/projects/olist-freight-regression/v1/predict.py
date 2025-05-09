# %%
import pandas as pd
import numpy as np
import os

base_dir = 'data/'
model = pd.read_pickle('model/xgb.pkl')
model

# %%
df = pd.read_csv(os.path.join(base_dir, 'df_final.csv'))
df

# %%
X = df[model['features']]
predict = model['model'].predict(X)
predict

# %%
df['freight-pred'] = predict
df

# %%
df[['price', 'distance', 'freight_value', 'freight-pred']]
# %%
