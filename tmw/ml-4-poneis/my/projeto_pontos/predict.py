# %%
import pandas as pd
import sqlalchemy

model = pd.read_pickle('modelo_rf.pkl')
model

# %%
df = pd.read_csv("../data/dados_pontos.csv", sep=";")
df

# %%
proba = model['model'].predict_proba(df[model['features']])[:, 1]
proba

# %%
df['proba_active'] = proba

(df[['Name', 'proba_active']]).sort_values(by='proba_active', ascending=False).head(25)
# %%
